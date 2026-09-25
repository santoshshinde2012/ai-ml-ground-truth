# Chapter 8: Finding the work

**Week 33 onward &nbsp;·&nbsp; runs alongside chapters 6 and 7.** &nbsp;·&nbsp; [Index](../README.md) &nbsp;·&nbsp; [Resources for this chapter](resources/README.md)

**The short version.** The search is a process you run, not a verdict on you: present three deep projects well, practise the interview stories out loud, track your numbers, and use the doors that are actually open. This chapter runs alongside the last two, because it takes months and starting early teaches you what the market wants.

---

## Your first month (alongside Chapters 6-7)

About three to four hours a week on the search, while you keep building. This is not full-time job hunting yet.

| Week (from Ch 6 start) | Focus | Do this | Done when |
|---|---|---|---|
| 1 | Portfolio hygiene | Archive tutorial forks; README template on best project | One README has all six sections |
| 2 | Stories | Write out three 90-second stories; say them twice | Timer ≤ 90s each |
| 3 | Tracker | Start spreadsheet; log every application; compute one conversion rate | 5+ rows |
| 4 | Visibility | One short write-up post; share in one community (not spam) | Link you can send recruiters |

After month one: keep logging applications weekly; refresh README when metrics move; do not wait until Chapter 7 finishes to start.

---

## What you will be able to do

Present three projects so that a reviewer understands them in two minutes, tell three interview
stories out loud without notes, and run a search you can measure and adjust rather than endure.

## Presenting your work

A reviewer gives a profile a minute or two. A few things help more than they should:

- **Archive the tutorial forks.** A weak repository sits next to your strong one and gets opened
  too. Three good projects beat ten thin ones, comfortably.
- **The README carries most of the weight,** because most reviewers never run the code. State the
  question, the result with a number, the architecture, the key decisions, what did not work, and
  the known failures. Those last two sections are unusual and they build trust quickly.
- **Deploy something.** A URL a stranger can click is worth a lot more than a description.
- **Write things up.** One short post per major topic, explaining it plainly. It is good revision,
  and it is how people find you.

**A README outline that works.** Copy this into each project and fill in the blanks:

```markdown
# [Project name]

## Question
One sentence: what did you try to answer?

## Result
One sentence with a number. Example: "Pass rate went from 41% to 67% after fixing retrieval."

## How it works
Three to five sentences, or a simple diagram. Link a live URL if you have one.

## Key decisions
Two or three bullets: what you chose and what you rejected.

## What did not work
One or two honest failures. This section builds trust.

## Known limitations
What the system should not be used for.
```

