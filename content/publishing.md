# Publishing and contributing

Ground Truth is an open engineering field guide by Santosh Shinde. The chapter Markdown is the
canonical book content; the website, search index and EPUB are generated from it.

## Run the book locally

Use Node.js 24 (see `.nvmrc`) and Python 3.10 or newer. The website dependencies are locked in
`package-lock.json`. From the repository root:

```bash
npm ci
npm run dev
```

The development server prints its local address. For a release build, run:

```bash
npm run check
npm test
npm run build
npm run preview
```

The build renders the book, creates a Pagefind search index, packages the EPUB and checks internal
page, anchor and asset links. `dist/` is generated output and is not committed.

## GitHub Pages

The deployment workflow builds on pushes to `main`, verifies the reference laboratory, and deploys
the static output using GitHub's Pages artifact workflow. Pull requests run the checks without
deployment and without write permissions. Pages must use **GitHub Actions** as its build source.

The default configuration uses the project prefix `/ai-ml-ground-truth/`. For a custom domain,
configure `SITE_URL` and `BASE_PATH` consistently, including the sitemap and canonical links.
Use an empty `BASE_PATH` when the book is served at a domain root. Never put a private credential in
a `PUBLIC_` environment variable or in a browser script.

## What to change where

| Change | Source |
| --- | --- |
| Chapter prose and resource annotations | The numbered chapter directories |
| Front matter | `content/` |
| Navigation and chapter descriptions | `src/lib/catalog.mjs` |
| Reading layout and typography | `src/layouts/` and `src/styles/` |
| Interactive explanations | `src/components/ConceptLab.astro` and `public/scripts/concept-lab.js` |
| Reproducible examples and meaningful checks | `labs/` |
| Build, export and link checks | `scripts/` |

Keep content in its source location rather than copying prose into page components. Relative
Markdown links are converted to book routes during the build; source files remain readable on GitHub.
Existing chapter and resource URLs remain available.

## Propose a useful correction

Open a repository issue or pull request with the page, the specific claim, what you observed, and a
primary source or reproducible example. Keep corrections bounded. For a model or library claim,
include the version and relevant date. An HTTP success response establishes availability, not
whether a source supports the prose.

Resource entries should say who they suit, which parts to study, and their limitations. Distinguish
an author recommendation from a measured comparison. Record preprints and peer-reviewed publications
accurately, and retain the version actually discussed when it matters.

## Review and release practice

Before a release, check changed technical claims against primary sources and run the book and lab
checks. Inspect a long chapter, a resource page, an applied guide and the print edition on desktop
and mobile. Test keyboard navigation, dark appearance, reduced motion, search, copy controls and
local progress. All learning interactions need an understandable static state.

The generated source inventory lists cited URLs and where they appear. Its edition date records an
editorial release, not a claim that every linked document has been independently validated that day.
Run `npm run check:links` for an on-demand external availability report; bot restrictions and timeouts
require manual follow-up. No scheduled automation is needed to read or use the book.

## Attribution and reuse

The repository's MIT license continues to apply. Original diagrams and teaching interactions are
maintained with their source. External papers, courses and illustrations retain their own terms;
link to them and identify the creator rather than copying their material into the book. Synthetic
laboratory data are explicitly labeled. The author's AI-assistance disclosure remains in the
[reader's guide](reader-guide.md#a-note-from-the-author).
