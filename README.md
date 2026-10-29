# Ground Truth

**A working developer's path into AI and machine learning.**

**The short version.** Eight core chapters take you from shipping software to shipping AI systems in
about 450 hours. A ninth applied chapter covers **offer recommendation, price recommendation and
churn**, with model choices and a full business decision workflow. You build on **one thread** — one
dataset becomes one model becomes one AI product. Each chapter has a practical plan and a
`resources` folder for deeper reading.

The illustrated web edition adds worked lessons, eight interactive explanations and a reproducible
reference laboratory. The [reader's guide](content/reader-guide.md) contains the original long-form
introduction, learning philosophy, [schedule and assumptions](content/reader-guide.md#time),
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
an applied extension after Chapters 3 and 6; one case can supply the Chapter 7 capstone. The
[reader's guide](content/reader-guide.md#how-to-use) explains the full sequence.

The applied guides cover [causal foundations](09-business-machine-learning/causal-primer.md),
[offers](09-business-machine-learning/offer-recommendation.md),
[prices](09-business-machine-learning/price-recommendation.md),
[churn and retention](09-business-machine-learning/churn.md), and a
[shared delivery plan](09-business-machine-learning/delivery-plan.md).

## Read, explore, practice

The web edition provides chapter and lesson navigation, local search, eight interactive field notes,
light/dark appearance, focus reading, optional progress saved on your device, a complete print
edition and an EPUB download. Core content is readable without JavaScript.

The Python laboratory runs without paid services, API keys or third-party Python packages:

```bash
python3 labs/ground_truth_lab.py all --output labs/output
python3 -m unittest discover -s labs/tests -v
```

Its data and business outcomes are explicitly simulated. See [the lab guide](labs/README.md) for
assumptions, exercises, filled reports and meaningful failure checks.

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
├── src/                      # Website components, layouts, routes, scripts and styles
├── public/                   # Cover, favicon and standalone interaction script
├── scripts/                  # Build preparation, EPUB export and link validation
├── tests/                    # Website content and interaction tests
├── .github/workflows/        # Pull-request checks and GitHub Pages deployment
├── README.md                 # Repository entry point
└── LICENSE
```

Each numbered chapter keeps its main `README.md` and annotated `resources/README.md`. Chapter 9
also contains the applied guides and shared delivery plan. These Markdown files are the canonical
book content; the website renders them directly and derives shorter lessons from their sections.

Keep chapter order, learning decisions, explanations and the author's voice intact when changing
organization or presentation. Put website implementation in `src/` and supporting build tools in
`scripts/`, rather than mixing them into the chapter folders.

`labs/reference/` contains maintained, versioned examples. Local lab runs go to the ignored
`labs/output/` directory. Website output (`dist/`), intermediates (`.astro/` and `.cache/`), generated
public assets and installed dependencies are also ignored. Edit the source files rather than those
generated copies; see [what to change where](content/publishing.md#what-to-change-where).

## Develop and publish

Use **Node.js 24** and Python 3.10 or newer:

```bash
npm ci
npm run dev
```

Before publishing:

```bash
npm run check
npm test
npm run build
npm run preview
```

A build generates the static site, Pagefind search index, offline EPUB and checks internal links.
Use the URL printed by `npm run preview` to check the complete built edition, including search;
the development server alone does not generate the search index.
GitHub Actions verifies pull requests and deploys successful builds from `main` to GitHub Pages.
See [publishing and contributing](content/publishing.md) for configuration, source locations,
review practices and external-link checking.

The reading budgets are planning estimates, not measured completion times or employment guarantees.

## Author and reuse

Written by **Santosh Shinde**. The [author’s note and AI-assistance disclosure](content/reader-guide.md#a-note-from-the-author)
explain the motivation and process. Corrections with primary sources and reproducible examples are
welcome. Released under the [MIT license](LICENSE); external resources retain their own terms.
