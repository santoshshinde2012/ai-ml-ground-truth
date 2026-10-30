/**
 * Render the complete print edition to a PDF with a local headless Chrome.
 * Run after the complete build. The built site is served from memory under the
 * configured base path, so the PDF matches the published print edition.
 * Set CHROME_PATH when Chrome or Chromium is not in a standard location.
 */
import fs from 'node:fs/promises';
import { existsSync } from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fromWebsite } from '../src/lib/paths.mjs';

const dist = fromWebsite('dist');
const output = path.join(dist, 'downloads/ground-truth.pdf');
const base = (process.env.BASE_PATH ?? '/ai-ml-ground-truth').replace(/\/$/, '');
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

function findChrome() {
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

const chrome = findChrome();
if (!chrome) {
  console.error('Chrome or Chromium was not found. Set CHROME_PATH to its executable.');
  process.exit(2);
}
if (!existsSync(path.join(dist, 'print/index.html'))) {
  console.error('dist/print/index.html was not found. Run the complete build first.');
  process.exit(2);
}

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
const profile = await fs.mkdtemp(path.join(os.tmpdir(), 'ground-truth-pdf-'));

try {
  await fs.mkdir(path.dirname(output), { recursive: true });
  // An asynchronous child keeps this process free to serve Chrome's requests.
  const chromeRun = spawn(
    chrome,
    [
      '--headless=new',
      '--disable-gpu',
      ...(process.platform === 'linux' ? ['--no-sandbox'] : []),
      '--no-pdf-header-footer',
      // Diagrams render in the browser; allow them to finish before printing.
      '--virtual-time-budget=30000',
      `--user-data-dir=${profile}`,
      `--print-to-pdf=${output}`,
      `http://127.0.0.1:${port}${base}/print/`,
    ],
    { stdio: ['ignore', 'ignore', 'pipe'], timeout: 180_000 },
  );
  let log = '';
  chromeRun.stderr.on('data', (chunk) => (log = (log + chunk).slice(-20_000)));
  const status = await new Promise((resolve) => {
    chromeRun.on('error', (error) => resolve(error));
    chromeRun.on('close', (code) => resolve(code));
  });
  const pdf = await fs.readFile(output).catch(() => null);
  if (status !== 0 || !pdf || pdf.subarray(0, 5).toString() !== '%PDF-') {
    console.error(log || status || 'Chrome did not produce a PDF.');
    process.exitCode = 1;
  } else {
    const pages = pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g)?.length ?? 0;
    console.log(
      `PDF exported: dist/downloads/ground-truth.pdf · ${pages} pages · ${Math.round(pdf.length / 1024)} KiB`,
    );
  }
} finally {
  server.close();
  await fs.rm(profile, { recursive: true, force: true });
}
