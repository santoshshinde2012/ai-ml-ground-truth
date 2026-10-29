# Ground Truth

**An illustrated engineering field guide for working developers moving into AI and machine learning.**

Nine chapters connect data foundations, honest model evaluation, deep learning, language-model
applications, production systems and business decisions. One project develops across the learning
path, supported by original worked lessons, eight interactive explanations and a reproducible
reference laboratory.

**[Read the web book](https://santoshshinde2012.github.io/ai-ml-ground-truth/)** ·
[Start here](content/start-here.md) · [Reader’s guide](content/reader-guide.md) ·
[Run the reference lab](labs/README.md)

## Chapters

| | Chapter | References |
|---|---|---|
| 01 | [Getting oriented](01-getting-oriented/README.md) | [Resources](01-getting-oriented/resources/README.md) |
| 02 | [Data foundations](02-data-foundations/README.md) | [Resources](02-data-foundations/resources/README.md) |
| 03 | [Core machine learning](03-core-machine-learning/README.md) | [Resources](03-core-machine-learning/resources/README.md) |
| 04 | [Deep learning](04-deep-learning/README.md) | [Resources](04-deep-learning/resources/README.md) |
| 05 | [Language models and AI engineering](05-language-models/README.md) | [Resources](05-language-models/resources/README.md) |
| 06 | [Running it in production](06-production/README.md) | [Resources](06-production/resources/README.md) |
| 07 | [Choosing a specialisation](07-specialisation/README.md) | [Resources](07-specialisation/resources/README.md) |
| 08 | [Finding the work](08-finding-the-work/README.md) | [Resources](08-finding-the-work/resources/README.md) |
| 09 | [Business machine learning](09-business-machine-learning/README.md) | [Resources](09-business-machine-learning/resources/README.md) |

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
```

A build generates the static site, Pagefind search index, offline EPUB and checks internal links.
GitHub Actions verifies pull requests and deploys successful builds from `main` to GitHub Pages.
See [publishing and contributing](content/publishing.md) for configuration, source locations,
review practices and external-link checking.

Chapter Markdown is the canonical source. Generated site files and local lab output are ignored.
The reading budgets are planning estimates, not measured completion times or employment guarantees.

## Author and reuse

Written by **Santosh Shinde**. The [author’s note and AI-assistance disclosure](content/reader-guide.md#a-note-from-the-author)
explain the motivation and process. Corrections with primary sources and reproducible examples are
welcome. Released under the [MIT license](LICENSE); external resources retain their own terms.
