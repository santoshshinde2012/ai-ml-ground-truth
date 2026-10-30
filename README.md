# Ground Truth

**A working developer's path into AI and machine learning.**

**The short version.** Eight core chapters take you from shipping software to shipping AI systems in
about 450 hours. A ninth applied chapter covers **offer recommendation, price recommendation and
churn**, with model choices and a full business decision workflow. You build on **one thread** —
one dataset becomes one model becomes one AI product. Each chapter has a practical plan and a
`resources` folder for deeper reading.

The illustrated web edition adds worked lessons, eight interactive explanations and a reproducible
reference lab. The [reader's guide](content/reader-guide.md) holds the original long introduction,
learning approach, [schedule and assumptions](content/reader-guide.md#time),
[glossary](content/reader-guide.md#glossary), [project ideas](content/reader-guide.md#projects) and
[author's note](content/reader-guide.md#a-note-from-the-author).

**[Read the web book](https://santoshshinde2012.github.io/ai-ml-ground-truth/)** ·
[Start here](content/start-here.md) · [Reader’s guide](content/reader-guide.md) ·
[Run the reference lab](labs/README.md)

## Chapters

| # | Chapter | References |
|---|---|---|
| 01 | [Getting oriented](01-getting-oriented/README.md) | [Resources](01-getting-oriented/resources/README.md) |
| 02 | [Data foundations](02-data-foundations/README.md) | [Resources](02-data-foundations/resources/README.md) |
| 03 | [Core machine learning](03-core-machine-learning/README.md) | [Resources](03-core-machine-learning/resources/README.md) |
| 04 | [Deep learning](04-deep-learning/README.md) | [Resources](04-deep-learning/resources/README.md) |
| 05 | [Language models and AI engineering](05-language-models/README.md) | [Resources](05-language-models/resources/README.md) |
| 06 | [Running it in production](06-production/README.md) | [Resources](06-production/resources/README.md) |
| 07 | [Choosing a specialisation](07-specialisation/README.md) | [Resources](07-specialisation/resources/README.md) |
| 08 | [Finding the work](08-finding-the-work/README.md) | [Resources](08-finding-the-work/resources/README.md) |
| 09 | [Business machine learning: offers, prices and churn](09-business-machine-learning/README.md) | [Resources](09-business-machine-learning/resources/README.md) |

Follow Chapters 1–8 in order, starting the Chapter 8 job search alongside Chapter 6. Chapter 9 is
an applied extension after Chapters 3 and 6. One case can be your Chapter 7 capstone. The
[reader's guide](content/reader-guide.md#how-to-use) explains the full order.

The applied guides cover [causal foundations](09-business-machine-learning/causal-primer.md),
[offers](09-business-machine-learning/offer-recommendation.md),
[prices](09-business-machine-learning/price-recommendation.md),
[churn and retention](09-business-machine-learning/churn.md), and a
[shared delivery plan](09-business-machine-learning/delivery-plan.md).

## Read, explore, practice

The web edition offers chapter and lesson menus, local search, eight interactive field notes, light
and dark themes, focus reading, optional progress saved on your device, a complete print edition and
an EPUB download. The core content works without JavaScript. Each edition is also on the
[releases page](https://github.com/santoshshinde2012/ai-ml-ground-truth/releases) as an EPUB and a
PDF for offline reading.

The Python lab runs without paid services, API keys or third-party packages:

```bash
python3 labs/ground_truth_lab.py all --output labs/output
python3 -m unittest discover -s labs/tests -v
```

Its data and business outcomes are labelled as simulated. See [the lab guide](labs/README.md) for
assumptions, exercises, filled reports and checks that stop a bad run.

## Repository structure

```text
ai-ml-ground-truth/
├── 01-getting-oriented/
├── 02-data-foundations/
├── 03-core-machine-learning/
├── 04-deep-learning/
├── 05-language-models/
├── 06-production/
├── 07-specialisation/
├── 08-finding-the-work/
├── 09-business-machine-learning/
├── content/                  # Reader's guide, start page and publishing guide
├── labs/                     # Runnable Python reference project and its guide
│   ├── reference/            # Checked-in example reports, figures and manifests
│   └── tests/                # Python lab tests
├── website/                  # All website implementation and build configuration
│   ├── src/                  # Components, layouts, routes, scripts and styles
│   ├── public/               # Cover, favicon and standalone interaction script
│   ├── scripts/              # Build preparation, EPUB export and link validation
│   ├── tests/                # Website content and interaction tests
│   ├── package.json
│   └── package-lock.json
├── .github/                  # Workflows, issue form, pull-request template and Dependabot
├── README.md                 # Repository entry point
├── CONTRIBUTING.md           # Short contribution guide
├── CITATION.cff              # Citation metadata for the current edition
├── LICENSE                   # CC BY 4.0 for the book's text, illustrations and lab reports
└── LICENSE-CODE              # MIT for the website, lab code and code examples
```

Each numbered chapter has its main `README.md` and annotated `resources/README.md`. Chapter 9
also holds the applied guides and shared delivery plan. These Markdown files are the book's source
of truth. The website renders them directly and builds shorter lessons from their sections. The
chapter folders, `content/` and teaching `labs/` stay at the repository root. The website reads
these files in place, so there is only one copy to maintain.

When reorganising or restyling, keep the chapter order, learning decisions, explanations and the
author's voice. Keep website code, assets, dependencies, tests and configuration in
`website/`. GitHub requires workflow files in the root `.github/workflows/` directory.

`labs/reference/` holds maintained, versioned examples. Local lab runs go to the ignored
`labs/output/` directory. Website output (`website/dist/`), intermediates (`website/.astro/`
and `website/.cache/`), generated public assets and installed dependencies are also ignored. Edit
the source files, not those generated copies. See
[what to change where](content/publishing.md#what-to-change-where).

## Develop and publish

Use **Node.js 24** (Astro needs at least 22.23.4) and Python 3.10 or newer. Run these commands
from the repository root:

```bash
npm --prefix website ci
npm --prefix website run dev
```

Before publishing:

```bash
npm --prefix website run format:check
npm --prefix website run check
npm --prefix website test
npm --prefix website run build
npm --prefix website run preview
```

A build creates the static site, Pagefind search index and offline EPUB, and checks internal
links. To check the complete built edition, including search, open the URL the preview command
prints. The development server alone does not build the search index.
GitHub Actions checks pull requests and deploys successful builds from `main` to GitHub Pages.
Pushing an `edition-*` tag publishes a GitHub release with the EPUB and a PDF of the print edition.
See [publishing and contributing](content/publishing.md) for configuration, source locations,
review practice and external-link checks.

The reading budgets are planning estimates, not measured completion times or job guarantees.

## Author and reuse

Written by **Santosh Shinde**. The [author’s note and AI-assistance disclosure](content/reader-guide.md#a-note-from-the-author)
explain the motivation and process. Corrections backed by primary sources and reproducible
examples are welcome (see [contributing](CONTRIBUTING.md)). To cite the book, use
[`CITATION.cff`](CITATION.cff) or GitHub's "Cite this repository" button.

**Licence.** The book's text, illustrations and lab reports are released under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE). You may share, translate and
adapt them, including commercially, if you give credit, link to the licence and note any
changes. The website, the lab code and the code examples in the chapters are under the
[MIT licence](LICENSE-CODE). A suitable credit is: *Ground Truth* by Santosh Shinde,
https://santoshshinde2012.github.io/ai-ml-ground-truth/, CC BY 4.0. External papers, courses,
datasets and fonts keep their own terms. Earlier commits of this repository are still available
under the MIT licence.
