import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, realpath } from 'node:fs/promises';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { getBook, resolveLink } from '../src/lib/book.mjs';
import { websiteRoot, repositoryRoot, fromWebsite, fromRepository } from '../src/lib/paths.mjs';

test('website implementation and canonical book sources have separate roots', async () => {
  assert.equal(await realpath(websiteRoot), await realpath(path.join(repositoryRoot, 'website')));
  assert.equal(
    await realpath(fromWebsite('public', 'cover.svg')),
    await realpath(new URL('../public/cover.svg', import.meta.url)),
  );
  assert.equal(path.relative(repositoryRoot, fromWebsite('dist')), path.join('website', 'dist'));
  assert.equal(
    path.relative(repositoryRoot, fromRepository('labs', 'reference', 'evaluation.md')),
    path.join('labs', 'reference', 'evaluation.md'),
  );
});

test('rendered chapters and lab guidance use the root Markdown without a copied book', async () => {
  const pages = await getBook();
  for (const file of [
    '02-data-foundations/README.md',
    'content/reader-guide.md',
    'labs/README.md',
  ]) {
    const page = pages.find((item) => item.file === file);
    assert.ok(page, `${file} remains part of the canonical book`);
    assert.equal(page.markdown, await readFile(fromRepository(file), 'utf8'));
    assert.ok(
      !path.relative(repositoryRoot, fromRepository(file)).startsWith(`website${path.sep}`),
    );
  }
});

test('moving website files does not change public chapter, resource or reference routes', () => {
  assert.equal(
    resolveLink('resources/README.md', '02-data-foundations/README.md'),
    '/ai-ml-ground-truth/book/02-data-foundations/resources/',
  );
  assert.equal(
    resolveLink('../labs/README.md', '06-production/README.md'),
    '/ai-ml-ground-truth/book/reference-lab/',
  );
  assert.equal(
    resolveLink('reference/calibration.svg', 'labs/README.md'),
    '/ai-ml-ground-truth/lab-reference/calibration.svg',
  );
});

test('book rendering resolves canonical files independently of the caller working directory', () => {
  const bookURL = new URL('../src/lib/book.mjs', import.meta.url).href;
  const script = `
    import { getBook } from ${JSON.stringify(bookURL)};
    const pages = await getBook();
    const chapter = pages.find(page => page.file === '03-core-machine-learning/README.md');
    const lab = pages.find(page => page.slug === 'reference-lab');
    console.log(JSON.stringify({ chapters: pages.filter(page => page.category === 'Chapter').length, chapter: chapter.markdown, lab: lab.markdown }));
  `;
  const results = [repositoryRoot, websiteRoot].map((cwd) => {
    const result = spawnSync(process.execPath, ['--input-type=module', '--eval', script], {
      cwd,
      env: { ...process.env, BASE_PATH: '/ai-ml-ground-truth/' },
      encoding: 'utf8',
      timeout: 30_000,
      maxBuffer: 2 * 1024 * 1024,
    });
    assert.equal(result.status, 0, `rendering from ${cwd}: ${result.stderr || result.error || ''}`);
    return JSON.parse(result.stdout);
  });
  assert.equal(results[0].chapters, 9);
  assert.match(results[0].chapter, /Core machine learning/i);
  assert.match(results[0].lab, /ground_truth_lab\.py/);
  assert.deepEqual(results[0], results[1]);
});
