# Chapter 8: Finding the work

**Week 33 onward &nbsp;·&nbsp; runs alongside chapters 6 and 7.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** The search is a process you run, not a verdict on you: present three deep
projects well, practise the interview stories out loud, track your numbers, and use the doors that
are actually open. This chapter runs alongside the last two, because a search can take months and
starting early teaches you what the market wants.

**In this chapter:** [First month](#your-first-month-alongside-chapters-67) &nbsp;·&nbsp;
[Portfolio](#presenting-your-work) &nbsp;·&nbsp; [Interviews](#the-interview-loop) &nbsp;·&nbsp;
[Search](#the-search-itself) &nbsp;·&nbsp; [Completion](#before-you-move-on)

---

## Your first month (alongside Chapters 6–7)

About three to four hours a week on the search, while you keep building. This is not full-time job
hunting yet.

| Week (from Ch 6 start) | Focus             | Do this                                                               | Done when                       |
| ---------------------- | ----------------- | --------------------------------------------------------------------- | ------------------------------- |
| 1                      | Portfolio hygiene | Archive tutorial forks; README template on best project               | One README has all six sections |
| 2                      | Stories           | Write out three 90-second stories; say them twice                     | Timer ≤ 90s each                |
| 3                      | Tracker           | Start spreadsheet; log every application; compute one conversion rate | 5+ rows                         |
| 4                      | Visibility        | One short write-up post; share in one community (not spam)            | Link you can send recruiters    |

After month one: keep logging applications weekly; refresh README when metrics move; do not wait
until Chapter 7 finishes to start.

---

## What you will be able to do

Present three projects so that a reviewer understands them in two minutes, tell three interview
stories out loud without notes, and run a search you can measure and adjust rather than endure.

Three projects is a planning target. Distinct case studies can come from the same coherent project:
data and validation, model or experiment results, and production delivery. Give each a clear
question and its own evidence, and prioritize the work relevant to your target roles.

## Presenting your work

Make the first two minutes useful for a reviewer. These are presentation recommendations, not
measured hiring effects:

- **Archive the tutorial forks.** A weak repository sits next to your strong one and gets opened
  too. Give your strongest projects clear prominence.
- **Make the README useful without running the code.** State the question, the result with a number,
  the architecture, the key decisions, what did not work, and the known failures. Those last two
  sections let a reviewer assess your judgement.
- **Demonstrate something.** Provide a working public demo, recorded walkthrough or reproducible
  local command appropriate to the data and cost.
- **Write things up.** One short post per major topic, explaining it plainly. It is good revision,
  and it is how people find you.

**A README outline that works.** Copy this into each project and fill in the blanks:

```markdown
# [Project name]

## Question

One sentence: what did you try to answer?

## Result

State the baseline, result, held-out sample size and uncertainty.
Say whether the evidence is synthetic, retrospective or from a live experiment.

## How it works

Three to five sentences, or a simple diagram. Link a live URL if you have one.

## Key decisions

Two or three bullets: what you chose and what you rejected.

## What did not work

One or two failures, with evidence and what you changed.

## Known limitations

What the system should not be used for.
```

A business project can use the
[Chapter 9 evidence levels](../09-business-machine-learning/README.md#what-to-build): "improved
policy value in a simulator" and "increased live contribution in a randomized test" are different
results. Include the assignment unit, horizon, no-action baseline and costs. If you have only
observational transactions, demonstrate predictive performance and describe the missing intervention
evidence. A reviewer should be able to reproduce the claim you actually make.

On open source, start with a bug you hit while building your own project. The entries in
[Chapter 7's resources](../07-specialisation/resources/README.md) cover the mechanics. Read the
project's current contribution policy:
[scikit-learn](https://scikit-learn.org/stable/developers/contributing.html) requires contextual
understanding, careful human review and disclosure of AI tool use;
[Transformers](https://github.com/huggingface/transformers/blob/main/CONTRIBUTING.md) welcomes
coordinated, verified AI assistance and requires disclosure and test evidence. You remain
responsible for every changed line and for the maintainer's review burden.

## The interview loop

Use [Eugene Yan and Jason Liu's hiring account](https://eugeneyan.com/writing/how-to-interview/) to
connect your projects to coding, data and evaluation questions. Confirm the actual stages, time
limits and allowed tools with the recruiter. Practise independent coding and explaining
assistant-produced code when the employer permits assistance.

Have three stories ready and practise them out loud, at ninety seconds each:

1. A time your numbers were wrong and you found out. The leakage exercise is built for this.
2. A time you chose the simpler option deliberately, with the numbers behind it.
3. A time you shipped something someone else used.

**Story structures, not results to borrow.** Replace each scenario with work you actually did and
measurements you can defend. Keep the task, mistake or tradeoff, evidence, change and outcome.

1. **Wrong numbers.** "My delivery model used a final-status field that only arrived after the
   decision. I removed it, rebuilt decision-time features, and evaluated on a later period with
   mature labels. Here are the original and corrected scores, sample sizes and release test."
2. **Simpler on purpose.** "I compared retrieval with fine-tuning on the same held-out questions.
   The paired comparison did not establish a meaningful improvement at the cost we could support. I
   chose retrieval and documented remaining errors and the evidence that would change my mind."
3. **Someone else used it.** "A team used my triage tool for a defined pilot. I recorded eligible
   cases, usage and failures. I fixed one failure class and tested the change on a separate release
   set. Here is the measured scope of the pilot and the reproducible evaluation."

A result on 50 examples is a useful starting signal, not a precise population guarantee. One extra
pass changes the rate by two percentage points. Show paired disagreement counts or an appropriate
interval, and separate pilot adoption from evidence that your change caused a business improvement.

## The search itself

Run it as a process. Track applications and three conversion rates: applications to screens, screens
to onsites, onsites to offers. Calculate rates for resolved stage transitions, show the
denominators, and keep awaiting decisions separate. Compare cohorts with similar time to resolve;
different response delays can change resolved-only rates without any improvement in applications.
Use each stage to locate a question to investigate before choosing more preparation.

**A tracker you can actually use.** One spreadsheet or markdown file; update it weekly:

| Date       | Company    | Role        | Source (referral / community / cold) | Stage  | Outcome | Notes                              |
| ---------- | ---------- | ----------- | ------------------------------------ | ------ | ------- | ---------------------------------- |
| 2026-09-01 | Example Co | AI Engineer | Referral from blog post              | Screen | Waiting | Sent portfolio link to RAG project |

Low application-to-screen conversion calls for a review of role fit, eligibility, CV and portfolio
signals. Low screen-to-onsite or onsite-to-offer conversion calls for feedback on the actual rounds,
including coding, SQL, design and communication where assessed. Review level or pay expectations
when those were a stated obstacle. A funnel rate alone cannot identify the cause.

Review a small sample of current postings in your target city and level before spending weeks on
preparation. Record the date, actual responsibilities, required skills, interview format if known
and which project supplies evidence. Revisit this monthly. Titles alone are unreliable: an "AI
Engineer" role can mean product integration, retrieval, modeling, infrastructure or research.

| Posting requirement                  | Evidence to prepare                                                  | Gap to close                                                         |
| ------------------------------------ | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Offer, pricing or retention modeling | Chapter 9 decision brief, realistic validation and experiment design | Explain prediction versus intervention, support and net contribution |
| LLM application engineering          | Chapter 5 held-out evaluation, failure analysis and access controls  | Explain retrieval, tool reliability and cost/quality tradeoffs       |
| ML platform or backend engineering   | Chapter 6 release, monitoring and rollback exercise                  | Explain compatibility, freshness, retries and operational ownership  |

Track referrals, community contacts and targeted applications separately; use your own funnel to
choose where to invest time. Small counts fluctuate, and a low response rate can reflect fit,
location, timing or application quality. Change one aspect, then review a new batch rather than
redesigning your whole portfolio after one rejection.

Consider adjacent roles whose responsibilities match your experience: data engineering, backend work
on an AI product, contract projects or an internal transfer. Check the actual mentorship, work and
transfer policy; a backend offer does not promise a move into ML within a year. Non-technology
employers may also have relevant tabular and document projects.

On pay, compare your level, location and compensation components.
[Indeed's September 2026 US analysis](https://hiringlab.indeed.com/2026/09/17/ai-exposure-isnt-squeezing-advertised-pay-in-the-us-its-boosting-it/)
finds seniority affects advertised-pay comparisons; its seniority-specific evidence is suggestive.
It studies salary-advertising US postings, not individual offers or Indian salaries. Self-reported
compensation trackers and aggregate AI wage premiums cannot predict your offer. Check current local
ranges and distinguish base pay, equity, bonuses and contract terms.

## Staying current afterwards

Split your attention. The fast layer, which turns over in a year or two, is model names, frameworks,
pricing, free tiers and specification versions. The slow layer, which is still true in a decade, is
attention, backpropagation, evaluation design, generalisation, retrieval, cost and latency,
statistics and SQL. Spend your study time on the slow layer and merely **monitor** the fast one; a
couple of hours a week on a small number of named, human-written sources is plenty.

Once a quarter, spend ninety minutes checking whether anything you depend on has changed price, been
deprecated or moved, and **re-run your evaluations before adopting a model version change**. Rolling
model aliases can change without a code change; record the resolved version and investigate
unexpected regressions with your evaluation suite.

## Resources

All 12 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [AI Engineer Compensation Trends (Q3 2025)](https://www.levels.fyi/blog/ai-engineer-compensation-trends-q3-2025.html)
  — Alina Kolesnikova, levels.fyi. A free article, under an hour, for calibrating pay expectations
  by level.
- [How to Interview and Hire ML/AI Engineers](https://eugeneyan.com/writing/how-to-interview/) —
  Eugene Yan and Jason Liu. A hiring-side account to turn your projects into interview evidence.
- [normcore-llm-reads](https://gist.github.com/veekaybee/be375ab33085102f9027853128dc5f0e) — Vicki
  Boykis. A free curated reading list for staying current without the noise.
- [State of AI Report 2026](https://www.stateof.ai/) — Nathan Benaich and Air Street Capital. An
  annual industry overview; follow its primary sources and verify actual openings before choosing a
  sector.

## Before you move on

- Your project case studies follow the outline above, including "what did not work."
- You have said each of the three interview stories out loud at least twice.
- Your tracker has at least ten rows and you know which conversion rate is weakest.
- You have checked pay expectations at **your** level and city, not the headline average.

---

[Previous: Choosing a specialisation](../07-specialisation/README.md) &nbsp;·&nbsp;
[Next: Business machine learning](../09-business-machine-learning/README.md) &nbsp;·&nbsp;
[Back to the index](../README.md)
