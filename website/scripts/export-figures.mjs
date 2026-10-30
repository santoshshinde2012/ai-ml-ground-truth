/**
 * Save the print edition's rendered diagrams and plates as self-contained SVG files,
 * so the EPUB carries the same pictures as the web book. Run after the Astro build.
 * Uses a local headless Chrome; without one, it explains and exits, and the EPUB keeps
 * its text descriptions. Writes .cache/figures/ and .cache/figures/index.json.
 */
import fs from 'node:fs/promises';
import { existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fromWebsite } from '../src/lib/paths.mjs';
import { base, chromeArguments, findChrome, serveDist } from './browser.mjs';

const dist = fromWebsite('dist');
const output = fromWebsite('.cache/figures');
await fs.rm(output, { recursive: true, force: true });

const chrome = findChrome();
if (!chrome) {
  console.log('Figures skipped: Chrome was not found, so the EPUB keeps text descriptions.');
  process.exit(0);
}
if (!existsSync(path.join(dist, 'print/index.html'))) {
  console.error('dist/print/index.html was not found. Run the Astro build first.');
  process.exit(2);
}

// Runs in the page. Diagrams keep their own <style>; plates take their computed
// styles as attributes, because the site's stylesheet does not travel with an image.
function collectFigures() {
  const properties = [
    'fill',
    'fill-opacity',
    'stroke',
    'stroke-width',
    'stroke-dasharray',
    'stroke-linecap',
    'stroke-linejoin',
    'opacity',
    'font-family',
    'font-size',
    'font-weight',
    'letter-spacing',
  ];
  const localURL = (value) => value.replace(/url\("?[^#")]*#([^")]+)"?\)/g, 'url(#$1)');
  const finish = (svg, clone) => {
    const { width, height } = svg.viewBox.baseVal;
    for (const node of [clone, ...clone.querySelectorAll('*')])
      for (const { name } of [...node.attributes])
        if (/^(role|tabindex)$|^aria-|^data-/.test(name)) node.removeAttribute(name);
    clone.removeAttribute('style');
    // Mermaid defines unused SVG 2 shadow filters; EPUB validation expects SVG 1.1.
    const markup = clone.outerHTML;
    for (const filter of clone.querySelectorAll('filter'))
      if (filter.querySelector('feDropShadow') && !markup.includes(`url(#${filter.id})`))
        filter.remove();
    // Mermaid starts each word's text run with a space; stricter renderers drop it.
    for (const text of clone.querySelectorAll('text'))
      text.setAttributeNS('http://www.w3.org/XML/1998/namespace', 'xml:space', 'preserve');
    clone.setAttribute('width', String(Math.round(width)));
    clone.setAttribute('height', String(Math.round(height)));
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    return new XMLSerializer().serializeToString(clone);
  };
  const diagrams = [...document.querySelectorAll('.mermaid[data-diagram]')].flatMap((box) => {
    const svg = box.querySelector('svg');
    return svg ? [{ key: box.dataset.diagram, svg: finish(svg, svg.cloneNode(true)) }] : [];
  });
  const plates = [...document.querySelectorAll('[data-slug] > .chapter-plate')].map((figure) => {
    const svg = figure.querySelector('svg');
    const clone = svg.cloneNode(true);
    const sources = [svg, ...svg.querySelectorAll('*')];
    const targets = [clone, ...clone.querySelectorAll('*')];
    sources.forEach((source, index) => {
      const style = getComputedStyle(source);
      for (const property of properties) {
        const value = style.getPropertyValue(property);
        if (value && value !== 'normal') targets[index].setAttribute(property, localURL(value));
      }
      targets[index].removeAttribute('class');
    });
    const background = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    background.setAttribute('width', '100%');
    background.setAttribute('height', '100%');
    background.setAttribute('fill', getComputedStyle(figure).backgroundColor);
    clone.insertBefore(background, clone.firstChild);
    return {
      slug: figure.closest('[data-slug]').dataset.slug,
      label: svg.getAttribute('aria-label') || '',
      caption: figure.querySelector('figcaption')?.firstChild?.textContent.trim() || '',
      svg: finish(svg, clone),
    };
  });
  return { diagrams, plates };
}

const site = await serveDist(dist);
const profile = await fs.mkdtemp(path.join(os.tmpdir(), 'ground-truth-figures-'));
const browser = spawn(
  chrome,
  [...chromeArguments(profile), '--remote-debugging-port=0', 'about:blank'],
  { stdio: 'ignore' },
);

try {
  let port;
  for (let attempt = 0; attempt < 100 && !port; attempt++) {
    await new Promise((resolve) => setTimeout(resolve, 100));
    port = (await fs.readFile(path.join(profile, 'DevToolsActivePort'), 'utf8').catch(() => ''))
      .split('\n')[0]
      .trim();
  }
  if (!port) throw new Error('Chrome did not start its DevTools endpoint.');
  const target = await (
    await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' })
  ).json();
  const socket = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    socket.addEventListener('open', resolve);
    socket.addEventListener('error', reject);
  });
  let id = 0;
  const pending = new Map();
  socket.addEventListener('message', (event) => {
    const message = JSON.parse(event.data);
    pending.get(message.id)?.(message);
    pending.delete(message.id);
  });
  const send = (method, params = {}) =>
    new Promise((resolve, reject) => {
      const messageId = ++id;
      pending.set(messageId, (message) =>
        message.error ? reject(new Error(message.error.message)) : resolve(message.result),
      );
      socket.send(JSON.stringify({ id: messageId, method, params }));
    });
  const evaluate = async (expression) =>
    (await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true })).result
      .value;

  // Pictures for paper and e-readers use the light theme, whatever this machine prefers.
  await send('Emulation.setEmulatedMedia', {
    features: [{ name: 'prefers-color-scheme', value: 'light' }],
  });
  await send('Page.navigate', { url: `${site.origin}${base}/print/` });
  let rendered = false;
  for (let attempt = 0; attempt < 240 && !rendered; attempt++) {
    await new Promise((resolve) => setTimeout(resolve, 250));
    rendered = await evaluate(
      `document.readyState === 'complete' && [...document.querySelectorAll('.mermaid')].every((box) => box.querySelector('svg'))`,
    ).catch(() => false);
  }
  if (!rendered) throw new Error('Diagrams did not finish rendering within 60 seconds.');
  await evaluate('document.fonts.ready.then(() => true)');
  const figures = await evaluate(`(${collectFigures})()`);
  socket.close();

  await fs.mkdir(output, { recursive: true });
  const index = { diagrams: {}, plates: {} };
  for (const { key, svg } of figures.diagrams) {
    const file = `diagram-${key}.svg`;
    await fs.writeFile(path.join(output, file), svg);
    index.diagrams[key] = file;
  }
  for (const { slug, label, caption, svg } of figures.plates) {
    const file = `plate-${slug.replaceAll('/', '-')}.svg`;
    await fs.writeFile(path.join(output, file), svg);
    index.plates[slug] = { file, label, caption };
  }
  await fs.writeFile(path.join(output, 'index.json'), JSON.stringify(index, null, 2));
  console.log(
    `Figures exported: ${figures.diagrams.length} diagrams and ${figures.plates.length} plates.`,
  );
} finally {
  // Chrome keeps writing to its profile while it shuts down; wait before removing it.
  const exited = new Promise((resolve) => browser.once('exit', resolve));
  browser.kill();
  await Promise.race([exited, new Promise((resolve) => setTimeout(resolve, 5000))]);
  site.close();
  await fs.rm(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
}
