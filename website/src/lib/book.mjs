import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import remarkRehype from 'remark-rehype';
import rehypeRaw from 'rehype-raw';
import rehypeKatex from 'rehype-katex';
import rehypeStringify from 'rehype-stringify';
import { visit } from 'unist-util-visit';
import GithubSlugger from 'github-slugger';
import { codeToHtml } from 'shiki';
import { documentList, repository } from './catalog.mjs';
import { fromRepository } from './paths.mjs';

/** @type {Map<string, Promise<import('./types').BookPage[]>>} */
const cache = new Map();
/** @type {Map<string, Promise<import('./types').BookPage[]>>} */
const readingCache = new Map();
export const escapeHTML = (text) =>
  String(text).replace(
    /[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c],
  );
export const basePath = () =>
  (import.meta.env?.BASE_URL ?? process.env.BASE_PATH ?? '/ai-ml-ground-truth/').replace(/\/$/, '');
export const bookHref = (slug) => `${basePath()}/book/${slug}/`;
export const homeHref = () => `${basePath()}/`;

export function resolveLink(href, source, docs = documentList(), base = basePath()) {
  if (/^(?:[a-z][a-z\d+.-]*:|\/\/|#)/i.test(href)) return href;
  const [raw, fragment] = href.split('#', 2);
  const [file, query] = raw.split('?', 2);
  const target = path.posix.normalize(
    path.posix.join(path.posix.dirname(source), decodeURIComponent(file)),
  );
  const suffix = `${query ? `?${query}` : ''}${fragment ? `#${fragment}` : ''}`;
  const doc = docs.find(
    (d) =>
      d.file === target ||
      ([path.posix.dirname(d.file), `${path.posix.dirname(d.file)}/`].includes(target) &&
        d.file.endsWith('/README.md')),
  );
  if (doc) return `${base}/book/${doc.slug}/${suffix}`;
  if (target === 'README.md') return `${base}/book/reader-guide/${suffix}`;
  if (target.startsWith('labs/reference/'))
    return `${base}/lab-reference/${target.slice(15)}${suffix}`;
  if (target === 'labs/' || target === 'labs') return `${base}/book/reference-lab/${suffix}`;
  return `${repository}/blob/main/${target}${suffix}`;
}

function plain(node) {
  if (node.type === 'text' || node.type === 'inlineCode') return node.value || '';
  return (node.children || []).map(plain).join('');
}

export async function renderContent(markdown, source, { removeTitle = true } = {}) {
  const headings = [];
  const slugger = new GithubSlugger();
  function teachingCode() {
    return async (tree) => {
      const tasks = [];
      visit(tree, 'code', (node, index, parent) => {
        tasks.push(
          (async () => {
            let value;
            if (node.lang === 'mermaid') {
              const diagramSource = node.value.replace(/^%%\{init:[^\n]*\}%%\s*\n?/m, '');
              const description =
                node.value.match(/accDescr:\s*(.+)/)?.[1] ||
                'A diagram of the process described in the surrounding text.';
              // A stable key lets the EPUB use the image rendered from this diagram.
              const key = crypto
                .createHash('sha256')
                .update(diagramSource)
                .digest('hex')
                .slice(0, 16);
              value = `<figure class="diagram"><div class="mermaid" data-diagram="${key}" aria-label="${escapeHTML(description)}">${escapeHTML(diagramSource)}</div><figcaption>${escapeHTML(description)}</figcaption></figure><details class="diagram-source" data-diagram="${key}"><summary>Diagram source</summary><pre><code>${escapeHTML(node.value)}</code></pre></details>`;
            } else {
              const language = node.lang || 'text';
              try {
                value = await codeToHtml(node.value, {
                  lang: language,
                  themes: { light: 'github-light', dark: 'github-dark' },
                  defaultColor: false,
                });
              } catch {
                value = `<pre><code>${escapeHTML(node.value)}</code></pre>`;
              }
              value = `<div class="code-block" data-language="${escapeHTML(language)}">${value}</div>`;
            }
            parent.children[index] = { type: 'html', value };
          })(),
        );
      });
      await Promise.all(tasks);
      if (removeTitle) {
        const first = tree.children.findIndex((n) => n.type === 'heading' && n.depth === 1);
        if (first >= 0) tree.children.splice(first, 1);
      }
    };
  }
  function bookLinks() {
    return (tree) => {
      visit(tree, 'element', (node, index, parent) => {
        if (/^h[2-6]$/.test(node.tagName)) {
          const text = plain(node);
          const id = node.properties.id || slugger.slug(text);
          node.properties.id = id;
          headings.push({ depth: Number(node.tagName[1]), text, id });
        }
        if (node.tagName === 'a' && node.properties.href)
          node.properties.href = resolveLink(String(node.properties.href), source);
        if (node.tagName === 'img') {
          node.properties.loading = 'lazy';
          node.properties.decoding = 'async';
          if (node.properties.src && !/^(https?:|data:|\/)/.test(String(node.properties.src)))
            node.properties.src = resolveLink(String(node.properties.src), source);
        }
        // Column alignment uses classes: `align` is obsolete in HTML and invalid in EPUB 3.
        if ((node.tagName === 'th' || node.tagName === 'td') && node.properties.align) {
          node.properties.className = [
            ...(node.properties.className || []),
            `align-${node.properties.align}`,
          ];
          delete node.properties.align;
        }
        if (node.tagName === 'table' && parent?.tagName !== 'div' && typeof index === 'number') {
          parent.children[index] = {
            type: 'element',
            tagName: 'div',
            properties: {
              className: ['table-scroll'],
              tabIndex: 0,
              role: 'region',
              ariaLabel: 'Scrollable data table',
            },
            children: [node],
          };
        }
      });
    };
  }
  const result = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkMath)
    .use(teachingCode)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeRaw)
    .use(rehypeKatex)
    .use(bookLinks)
    .use(rehypeStringify)
    .process(markdown);
  return { html: String(result), headings };
}

