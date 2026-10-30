# Chapter 8: Finding the work

**Week 33 onward &nbsp;·&nbsp; about three to four hours a week, alongside chapters 6 and 7.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** The search is a process you run, not a verdict on you. Present three deep
projects well, practise your interview stories out loud, track your numbers, and use the doors that
are actually open. This chapter runs alongside the last two, because a search can take months and
starting early shows you what the market wants.

**In this chapter:** [First month](#your-first-month-alongside-chapters-67) &nbsp;·&nbsp;
[Portfolio](#presenting-your-work) &nbsp;·&nbsp; [Interviews](#the-interview-loop) &nbsp;·&nbsp;
[Search](#the-search-itself) &nbsp;·&nbsp; [Completion](#before-you-move-on)

---

## Your first month (alongside Chapters 6–7)

Spend about three to four hours a week on the search while you keep building. Full-time job hunting
comes later.

| Week (from Ch 6 start) | Focus             | Do this                                                               | Done when                       |
| ---------------------- | ----------------- | --------------------------------------------------------------------- | ------------------------------- |
| 1                      | Portfolio hygiene | Archive tutorial forks; README template on best project               | One README has every section    |
| 2                      | Stories           | Write out three 90-second stories; say them twice                     | Timer ≤ 90s each                |
| 3                      | Tracker           | Start spreadsheet; log every application; compute one conversion rate | 5+ rows                         |
| 4                      | Visibility        | One short write-up post; share in one community (not spam)            | Link you can send recruiters    |

After month one, log applications weekly and refresh your README when metrics move. Start now,
before Chapter 7 finishes.

---

## What you will be able to do

Present three projects so that a reviewer understands them in two minutes, tell three interview
stories out loud without notes, and run a search you can measure and adjust rather than endure.

Three projects is a planning target. The case studies can come from one connected project: data and
validation, model or experiment results, and production delivery. Give each a clear question and its
own evidence, and put work relevant to your target roles first.

## Presenting your work

Make a reviewer's first two minutes count. These are presentation suggestions, not measured hiring
effects:

- **Archive the tutorial forks.** A weak repository sits next to your strong one and gets opened
  too. Make your strongest projects easy to find.
- **Make the README useful without running the code.** State the question, the result with a number,
  the architecture, the key decisions, what did not work, and the known failures. Those last two
  sections show a reviewer your judgement.
- **Show something working.** Offer a public demo, recorded walkthrough or reproducible
  local command that suits the data and cost.
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

## Operations evidence

If it is deployed: release manifest, the alerts you act on, cost per 1k requests, and a link to
the incident report from a deliberate failure.

## Known limitations

What the system should not be used for.
```

For the operations section, link your [Chapter 6](../06-production/README.md) artifacts directly:
the incident report, rollback runbook, cost table and model card. The
[reference lab](../labs/README.md) has filled, simulated examples of a
[model card](../labs/reference/model-card.md) and an
[incident rehearsal](../labs/reference/incident-report.md). Use them as formats, not as your
evidence.

A business project can use the
[Chapter 9 evidence levels](../09-business-machine-learning/README.md#what-to-build). "Improved
policy value in a simulator" and "increased live contribution in a randomised test" are different
results. Include the assignment unit, horizon, no-action baseline and costs. If you only have
observational transactions, show predictive performance and say what intervention evidence is
missing. A reviewer should be able to reproduce the claim you actually make.

**Try it yourself.** A README's Result section says: "Churn model achieves 94% accuracy and will
save the business \$200k a year." What would a reviewer object to, and how would you rewrite it?

<details>
<summary>Hint and explained answer</summary>

Ask what the baseline is and what links a prediction to money. If 6% of customers churn, predicting
that nobody leaves is also 94% accurate, so the number says nothing on its own. The savings figure
needs a retention effect, which a churn classifier does not estimate. A checkable version names the
baseline, the held-out cohort and its size, a decision metric with an interval, and the evidence
level: "On a later cohort of 2,000 customers (6% churned), precision among the 100 we can contact
was 0.31 against 0.18 for a recency rule, with a paired bootstrap interval for the difference.
Retrospective evidence only. Savings need the proposed randomised retention test."

</details>

For open source, start with a bug you hit while building your own project. The entries in
[Chapter 7's resources](../07-specialisation/resources/README.md) cover the mechanics. Read each
project's current contribution policy.
[scikit-learn](https://scikit-learn.org/stable/developers/contributing.html) requires contextual
understanding, careful human review and disclosure of AI tool use.
[Transformers](https://github.com/huggingface/transformers/blob/main/CONTRIBUTING.md) welcomes
coordinated, verified AI assistance and requires disclosure and test evidence. You stay responsible
for every changed line and for the maintainers' review burden.

## The interview loop

Use [Eugene Yan and Jason Liu's hiring account](https://eugeneyan.com/writing/how-to-interview/) to
connect your projects to coding, data and evaluation questions. Confirm the actual stages, time
limits and allowed tools with the recruiter. Practise coding on your own, and explaining
assistant-written code where the employer allows it.

Have three stories ready and practise them out loud, at ninety seconds each:

1. A time your numbers were wrong and you found out. The
   [Chapter 3 leakage exercise](../03-core-machine-learning/README.md#what-to-build) is built for
   this.
2. A time you chose the simpler option deliberately, with the numbers behind it.
3. A time you shipped something someone else used.

**Story structures, not results to borrow.** Swap each scenario for work you actually did and
numbers you can defend. Keep the task, mistake or tradeoff, evidence, change and outcome.

1. **Wrong numbers.** "My delivery model used a final-status field that only arrived after the
   decision. I removed it, rebuilt decision-time features, and evaluated on a later period with
   mature labels. Here are the original and corrected scores, sample sizes and release test."
2. **Simpler on purpose.** "I compared retrieval with fine-tuning on the same held-out questions.
   The paired comparison did not show a meaningful improvement at a cost we could support. I chose
   retrieval and documented the remaining errors and the evidence that would change my mind."
3. **Someone else used it.** "A team used my triage tool for a defined pilot. I recorded eligible
   cases, usage and failures. I fixed one failure class and tested the change on a separate release
   set. Here is the measured scope of the pilot and the reproducible evaluation."

A result on 50 examples is a useful first signal, not a precise population guarantee. One extra pass
moves the rate by two percentage points. Show paired disagreement counts or a suitable interval.
Keep pilot adoption separate from evidence that your change caused a business improvement.

## The search itself

Run it as a process. Track applications and three conversion rates: applications to screens, screens
to onsites, onsites to offers. Calculate each rate from resolved stage transitions, show the
denominators, and keep pending decisions separate. Compare cohorts with a similar time to resolve.
Different response delays can change resolved-only rates without any real improvement. Use each
stage to find a question to investigate before choosing more preparation.

**A tracker you can actually use.** One spreadsheet or markdown file, updated weekly:

| Date       | Company    | Role        | Source (referral / community / cold) | Stage  | Outcome | Notes                              |
| ---------- | ---------- | ----------- | ------------------------------------ | ------ | ------- | ---------------------------------- |
| 2026-09-01 | Example Co | AI Engineer | Referral from blog post              | Screen | Waiting | Sent portfolio link to RAG project |

If few applications become screens, review role fit, eligibility, CV and portfolio signals. If few
screens or onsites move forward, ask for feedback on the actual rounds, including coding, SQL,
design and communication where assessed. Review level or pay expectations when those were a stated
obstacle. A funnel rate alone cannot identify the cause.

Before weeks of preparation, review a few current postings for your target city and level. Record
the date, actual responsibilities, required skills, interview format if known, and which project
supplies evidence. Revisit this monthly. Titles alone can mislead. An "AI Engineer" role can mean
product integration, retrieval, modelling, infrastructure or research.

| Posting requirement                   | Evidence to prepare                                                  | Gap to close                                                         |
| ------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Offer, pricing or retention modelling | Chapter 9 decision brief, realistic validation and experiment design | Explain prediction versus intervention, support and net contribution |
| LLM application engineering           | Chapter 5 held-out evaluation, failure analysis and access controls  | Explain retrieval, tool reliability and cost/quality tradeoffs       |
| ML platform or backend engineering    | Chapter 6 release, monitoring and rollback exercise                  | Explain compatibility, freshness, retries and operational ownership  |

Track referrals, community contacts and targeted applications separately, and use your own funnel to
decide where to spend time. Small counts jump around, and a low response rate can reflect fit,
location, timing or application quality. Change one thing, then review a new batch. One rejection is
no reason to redesign your whole portfolio.

Consider nearby roles that match your experience: data engineering, backend work on an AI product,
contract projects or an internal transfer. Check the actual mentorship, work and transfer policy,
because a backend offer does not promise a move into ML within a year. Employers outside technology
may also have relevant tabular and document projects.

On pay, compare your level, location and pay components.
[Indeed's September 2026 US analysis](https://hiringlab.indeed.com/2026/09/17/ai-exposure-isnt-squeezing-advertised-pay-in-the-us-its-boosting-it/)
finds seniority affects advertised-pay comparisons, though its seniority-specific evidence is only
suggestive. It studies US postings with an advertised salary, not individual offers or Indian
salaries. Self-reported pay trackers and aggregate AI wage premiums cannot predict your offer. Check
current local ranges, and separate base pay, equity, bonuses and contract terms.

## Staying current afterwards

Split your attention. The fast layer turns over in a year or two: model names, frameworks, pricing,
free tiers and specification versions. The slow layer will still be true in a decade: attention,
backpropagation, evaluation design, generalisation, retrieval, cost and latency, statistics and SQL.
Spend your study time on the slow layer and simply **monitor** the fast one. A couple of hours a
week on a few named, human-written sources is plenty.

Once a quarter, spend ninety minutes checking whether anything you depend on has changed price, been
deprecated or moved. **Re-run your evaluations before adopting a model version change.** Rolling
model aliases can change without a code change. Record the resolved version, and investigate
unexpected regressions with your evaluation suite.

## Resources

All 12 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [AI Engineer Compensation Trends (Q3 2025)](https://www.levels.fyi/blog/ai-engineer-compensation-trends-q3-2025.html)
  — Alina Kolesnikova, levels.fyi. A free article, under an hour, for setting pay expectations by
  level.
- [How to Interview and Hire ML/AI Engineers](https://eugeneyan.com/writing/how-to-interview/) —
  Eugene Yan and Jason Liu. A hiring-side account to help turn your projects into interview
  evidence.
- [normcore-llm-reads](https://gist.github.com/veekaybee/be375ab33085102f9027853128dc5f0e) — Vicki
  Boykis. A free curated reading list for staying current without the noise.
- [State of AI Report 2026](https://www.stateof.ai/) — Nathan Benaich and Air Street Capital. An
  annual industry overview. Follow its primary sources, and check real openings before choosing a
  sector.

## Before you move on

- Your project case studies follow the outline above, including "what did not work."
- You have said each of the three interview stories out loud at least twice.
- Your tracker separates pending from resolved outcomes and records dates, role, location and
  channel. With small counts, describe the uncertainty and ask for specific feedback, rather than
  declaring one funnel stage definitely weakest.
- You have checked pay expectations at **your** level and city, not the headline average.

---

[Previous: Choosing a specialisation](../07-specialisation/README.md) &nbsp;·&nbsp;
[Next: Business machine learning](../09-business-machine-learning/README.md) &nbsp;·&nbsp;
[Back to the index](../README.md)
