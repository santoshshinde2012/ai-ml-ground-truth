import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import vm from 'node:vm';

const source = await readFile(new URL('../public/scripts/concept-lab.js', import.meta.url), 'utf8');
const kinds = [
  'broadcasting',
  'timeline',
  'validation',
  'gradients',
  'retrieval',
  'evaluation',
  'pricing',
  'retention',
];

// A deliberately small DOM boundary: keep the real interaction/evaluation code,
// replace only event delivery and the elements it reads or writes.
function element(dataset = {}, value = '') {
  const listeners = new Map();
  const attributes = new Map();
  const classes = new Set();
  let textContent = '';
  let innerHTML = '';
  return {
    dataset,
    value,
    checked: true,
    listeners,
    attributes,
    get textContent() {
      return textContent;
    },
    set textContent(value) {
      textContent = String(value);
    },
    get innerHTML() {
      return innerHTML;
    },
    set innerHTML(value) {
      innerHTML = String(value);
    },
    classList: { add: (name) => classes.add(name), contains: (name) => classes.has(name) },
    addEventListener(name, listener) {
      const current = listeners.get(name) || [];
      listeners.set(name, [...current, listener]);
    },
    setAttribute(name, value) {
      attributes.set(name, value);
    },
    dispatch(name) {
      for (const listener of listeners.get(name) || []) listener({ target: this });
    },
  };
}

function fixture(kind) {
  const elements = new Map();
  function add(selector, dataset = {}, value = '') {
    const item = element(dataset, value);
    elements.set(selector, [...(elements.get(selector) || []), item]);
    return item;
  }
  add('[data-stage]').innerHTML = '<svg role="img" aria-label="Static reference"></svg>';
  add('[data-result]').textContent = 'Static explanation.';
  const choices = {
    broadcasting: ['pair', ['column', 'rows', 'mismatch']],
    validation: ['split', ['random', 'time', 'group']],
    evaluation: ['candidate', ['small', 'clear', 'regress']],
    gradients: ['gradient', ['add', 'overwrite']],
    retention: ['policy', ['risk', 'benefit']],
  };
  if (choices[kind]) {
    const [attribute, values] = choices[kind];
    for (const value of values) add(`[data-${attribute}]`, { [attribute]: value });
  }
  if (kind === 'broadcasting') add('[data-reveal]');
  if (kind === 'timeline') {
    add('[data-clock]', {}, '5');
    add('[data-clock-value]');
  }
  if (kind === 'gradients') {
    add('[data-x]', {}, '3');
    add('[data-x-value]');
  }
  if (kind === 'retrieval') {
    add('[data-query]', {}, 'refund');
    add('[data-filter]');
  }
  if (kind === 'pricing') {
    add('[data-price]', {}, '120');
    add('[data-price-value]');
    add('[data-stock]', {}, '60');
  }
  if (kind === 'retention') add('[data-budget]', {}, '2');
  const root = Object.assign(element({ lab: kind }), {
    querySelector: (selector) => elements.get(selector)?.[0] || null,
    querySelectorAll: (selector) => elements.get(selector) || [],
  });
  const errors = [];
  const document = Object.assign(element(), {
    readyState: 'complete',
    querySelectorAll: () => [root],
  });
  const context = vm.createContext({
    document,
    Intl,
    console: { error: (...args) => errors.push(args) },
  });
  const start = () => vm.runInContext(source, context, { timeout: 5_000 });
  start();
  return {
    root,
    document,
    errors,
    start,
    get: (selector, index = 0) => elements.get(selector)?.[index],
    result: () => elements.get('[data-result]')[0].textContent,
    graphic: () => elements.get('[data-stage]')[0].innerHTML,
    click(selector, index = 0) {
      elements.get(selector)[index].dispatch('click');
    },
    change(selector, value, event = 'change') {
      const item = elements.get(selector)[0];
      item.value = String(value);
      item.dispatch(event);
    },
  };
}

