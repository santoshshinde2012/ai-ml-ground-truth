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
and scientific breadth/depth, plus behavioural signs of handling ambiguity and execution. Use it to
review your project and prepare concrete examples. It reflects one manager's priorities, so check
each employer's actual interview format.

### [The Rise of the AI Engineer](https://www.latent.space/p/ai-engineer)

_Shawn "swyx" Wang_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The 2023 essay that popularised this role's current framing: developers building products on
pretrained models, with substantial work in integration, evaluation and operations. It explains the
work, not how many jobs exist or whether an employer requires a degree. Its forecasts are the
author's argument, not measured hiring results.

> **Worth knowing.** Read it as the origin of the term, not current market analysis. Its 2023
> supply/demand reasoning predates both the agent era and the shrinking junior market.

### [AI and Job Postings: From Destruction to Creation?](https://hiringlab.indeed.com/2026/07/08/ai-and-job-postings-from-destruction-to-creation/)

_Guillermo Gallacher_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

An analysis of US Indeed postings, published July 2026. Software development postings rose roughly
15% from late February 2025 while overall postings fell 7%. They were still 27.5% below February
2020. In May 2026 senior roles made up 71% of the year-over-year increase and AI-titled roles 37%.
These categories can overlap. Cite the measured market, dates and denominators with the findings.
Postings and a rebound do not prove that AI caused hiring, or that your country follows suit.

> **Worth knowing.** The headline finding is a correlation. The roughly 15% rebound is measured from
> a coding-assistant release date, which invites a causal reading the data does not support.

### [Teach Yourself Programming in Ten Years](https://www.norvig.com/21-days.html)

_Peter Norvig_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

A lasting argument for steady practice: write programs, read other people's code, build projects,
ask for feedback and understand the hardware. The title is a reply to instant-expertise marketing,
not a tested ten-year rule for every learner or role.

### [uv: Working on projects and locking dependencies](https://docs.astral.sh/uv/guides/projects/)

_Astral maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

