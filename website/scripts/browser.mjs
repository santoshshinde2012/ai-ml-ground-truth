/**
 * Shared helpers for the build steps that use a local headless Chrome:
 * find the browser, serve the built site under its configured base path, and
 * drive pages through the DevTools protocol.
 * Set CHROME_PATH when Chrome or Chromium is not in a standard location.
 */
import fs from 'node:fs/promises';
import { existsSync } from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';

export const base = (process.env.BASE_PATH ?? '/ai-ml-ground-truth').replace(/\/$/, '');

const mediaTypes = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.mjs': 'text/javascript',
  '.json': 'application/json',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.ttf': 'font/ttf',
};

export function findChrome() {
  const candidates = [
    process.env.CHROME_PATH,
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  ];
  return candidates.find((candidate) => candidate && existsSync(candidate));
}

/** Arguments shared by every headless Chrome run. */
export function chromeArguments(profile) {
  return [
    '--headless=new',
    '--disable-gpu',
    // An unfocused tab would otherwise slow its timers and pause animation frames.
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding',
    ...(process.platform === 'linux' ? ['--no-sandbox'] : []),
    `--user-data-dir=${profile}`,
  ];
}

/** Serve `dist` from memory at http://127.0.0.1:<port><base>/ until `close()`. */
export async function serveDist(dist) {
  const server = http.createServer(async (request, response) => {
    const { pathname } = new URL(request.url, 'http://localhost');
    const relative = decodeURIComponent(pathname).slice(base.length).replace(/^\/+/, '');
    let file = path.resolve(dist, relative);
    if (!pathname.startsWith(`${base}/`) || (file !== dist && !file.startsWith(dist + path.sep))) {
      response.writeHead(404).end();
      return;
    }
    if (!path.extname(file)) file = path.join(file, 'index.html');
    try {
      const body = await fs.readFile(file);
      response.writeHead(200, {
        'Content-Type': mediaTypes[path.extname(file)] ?? 'application/octet-stream',
      });
      response.end(body);
    } catch {
      response.writeHead(404).end();
    }
  });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const { port } = /** @type {import('node:net').AddressInfo} */ (server.address());
  return { origin: `http://127.0.0.1:${port}`, close: () => server.close() };
}

/**
 * Start headless Chrome with the DevTools protocol. `newPage()` opens a tab whose
 * `send(method, params)` calls the protocol and `evaluate(expression)` returns a value.
 */
export async function launchChrome(chrome) {
  const profile = await fs.mkdtemp(path.join(os.tmpdir(), 'ground-truth-chrome-'));
  const browser = spawn(
    chrome,
    [...chromeArguments(profile), '--remote-debugging-port=0', 'about:blank'],
    { stdio: 'ignore' },
  );
  const sockets = new Set();
  async function close() {
    for (const socket of sockets) socket.close();
    // Chrome keeps writing to its profile while it shuts down; wait before removing it.
    const exited = new Promise((resolve) => browser.once('exit', resolve));
    browser.kill();
    await Promise.race([exited, new Promise((resolve) => setTimeout(resolve, 5000))]);
    await fs.rm(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
  }
  let port;
  for (let attempt = 0; attempt < 100 && !port; attempt++) {
    await new Promise((resolve) => setTimeout(resolve, 100));
    port = (await fs.readFile(path.join(profile, 'DevToolsActivePort'), 'utf8').catch(() => ''))
      .split('\n')[0]
      .trim();
  }
  if (!port) {
    await close();
    throw new Error('Chrome did not start its DevTools endpoint.');
  }
  async function newPage() {
    const target = await (
      await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, { method: 'PUT' })
    ).json();
    const socket = new WebSocket(target.webSocketDebuggerUrl);
    sockets.add(socket);
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
    const evaluate = async (expression) => {
      const { result, exceptionDetails } = await send('Runtime.evaluate', {
        expression,
        returnByValue: true,
        awaitPromise: true,
      });
      if (exceptionDetails)
        throw new Error(exceptionDetails.exception?.description || exceptionDetails.text);
      return result.value;
    };
    /** Poll `expression` until it is truthy; fail with `message` after `seconds`. */
    const waitFor = async (expression, seconds, message) => {
      for (let attempt = 0; attempt < seconds * 4; attempt++) {
        if (await evaluate(expression).catch(() => false)) return;
        await new Promise((resolve) => setTimeout(resolve, 250));
      }
      throw new Error(message);
    };
    await send('Page.bringToFront');
    await send('Emulation.setFocusEmulationEnabled', { enabled: true });
    return { send, evaluate, waitFor };
  }
  return { newPage, close };
}

/** Load the print-ready page at `url` and wait until its diagrams and fonts are ready. */
export async function openRenderedPage(page, url) {
  // Pictures for paper and e-readers use the light theme, whatever this machine prefers.
  await page.send('Emulation.setEmulatedMedia', {
    features: [{ name: 'prefers-color-scheme', value: 'light' }],
  });
  await page.send('Page.navigate', { url });
  // Check the address too: until the new page commits, the blank tab also reads complete.
  await page.waitFor(
    `location.href === ${JSON.stringify(url)} && document.readyState === 'complete' && [...document.querySelectorAll('.mermaid')].every((box) => box.querySelector('svg'))`,
    60,
    'Diagrams did not finish rendering within 60 seconds.',
  );
  // Lazy images load only when scrolled into view; captures and print need them all now.
  await page.evaluate(`Promise.all([...document.images].map((image) => {
    image.loading = 'eager';
    return image.complete && image.naturalWidth
      ? true
      : new Promise((resolve) => image.addEventListener('load', resolve) || image.addEventListener('error', resolve));
  })).then(() => true)`);
  await page.waitFor(
    `[...document.images].every((image) => image.complete && image.naturalWidth)`,
    30,
    'Images did not finish loading within 30 seconds.',
  );
  await page.evaluate('document.fonts.ready.then(() => true)');
}

/**
 * Fonts that draw text in `selector` but are installed on this computer rather than
 * bundled with the book. Such text would print differently on another machine.
 */
export async function unbundledFonts(page, selector) {
  await page.send('DOM.enable');
  await page.send('CSS.enable');
  const { root } = await page.send('DOM.getDocument', { depth: -1 });
  const { nodeIds } = await page.send('DOM.querySelectorAll', {
    nodeId: root.nodeId,
    selector,
  });
  const found = new Map();
  for (const nodeId of nodeIds) {
    const { fonts } = await page.send('CSS.getPlatformFontsForNode', { nodeId });
    for (const { familyName, isCustomFont } of fonts)
      if (!isCustomFont && !found.has(familyName)) {
        const { outerHTML } = await page.send('DOM.getOuterHTML', { nodeId });
        found.set(familyName, outerHTML.replaceAll(/\s+/g, ' ').slice(0, 160));
      }
  }
  return [...found].map(([family, sample]) => `${family}: ${sample}`);
}
