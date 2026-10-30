/**
 * Build an offline EPUB 3 from the same canonical prose used by the web edition.
 * The archive is deterministic: no wall-clock timestamps, network fetches or
 * third-party services. Run after `scripts/prepare.mjs` and the Astro build.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { parse, parseFragment } from 'parse5';
import { zipSync, strToU8 } from 'fflate';
import { websiteRoot, repositoryRoot, fromRepository } from '../src/lib/paths.mjs';
import { updated } from '../src/lib/catalog.mjs';

const root = websiteRoot;
const siteOrigin = new URL(process.env.SITE_URL ?? 'https://santoshshinde2012.github.io').origin;
const defaultBase = '/ai-ml-ground-truth/';
const siteBase = (process.env.BASE_PATH ?? defaultBase).replace(/\/?$/, '/');
const siteURL = `${siteOrigin}${siteBase}`;
const output = path.join(root, 'dist/downloads/ground-truth.epub');
const htmlNamespace = 'http://www.w3.org/1999/xhtml';
const mathNamespace = 'http://www.w3.org/1998/Math/MathML';
const svgNamespace = 'http://www.w3.org/2000/svg';
const voidElements = new Set([
  'area',
  'base',
  'br',
  'col',
  'embed',
  'hr',
  'img',
  'input',
  'link',
  'meta',
  'param',
  'source',
  'track',
  'wbr',
]);
const removedElements = new Set([
  'script',
  'style',
  'link',
  'template',
  'button',
  'input',
  'select',
  'textarea',
]);
const mediaTypes = {
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
};
const assets = new Map();
const warnings = new Set();
let coverImageHref = null;
let coverImageFilename = null;

function cleanXML(value) {
  return String(value).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '\ufffd');
}
function escapeText(value) {
  return cleanXML(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}
function escapeAttribute(value) {
  return escapeText(value).replaceAll('"', '&quot;');
}
function attributes(node) {
  return Object.fromEntries(
    (node.attrs || []).map((attribute) => [attribute.name, attribute.value]),
  );
}
function children(node) {
  return node.childNodes || [];
}
function findNode(node, predicate) {
  if (predicate(node)) return node;
  for (const child of children(node)) {
    const result = findNode(child, predicate);
    if (result) return result;
  }
  return null;
}
function textContent(node) {
  return node.nodeName === '#text' ? node.value : children(node).map(textContent).join('');
}
function hasClass(node, className) {
  return (attributes(node).class || '').split(/\s+/).includes(className);
}
async function exists(file) {
  try {
    return (await fs.stat(file)).isFile();
  } catch {
    return false;
  }
}

async function readBook() {
  const cachePath = path.join(root, '.cache/book-export.json');
  if (await exists(cachePath)) {
    const docs = JSON.parse(await fs.readFile(cachePath, 'utf8'));
    if (!Array.isArray(docs))
      throw new Error('.cache/book-export.json must be an ordered array of {title, slug, html}.');
    return docs;
  }
  const directory = path.join(root, 'dist/book');
  const docs = [];
  async function walk(folder) {
    for (const entry of await fs.readdir(folder, { withFileTypes: true })) {
      const file = path.join(folder, entry.name);
      if (entry.isDirectory()) await walk(file);
      else if (entry.name === 'index.html') {
        const document = parse(await fs.readFile(file, 'utf8'));
        const article = findNode(
          document,
          (node) => node.tagName === 'article' && hasClass(node, 'prose'),
        );
        const title = findNode(document, (node) => node.tagName === 'h1');
        if (!article || !title)
          throw new Error(`Built page has no canonical article/title: ${file}`);
        docs.push({
          title: textContent(title),
          slug: path.relative(directory, folder).split(path.sep).join('/'),
          tree: article,
        });
      }
    }
  }
  try {
    await walk(directory);
  } catch (error) {
    throw new Error(
      `No usable book export found. Run prepare and the site build first. ${error.message}`,
    );
  }
  // The canonical cache supplies reading order. This fallback is a recovery path.
  return docs.sort((a, b) => a.slug.localeCompare(b.slug, 'en'));
}

const documents = (await readBook()).filter((document) => document.slug !== 'publishing');
if (!documents.length) throw new Error('Refusing to export an empty book.');
const routes = new Map();
for (const [index, document] of documents.entries()) {
  if (
    typeof document.title !== 'string' ||
    typeof document.slug !== 'string' ||
    (!document.tree && typeof document.html !== 'string')
  ) {
    throw new Error(`Invalid book document at position ${index}.`);
  }
  document.slug = document.slug.replace(/^\/+|\/+$/g, '');
  if (!document.slug || routes.has(document.slug))
    throw new Error(`Duplicate/empty book slug: ${document.slug}`);
  document.filename =
    document.slug === 'title-page'
      ? 'cover.xhtml'
      : `chapter-${String(index + 1).padStart(3, '0')}.xhtml`;
  document.id = document.slug === 'title-page' ? 'cover-page' : `chapter-${index + 1}`;
  routes.set(document.slug, document.filename);
}

function resolveURL(value, document) {
  try {
    return new URL(value, `${siteURL}book/${document.slug}/`);
  } catch {
    return null;
  }
}

function rewriteLink(value, document) {
  if (value.startsWith('#')) return value;
  const url = resolveURL(value, document);
  if (!url) return null;
  if (!['http:', 'https:', 'mailto:', 'tel:'].includes(url.protocol)) return null;
  if (url.origin !== siteOrigin) return url.href;
  const match = decodeURIComponent(url.pathname).match(/(?:^|\/)book\/(.*?)\/?$/);
  const slug = match?.[1]?.replace(/\/+$/, '');
  if (slug && routes.has(slug)) return `${routes.get(slug)}${url.hash}`;
  // Downloads and pages outside the reading spine retain explicit online URLs.
  return url.href;
}

async function registerImage(source) {
  const extension = path.extname(source).toLowerCase();
  const mediaType = mediaTypes[extension];
  if (!mediaType) return null;
  const bytes = await fs.readFile(source);
  const hash = crypto.createHash('sha256').update(bytes).digest('hex').slice(0, 16);
  const filename = `${hash}${extension}`;
  if (!assets.has(filename)) assets.set(filename, { bytes, mediaType });
  return `../Images/${filename}`;
}

async function bundleImage(value, document) {
  const url = resolveURL(value, document);
  if (!url || url.origin !== siteOrigin) return null;
  const decoded = decodeURIComponent(url.pathname);
  const relative = decoded.startsWith(siteBase)
    ? decoded.slice(siteBase.length)
    : decoded.replace(/^\/+/, '');
  const candidates = [path.join(root, 'dist', relative), path.join(root, 'public', relative)];
  if (relative.startsWith('lab-reference/'))
    candidates.push(fromRepository('labs/reference', relative.slice('lab-reference/'.length)));
  const source = await (async () => {
    for (const candidate of candidates) {
      if (candidate.startsWith(`${repositoryRoot}${path.sep}`) && (await exists(candidate)))
        return candidate;
    }
    return null;
  })();
  if (!source) return null;
  return registerImage(source);
}

async function serialize(node, document, parentNamespace = htmlNamespace) {
  if (node.nodeName === '#text') return escapeText(node.value);
  if (node.nodeName === '#comment' || node.nodeName === '#documentType') return '';
  if (!node.tagName)
    return (
      await Promise.all(children(node).map((child) => serialize(child, document, parentNamespace)))
    ).join('');
  if (removedElements.has(node.tagName) || hasClass(node, 'katex-html')) return '';
  const original = attributes(node);
  if (hasClass(node, 'mermaid')) {
    return '<p class="diagram-offline">The diagram is described below. Its complete source follows the caption; the web edition provides the rendered graphic.</p>';
  }
  if (node.tagName === 'iframe' || node.tagName === 'video' || node.tagName === 'audio') {
    const href = rewriteLink(original.src || '', document);
    warnings.add(`Embedded media in ${document.slug} is represented by its online link.`);
    return `<p>Online media${href ? `: <a href="${escapeAttribute(href)}">${escapeText(original.title || original.src || 'Open the media')}</a>` : ' is available in the web edition.'}</p>`;
  }
  if (node.tagName === 'img') {
    const src =
      document.slug === 'title-page' &&
      /(?:^|\/)cover\.(?:svg|png)(?:[?#].*)?$/.test(original.src || '') &&
      coverImageHref
        ? coverImageHref
        : await bundleImage(original.src || '', document);
    if (!src) {
      warnings.add(
        `Image ${original.src || '(missing source)'} in ${document.slug} has a text/online alternative.`,
      );
      const href = rewriteLink(original.src || '', document);
      return `<p class="image-alternative">Illustration: ${escapeText(original.alt || 'See the web edition')}${href ? ` (<a href="${escapeAttribute(href)}">online image</a>)` : ''}.</p>`;
    }
    return `<img src="${escapeAttribute(src)}" alt="${escapeAttribute(original.alt || '')}" />`;
  }
  const tag =
    node.tagName === 'details' ? 'section' : node.tagName === 'summary' ? 'h3' : node.tagName;
  const namespace = node.namespaceURI || parentNamespace;
  const renderedAttributes = [];
  if (namespace !== parentNamespace)
    renderedAttributes.push(`xmlns="${escapeAttribute(namespace)}"`);
  for (const attribute of node.attrs || []) {
    if (
      /^on/i.test(attribute.name) ||
      /^(?:style|data-|aria-|role|tabindex|hidden|inert|open|loading|decoding)/i.test(
        attribute.name,
      )
    )
      continue;
    if (attribute.name === 'xmlns') continue;
    const name = attribute.prefix ? `${attribute.prefix}:${attribute.name}` : attribute.name;
    if (name === 'href' || name === 'xlink:href') {
      const href = rewriteLink(attribute.value, document);
      if (href) renderedAttributes.push(`${name}="${escapeAttribute(href)}"`);
    } else {
      renderedAttributes.push(`${name}="${escapeAttribute(attribute.value)}"`);
    }
  }
  const opening = `<${tag}${renderedAttributes.length ? ` ${renderedAttributes.join(' ')}` : ''}`;
  if (voidElements.has(tag)) return `${opening} />`;
  return `${opening}>${(await Promise.all(children(node).map((child) => serialize(child, document, namespace)))).join('')}</${tag}>`;
}

function xhtml(title, body) {
  return `<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="${htmlNamespace}" xmlns:epub="http://www.idpf.org/2007/ops" xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en" lang="en"><head><meta charset="utf-8" /><title>${escapeText(title)}</title><link rel="stylesheet" type="text/css" href="../Styles/book.css" /></head><body>${body}</body></html>`;
}

// Prefer the portrait book cover, then the raster social image, for broad reader
// compatibility. Register it directly from public/ so an older built asset cannot
// replace the current cover.
for (const candidate of ['public/book-cover.png', 'public/cover.png', 'public/cover.svg']) {
  if (await exists(path.join(root, candidate))) {
    coverImageHref = await registerImage(path.join(root, candidate));
    coverImageFilename = path.posix.basename(coverImageHref);
    break;
  }
}
const coverDocument = documents.find((document) => document.slug === 'title-page');
const readingDocuments = documents.filter((document) => document !== coverDocument);
const firstReadingDocument =
  readingDocuments.find((document) => /^01-/.test(document.slug)) || readingDocuments[0];

const archive = {
  mimetype: [strToU8('application/epub+zip'), { level: 0 }],
  'META-INF/container.xml': strToU8(
    '<?xml version="1.0" encoding="utf-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml" /></rootfiles></container>',
  ),
};
const contentManifest = [];
for (const document of documents) {
  const tree = document.tree || parseFragment(document.html);
  const html = await serialize(tree, document);
  const features = [
    html.includes(`xmlns="${mathNamespace}"`) ? 'mathml' : '',
    html.includes(`xmlns="${svgNamespace}"`) ? 'svg' : '',
  ].filter(Boolean);
  contentManifest.push(
    `<item id="${document.id}" href="Text/${document.filename}" media-type="application/xhtml+xml"${features.length ? ` properties="${features.join(' ')}"` : ''} />`,
  );
  archive[`EPUB/Text/${document.filename}`] = strToU8(
    xhtml(
      document.title,
      document === coverDocument
        ? `<section epub:type="cover" class="cover-page" id="cover">${html}</section>`
        : `<section epub:type="chapter"><h1>${escapeText(document.title)}</h1>${html}<p class="web-source">Web edition: <a href="${escapeAttribute(`${siteURL}book/${document.slug}/`)}">${escapeText(document.title)}</a></p></section>`,
    ),
  );
}

if (!coverDocument) {
  contentManifest.unshift(
    '<item id="cover-page" href="Text/cover.xhtml" media-type="application/xhtml+xml" />',
  );
  archive['EPUB/Text/cover.xhtml'] = strToU8(
    xhtml(
      'Ground Truth · Cover',
      `<section epub:type="cover" class="cover-page" id="cover">${coverImageHref ? `<img src="${escapeAttribute(coverImageHref)}" alt="Ground Truth book cover" />` : ''}<h1>Ground Truth</h1><p>A working developer’s path into AI and machine learning.</p><p>By Santosh Shinde · October 2026</p></section>`,
    ),
  );
}
archive['EPUB/Text/about.xhtml'] = strToU8(
  xhtml(
    'About this edition',
    `<section epub:type="preface"><h1>About this edition</h1><p>This EPUB holds the canonical chapters, applied guides, annotated resources and reference-lab instructions from the web book. Exercise answers are expanded for offline reading. The interactive controls are in the <a href="${escapeAttribute(siteURL)}">web edition</a>. The worked examples around them and the diagram descriptions are all here.</p><p>The companion data and numerical reference results are synthetic teaching material. They show nothing about real customer performance, causal benefit or production readiness.</p><p>Copyright © 2026 Santosh Shinde. The text, illustrations and laboratory reports are licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. The code is licensed under the <a href="https://github.com/santoshshinde2012/ai-ml-ground-truth/blob/main/LICENSE-CODE">MIT licence</a>. Linked external resources keep their own terms.</p></section>`,
  ),
);
const navigation = `<nav epub:type="toc" id="toc"><h1>Contents</h1><ol><li><a href="cover.xhtml">Ground Truth · Cover</a></li><li><a href="about.xhtml">About this edition</a></li>${readingDocuments.map((document) => `<li><a href="${document.filename}">${escapeText(document.title)}</a></li>`).join('')}</ol></nav><nav epub:type="landmarks" hidden="hidden"><h2>Book landmarks</h2><ol><li><a epub:type="cover" href="cover.xhtml">Cover</a></li><li><a epub:type="toc" href="nav.xhtml#toc">Contents</a></li><li><a epub:type="bodymatter" href="${firstReadingDocument?.filename || 'about.xhtml'}">Start reading</a></li></ol></nav>`;
archive['EPUB/Text/nav.xhtml'] = strToU8(xhtml('Contents', navigation));
archive['EPUB/Styles/book.css'] = strToU8(`
html { color: #173d35; background: #fffef9; }
body { font-family: Georgia, serif; line-height: 1.55; margin: 1em; }
h1,h2,h3,h4 { font-family: sans-serif; line-height: 1.2; break-after: avoid; }
h1 { font-size: 1.9em; margin-top: 1em; }
h2 { font-size: 1.35em; margin-top: 1.6em; }
h3 { font-size: 1.1em; margin-top: 1.3em; }
p,li { orphans: 2; widows: 2; }
a { color: #156952; text-decoration: underline; }
pre,code { font-family: monospace; font-size: .86em; }
pre { background: #f1f0e8; padding: .7em; white-space: pre-wrap; overflow-wrap: anywhere; }
code { overflow-wrap: anywhere; }
table { border-collapse: collapse; width: 100%; font-size: .82em; margin: 1em 0; }
th,td { border: 1px solid #b8c3b7; text-align: left; padding: .35em; vertical-align: top; overflow-wrap: anywhere; }
blockquote { margin: 1em 0; padding-left: 1em; border-left: .2em solid #749985; }
img,svg,figure { max-width: 100%; height: auto; }
figure { margin: 1em 0; }
figcaption,.web-source,.diagram-offline,.image-alternative { font-size: .85em; color: #45594c; }
section > h1 { break-before: page; }
.book-title { font-size: 3em; margin-top: 2em; }
.cover-page > h1 { break-before: auto; }
.cover-page img { display: block; margin: 0 auto; }
.edition { font-family: sans-serif; font-size: .8em; letter-spacing: .12em; }
.diagram-source { font-size: .8em; }
.align-left { text-align: left; }
.align-center { text-align: center; }
.align-right { text-align: right; }
nav ol { padding-left: 1.4em; }
nav li { margin: .5em 0; }
`);
const sortedAssets = [...assets.entries()].sort(([a], [b]) => a.localeCompare(b, 'en'));
for (const [filename, asset] of sortedAssets) archive[`EPUB/Images/${filename}`] = asset.bytes;

const identifier = `urn:sha256:${crypto
  .createHash('sha256')
  .update(
    documents
      .map(
        (document) =>
          `${document.slug}\n${document.title}\n${document.html || textContent(document.tree)}`,
      )
      .join('\n'),
  )
  .digest('hex')}`;
const modified = `${updated}T00:00:00Z`;
const coverMetadata = coverImageFilename ? '<meta name="cover" content="cover-image" />' : '';
const imageManifest = sortedAssets
  .map(([filename, asset], index) => {
    const isCover = filename === coverImageFilename;
    return `<item id="${isCover ? 'cover-image' : `image-${index + 1}`}" href="Images/${filename}" media-type="${asset.mediaType}"${isCover ? ' properties="cover-image"' : ''} />`;
  })
  .join('');
const spine = `<itemref idref="cover-page" /><itemref idref="about" />${readingDocuments.map((document) => `<itemref idref="${document.id}" />`).join('')}`;
archive['EPUB/package.opf'] = strToU8(
  `<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="en" prefix="schema: http://schema.org/"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">${identifier}</dc:identifier><dc:title>Ground Truth</dc:title><dc:creator>Santosh Shinde</dc:creator><dc:language>en</dc:language><dc:rights>Copyright © 2026 Santosh Shinde. Text and illustrations: CC BY 4.0. Code: MIT license.</dc:rights><dc:description>A working developer’s path into AI and machine learning: an illustrated engineering field guide with applied business cases and reproducible labs.</dc:description><meta property="dcterms:modified">${modified}</meta>${coverMetadata}<meta property="schema:accessMode">textual</meta><meta property="schema:accessMode">visual</meta><meta property="schema:accessibilityFeature">tableOfContents</meta><meta property="schema:accessibilityFeature">structuralNavigation</meta><meta property="schema:accessibilitySummary">Reflowable text with headings, expanded exercise answers, a table of contents and image alternatives. Interactive web graphics are represented by descriptive text and source; the web edition supplies their controls.</meta></metadata><manifest><item id="about" href="Text/about.xhtml" media-type="application/xhtml+xml" /><item id="nav" href="Text/nav.xhtml" media-type="application/xhtml+xml" properties="nav" /><item id="css" href="Styles/book.css" media-type="text/css" />${contentManifest.join('')}${imageManifest}</manifest><spine>${spine}</spine></package>`,
);

await fs.mkdir(path.dirname(output), { recursive: true });
// ZIP timestamps use local calendar components; construct local midnight so the
// serialized value is stable across build-host timezones (including UTC−12).
await fs.writeFile(output, zipSync(archive, { level: 6, mtime: new Date(1980, 0, 1, 0, 0, 0) }));

// XML and link validation uses Python's standard library. This catches malformed
// XHTML (HTML parsing alone cannot), missing files/fragments and packaging errors.
const validation = spawnSync(
  'python3',
  [
    '-c',
    `
import posixpath, sys, urllib.parse, zipfile, xml.etree.ElementTree as ET
book = sys.argv[1]
with zipfile.ZipFile(book) as z:
    files = z.namelist()
    assert files[0] == 'mimetype', 'EPUB mimetype must be the first archive entry'
    assert z.getinfo('mimetype').compress_type == zipfile.ZIP_STORED, 'EPUB mimetype must be uncompressed'
    assert not z.getinfo('mimetype').extra, 'EPUB mimetype must not have ZIP extra fields'
    assert z.read('mimetype') == b'application/epub+zip', 'Incorrect EPUB mimetype'
    assert len(files) == len(set(files)), 'Duplicate archive entries'
    trees = {}
    for name in files:
        if name.endswith(('.xml', '.opf', '.xhtml', '.svg')):
            trees[name] = ET.fromstring(z.read(name))
    package = trees['EPUB/package.opf']
    ns = {'opf': 'http://www.idpf.org/2007/opf'}
    manifest = package.find('opf:manifest', ns)
    items = {item.attrib['id']: item for item in manifest}
    assert len(items) == len(manifest), 'Duplicate manifest IDs'
    covers = [item for item in manifest if 'cover-image' in item.attrib.get('properties', '').split()]
    assert len(covers) <= 1, 'An EPUB must not declare multiple cover images'
    if covers:
        assert covers[0].attrib['id'] == 'cover-image', 'Cover metadata must identify the declared image'
        assert covers[0].attrib['media-type'].startswith('image/'), 'Cover resource must be an image'
        assert package.find('opf:metadata/opf:meta[@name="cover"]', ns).attrib['content'] == 'cover-image', 'Legacy cover metadata mismatch'
    assert package.find('opf:spine', ns)[0].attrib['idref'] == 'cover-page', 'Cover must begin the reading spine'
    for item in manifest:
        target = posixpath.normpath('EPUB/' + item.attrib['href'])
        assert target in files, 'Missing manifest resource: ' + target
    for itemref in package.find('opf:spine', ns):
        assert itemref.attrib['idref'] in items, 'Missing spine item'
    for name, tree in trees.items():
        if not name.endswith('.xhtml'):
            continue
        ids = [element.attrib['id'] for element in tree.iter() if 'id' in element.attrib]
        assert len(ids) == len(set(ids)), 'Duplicate XHTML ID in ' + name
        for element in tree.iter():
            for key in ['href', 'src']:
                value = element.attrib.get(key)
                if not value:
                    continue
                link = urllib.parse.urlsplit(value)
                if link.scheme or link.netloc:
                    continue
                target = posixpath.normpath(posixpath.join(posixpath.dirname(name), urllib.parse.unquote(link.path))) if link.path else name
                assert target in files, 'Missing EPUB resource from ' + name + ': ' + value
                if link.fragment and target.endswith('.xhtml'):
                    target_ids = {e.attrib.get('id') for e in trees[target].iter()}
                    assert urllib.parse.unquote(link.fragment) in target_ids, 'Missing EPUB anchor from ' + name + ': ' + value
print('EPUB XML, manifest, spine, local links and ZIP ordering verified')
`,
    output,
  ],
  { encoding: 'utf8' },
);
if (validation.error || validation.status !== 0) {
  await fs.rm(output, { force: true });
  throw new Error(
    `EPUB validation failed; invalid output removed.\n${validation.error?.message || validation.stderr || validation.stdout}`,
  );
}
console.log(validation.stdout.trim());
console.log(
  `EPUB exported: ${path.relative(root, output)} · ${documents.length} documents · ${assets.size} bundled images · ${Math.ceil((await fs.stat(output)).size / 1024)} KiB`,
);
for (const warning of warnings) console.warn(`EPUB note: ${warning}`);