Start with [installation](https://docs.astral.sh/uv/getting-started/installation/), then use this
for the Chapter 1 setup, interpreter choice and project files. Read
[locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) to understand `--locked`,
planned upgrades and syncing the environment. Commit the Python version and dependency lock, then
check a fresh clone. A lockfile does not capture datasets or hardware.

### [Official compute limits and pricing](https://research.google.com/colaboratory/faq.html)

_Service maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free to read &nbsp;·&nbsp; 30
minutes

Start with the Colab FAQ linked in the heading, then check
[Kaggle notebook documentation](https://www.kaggle.com/docs/notebooks),
[Lightning pricing](https://lightning.ai/pricing) and [Modal pricing](https://modal.com/pricing)
before choosing a runtime. Colab does not promise a specific free GPU or a fixed, published usage
limit. Modal Starter credits do not cover per-token Shared Endpoints charges. Choose by measured
memory and runtime needs. Save checkpoints outside temporary sessions, and set a spending limit
before paid use. Chapters 1–3 can run on CPU.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [2026 Stack Overflow Developer Survey](https://survey.stackoverflow.co/2026)

_Stack Overflow research team_ &nbsp;·&nbsp; Dataset &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The latest edition was released on
[October 6, 2026](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here).
Explore AI use, trust, work and learning, and check the respondent count and subgroup for each
question. It is a voluntary survey, so reported tool use and opinions do not measure productivity
or show what causes better learning. Before comparing with the
[2025 AI section](https://survey.stackoverflow.co/2025/ai), check whether the questions and
respondents changed.

> **Worth knowing.** A percentage of AI users is not automatically a percentage of all developers.
> Each year's respondents are a new sample, not a panel followed over time.

### [Experiments on AI assistance and learning](https://arxiv.org/abs/2607.08849v2)

_Zara Contractor & Germán Reyes_ &nbsp;·&nbsp; Preprint revised 4 October 2026 &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 1–2 hours of selected reading

In an AI-access experiment, 211 undergraduates wrote an essay on an unfamiliar topic. Access improved
their later unaided knowledge-test scores, with a smaller gain at one week. Its tutoring and
delegation comparisons are descriptive, and an essay differs from learning a programming library.
Pair it with
[Heickal and Lan's 2026 classroom-feedback workshop paper](https://proceedings.mlr.press/v339/heickal26a.html).
There, feedback went to failed submissions, and the reported links are with completion and retries,
not later unaided mastery. Read both alongside the book's coding trial to keep interventions and
outcomes apart. A polished artefact made with AI help is not a retention test.

### [Deliberate Practice and Performance: A Meta-Analysis](https://journals.sagepub.com/doi/10.1177/0956797614535810)

_Brooke N. Macnamara, David Z. Hambrick & Frederick L. Oswald_ &nbsp;·&nbsp; Paper &nbsp;·&nbsp;
Abstract free; full text may require access &nbsp;·&nbsp; 2 hours

Read it for one distinction: practice can help without explaining every difference in performance.
The 2014 meta-analysis found large variation across domains, and its
[2018 correction](https://journals.sagepub.com/doi/10.1177/0956797618769891) revised some estimates.
How each study defines and measures deliberate practice matters. Variance explained across people
does not set your own learning ceiling or show that feedback is unnecessary.

> **Worth knowing.** This is older research with a published correction, not a current experiment
> on learning AI engineering.

### [Make It Stick: The Science of Successful Learning](https://www.makeitstick.com/)

_Peter C. Brown with Henry L. Roediger III & Mark A. McDaniel_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid
&nbsp;·&nbsp; 8–10 hours

A readable account of research on learning and memory, from a ten-year collaboration among 11
cognitive scientists at six universities. Its focus on retrieval practice, spacing and interleaving
fits this roadmap: rebuild a small example from memory, revisit it later, and check your mistakes
against working code. The book is optional. Apply the practices to your weekly sessions before
adding more reading.

### [The MOOC Pivot](https://webs.um.es/jruiperez/papers/journals/2019_Science_MOOCPivot_postprint.pdf)

_Justin Reich & José A. Ruipérez-Valiente_ &nbsp;·&nbsp; Science paper, author postprint
&nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The original 2019 paper using MITx/HarvardX data from 2012–2018, replacing a press summary. It
separates completion for all participants, those who said they intended to finish and paid
verified-track learners. Many registrants never opened the courseware. So overall completion says
little about a committed learner, and it does not mean a certificate only signals enrolment. This
book's practical answer: make each week produce working code, and ask for feedback.

> **Worth knowing.** Older platform data is useful context, not a current estimate for every online
> course or learner.

### [The 2026 AI Index Report — Economy chapter](https://hai.stanford.edu/ai-index/2026-ai-index-report/economy)

_Stanford Institute for Human-Centered AI_ &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2
hours

An annual summary of investment, adoption, labour market and productivity research. Before
reusing a number, follow its citation to the original study. Employer expectations, job postings,
employment and measured task productivity answer different questions. Check the population, period
and causal design, especially when applying a US finding to your own market. Treat the chapter as a
map of sources, not one experiment with a common denominator.

### [The Labor Market Is Tilting Toward Seniority](https://hiringlab.indeed.com/2026/07/23/the-labor-market-is-tilting-toward-seniority/)

_Felix Aidala & Sneha Puri, Indeed Hiring Lab_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free
&nbsp;·&nbsp; under an hour

A second Indeed analysis: in Q1 2026, senior roles made up 69.3% of US software development postings
and entry-level roles 4.5%. Across all US postings, senior roles were roughly 14% of the total. Note
how the authors classify seniority, and keep a share separate from a change over time. Use it to see
what experience your target vacancies ask for and what you still need to prove.

> **Worth knowing.** It counts US postings on one job site, not hires, so it shows demand rather
> than who actually gets the jobs. The authors also weigh causes other than AI, such as remote work
> and interest rates.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
