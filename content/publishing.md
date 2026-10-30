# Publishing and contributing

Ground Truth is an open engineering field guide by Santosh Shinde. The chapter Markdown is the
book's source of truth. The website, search index and EPUB are built from it.

## Run the book locally

Use Python 3.10 or newer and Node.js 24 (the version in `website/.nvmrc`). Astro needs at least
22.23.4. The website dependencies are locked in `website/package-lock.json`. From the repository
root:

```bash
npm --prefix website ci
npm --prefix website run dev
```

The development server prints its local address. For a release build, run:

```bash
npm --prefix website run format:check
npm --prefix website run check
npm --prefix website test
npm --prefix website run build
npm --prefix website run preview
```

`npm --prefix website run format` applies the Prettier style that the format check expects. The
build renders the book, creates a Pagefind search index, packages the EPUB and checks internal page,
anchor and asset links. `website/dist/` is generated output and is not committed. To test full-text
search and the offline download, open the address the preview server prints. The development
command prepares content and assets but does not build the search index or EPUB. You can also
change into `website/` and run the same npm commands without `--prefix website`. Run the standalone
Python lab commands from the repository root.

## GitHub Pages

The deployment workflow builds each push to `main`, checks the reference lab and deploys the
static output through GitHub's Pages artifact workflow. Pull requests run the checks without
deploying and without write permissions. Pages must use **GitHub Actions** as its build source.
Workflow run steps use `website/` as their working directory and upload `website/dist/`. The
workflow files stay in the root `.github/workflows/`, where GitHub finds them.

By default the site uses the project prefix `/ai-ml-ground-truth/`. For a custom domain, set
`SITE_URL` and `BASE_PATH` consistently, including the sitemap and canonical links. Use an empty
`BASE_PATH` when the book is served from a domain root. Never put a private credential in a
`PUBLIC_` environment variable or in a browser script.

## Editions and downloads

The web book always shows `main`. An edition is a fixed, citable snapshot with offline files:

1. Update `edition` and `updated` in `website/src/lib/catalog.mjs`, and `version` and
   `date-released` in `CITATION.cff`. The page dates and EPUB metadata follow the catalog.
