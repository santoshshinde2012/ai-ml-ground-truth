# Resources — Chapter 8: Finding the work

Everything referenced in [the chapter](../README.md), grouped by how central it is, with a short
note on what each one is for.

Prices and free tiers change often, so check a resource's own page before you plan around one.

---

## Start here

The resources on the main path for this chapter. If you only do a few things, do these.

### [AI Engineer Compensation Trends (Q3 2025)](https://www.levels.fyi/blog/ai-engineer-compensation-trends-q3-2025.html)

*Alina Kolesnikova* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

The one pay source that breaks the AI premium down **by level**, which corrects the most common expectation: the entry-level AI premium is just 6.2% (down from 10.7% in 2024), standard 11.9%, senior 14.2%, staff 18.7% (up from 15.8%). Average US AI engineer $245K; median peaked at $295K in Mar 2024, dipped to $228.5K by Jan 2025, rebounded to ~$260–269K. The short version: the AI premium is a seniority premium, and it is shrinking at the entry level. Pair it with the caveat that levels.fyi is self-reported and big-tech-skewed.

> **Worth knowing.** Published July 2025 despite the Q3 2025 label and now over a year stale, and compensation data decays fast. levels.fyi figures are self-reported and skewed toward US big tech and senior levels.

### [normcore-llm-reads](https://gist.github.com/veekaybee/be375ab33085102f9027853128dc5f0e)

*Vicki Boykis* &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; varies

