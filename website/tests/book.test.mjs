import test from 'node:test';
import assert from 'node:assert/strict';
import { documentList } from '../src/lib/catalog.mjs';
import {
  resolveLink,
  renderContent,
  getBook,
  getReadingPages,
  printContent,
} from '../src/lib/book.mjs';

test('GitHub-readable links become base-aware reader routes', () => {
  assert.equal(
    resolveLink(
      '../03-core-machine-learning/README.md#validation',
      '02-data-foundations/README.md',
    ),
    '/ai-ml-ground-truth/book/03-core-machine-learning/#validation',
  );
  assert.equal(
    resolveLink('resources/README.md', '03-core-machine-learning/README.md'),
    '/ai-ml-ground-truth/book/03-core-machine-learning/resources/',
  );
  assert.equal(
    resolveLink('../labs/README.md', '02-data-foundations/README.md'),
    '/ai-ml-ground-truth/book/reference-lab/',
  );
  assert.equal(
    resolveLink('../README.md#who', '03-core-machine-learning/README.md'),
    '/ai-ml-ground-truth/book/reader-guide/#who',
  );
  assert.equal(
    resolveLink('reference/calibration.svg', 'labs/README.md'),
    '/ai-ml-ground-truth/lab-reference/calibration.svg',
  );
  assert.equal(
    resolveLink('https://example.com/paper?q=1#section', 'README.md'),
    'https://example.com/paper?q=1#section',
  );
});

test('domain-root publishing does not retain the repository prefix', () => {
  assert.equal(
    resolveLink('../labs/README.md', '03-core-machine-learning/README.md', documentList(), ''),
    '/book/reference-lab/',
  );
});

test('rendering preserves disclosures, math, stable headings and readable code', async () => {
  const { html, headings } = await renderContent(
    '# Title\n\n## Honest test\n\n$x^2$\n\n<details>\n<summary>Answer</summary>\n\nA held-out result.\n\n</details>\n\n```python\nx = 3\n```\n\n| Cost | Result |\n|---|---|\n| 2 | 4 |',
    '03-core-machine-learning/README.md',
  );
  assert.ok(!html.includes('<h1'));
  assert.ok(html.includes('<details>'));
  assert.ok(html.includes('A held-out result.'));
  assert.ok(html.includes('katex'));
  assert.ok(html.includes('code-block'));
  assert.ok(html.includes('Scrollable data table'));
  assert.deepEqual(
    headings.map((h) => h.id),
    ['honest-test'],
  );
});

test('the canonical book includes all chapters, references and runnable lab guidance', async () => {
  const pages = await getBook();
  assert.equal(pages.filter((p) => p.category === 'Chapter').length, 9);
  assert.equal(pages.filter((p) => p.category === 'Resources').length, 9);
  assert.ok(pages.find((p) => p.slug === 'reference-lab').html.includes('ground_truth_lab.py'));
  assert.ok(pages.find((p) => p.slug.endsWith('/causal-primer')));
  assert.equal(new Set(pages.map((p) => p.slug)).size, pages.length);
});

test('short lessons retain the text of their source section and return to their source', async () => {
  const pages = await getReadingPages();
  const pricing = pages.find((p) => p.slug === '09-business-machine-learning/price-recommendation');
  assert.ok(pricing.lessons.length > 3);
  const lesson = pages.find((p) => p.parentSlug === pricing.slug);
  assert.ok(lesson.html.length > 100);
  assert.ok(lesson.minutes < pricing.minutes);
  assert.ok(lesson.parentSlug === pricing.slug);
  assert.ok(!/href="#/.test(lesson.html));
});

test('print edition isolates repeated chapter anchors', () => {
  const one = printContent(
    '<h2 id="resources">Resources</h2><a href="#resources">Read</a>',
    '01-getting-oriented',
  );
  const two = printContent('<h2 id="resources">Resources</h2>', '02-data-foundations');
  assert.ok(one.includes('href="#p-01-getting-oriented-resources"'));
  assert.ok(!two.includes('id="p-01-getting-oriented-resources"'));
});

test('legacy diagram themes cannot override the reader appearance', async () => {
  const source =
    '```mermaid\n%%{init: {"theme":"base"}}%%\nflowchart LR\n accDescr: Data becomes evidence.\n A[Data] --> B[Evidence]\n```';
  const { html } = await renderContent(source, 'content/reader-guide.md');
  const rendered = html.slice(html.indexOf('class="mermaid"'), html.indexOf('</div>'));
  assert.ok(!rendered.includes('init:'));
  assert.ok(html.includes('init:'));
  assert.ok(html.includes('Data becomes evidence.'));
});

test('currency and prose are not rendered as mathematics', async () => {
  // Two unescaped dollar amounts in one paragraph become inline math; escape them as \$.
  const prose = [];
  for (const page of await getBook()) {
    for (const [, tex] of page.html.matchAll(
      /<annotation encoding="application\/x-tex">([^<]*)</g,
    )) {
      if (/[a-z]{2,} [a-z]{2,} [a-z]{2,}/i.test(tex.replace(/\\text\{[^}]*\}/g, '')))
        prose.push(`${page.file}: ${tex}`);
    }
  }
  assert.deepEqual(prose, []);
});