2. Add a short entry to [keeping this book current](reader-guide.md#current).
3. Merge to `main`, then tag that commit `edition-<edition>` (for example `edition-2026.10`) and
   push the tag.

The release workflow rejects a tag that does not match the catalog and citation file. It reruns the
checks, builds the book, renders the print edition to PDF with headless Chrome, and attaches
`ground-truth-<edition>.epub` and `ground-truth-<edition>.pdf` to a GitHub release. Locally, after
a build, `npm --prefix website run export:pdf` writes `website/dist/downloads/ground-truth.pdf`.
Set `CHROME_PATH` if Chrome or Chromium is not in a standard location.

## What to change where

| Change | Source |
| --- | --- |
| Chapter prose and resource notes | The numbered chapter directories |
| Front matter | `content/` |
| Site menus and chapter descriptions | `website/src/lib/catalog.mjs` |
| Edition number and date | `website/src/lib/catalog.mjs` and `CITATION.cff` |
| Reading layout and typography | `website/src/layouts/` and `website/src/styles/` |
| Interactive explanations | `website/src/components/ConceptLab.astro` and `website/public/scripts/concept-lab.js` |
| Chapter, guide and lab plates | `website/src/components/ChapterPlate.astro` |
| Reproducible examples and the checks that stop a bad run | `labs/` |
| Checked-in reference reports and figures | `labs/reference/` |
| Website content and interaction tests | `website/tests/` |
| Python reference-lab tests | `labs/tests/` |
| Build, EPUB and PDF export, and link checks | `website/scripts/` |
| Website dependencies and configuration | `website/package.json`, `website/package-lock.json` and `website/astro.config.mjs` |
| Pull-request checks, deployment, releases and the link report | `.github/workflows/` |
| Issue form, pull-request template and dependency updates | `.github/` |

The nine numbered folders keep the chapter structure and learning order. Each chapter has a main
`README.md` and a `resources/README.md`. Chapter 9 also holds the applied case guides.
`content/reader-guide.md` holds the long introduction, learning approach, schedule, glossary and
author's note. The root `README.md` is the repository's front page and folder map. The teaching
project in `labs/` also stays at the root. All website code belongs in `website/`. The renderer
reads root-level Markdown and reference files directly, so the book is never copied into the
website.

Within `website/src/`, use `components/` for reusable visual explanations, `layouts/` for shared page chrome,
`lib/` for the catalog and content renderer, `pages/` for routes, `scripts/` for bundled reader
behaviour, and `styles/` for shared typography and layout. The standalone interaction script in
`website/public/scripts/` is served as is. Its component loads it using the configured site base path.

Keep content in its source file instead of copying prose into page components. The build turns
relative Markdown links into book routes, and the source files stay readable on GitHub. Existing
chapter and resource URLs keep working.

When reorganising or restyling, keep the original thinking: the intended audience, learning order,
continuing project, explanations, qualifications and the author's voice. Make content changes
separately and explain why. A folder clean-up is no reason to rewrite the chapters.

## Source files and generated output

`labs/reference/` is a maintained set of example results, committed on purpose. When the lab
changes, regenerate those reports with the command in the [lab guide](../labs/README.md) and review
what changed. A lab test fails when the checked-in reference no longer matches a fresh run.
Ordinary local runs belong in the ignored `labs/output/` directory.

The build also creates ignored files under `website/`: `dist/`, `.astro/`, `.cache/`,
`public/lab-reference/`, `public/sources.json` and `public/cover.png`. The reference copy comes from
the root `labs/reference/`, the source inventory from the book's Markdown, and the PNG cover from
`website/public/cover.svg`. The EPUB is written to `website/dist/downloads/ground-truth.epub`.
Edit the matching source, not a generated copy. Install dependencies from the committed lockfile
with `npm --prefix website ci` from the repository root.

## Propose a useful correction

Open a [correction issue](https://github.com/santoshshinde2012/ai-ml-ground-truth/issues/new?template=correction.yml)
or a pull request with the page, the exact claim, what you saw, and a primary source or
reproducible example. Each web page's "Suggest a correction" link fills in the page and source
file. Keep corrections focused. For a model or library claim, include the version and relevant
date. A page that loads shows the source is online, not that it supports the text.

Resource entries should say who they suit, which parts to study, and their limits. Keep an
author's recommendation distinct from a measured comparison. Label preprints and peer-reviewed papers
correctly, and keep the version actually discussed when it matters.

## Review and release practice

Before a release, check changed technical claims against primary sources, and run the book and lab
checks. Look through a long chapter, a resource page, an applied guide and the print edition on
desktop and mobile. Test keyboard access, dark mode, reduced motion, search, copy buttons and local
progress. Every learning interaction needs an understandable static state.

The generated source inventory lists each cited URL and where it appears. Its edition date marks an
editorial release, not a claim that every linked document was independently rechecked that day.
For an on-demand report on external links, run `npm --prefix website run check:links` from the
repository root. Bot blocks and timeouts need a manual follow-up. The external link report workflow
runs the same check monthly and on demand, summarises it on the run page, and fails only on
repeated 404 or 410 responses. It never blocks publishing, and reading or using the book needs
nothing scheduled. Dependabot proposes grouped monthly updates for the pinned actions and the
website dependencies. Review each like any other change.

## Attribution and reuse

The book's text, illustrations and lab reports are licensed under [CC BY 4.0](../LICENSE). The
website, lab code and code examples are under the [MIT licence](../LICENSE-CODE). Original diagrams
and teaching interactions are kept with their source. External papers, courses and illustrations
keep their own terms. Link to them and name the creator, instead of copying their material into the
book. Synthetic lab data are clearly labelled. The author's AI-assistance disclosure stays in the
[reader's guide](reader-guide.md#a-note-from-the-author).