On open source: it is a genuinely good path and slower than the internet suggests. The open-source
entries in [Chapter 7's resources](../07-specialisation/resources/README.md) cover the mechanics and
the honest odds. The tactic that works best is to contribute the fix for a bug you hit while
building your own project. Projects have also started setting rules for AI help: scikit-learn asks
you to say when you used AI tools, and Hugging Face Transformers may close agent-written pull
requests without review. Write and understand your first contribution yourself.

## The interview loop

A recruiter screen, a technical screen, sometimes a take-home, then four to six rounds mixing coding,
machine learning fundamentals, a systems design round and behavioural conversations. Two current
notes: the coding bar in ML loops has risen close to general software engineering, and some companies
now build an AI assistant into the coding round. Meta, for one, says on its hiring page that candidates
are expected to use it. Practise reading, debugging and extending existing code with an assistant, and
explaining what you accepted and why.

Have three stories ready and practise them out loud, at ninety seconds each:

1. A time your numbers were wrong and you found out. The leakage exercise is built for this.
2. A time you chose the simpler option deliberately, with the numbers behind it.
3. A time you shipped something someone else used.

**Sample scripts at ninety seconds each.** Adapt the details; keep the structure.

1. **Wrong numbers.** "I was building a classifier on delivery data and validation accuracy looked
   great — 0.91. When I checked leakage, I had fit the scaler on the full dataset before splitting.
   Inside a Pipeline the honest score was 0.78. I wrote up the gap and added a data test so it
   cannot happen again."
2. **Simpler on purpose.** "I could have fine-tuned a 7B model. I tried prompt + retrieval first,
   measured on fifty labelled examples, and got to 84% pass rate. Fine-tuning bought two points at
   ten times the ops cost. I shipped the simpler stack and documented the comparison."
3. **Someone else used it.** "I built a triage tool for our support queue — one screen, one metric.
   Three teammates used it for two weeks. I logged every failure, fixed the top one, and the
   pass rate moved from 52% to 71%. Here is the public URL and the eval suite."

## The search itself

Run it as a process. Track applications, and watch three conversion rates: applications to screens,
screens to onsites, onsites to offers. Most people never look at these and spend months improving
the wrong thing.

**A tracker you can actually use.** One spreadsheet or markdown file; update it weekly:

| Date | Company | Role | Source (referral / community / cold) | Stage | Outcome | Notes |
|---|---|---|---|---|---|---|
| 2026-09-01 | Example Co | AI Engineer | Referral from blog post | Screen | Waiting | Sent portfolio link to RAG project |

Each rate points at a different fix. If screens are near zero, improve the README and the top
project first. If onsites stall, practise the stories and system design out loud. If offers stall,
calibrate level and pay expectations against current sources.

Where the leads come from matters as much as how many you send. Roughly in order of how well
they work: people who have seen your work; communities you are part of;
referrals; targeted applications; and cold applications at volume.

Consider the adjacent doors too. They are not consolation prizes. **Data engineering** hires steadily
at junior level. **A backend role at a company doing AI work** lets you move internally within a
year, and is one of the most reliable routes in. **Contract work** has faster decisions and compounds
into references. **An internal transfer** is usually the cheapest AI role you will ever get.
**Non-technology companies** need exactly the tabular and document work in this book and compete
with fewer candidates.

On pay: published averages skew high, because they are self-reported and weighted towards large
technology employers. The premium for AI skills sits mostly at senior levels and is smaller at entry
level than headlines suggest. Anchoring on a headline figure is a quick way to be disappointed by
every offer you actually receive. Compensation is also the fastest-decaying information here, so
check current sources.

## Staying current afterwards

Split your attention. The fast layer, which turns over in a year or two, is model names, frameworks,
pricing, free tiers and specification versions. The slow layer, which is still true in a decade, is
attention, backpropagation, evaluation design, generalisation, retrieval, cost and latency,
statistics and SQL. Spend your study time on the slow layer and merely **monitor** the fast one; a
couple of hours a week on a small number of named, human-written sources is plenty.

Once a quarter, spend ninety minutes checking whether anything you depend on has changed price, been
deprecated or moved, and **re-run your evaluations against the current model version**. Providers
update models underneath you, and your evaluation suite is what tells you.

## Resources

All 11 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [AI Engineer Compensation Trends (Q3 2025)](https://www.levels.fyi/blog/ai-engineer-compensation-trends-q3-2025.html) — Alina Kolesnikova, levels.fyi. A free article, under an hour, for calibrating pay expectations by level.
- [Machine Learning Interview Prep Guide (2026)](https://www.tryexponent.com/blog/machine-learning-interview-guide) — Exponent team. A free article, 3 hours, as a map of the interview loop; ignore the product pitch.
- [normcore-llm-reads](https://gist.github.com/veekaybee/be375ab33085102f9027853128dc5f0e) — Vicki Boykis. A free curated reading list for staying current without the noise.
- [State of AI Report 2025](https://www.stateof.ai/) — Nathan Benaich. A free annual report, 3 hours, for choosing which sectors to target.

## Before you move on

- Three projects have READMEs that follow the outline above, including "what did not work."
- You have said each of the three interview stories out loud at least twice.
- Your tracker has at least ten rows and you know which conversion rate is weakest.
- You have checked pay expectations at **your** level and city, not the headline average.

---

[Previous: Choosing a specialisation](../07-specialisation/README.md) &nbsp;·&nbsp; [Back to the index](../README.md)
