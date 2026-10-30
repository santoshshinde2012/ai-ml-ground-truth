import fs from 'node:fs/promises';
import sharp from 'sharp';
import { getBook, bookHref, basePath, orderForEdition } from '../src/lib/book.mjs';
import { edition, updated } from '../src/lib/catalog.mjs';
import { fromRepository, fromWebsite } from '../src/lib/paths.mjs';

await fs.mkdir(fromWebsite('.cache'), { recursive: true });
await fs.cp(fromRepository('labs/reference'), fromWebsite('public/lab-reference'), {
  recursive: true,
});
await sharp(fromWebsite('public/cover.svg')).png().toFile(fromWebsite('public/cover.png'));
const pages = await getBook();
const sources = new Map();
for (const page of pages) {
  const pattern = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)(?:\s+[^)]*)?\)/g;
  for (const match of page.markdown.matchAll(pattern)) {
    const [, label, url] = match;
    if (!sources.has(url))
      sources.set(url, { url, label: label.replaceAll('**', ''), locations: [] });
    const location = { title: page.title, href: bookHref(page.slug), file: page.file };
    if (!sources.get(url).locations.some((x) => x.file === page.file))
      sources.get(url).locations.push(location);
  }
}
await fs.writeFile(
  fromWebsite('public/sources.json'),
  JSON.stringify(
    {
      edition,
      updated,
      note: 'Editorial inventory; inclusion and HTTP availability do not independently validate a claim.',
      sources: [...sources.values()].sort((a, b) => a.url.localeCompare(b.url)),
    },
    null,
    2,
  ),
);
const titlePage = {
  title: 'Ground Truth',
  slug: 'title-page',
  html: `<img src="${basePath()}/cover.png" alt="Ground Truth. Build the thing. Understand why. An open field guide for working developers."/><h1>Ground Truth</h1><p>A working developer’s path into AI and machine learning.</p><p>Written by Santosh Shinde · Edition ${edition}</p><p>Text and illustrations: CC BY 4.0. Code: MIT licence. External sources keep their own terms. The reference data and business results are simulated teaching examples.</p>`,
};
await fs.writeFile(
  fromWebsite('.cache/book-export.json'),
  JSON.stringify([
    titlePage,
    ...orderForEdition(pages).map(({ title, slug, html }) => ({ title, slug, html })),
  ]),
);
console.log(
  `Prepared ${pages.length} canonical documents, ${sources.size} source URLs and reference assets.`,
);
