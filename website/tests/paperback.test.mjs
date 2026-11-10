import test from 'node:test';
import assert from 'node:assert/strict';
import { displayURL, showLinkTargets, stripNavigation } from '../src/lib/paperback.mjs';
import {
  coverSize,
  interiorProblems,
  margins,
  minimumInsideMargin,
  spineWidth,
} from '../src/lib/print-spec.mjs';
import { getBook, orderForEdition } from '../src/lib/book.mjs';

test('paper shows web addresses the way a reader types them', () => {
  assert.equal(displayURL('https://www.example.org/'), 'example.org');
  assert.equal(displayURL('https://example.org/a/b/?q=1#x'), 'example.org/a/b/?q=1#x');
  assert.equal(
    showLinkTargets('<a href="https://www.example.org/docs/">the docs</a>'),
    '<a href="https://www.example.org/docs/">the docs</a><span class="paperback-url"> example.org/docs</span>',
  );
  assert.equal(
    showLinkTargets('<a href="https://example.org">example.org</a>'),
    '<a href="https://example.org">example.org</a>',
    'a link that already shows its address is not repeated',
  );
  assert.equal(showLinkTargets('<a href="/book/x/">Chapter</a>'), '<a href="/book/x/">Chapter</a>');
});

test('paper drops paragraphs that only link to other pages', async () => {
  const top = '<p><a href="/b/9/">Chapter 9</a>&nbsp;·&nbsp;<a href="/b/9/plan/">Plan</a></p>\n';
  const kept =
    '<p><strong>In this chapter:</strong> <a href="#plan">Plan</a></p>\n<p>See <a href="/b/lab/">the lab</a>.</p>\n';
  const bottom =
    '<hr>\n<p><a href="/b/2/">Previous: Data</a>  · \n<a href="/b/4/">Next: Deep</a></p>';
  assert.equal(stripNavigation(`${top}${kept}${bottom}`), kept);
  for (const page of orderForEdition(await getBook()))
    assert.doesNotMatch(
      stripNavigation(page.html).slice(-400),
      />(Previous|Next):/,
      `${page.slug} keeps no closing navigation`,
    );
});

test('the paperback follows KDP rules for size, margins and spine', () => {
  assert.equal(minimumInsideMargin(150), 0.375);
  assert.equal(minimumInsideMargin(151), 0.5);
  assert.equal(minimumInsideMargin(500), 0.625);
  assert.equal(minimumInsideMargin(701), 0.875);
  assert.ok(Math.abs(spineWidth(400) - 0.9008) < 1e-9);
  const cover = coverSize(400);
  assert.ok(Math.abs(cover.width - (0.125 * 2 + 14 + 0.9008)) < 1e-9);
  assert.equal(cover.height, 10.25);
  assert.ok(margins.inside >= minimumInsideMargin(828), 'the margins suit any page count');
  assert.deepEqual(interiorProblems(420), []);
  assert.match(interiorProblems(900)[0], /24 to 828/);
});
