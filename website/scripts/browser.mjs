/**
 * Shared helpers for the build steps that use a local headless Chrome:
 * find the browser and serve the built site under its configured base path.
 * Set CHROME_PATH when Chrome or Chromium is not in a standard location.
 */
import fs from 'node:fs/promises';
import { existsSync } from 'node:fs';
import http from 'node:http';
import path from 'node:path';

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
