/**
 * Save the print edition's rendered diagrams and plates as self-contained SVG files,
 * so the EPUB carries the same pictures as the web book. Each picture, and each SVG
 * image in the chapters, is also saved as an opaque PNG for the Kindle edition, which
 * does not reliably display SVG. Run after the Astro build.
 * Uses a local headless Chrome; without one, it explains and exits, and the EPUB keeps
 * its text descriptions. Writes .cache/figures/ and .cache/figures/index.json.
 */
import fs from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';
import { fromWebsite } from '../src/lib/paths.mjs';
import { base, findChrome, launchChrome, openRenderedPage, serveDist } from './browser.mjs';

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
  // Where a picture sits on the page, for its PNG capture.
  const box = (element) => {
    const { left, top, width, height } = element.getBoundingClientRect();
    return { x: left + scrollX, y: top + scrollY, width, height };
  };
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
  const diagrams = [...document.querySelectorAll('.mermaid[data-diagram]')].flatMap((container) => {
    const svg = container.querySelector('svg');
    return svg
      ? [{ key: container.dataset.diagram, svg: finish(svg, svg.cloneNode(true)), box: box(svg) }]
      : [];
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
      box: box(svg),
    };
  });
  const images = [...document.querySelectorAll('.prose img')]
    .filter((image) => new URL(image.src).pathname.endsWith('.svg'))
    .map((image) => ({
      pathname: decodeURIComponent(new URL(image.src).pathname),
      box: box(image),
    }));
  return { diagrams, plates, images };
}

/** Capture `box` as an opaque, palette-compressed PNG about 1600 px wide. */
async function capturePNG(page, box, file) {
  const scale = Math.max(1, Math.min(4, 1600 / box.width, 2400 / box.height));
  const { data } = await page.send('Page.captureScreenshot', {
    format: 'png',
    captureBeyondViewport: true,
    clip: { ...box, scale },
  });
  await sharp(Buffer.from(data, 'base64'))
    .flatten({ background: '#ffffff' })
    .resize({ width: 1600, withoutEnlargement: true })
    // Flat-colour line art needs no dithering, which only adds noise that compresses badly.
    .png({ palette: true, quality: 90, dither: 0, compressionLevel: 9, effort: 10 })
    .toFile(file);
}

const site = await serveDist(dist);
const browser = await launchChrome(chrome);
try {
  const page = await browser.newPage();
  await openRenderedPage(page, `${site.origin}${base}/print/`);
  // Kindle pages are white: capture pictures on white rather than the site's paper colour.
  await page.evaluate(
    `document.head.insertAdjacentHTML('beforeend', '<style>html, body, main { background: #fff !important; }</style>'); true`,
  );
  const figures = await page.evaluate(`(${collectFigures})()`);

  await fs.mkdir(output, { recursive: true });
  const index = { diagrams: {}, plates: {}, images: {} };
  for (const { key, svg, box } of figures.diagrams) {
    const file = `diagram-${key}.svg`;
    await fs.writeFile(path.join(output, file), svg);
    await capturePNG(page, box, path.join(output, file.replace(/\.svg$/, '.png')));
    index.diagrams[key] = file;
  }
  for (const { slug, label, caption, svg, box } of figures.plates) {
    const file = `plate-${slug.replaceAll('/', '-')}.svg`;
    await fs.writeFile(path.join(output, file), svg);
    await capturePNG(page, box, path.join(output, file.replace(/\.svg$/, '.png')));
    index.plates[slug] = { file, label, caption };
  }
  // SVG images in the chapters, keyed by their path under the site base.
  for (const { pathname, box } of figures.images) {
    const relative = pathname.slice(base.length).replace(/^\/+/, '');
    if (index.images[relative]) continue;
    const file = `image-${relative.replace(/\.svg$/, '').replaceAll(/[^a-z0-9]+/gi, '-')}.png`;
    await capturePNG(page, box, path.join(output, file));
    index.images[relative] = file;
  }
  await fs.writeFile(path.join(output, 'index.json'), JSON.stringify(index, null, 2));
  const pngs = (await fs.readdir(output)).filter((name) => name.endsWith('.png'));
  const details = await Promise.all(
    pngs.map(async (name) => ({
      name,
      bytes: (await fs.stat(path.join(output, name))).size,
      ...(await sharp(path.join(output, name)).metadata()),
    })),
  );
  const largest = details.toSorted((a, b) => b.bytes - a.bytes)[0];
  console.log(
    `Figures exported: ${figures.diagrams.length} diagrams, ${figures.plates.length} plates and ${Object.keys(index.images).length} chapter images · PNGs ${Math.ceil(details.reduce((total, { bytes }) => total + bytes, 0) / 1024)} KiB, ${details.filter(({ isPalette }) => isPalette).length} of ${details.length} with a palette, largest ${largest.name} ${largest.width} x ${largest.height}`,
  );
} finally {
  await browser.close();
  site.close();
}
