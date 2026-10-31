/**
 * Render the complete print edition to a PDF with a local headless Chrome.
 * Run after the complete build. The built site is served from memory under the
 * configured base path, so the PDF matches the published print edition.
 * Set CHROME_PATH when Chrome or Chromium is not in a standard location.
 */
import fs from 'node:fs/promises';
import { existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fromWebsite } from '../src/lib/paths.mjs';
import { base, chromeArguments, findChrome, serveDist } from './browser.mjs';

const dist = fromWebsite('dist');
const output = path.join(dist, 'downloads/ground-truth.pdf');

const chrome = findChrome();
if (!chrome) {
  console.error('Chrome or Chromium was not found. Set CHROME_PATH to its executable.');
  process.exit(2);
}
if (!existsSync(path.join(dist, 'print/index.html'))) {
  console.error('dist/print/index.html was not found. Run the complete build first.');
  process.exit(2);
}

const site = await serveDist(dist);
const profile = await fs.mkdtemp(path.join(os.tmpdir(), 'ground-truth-pdf-'));

try {
  await fs.mkdir(path.dirname(output), { recursive: true });
  // An asynchronous child keeps this process free to serve Chrome's requests.
  const chromeRun = spawn(
    chrome,
    [
      ...chromeArguments(profile),
      '--no-pdf-header-footer',
      // Diagrams render in the browser; allow them to finish before printing.
      '--virtual-time-budget=30000',
      `--print-to-pdf=${output}`,
      `${site.origin}${base}/print/`,
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
  site.close();
  await fs.rm(profile, { recursive: true, force: true });
}
