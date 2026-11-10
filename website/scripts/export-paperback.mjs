/**
 * Print the paperback interior for Amazon KDP: 7 x 10 inch pages with mirrored margins,
 * running heads, page numbers and a contents page with page numbers. Run after the
 * complete build. The first print finds the page where each section starts, from the
 * PDF's bookmarks; a blank page then goes before any section that would start on a
 * left-hand page, and the last print carries the page numbers in the contents. It is then
 * checked against KDP's rules, including where ink falls on every page when Poppler's
 * pdftoppm is installed. Set PAPERBACK_ISBN to print the ISBN on the copyright page.
 * Writes dist/downloads/ground-truth-paperback.pdf and .cache/paperback.json.
 */
import fs from 'node:fs/promises';
import { existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import sharp from 'sharp';
import { PDFArray, PDFDict, PDFDocument, PDFName } from 'pdf-lib';
import { fromWebsite } from '../src/lib/paths.mjs';
import { edition } from '../src/lib/catalog.mjs';
import {
  interiorProblems,
  margins,
  minimumInsideMargin,
  minimumOuterMargin,
  trim,
} from '../src/lib/print-spec.mjs';
import {
  base,
  findChrome,
  launchChrome,
  openRenderedPage,
  serveDist,
  unbundledFonts,
} from './browser.mjs';

const dist = fromWebsite('dist');
const output = path.join(dist, 'downloads/ground-truth-paperback.pdf');
const isbn = process.env.PAPERBACK_ISBN?.trim();

function validISBN(value) {
  const digits = value.replaceAll(/[\s-]/g, '');
  if (!/^97[89]\d{10}$/.test(digits)) return false;
  const sum = [...digits].reduce((total, digit, index) => total + digit * (index % 2 ? 3 : 1), 0);
  return sum % 10 === 0;
}
if (isbn && !validISBN(isbn)) {
  console.error(`PAPERBACK_ISBN is not a valid ISBN-13: ${isbn}`);
  process.exit(2);
}
const chrome = findChrome();
if (!chrome) {
  console.error('Chrome or Chromium was not found. Set CHROME_PATH to its executable.');
  process.exit(2);
}
if (!existsSync(path.join(dist, 'paperback/index.html'))) {
  console.error('dist/paperback/index.html was not found. Run the complete build first.');
  process.exit(2);
}

/** Elements wider than the text block, measured at the printed width. */
async function overflowingElements(page) {
  const width = Math.round((trim.width - margins.inside - margins.outside) * 96);
  await page.send('Emulation.setDeviceMetricsOverride', {
    width,
    height: 1200,
    deviceScaleFactor: 1,
    mobile: false,
  });
  const found = await page.evaluate(`new Promise((resolve) => requestAnimationFrame(() => {
    const limit = document.documentElement.clientWidth + 0.5;
    const wide = [];
    for (const element of document.querySelectorAll('.paperback-book *')) {
      const { right, width } = element.getBoundingClientRect();
      const clipped = element.scrollWidth > element.clientWidth + 1 &&
        !['visible', 'clip'].includes(getComputedStyle(element).overflowX);
      if (width && (right > limit || clipped))
        wide.push(element.closest('[data-slug]')?.dataset.slug + ': <' + element.tagName.toLowerCase() + '> ' +
          (element.textContent || '').trim().slice(0, 60));
    }
    resolve(wide);
  }))`);
  await page.send('Emulation.clearDeviceMetricsOverride');
  return found;
}

async function printPDF(page) {
  const { stream } = await page.send('Page.printToPDF', {
    preferCSSPageSize: true,
    printBackground: true,
    generateTaggedPDF: true,
    generateDocumentOutline: true,
    transferMode: 'ReturnAsStream',
  });
  const chunks = [];
  for (;;) {
    const { data, base64Encoded, eof } = await page.send('IO.read', { handle: stream });
    chunks.push(Buffer.from(data, base64Encoded ? 'base64' : 'utf8'));
    if (eof) break;
  }
  await page.send('IO.close', { handle: stream });
  return Buffer.concat(chunks);
}

/** Bookmarks in reading order, with the page each one points to. */
function bookmarks(pdf) {
  const pageNumbers = new Map(
    pdf.getPages().map((page, index) => [page.ref.toString(), index + 1]),
  );
  const named = new Map();
  const collect = (node) => {
    const pairs = node?.lookup(PDFName.of('Names'));
    for (let index = 0; pairs && index < pairs.size(); index += 2)
      named.set(
        pairs.lookup(index).decodeText?.() ?? pairs.lookup(index).toString(),
        pairs.lookup(index + 1),
      );
    const kids = node?.lookup(PDFName.of('Kids'));
    for (let index = 0; kids && index < kids.size(); index++) collect(kids.lookup(index));
  };
  collect(pdf.catalog.lookup(PDFName.of('Names'))?.lookup(PDFName.of('Dests')));
  const target = (item) => {
    let destination =
      item.lookup(PDFName.of('Dest')) ?? item.lookup(PDFName.of('A'))?.lookup(PDFName.of('D'));
    if (destination && !(destination instanceof PDFArray))
      destination = named.get(destination.decodeText?.() ?? destination.toString());
    if (destination instanceof PDFDict) destination = destination.lookup(PDFName.of('D'));
    return destination instanceof PDFArray ? pageNumbers.get(destination.get(0).toString()) : null;
  };
  const items = [];
  const visit = (item) => {
    for (; item; item = item.lookup(PDFName.of('Next'))) {
      items.push({
        title: item.lookup(PDFName.of('Title')).decodeText().trim(),
        page: target(item),
      });
      visit(item.lookup(PDFName.of('First')));
    }
  };
  visit(pdf.catalog.lookup(PDFName.of('Outlines'))?.lookup(PDFName.of('First')));
  return items;
}

/**
 * The page where each section starts, matched to the bookmarks in order. Bookmarks lose
 * the space where a long heading wraps, so titles are compared without spaces.
 */
function sectionStarts(items, sections) {
  const key = (text) => text.replaceAll(/\s+/g, '');
  const starts = {};
  let position = 0;
  for (const { id, title } of sections) {
    while (position < items.length && key(items[position].title) !== key(title)) position++;
    if (position === items.length || !items[position].page)
      throw new Error(`No bookmark for the section "${title}".`);
    starts[id] = items[position++].page;
  }
  return starts;
}

/** Fonts that are not embedded, or are Type 3, which printers handle poorly. */
function fontProblems(pdf) {
  const problems = new Set();
  for (const [, object] of pdf.context.enumerateIndirectObjects()) {
    if (!(object instanceof PDFDict) || object.lookup(PDFName.of('Type')) !== PDFName.of('Font'))
      continue;
    const subtype = object.lookup(PDFName.of('Subtype'));
    const name = object.lookup(PDFName.of('BaseFont'))?.toString() ?? '(unnamed)';
    if (subtype === PDFName.of('Type3')) {
      problems.add(`${name} is a Type 3 font`);
      continue;
    }
    const font =
      subtype === PDFName.of('Type0')
        ? object.lookup(PDFName.of('DescendantFonts')).lookup(0)
        : object;
    const descriptor = font.lookup(PDFName.of('FontDescriptor'));
    if (!['FontFile', 'FontFile2', 'FontFile3'].some((key) => descriptor?.has(PDFName.of(key))))
      problems.add(`${name} is not embedded`);
  }
  return [...problems];
}

/**
 * Where ink falls on each page, in inches from each edge, when pdftoppm is available.
 * Odd pages are right-hand pages, so their binding edge is on the left.
 */
async function inkProblems(file, pages) {
  if (spawnSync('pdftoppm', ['-v']).error) return null;
  const folder = await fs.mkdtemp(path.join(os.tmpdir(), 'ground-truth-ink-'));
  const dpi = 40;
  try {
    const run = spawnSync('pdftoppm', [
      '-r',
      String(dpi),
      '-gray',
      '-png',
      file,
      path.join(folder, 'p'),
    ]);
    if (run.status !== 0) throw new Error(`pdftoppm failed: ${run.stderr}`);
    const inside = minimumInsideMargin(pages);
    const tolerance = 1.5 / dpi;
    const problems = [];
    for (const name of (await fs.readdir(folder)).sort()) {
      const number = Number(name.match(/(\d+)\.png$/)[1]);
      const { data, info } = await sharp(path.join(folder, name))
        .raw()
        .toBuffer({ resolveWithObject: true });
      let [left, top, right, bottom] = [info.width, info.height, -1, -1];
      for (let y = 0; y < info.height; y++)
        for (let x = 0; x < info.width; x++)
          if (data[(y * info.width + x) * info.channels] < 235) {
            left = Math.min(left, x);
            right = Math.max(right, x);
            top = Math.min(top, y);
            bottom = Math.max(bottom, y);
          }
      if (right < 0) continue;
      const distance = {
        left: left / dpi,
        right: (info.width - 1 - right) / dpi,
        top: top / dpi,
        bottom: (info.height - 1 - bottom) / dpi,
      };
      const binding = number % 2 ? 'left' : 'right';
      for (const [edge, value] of Object.entries(distance)) {
        const needed = edge === binding ? inside : minimumOuterMargin;
        if (value + tolerance < needed)
          problems.push(
            `page ${number}: ink ${value.toFixed(2)} in from the ${edge} edge (needs ${needed} in)`,
          );
      }
    }
    return problems;
  } finally {
    await fs.rm(folder, { recursive: true, force: true });
  }
}

const site = await serveDist(dist);
const browser = await launchChrome(chrome);
try {
  const page = await browser.newPage();
  await openRenderedPage(page, `${site.origin}${base}/paperback/`);
  // Lay the page out with its print styles from here on, and let the fonts they need load.
  await page.send('Emulation.setEmulatedMedia', {
    media: 'print',
    features: [{ name: 'prefers-color-scheme', value: 'light' }],
  });
  await page.evaluate(
    'document.fonts.ready.then(() => new Promise((resolve) => setTimeout(resolve, 300))).then(() => document.fonts.ready).then(() => true)',
  );
  const wide = await overflowingElements(page);
  if (wide.length)
    throw new Error(
      `Content is wider than the printed text block:\n${wide.slice(0, 15).join('\n')}`,
    );
  const unbundled = await unbundledFonts(page, '.paperback-book, .paperback-book *');
  if (unbundled.length)
    throw new Error(
      `Some text uses fonts that are not bundled with the book:\n${unbundled.join('\n')}`,
    );
  if (isbn)
    await page.evaluate(`(() => {
      const line = document.querySelector('.paperback-isbn');
      line.textContent = ${JSON.stringify(`ISBN ${isbn} (paperback)`)};
      line.hidden = false;
      return true;
    })()`);
  const sections = await page.evaluate(
    `[...document.querySelectorAll('.paperback-section')].map((section) => ({ id: section.id, title: section.querySelector(':scope > h1').textContent.trim() }))`,
  );

  const starts = async (pdf) => sectionStarts(bookmarks(await PDFDocument.load(pdf)), sections);
  // Each section begins on a fresh page, so a blank page before one moves only what follows.
  const first = await starts(await printPDF(page));
  await page.evaluate(`(() => {
    const starts = ${JSON.stringify(first)};
    let added = 0;
    for (const section of document.querySelectorAll('.paperback-section'))
      if ((starts[section.id] + added) % 2 === 0) {
        const blank = document.createElement('div');
        blank.className = 'paperback-front paperback-blank';
        section.before(blank);
        added++;
      }
    return true;
  })()`);
  const placed = await starts(await printPDF(page));
  const leftHand = sections.filter(({ id }) => placed[id] % 2 === 0);
  if (leftHand.length)
    throw new Error(
      `Sections still start on left-hand pages: ${leftHand.map(({ title }) => title).join(', ')}`,
    );
  // The numbers sit in a fixed column, so writing them in does not move the text.
  await page.evaluate(`(() => {
    const starts = ${JSON.stringify(placed)};
    for (const number of document.querySelectorAll('[data-section]'))
      number.textContent = starts[number.dataset.section];
    return true;
  })()`);
  const bytes = await printPDF(page);
  if (JSON.stringify(await starts(bytes)) !== JSON.stringify(placed))
    throw new Error('Writing the contents page numbers moved the sections.');

  const pdf = await PDFDocument.load(bytes);
  const pages = pdf.getPageCount();
  const problems = [...interiorProblems(pages), ...fontProblems(pdf)];
  for (const [index, sheet] of pdf.getPages().entries()) {
    const { width, height } = sheet.getSize();
    if (Math.abs(width - trim.width * 72) > 0.5 || Math.abs(height - trim.height * 72) > 0.5)
      problems.push(
        `page ${index + 1} is ${width} x ${height} pt, not ${trim.width} x ${trim.height} in`,
      );
  }
  pdf.setTitle('Ground Truth: A working developer’s path into AI and machine learning');
  pdf.setAuthor('Santosh Shinde');
  pdf.setSubject(`Paperback interior, open edition ${edition}`);
  await fs.mkdir(path.dirname(output), { recursive: true });
  await fs.writeFile(output, await pdf.save({ useObjectStreams: false }));
  const ink = await inkProblems(output, pages);
  if (ink) problems.push(...ink);
  if (problems.length) {
    const rejected = fromWebsite('.cache/paperback-rejected.pdf');
    await fs.rename(output, rejected);
    throw new Error(
      `The paperback interior does not meet KDP's rules; it is kept at ${path.relative(process.cwd(), rejected)}:\n${problems.slice(0, 20).join('\n')}`,
    );
  }
  await fs.mkdir(fromWebsite('.cache'), { recursive: true });
  await fs.writeFile(
    fromWebsite('.cache/paperback.json'),
    JSON.stringify({ edition, pages, isbn: isbn ?? null }, null, 2),
  );
  console.log(
    `Paperback interior exported: dist/downloads/ground-truth-paperback.pdf · ${pages} pages · ${Math.round((await fs.stat(output)).size / 1024)} KiB · ${ink ? 'margins checked on every page' : 'install Poppler to check margins on every page'}`,
  );
} finally {
  await browser.close();
  site.close();
}
