import { chapters } from '../lib/catalog.mjs';
const base = import.meta.env.BASE_URL.replace(/\/$/, '');
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const read = (key) => {
  try {
    return localStorage.getItem(key);
  } catch {
    return null;
  }
};
const save = (key, value) => {
  try {
    localStorage.setItem(key, value);
    return true;
  } catch {
    return false;
  }
};

const themeButton = $('[data-theme-toggle]');
themeButton?.addEventListener('click', () => {
  const isDark = document.documentElement.dataset.theme
    ? document.documentElement.dataset.theme === 'dark'
    : matchMedia('(prefers-color-scheme:dark)').matches;
  const theme = isDark ? 'light' : 'dark';
  document.documentElement.dataset.theme = theme;
  save('ground-truth-theme', theme);
  themeButton.setAttribute('aria-label', `Use ${theme === 'dark' ? 'light' : 'dark'} appearance`);
  document.dispatchEvent(new CustomEvent('book-theme-change'));
});

const dialog = $('#book-search');
let searchLoaded = false;
let searchLoading = false;
let searchOpener;
async function openSearch() {
  searchOpener = document.activeElement;
  dialog?.showModal();
  if (searchLoaded) {
    $('.pagefind-ui__search-input')?.focus();
    return;
  }
  if (searchLoading) return;
  searchLoading = true;
  const css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = `${base}/pagefind/pagefind-ui.css`;
  document.head.append(css);
  try {
    await new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = `${base}/pagefind/pagefind-ui.js`;
      script.onload = resolve;
      script.onerror = reject;
      document.head.append(script);
    });
    $('#search-results').replaceChildren();
    new window.PagefindUI({
      element: '#search-results',
      bundlePath: `${base}/pagefind/`,
      showSubResults: true,
      showImages: false,
      resetStyles: false,
    });
    searchLoaded = true;
    setTimeout(() => $('.pagefind-ui__search-input')?.focus(), 100);
  } catch {
    $('#search-results').innerHTML =
      `<p>Search is available in the built edition. <a href="${base}/#contents">Browse the chapters</a>.</p>`;
  } finally {
    searchLoading = false;
  }
}
$$('[data-open-search]').forEach((b) => b.addEventListener('click', openSearch));
$('[data-close-search]')?.addEventListener('click', () => dialog.close());
dialog?.addEventListener('click', (event) => {
  if (event.target === dialog) {
    const r = dialog.getBoundingClientRect();
    if (
      event.clientX < r.left ||
      event.clientX > r.right ||
      event.clientY < r.top ||
      event.clientY > r.bottom
    )
      dialog.close();
  }
});
dialog?.addEventListener('close', () => searchOpener?.focus());
document.addEventListener('keydown', (event) => {
  const target = event.target;
  if (
    (event.key === '/' || (event.key.toLowerCase() === 'k' && (event.metaKey || event.ctrlKey))) &&
    !(
      target instanceof HTMLElement &&
      (target.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName))
    )
  ) {
    event.preventDefault();
    openSearch();
  }
});

const allowedChapters = new Set(chapters.map((c) => c.dir));
let completed = new Set();
try {
  const stored = JSON.parse(read('ground-truth-progress') || '[]');
  if (Array.isArray(stored)) completed = new Set(stored.filter((s) => allowedChapters.has(s)));
} catch {}
function updateProgress() {
  $$('[data-completed-for]').forEach((el) => {
    el.hidden = !completed.has(el.dataset.completedFor);
  });
  $$('[data-progress-label]').forEach(
    (el) => (el.textContent = `${completed.size} of 9 chapters complete`),
  );
  $$('[data-book-progress]').forEach((el) => {
    el.value = completed.size;
    el.textContent = `${completed.size} of 9`;
  });
  $$('[data-mark-complete]').forEach((button) => {
    const done = completed.has(button.dataset.markComplete);
    button.setAttribute('aria-pressed', String(done));
    button.textContent = done ? 'Chapter completed ✓' : 'Mark chapter complete ✓';
  });
}
$$('[data-mark-complete]').forEach((button) =>
  button.addEventListener('click', () => {
    const slug = button.dataset.markComplete;
    if (completed.has(slug)) completed.delete(slug);
    else if (allowedChapters.has(slug)) completed.add(slug);
    const persisted = save('ground-truth-progress', JSON.stringify([...completed]));
    updateProgress();
    if (!persisted) $('[data-progress-label]').textContent += ' · session only';
  }),
);
$('[data-clear-progress]')?.addEventListener('click', () => {
  completed.clear();
  save('ground-truth-progress', '[]');
  updateProgress();
});
updateProgress();
window.addEventListener('storage', (event) => {
  if (event.key === 'ground-truth-progress') {
    try {
      const value = JSON.parse(event.newValue || '[]');
      completed = new Set(Array.isArray(value) ? value.filter((s) => allowedChapters.has(s)) : []);
      updateProgress();
    } catch {}
  }
});