for (const kind of kinds) {
  test(`${kind} initializes with an accessible graphic and a finite result`, () => {
    const lab = fixture(kind);
    assert.deepEqual(lab.errors, []);
    assert.equal(lab.root.classList.contains('is-enhanced'), true);
    assert.match(lab.graphic(), /role="img"/);
    assert.match(lab.graphic(), /aria-label="[^\"]+/);
    assert.doesNotMatch(lab.graphic(), /NaN|undefined|Infinity/);
    assert.ok(lab.result().length > 50);
  });
}

test('broadcasting reveals expansion and rejects incompatible trailing dimensions', () => {
  const lab = fixture('broadcasting');
  assert.match(lab.result(), /What shape/);
  lab.click('[data-reveal]');
  assert.match(lab.result(), /\(3, 1\) \+ \(3,\) → \(3, 3\)/);
  lab.click('[data-pair]', 1);
  lab.click('[data-reveal]');
  assert.match(lab.result(), /\(2, 3\) \+ \(3,\) → \(2, 3\)/);
  lab.click('[data-pair]', 2);
  lab.click('[data-reveal]');
  assert.match(lab.result(), /broadcasting error/);
  assert.equal(lab.get('[data-pair]', 2).attributes.get('aria-pressed'), 'true');
  assert.equal(lab.get('[data-pair]', 0).attributes.get('aria-pressed'), 'false');
});

test('historical snapshots require arrival, including a second late-arriving event', () => {
  const lab = fixture('timeline');
  assert.match(lab.result(), /Day 5: 2 available records \(account created, support request\)/);
  lab.change('[data-clock]', 7, 'input');
  assert.match(
    lab.result(),
    /3 available records \(account created, purchase recorded, support request\)/,
  );
  lab.change('[data-clock]', 8, 'input');
  assert.match(lab.result(), /3 available records/);
  assert.match(lab.result(), /refund completed.*exclude/i);
  lab.change('[data-clock]', 9, 'input');
  assert.match(lab.result(), /4 available records/);
  assert.equal(lab.get('[data-clock-value]').textContent, '9');
});

test('validation choices explain the distinct future-time and unseen-customer questions', () => {
  const lab = fixture('validation');
  assert.match(lab.result(), /training records occur after test records/);
  lab.click('[data-split]', 1);
  assert.match(lab.result(), /train on days 1–3 and test on day 4/);
  assert.match(lab.result(), /existing customers/);
  lab.click('[data-split]', 2);
  assert.match(lab.result(), /customer C appears only in the test set/);
  assert.match(lab.result(), /does not by itself test future-time/);
});

test('shared-node gradient accumulates both paths and reveals an overwrite bug', () => {
  const lab = fixture('gradients');
  assert.match(lab.result(), /x = 3, y = 18.*Computed dy\/dx = 12; analytic derivative = 12/);
  lab.click('[data-gradient]', 1);
  assert.match(lab.result(), /Computed dy\/dx = 6; analytic derivative = 12/);
  lab.change('[data-x]', 5, 'input');
  assert.match(lab.result(), /x = 5, y = 50.*Computed dy\/dx = 10; analytic derivative = 20/);
  lab.click('[data-gradient]', 0);
  assert.match(lab.result(), /Computed dy\/dx = 20; analytic derivative = 20/);
});

test('retrieval respects both permissions and current versions before choosing evidence', () => {
  const lab = fixture('retrieval');
  assert.match(lab.result(), /Refund policy · current.*30 days/);
  lab.get('[data-filter]').checked = false;
  lab.get('[data-filter]').dispatch('change');
  assert.match(lab.result(), /Internal retention exceptions.*restricted/);
  lab.get('[data-filter]').checked = true;
  lab.get('[data-filter]').dispatch('change');
  assert.match(lab.result(), /Refund policy · current.*30 days/);
  lab.change('[data-query]', 'shipping');
  assert.match(lab.result(), /Shipping policy · current.*2 business days/);
});

test('paired evaluation distinguishes uncertain gain, convincing gain and regression', () => {
  const lab = fixture('evaluation');
  assert.match(lab.result(), /Baseline 40\/50; candidate 42\/50/);
  assert.match(lab.result(), /interval includes zero/);
  lab.click('[data-candidate]', 1);
  assert.match(lab.result(), /Baseline 40\/50; candidate 48\/50/);
  assert.match(lab.result(), /supports an improvement/);
  const interval = lab.result().match(/difference: ([+-]?\d+) to ([+-]?\d+)/);
  assert.ok(Number(interval[1]) > 0, 'the positive decision must have a wholly positive interval');
  lab.click('[data-candidate]', 2);
  assert.match(lab.result(), /candidate 30\/50/);
  assert.match(lab.result(), /retain the baseline/);
  lab.click('[data-candidate]', 0);
  assert.equal(
    lab.result(),
    fixture('evaluation').result(),
    'resampling is reproducible for the same data',
  );
});

test('pricing caps sales by stock and computes contribution after unit cost', () => {
  const lab = fixture('pricing');
  // At price 120, deterministic demand is 52 and unit margin is 65.
  assert.match(lab.result(), /demand 52\.0 units; sales 52\.0; contribution ₹3,380/);
  lab.change('[data-stock]', 20);
  assert.match(lab.result(), /sales 20\.0; contribution ₹1,300/);
  lab.change('[data-price]', 80, 'input');
  assert.match(lab.result(), /sales 20\.0; contribution ₹500/);
  assert.match(lab.result(), /uncertain demand requires integrating/);
});

test('retention ranks benefit separately from risk and treats contact budget as a ceiling', () => {
  const lab = fixture('retention');
  assert.match(lab.result(), /contacts A, D/);
  assert.match(lab.result(), /−₹29\.2 across 2 contacts/);
  lab.click('[data-policy]', 1);
  assert.match(lab.result(), /contacts B, C/);
  assert.match(lab.result(), /₹50\.0 across 2 contacts/);
  lab.change('[data-budget]', 4);
  assert.match(lab.result(), /contacts B, C, E/);
  assert.match(lab.result(), /₹57\.0 across 3 contacts \(capacity 4\)/);
  assert.match(lab.result(), /remaining capacity is unused/);
});

test('reloading the enhancement leaves existing controls bound once', () => {
  const lab = fixture('broadcasting');
  lab.start();
  assert.equal(lab.get('[data-reveal]').listeners.get('click').length, 1);
  lab.click('[data-reveal]');
  assert.match(lab.result(), /\(3, 3\)/);
});

test('an unknown lab leaves the static fallback intact without throwing', () => {
  const lab = fixture('future-lesson');
  assert.deepEqual(lab.errors, []);
  assert.equal(lab.root.classList.contains('is-enhanced'), false);
  assert.equal(lab.root.dataset.initialized, undefined);
  assert.equal(lab.graphic(), '<svg role="img" aria-label="Static reference"></svg>');
  assert.equal(lab.result(), 'Static explanation.');
});