/** @returns {Promise<import('./types').BookPage[]>} */
export async function getBook() {
  const key = basePath();
  if (!cache.has(key))
    cache.set(
      key,
      (async () => {
        const docs = documentList();
        return Promise.all(
          docs.map(async (doc) => {
            const markdown = await fs.readFile(fromRepository(doc.file), 'utf8');
            const words =
              markdown.replace(/```[\s\S]*?```/g, '').match(/\b[\p{L}\p{N}’'-]+\b/gu)?.length || 0;
            const rendered = await renderContent(markdown, doc.file);
            return {
              ...doc,
              ...rendered,
              words,
              minutes: Math.max(1, Math.ceil(words / 220)),
              markdown,
            };
          }),
        );
      })(),
    );
  return /** @type {Promise<import('./types').BookPage[]>} */ (cache.get(key));
}

/** @returns {Promise<import('./types').BookPage[]>} */
async function buildReadingPages() {
  const docs = await getBook();
  const lessons = [];
  for (const doc of docs.filter((d) => ['Chapter', 'Applied guide'].includes(d.category))) {
    const tree = unified().use(remarkParse).use(remarkGfm).parse(doc.markdown);
    const sections = tree.children.filter((n) => n.type === 'heading' && n.depth === 2);
    const links = [];
    for (let i = 0; i < sections.length; i++) {
      const section = sections[i];
      const title = plain(section);
      const heading = doc.headings.find((h) => h.depth === 2 && h.text === title);
      if (!heading || /^(?:Resources|Before you|A few things|What you will)/i.test(title)) continue;
      const start = section.position.start.offset;
      const end = sections[i + 1]?.position.start.offset ?? doc.markdown.length;
      const markdown = doc.markdown.slice(start, end).replace(/^## /, '# ');
      const words = markdown.match(/\b[\p{L}\p{N}’'-]+\b/gu)?.length || 0;
      if (words < 90) continue;
      const slug = `${doc.slug}/lessons/${heading.id}`;
      const rendered = await renderContent(markdown, doc.file);
      // A section may refer to another section of its complete source chapter.
      rendered.html = rendered.html.replace(
        /href="#([^"]+)"/g,
        (_, anchor) => `href="${bookHref(doc.slug)}#${anchor}"`,
      );
      const lesson = {
        ...doc,
        ...rendered,
        slug,
        title,
        category: 'Lesson',
        lab: null,
        markdown,
        words,
        minutes: Math.max(1, Math.ceil(words / 220)),
        parentSlug: doc.slug,
        lessonIndex: links.length,
      };
      lessons.push(lesson);
      links.push({ slug, title, minutes: lesson.minutes });
    }
    doc.lessons = links;
    for (const lesson of lessons.filter((l) => l.parentSlug === doc.slug))
      lesson.lessonCount = links.length;
  }
  return [...docs, ...lessons];
}

/** @returns {Promise<import('./types').BookPage[]>} */
export async function getReadingPages() {
  const key = basePath();
  if (!readingCache.has(key)) readingCache.set(key, buildReadingPages());
  return /** @type {Promise<import('./types').BookPage[]>} */ (readingCache.get(key));
}

export function printContent(html, slug) {
  const prefix = `p-${slug.replaceAll('/', '-')}-`;
  return html
    .replace(/\bid="([^"]+)"/g, (_, id) => `id="${prefix}${id}"`)
    .replace(/href="#([^"]+)"/g, (_, id) => `href="#${prefix}${id}"`);
}

/** @param {import('./types').BookPage[]} pages */
export function orderForEdition(pages) {
  const order = (page) =>
    page.slug === 'start-here'
      ? 0
      : page.slug === 'reader-guide'
        ? 1
        : page.category === 'Chapter'
          ? 10 + page.chapter
          : page.category === 'Applied guide'
            ? 30
            : page.category === 'Laboratory'
              ? 40
              : page.category === 'Lab report'
                ? 41
                : page.category === 'Resources'
                  ? 60 + page.chapter
                  : 100;
  return pages.filter((p) => p.slug !== 'publishing').toSorted((a, b) => order(a) - order(b));
}
