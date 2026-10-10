# Resources — Chapter 1: Getting oriented

Everything referenced in [the chapter](../README.md), grouped by how central it is, with a short
note on what each one is for.

Prices and free tiers change often, so check a resource's own page before you plan around one.

**Browse:** [Start here](#start-here) &nbsp;·&nbsp; [Optional depth](#optional-depth)

---

## Start here

The resources on the main path for this chapter, in the order the chapter uses them. If you only do
a few things, do these.

### [How to Interview and Hire ML/AI Engineers](https://eugeneyan.com/writing/how-to-interview/)

_Eugene Yan_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

One hiring manager's detailed rubric: software engineering, data literacy, uncertainty, evaluation,
and scientific breadth/depth, with behavioural evidence of handling ambiguity and execution. Use it
to review your project and prepare concrete examples. Check each employer's actual interview format;
the article does not establish which skills are most tested across the industry.

### [The Rise of the AI Engineer](https://www.latent.space/p/ai-engineer)

_Shawn "swyx" Wang_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The 2023 essay that popularised this role's current framing: developers building products on
pretrained models, with substantial work in integration, evaluation and operations. Useful for
understanding the work, rather than predicting how many jobs exist or whether a particular employer
requires a degree. Its forecasts are the author's argument, not measured hiring results.

> **Worth knowing.** Read it as the origin document for the term, not as current market analysis —
> its 2023 supply/demand reasoning predates both the agent era and the junior-market contraction.

### [AI and Job Postings: From Destruction to Creation?](https://hiringlab.indeed.com/2026/07/08/ai-and-job-postings-from-destruction-to-creation/)

_Guillermo Gallacher_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

An analysis of US Indeed postings, published July 2026. Software development postings rose roughly
15% from late February 2025 while overall postings fell 7%, yet remained 27.5% below February 2020.
Senior roles accounted for 71% of the year-over-year increase in May 2026; AI-titled roles accounted
for 37% of that increase. These categories can overlap. Use the measured market, dates and
denominators when citing the findings; neither postings nor a rebound prove that AI caused hiring or
that the same pattern holds in your country.

> **Worth knowing.** The headline finding is correlational: the roughly 15% rebound is anchored to a
> coding-assistant release date, which invites a causal reading the data does not support.

### [Teach Yourself Programming in Ten Years](https://www.norvig.com/21-days.html)

_Peter Norvig_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

A durable argument for sustained practice: program actively, read other people's code, build
projects, seek feedback and understand the hardware. The title is an antidote to instant-expertise
marketing, rather than a validated ten-year requirement for every learner or role.

### [uv: Working on projects and locking dependencies](https://docs.astral.sh/uv/guides/projects/)

_Astral maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

Start with [installation](https://docs.astral.sh/uv/getting-started/installation/), then use this
for the Chapter 1 setup, interpreter selection and project files. Read
[locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) to understand `--locked`,
deliberate upgrades and environment synchronization. Commit the Python version and dependency lock,
and verify a fresh clone; a lockfile does not capture datasets or hardware.

### [Official compute limits and pricing](https://research.google.com/colaboratory/faq.html)

_Service maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free to read &nbsp;·&nbsp; 30
minutes

Check the [Colab FAQ](https://research.google.com/colaboratory/faq.html),
[Kaggle notebook documentation](https://www.kaggle.com/docs/notebooks),
[Lightning pricing](https://lightning.ai/pricing) and [Modal pricing](https://modal.com/pricing)
before choosing a runtime. Colab does not guarantee a specific free GPU or fixed published usage
limit. Modal Starter credits do not cover per-token Shared Endpoints charges. Choose using measured
memory/runtime needs, save checkpoints outside ephemeral sessions, and set a spending limit before
paid use. Chapters 1–3 can run on CPU.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [2026 Stack Overflow Developer Survey](https://survey.stackoverflow.co/2026)

_Stack Overflow research team_ &nbsp;·&nbsp; Dataset &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The latest edition was released on
[October 6, 2026](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here).
Explore AI use, trust, work and learning, checking the respondent count and subgroup for each
question. It is a voluntary developer survey: reported tool use and opinions do not measure
productivity or establish causal learning effects. Compare with the
[2025 AI section](https://survey.stackoverflow.co/2025/ai) only after checking whether questions and
respondent populations changed.

> **Worth knowing.** A percentage of AI users is not automatically a percentage of all developers.
> Annual respondent samples are not a longitudinal panel.

### [Experiments on AI assistance and learning](https://arxiv.org/abs/2607.08849v2)

_Zara Contractor & Germán Reyes_ &nbsp;·&nbsp; Preprint revised 4 October 2026 &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 1–2 hours of selected reading

An AI-access experiment with 211 undergraduates found improved unaided knowledge tests after an
unfamiliar-topic essay task, including a smaller gain at one week. Its tutoring/delegation
comparisons are descriptive, and the task differs from learning a programming library. Pair it with
[Heickal and Lan's 2026 classroom-feedback workshop paper](https://proceedings.mlr.press/v339/heickal26a.html):
feedback reached failed submissions, and its reported associations concern completion and retries,
not delayed independent mastery. Use these alongside the book's coding trial to distinguish
interventions and outcomes; a polished assisted artifact is not a retention test.

### [Deliberate Practice and Performance: A Meta-Analysis](https://journals.sagepub.com/doi/10.1177/0956797614535810)

_Brooke N. Macnamara, David Z. Hambrick & Frederick L. Oswald_ &nbsp;·&nbsp; Paper &nbsp;·&nbsp;
Abstract free; full text may require access &nbsp;·&nbsp; 2 hours

Read for the distinction between practice helping and practice explaining every difference in
performance. The 2014 meta-analysis found substantial variation across domains; its
[2018 correction](https://journals.sagepub.com/doi/10.1177/0956797618769891) revised some estimates.
Definitions of deliberate practice and study measurements matter. Explained variance across people
is not an individual's learning ceiling or evidence that feedback is unnecessary.

> **Worth knowing.** This is historical evidence with a published correction, rather than a current
> experiment on learning AI engineering.

### [Make It Stick: The Science of Successful Learning](https://www.makeitstick.com/)

_Peter C. Brown with Henry L. Roediger III & Mark A. McDaniel_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid
&nbsp;·&nbsp; 8–10 hours

An accessible account of research on learning and memory, produced out of a ten-year collaboration
among 11 cognitive scientists at six universities. Its emphasis on retrieval practice, spacing and
interleaving fits this roadmap: rebuild a small example from memory, revisit it later, and check
your mistakes against working code. Reading the book is optional; apply the practices to your weekly
sessions before adding another reading commitment.

### [The MOOC Pivot](https://webs.um.es/jruiperez/papers/journals/2019_Science_MOOCPivot_postprint.pdf)

_Justin Reich & José A. Ruipérez-Valiente_ &nbsp;·&nbsp; Science paper, author postprint
&nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

Original 2019 paper using MITx/HarvardX data from 2012–2018, replacing a press summary. It separates
completion across all participants, people who reported an intention to finish and paid
verified-track learners. Many registrants never opened the courseware. That distinction makes
aggregate completion a poor prediction for a committed learner and does not imply that a certificate
only signals enrolment. Our practical response is to make each week produce working code and to seek
feedback.

> **Worth knowing.** Historical platform data is useful context, not a current estimate for every
> online course or learner.

### [The 2026 AI Index Report — Economy chapter](https://hai.stanford.edu/ai-index/2026-ai-index-report/economy)

_Stanford Institute for Human-Centered AI_ &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2
hours

An annual synthesis of investment, adoption, labour markets and productivity research. Follow its
citations to the underlying study before reusing a number: employer expectations, job postings,
employment and measured task productivity answer different questions. Check population, observation
period and causal design, especially when translating a US finding to your own market. The chapter
is a useful source map, rather than one experiment with a common denominator.

### [The Labor Market Is Tilting Toward Seniority](https://hiringlab.indeed.com/2026/07/23/the-labor-market-is-tilting-toward-seniority/)

_Felix Aidala & Sneha Puri, Indeed Hiring Lab_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free
&nbsp;·&nbsp; under an hour

A second Indeed analysis: in Q1 2026, senior roles made up 69.3% of US software development postings
and entry-level roles 4.5%. Across all US postings, senior roles were roughly 14% of the total. The
authors' seniority classification and the distinction between a share and a change over time matter.
Use this to examine the experience requested in your target vacancies and identify evidence you need
to build.

> **Worth knowing.** It counts US postings on one job site, not hires, so it shows demand rather
> than who actually gets the jobs. The authors also weigh causes other than AI, such as remote work
> and interest rates.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