An explicitly anti-hype curated reading list — Boykis's stated filter is 'no hype, no langchain, no apocalyptic AI predictions', collecting material that explains how things actually work. For a beginner drowning in LinkedIn-grade content, a named engineer's taste is worth more than an algorithmic feed. Pair with her essay ['What we don't talk about when we talk about building AI apps'](https://vickiboykis.com/2023/07/18/what-we-dont-talk-about-when-we-talk-about-building-ai-apps/), which covers the unglamorous reality — 10GB GPU Docker images and similar — that no course teaches.

> **Worth knowing.** A curated reading list published as a GitHub gist rather than a repository or a course.

### [State of AI Report 2025](https://www.stateof.ai/)

*Nathan Benaich* &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3 hours

The best single 'where is the industry actually going' briefing, and it is written by an investor with skin in the game rather than a content marketer. Its 2025 findings relevant to a job-seeker: 44% of US businesses now PAY for AI tools (up from 5% in 2023), average contract $530K, AI-first startups growing 1.5x faster than peers, 95% of surveyed professionals using AI at work or home. Use it to justify which *sectors* a beginner should target, not for career advice per se.

> **Worth knowing.** The site root serves whichever edition is current, so it will silently switch to a later report and leave any "2025" figures unsupported — find the specific 2025 deck.

### [AI Engineer Roadmap (roadmap.sh)](https://roadmap.sh/ai-engineer)

*Kamran Ahmed* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; varies

The most-used roadmap in the world, and worth knowing. It correctly frames the AI Engineer as someone who 'uses pre-trained models and existing AI tools' rather than training from scratch, which is the right 2026 framing. Its failures: it is a topic **graph**, not a sequence — no time budgets, no prerequisites made explicit, no assessment, no projects tied to nodes, and dozens of parallel branches that induce exactly the decision paralysis that precedes abandonment. Its sibling, the [AI and Data Scientist roadmap](https://roadmap.sh/ai-data-scientist), is worse: it offers generic 'learn stats and Python, build a portfolio' guidance with no LLM, transformer, MLOps or deployment coverage.

> **Worth knowing.** A topic graph, not a curriculum: it shows what exists, not how or in what depth to learn it, and the linked leaf resources vary widely in quality with no editorial vetting. The "2026" label is rolling, with no update date behind it.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [CIRR verified bootcamp outcomes](https://www.cirr.org/schooldata)

*Council on Integrity in Results Reporting* &nbsp;·&nbsp; Dataset &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

Include it for what it **no longer** shows, which is a finding in itself. CIRR is the only standard that defines 'employed' as full-time professional work in a field requiring the skills taught, reported at 90/180/360 days with independent audit. Only three schools had current reports (Codesmith, Code Platoon, Hacktiv8) and their headline rates displayed as 'TBD'. Bootcamp outcome transparency has effectively collapsed, which means every '79% placed in 1–6 months' or '94% hired' figure circulating in 2026 is self-reported marketing.

> **Worth knowing.** The latest cohort data predates the 2025–26 junior-hiring contraction, and almost all covered schools are software-engineering bootcamps, not AI/ML programmes.

### [The Fearless Future: PwC's 2025 Global AI Jobs Barometer](https://www.pwc.com/gx/en/issues/artificial-intelligence/job-barometer/2025/report.pdf)

*PwC global research team* &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The largest-N job-ad study available and the origin of the widely-quoted '56% wage premium for AI skills' (up from 25% the prior year) and 'skills sought are changing 66% faster in the most AI-exposed jobs'. That second number matters more than the first: it is the empirical case for building *learning velocity* rather than a fixed tool stack. A 2026 edition has since been published; search for the current PwC AI Jobs Barometer before quoting figures. Caveat: consultancy report, incentive to overstate the premium.

> **Worth knowing.** PwC is a consultancy with a commercial interest in AI-transformation advisory, and the wage-premium headlines are its own analysis, not peer-reviewed. 2025 data being read in late 2026.

## Keep for reference

Not for reading end to end. Useful to have when you need to look something up.

### [Machine Learning Interview Prep Guide (2026)](https://www.tryexponent.com/blog/machine-learning-interview-guide)

*Exponent Team* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 3 hours

Useful only as a structural map of the 2026 loop, which it describes consistently with Eugene Yan's hiring-side account: recruiter screen, technical phone screen, sometimes a take-home notebook, then an onsite of 4–6 rounds mixing 1–2 coding rounds, an ML coding round, a 45–55 minute ML system design round (frame the task, data pipeline, training, evaluation, drift monitoring), and 1–2 behavioural rounds. Two 2026-specific signals worth verifying independently: the coding bar in ML loops has risen close to general SWE level, and Meta reportedly now runs an AI-assisted coding round where you debug and extend a real codebase using an LLM.

> **Worth knowing.** Commercial content marketing from a company that sells interview prep, so its recommendations map onto its paid product; the 'DRIVE framework' is proprietary branding, not an industry standard.

### [ML / AI Software Engineer salary tracker](https://www.levels.fyi/t/software-engineer/focus/ml-ai)

*levels.fyi* &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

Use as a live lookup, not as a target. Average ML/AI SWE total compensation is around $245,000 in the US. Use it as a *calibration exercise*: filter to entry-level in your own city and compare that to the headline figure. The gap is usually large. Its weakness is severe survivorship and big-tech bias — nobody posts their ₹6 LPA or $78K offer.

> **Worth knowing.** A tool, not a learning resource. The $245,000 figure is average total compensation, United States, self-reported and undated — not a median, and not what an entry-level candidate should expect.

### [ML-YouTube-Courses](https://github.com/dair-ai/ML-YouTube-Courses)

*DAIR.AI* &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The best free index of university-grade ML lectures, 17.4k stars with categories for ML (Stanford CS229, Caltech CS156), deep learning (Stanford CS230), NLP (Stanford CS25 Transformers, CMU Advanced NLP), CV (CS231n), RL (CS234, DeepMind), practical ML/LLMOps, and graph/scientific ML. Use it as a lookup table for depth on a specific topic, never as a path — an undifferentiated list of 1,000+ hours of lectures is a dropout machine, and its LLM section still leans on 2023–24 material (ChatGPT Prompt Engineering for Developers, LangChain, Full Stack LLM Bootcamp) that has aged fast.

> **Worth knowing.** A curated index whose newest entries are roughly two years old, so it points at superseded courses; check that individual course links are still live before committing to one.

### [OSSU Data Science curriculum](https://github.com/ossu/data-science)

*Open Source Society University* &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2 hours

Include it as the honest benchmark for what a full self-taught degree-equivalent actually costs, and as a cautionary structure. 11 sequential topic areas with a dependency graph, covering intro CS/DS, calculus, linear algebra, statistics, databases, DSA, ML, data mining and tools, ending in a capstone; the repo itself warns that its own planning spreadsheet may be out of date. Strengths — honest hour budgets, explicit prerequisites, sequencing. Weaknesses for a 2026 job-seeker — it is optimised for academic breadth, not hireability; it has essentially no transformer/LLM/agent/eval content; and a 20 h/week/2-year commitment collides directly with how rarely long unsupported online courses are finished (the completion data is in Chapter 1's resources).

> **Worth knowing.** A classical data-science degree substitute, not an AI/ML path. Its component MOOCs age independently of the repo, so recent commits do not mean fresh material — and it asks for about two years at 20h/week.

---
[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
