/**
 * Render the book's covers from design/cover.html with a local headless Chrome:
 * - public/book-cover.png: 1600 x 2400 px store cover, used by the EPUB and Google Play
 * - dist/downloads/ground-truth-kindle-cover.jpg: 1600 x 2560 px, Amazon's ideal Kindle size
 * - dist/downloads/ground-truth-paperback-cover.pdf: back, spine and front on one sheet at
 *   400 DPI, sized for the page count in .cache/paperback.json from export-paperback.mjs
 * Every glyph must come from a font bundled with the book, so the covers look the same
 * whichever computer renders them.
 */
import fs from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import sharp from 'sharp';
import { PDFDocument } from 'pdf-lib';
import { fromWebsite } from '../src/lib/paths.mjs';
import { edition } from '../src/lib/catalog.mjs';
import { bleed, coverSize, spineTextMinimumPages, trim } from '../src/lib/print-spec.mjs';
import { findChrome, launchChrome, unbundledFonts } from './browser.mjs';

const chrome = findChrome();
if (!chrome) {
  console.error('Chrome or Chromium was not found. Set CHROME_PATH to its executable.');
  process.exit(2);
}
const design = pathToFileURL(fromWebsite('design/cover.html')).href;
const downloads = fromWebsite('dist/downloads');
// The front is 1600 design pixels wide, whatever the format.
const pixelsPerInch = 1600 / trim.width;

/** Render one format at `scale` device pixels per design pixel, as a PNG buffer. */
async function render(page, format, width, height, scale, properties = {}) {
  await page.send('Emulation.setDeviceMetricsOverride', {
    width: Math.ceil(width),
    height: Math.ceil(height),
    deviceScaleFactor: scale,
    mobile: false,
  });
  await page.send('Page.navigate', { url: 'about:blank' });
  await page.send('Page.navigate', { url: design });
  await page.waitFor(
    `location.href === ${JSON.stringify(design)} && document.readyState === 'complete'`,
    30,
    'The cover design did not load.',
  );
  await page.evaluate(`(() => {
    const root = document.documentElement;
    root.dataset.format = ${JSON.stringify(format)};
    for (const [name, value] of Object.entries(${JSON.stringify(properties)}))
      root.style.setProperty(name, value);
    return document.fonts.ready.then(() => true);
  })()`);
  const unbundled = await unbundledFonts(page, 'body, body *');
  if (unbundled.length)
    throw new Error(
      `The ${format} cover uses fonts that are not bundled:\n${unbundled.join('\n')}`,
    );
  const { data } = await page.send('Page.captureScreenshot', {
    format: 'png',
    captureBeyondViewport: true,
    clip: { x: 0, y: 0, width, height, scale: 1 },
  });
  return Buffer.from(data, 'base64');
}

const browser = await launchChrome(chrome);
try {
  const page = await browser.newPage();
  await fs.mkdir(downloads, { recursive: true });

  await sharp(await render(page, 'store', 1600, 2400, 1))
    .png({ compressionLevel: 9 })
    .toFile(fromWebsite('public/book-cover.png'));

  const kindle = path.join(downloads, 'ground-truth-kindle-cover.jpg');
  await sharp(await render(page, 'kindle', 1600, 2560, 1))
    .jpeg({ quality: 92, chromaSubsampling: '4:4:4', mozjpeg: true })
    .toFile(kindle);

  const record = fromWebsite('.cache/paperback.json');
  if (!existsSync(record)) {
    console.log(
      'Covers exported: store and Kindle. Run export-paperback.mjs first for the paperback cover.',
    );
  } else {
    const { pages } = JSON.parse(await fs.readFile(record, 'utf8'));
    const size = coverSize(pages);
    const width = size.width * pixelsPerInch;
    const height = size.height * pixelsPerInch;
    const dpi = 400;
    const png = await render(page, 'print', width, height, dpi / pixelsPerInch, {
      '--spine': `${size.spine * pixelsPerInch}px`,
      '--bleed': `${bleed * pixelsPerInch}px`,
      ...(pages < spineTextMinimumPages ? { '--spine-text': 'none' } : {}),
    });
    const pdf = await PDFDocument.create();
    pdf.setTitle('Ground Truth: A working developer’s path into AI and machine learning');
    pdf.setAuthor('Santosh Shinde');
    pdf.setSubject(`Paperback cover, open edition ${edition}, ${pages} pages`);
    const sheet = pdf.addPage([size.width * 72, size.height * 72]);
    sheet.drawImage(await pdf.embedPng(png), {
      x: 0,
      y: 0,
      width: size.width * 72,
      height: size.height * 72,
    });
    const output = path.join(downloads, 'ground-truth-paperback-cover.pdf');
    await fs.writeFile(output, await pdf.save({ useObjectStreams: false }));
    await sharp(png)
      .resize({ width: 1600 })
      .png()
      .toFile(fromWebsite('.cache/paperback-cover-preview.png'));
    console.log(
      `Covers exported: store, Kindle and paperback · ${pages} pages · spine ${size.spine.toFixed(3)} in · cover ${size.width.toFixed(3)} x ${size.height} in at ${dpi} DPI · ${Math.round((await fs.stat(output)).size / 1024)} KiB`,
    );
  }
} finally {
  await browser.close();
}