const focusButton = $('[data-focus-toggle]');
function setFocus(active) {
  document.body.classList.toggle('focus-reading', active);
  focusButton?.setAttribute('aria-pressed', String(active));
  if (focusButton) focusButton.textContent = active ? 'Exit focus reading' : 'Focus reading';
}
setFocus(read('ground-truth-focus') === 'true');
focusButton?.addEventListener('click', () => {
  const active = !document.body.classList.contains('focus-reading');
  setFocus(active);
  save('ground-truth-focus', String(active));
});
const fontButton = $('[data-font-toggle]');
function setSize(large) {
  document.body.classList.toggle('large-reading', large);
  fontButton?.setAttribute('aria-pressed', String(large));
  if (fontButton) fontButton.textContent = large ? 'Standard text' : 'Larger text';
}
setSize(read('ground-truth-large-text') === 'true');
fontButton?.addEventListener('click', () => {
  const large = !document.body.classList.contains('large-reading');
  setSize(large);
  save('ground-truth-large-text', String(large));
});
const mobileQuery = matchMedia('(max-width:680px)');
const chapterDisclosure = $('.mobile-chapters');
function resizeNavigation() {
  if (chapterDisclosure) chapterDisclosure.open = !mobileQuery.matches;
}
resizeNavigation();
mobileQuery.addEventListener('change', resizeNavigation);

$$('.code-block').forEach((block) => {
  const code = $('code', block);
  if (!code) return;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'copy-code';
  button.textContent = 'Copy';
  button.setAttribute('aria-label', `Copy ${block.dataset.language || ''} code`);
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = 'Copied';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = 'Selected';
    }
    setTimeout(() => (button.textContent = 'Copy'), 1800);
  });
  block.append(button);
});

const tocLinks = $$('.page-toc nav a');
if (tocLinks.length && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      const active = entries
        .filter((e) => e.isIntersecting)
        .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
      if (active)
        tocLinks.forEach((a) => {
          a.classList.toggle('active', a.hash === `#${active.target.id}`);
        });
    },
    { rootMargin: '-15% 0px -65% 0px' },
  );
  $$('.prose h2').forEach((heading) => observer.observe(heading));
}

const sourceInput = $('#source-filter');
sourceInput?.addEventListener('input', () => {
  const value = sourceInput.value.trim().toLowerCase();
  let count = 0;
  $$('.source-row').forEach((row) => {
    row.hidden = !row.dataset.sourceText.includes(value);
    if (!row.hidden) count++;
  });
  $('[data-source-count]').textContent = `${count} sources`;
  $('[data-source-empty]').hidden = count !== 0;
});

const disclosures = [];
window.addEventListener('beforeprint', () => {
  $$('.prose details').forEach((el) => {
    disclosures.push([el, el.open]);
    el.open = true;
  });
});
window.addEventListener('afterprint', () => {
  disclosures.splice(0).forEach(([el, open]) => (el.open = open));
});

const diagrams = $$('.mermaid');
if (diagrams.length) {
  const originals = diagrams.map((el) => el.textContent);
  let rendering = false;
  let redrawRequested = false;
  async function drawDiagrams() {
    if (rendering) {
      redrawRequested = true;
      return;
    }
    rendering = true;
    try {
      const { default: mermaid } = await import('mermaid');
      const dark =
        document.documentElement.dataset.theme === 'dark' ||
        (!document.documentElement.dataset.theme &&
          matchMedia('(prefers-color-scheme:dark)').matches);
      mermaid.initialize({
        startOnLoad: false,
        securityLevel: 'strict',
        theme: dark ? 'dark' : 'neutral',
        fontFamily: 'DM Sans Variable, sans-serif',
        flowchart: { useMaxWidth: true, htmlLabels: false },
      });
      for (let i = 0; i < diagrams.length; i++) {
        const el = diagrams[i];
        el.removeAttribute('data-processed');
        el.textContent = originals[i];
      }
      await mermaid.run({ nodes: diagrams, suppressErrors: true });
    } catch {
      /* The caption and expandable original remain available when a diagram cannot render. */
    } finally {
      rendering = false;
      if (redrawRequested) {
        redrawRequested = false;
        drawDiagrams();
      }
    }
  }
  if ($('.print-book')) drawDiagrams();
  else if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          observer.disconnect();
          drawDiagrams();
        }
      },
      { rootMargin: '300px' },
    );
    diagrams.forEach((el) => observer.observe(el));
  } else drawDiagrams();
  document.addEventListener('book-theme-change', drawDiagrams);
}
