# Chapter 7: Choosing a specialisation

**Weeks 38-43 &nbsp;·&nbsp; about 70 hours.** &nbsp;·&nbsp; [Index](../README.md) &nbsp;·&nbsp; [Resources for this chapter](resources/README.md)

**The short version.** The shared path ends here. You pick one of three roles — AI Engineer, ML Engineer, or Data Scientist — spend about forty hours going deeper, and thirty building a capstone matched to that role's interviews. One branch done well beats three sampled.

**Extend the same thread.** Your capstone should build on the dataset, model, or LLM app from Chapters 2-6 — not a new tutorial project. One coherent story beats three unrelated repos.

---

Plan roughly 40 hours of depth and 30 on the capstone — and budget the capstone first. It is the
point of this chapter, and the depth sections should be cut to fit around it, not the other way
round.

Do one branch. The shared path you have finished is what makes the other two accessible later.

[Chapter 8: Finding the work](../08-finding-the-work/README.md) should already be running alongside
this chapter. If it is not open yet, open it today.

## What you will be able to do

Go deep on one role, finish a capstone that matches its interviews, and explain in writing why you
did not sample the other two.

## Branch A — AI Engineer

**Go deeper on four things.**

- **Agent harnesses.** Sub-agents, memory, verification loops, durable execution, and
  human-in-the-loop gates.
- **Evaluation as a speciality.** Judging the whole trajectory, not just the final answer;
  tool-call correctness; multi-turn evaluation; keeping a judge calibrated over time.
- **Reliability and safety.** Guardrails; prompt injection — hostile instructions hidden in
  content the model reads — and why it is unsolved; least privilege for tools; rate limits and
  per-user cost caps.
- **The product layer.** Designing for a component that is sometimes wrong, and capturing user
  feedback that feeds your evaluation set.

The depth material is a deliberate return to the strongest of the [Chapter 5](../05-language-models/resources/README.md)
and [Chapter 6](../06-production/resources/README.md) resources, read fully this time: the Anthropic
engineering blog's agent sequence end to end, [12-Factor Agents](https://github.com/humanlayer/12-factor-agents),
and Husain and Shankar's evals course applied to your own traces. There is no CS336 equivalent for
this branch yet; its depth lives in the engineering literature and in systems you instrument yourself.

**Capstone, pick one:** a rigorous public evaluation of something the field has not measured well; an
agentic system with trajectory evaluation and real users; or an open-source tool other people come to
depend on.

**Interviews** centre on an AI systems design round. Expect: design a triage system for ten thousand
tickets a day; how do you know it works; it is too expensive, halve it; it is wrong twenty per cent
of the time, what now; and would you use an agent here. Three of those five are answered by artefacts
you already have.

**A simple six-week plan** (about 12 hours a week):

| Week | Depth (about 7 h) | Capstone (about 5 h) |
|---|---|---|
| 1 | Re-read [Chapter 5](../05-language-models/resources/README.md) eval resources; instrument one live trace end to end | Pick capstone; write README with success metric |
| 2 | Anthropic agent sequence + [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) | Ship roughest version; collect 50 traces |
| 3 | Husain and Shankar evals course applied to your traces | Build trajectory judge; check against your labels |
| 4 | Guardrails, injection cases, least-privilege tools | Fix top failure mode; re-measure |
| 5 | Cost and latency table from [Chapter 6](../06-production/README.md) | Harden deploy; add kill switch |
| 6 | Write interview stories from the capstone | Polish README; publish write-up |

## Branch B — ML Engineer

**Go deeper on four things.**

- **The data layer.** Orchestration, warehouse modelling, data quality tests, and point-in-time
  correctness at scale.
- **Training at scale.** Data and model parallelism, mixed precision, gradient accumulation and
  checkpointing, profiling, and scaling laws.
- **Serving and inference optimisation.** Quantisation — storing weights in lower precision to
  shrink and speed up a model — plus distillation, compilation, batching strategies, and managing
  the KV cache, the memory a model keeps of the tokens it has already processed.
- **Post-training.** Supervised fine-tuning, preference optimisation, and reinforcement learning
  from verifiable rewards.

[Stanford's CS336](https://cs336.stanford.edu/) is the rigorous free path here — see the full
annotated entry under **Branch B — ML Engineer depth** in [resources/](resources/README.md). It is a
graduate systems course rather than an introduction. For six weeks, watch four lectures and do
**Assignment 1 only**, timeboxed at forty to sixty hours, treating it as your capstone. The rest is
a second-year project.

**Capstone, pick one:** an end-to-end training and serving system with a documented retraining
trigger, keeping the model deliberately simple because the system is what is being assessed; a paper
reproduction with an honest account of where your numbers differ; or one from-scratch
language-model stage done to course standard.

**Interviews** centre on a machine learning systems design round covering data, training, evaluation,
serving and monitoring in forty-five minutes. Proposing the simple thing and saying what evidence
would justify escalating is usually the strongest move available.

**A simple six-week plan** (about 12 hours a week):

| Week | Depth (about 7 h) | Capstone (about 5 h) |
|---|---|---|
| 1 | CS336 lectures 1-2; set up assignment repo | Pick capstone; pin data and config versions |
| 2 | CS336 lectures 3-4; start Assignment 1 | Training loop running on small subset |
| 3 | Finish Assignment 1; profile one bottleneck | Document what you measured and changed |
| 4 | [Chapter 6](../06-production/resources/README.md) serving + vLLM docs | Serve the checkpoint; log latency |
| 5 | Retraining trigger doc; cost table | Break something on purpose; write rollback steps |
| 6 | Re-read one systems-design interview guide | README + honest numbers; rehearse 45-min design |

## Branch C — Data Scientist

**Go deeper on four things.**

- **Experimentation.** Randomisation units, power calculations before you run, the peeking
  problem, multiple comparisons, novelty effects, interference in marketplaces, variance
  reduction, and guardrail metrics.
- **Causal inference.** Potential outcomes, confounders and colliders, difference-in-differences,
  instrumental variables, regression discontinuity, matching, and sensitivity analysis.
- **The classical statistics** deliberately deferred earlier in the book.
- **Communication** — the highest-leverage and least-taught part of the role.

One honest caveat: **experimentation and causal inference use references that sit outside the rest
of this book's heaviest curation**, so vet whatever you pick with particular care. The annotated
list is in [resources/](resources/README.md) under **Branch C — Data Scientist depth**: Kohavi,
Tang and Xu on trustworthy online experiments (companion site at experimentguide.com), Cunningham's
*Causal Inference: The Mixtape*, and Huntington-Klein's *The Effect*, both free online.

**Capstone, pick one:** a full experiment analysis with a causal claim and a sensitivity analysis; a
metric system for a real product, with a decision memo; or a data engineering project with no machine
learning in it at all, which is a surprisingly strong and under-used signal.

**Interviews** include a live SQL screen, statistics, a product-sense case and an experimentation
case. A dashboard makes a weak capstone; a memo that leads to a decision makes a strong one.

**A simple six-week plan** (about 12 hours a week):

| Week | Depth (about 7 h) | Capstone (about 5 h) |
|---|---|---|
| 1 | [experimentguide.com](https://www.experimentguide.com/) companion materials; power and peeking | Pick capstone question; write one-page memo outline |
| 2 | *Mixtape* or *The Effect* Part 1 — identification and diagrams | SQL + point-in-time query for your dataset |
| 3 | Continue causal text; one method applied to a public dataset | First analysis draft with explicit limitations |
| 4 | Sensitivity analysis on your main claim | Revise memo; cut every chart that does not move a decision |
| 5 | [Chapter 2](../02-data-foundations/README.md) SQL drills or DataLemur if interviews are near | Practise live SQL screen out loud |
| 6 | Rehearse experimentation and product-sense cases | Publish memo or experiment write-up; link from portfolio |

## Resources

All 14 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**,
grouped by branch.

The ones to begin with depend on the branch you chose:

- **Branch A** — re-read the "Start here" lists of [Chapter 5](../05-language-models/resources/README.md) and [Chapter 6](../06-production/resources/README.md) in full, then [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) — Dex Horthy. Free, 3-5 hours.
- **Branch B** — [Stanford CS336: Language Modelling from Scratch](https://cs336.stanford.edu/) — Percy Liang & Tatsunori Hashimoto. A free course; 40-60 hours for Assignment 1 alone.
- **Branch C** — [Trustworthy Online Controlled Experiments (companion site)](https://www.experimentguide.com/) — Ron Kohavi, Diane Tang & Ya Xu. Free companion materials to a paid book, 20-30 hours. Then [The Effect](https://theeffectbook.net/) — Nicholas Huntington-Klein. A free book, 25-40 hours.
- **Any branch** — [Kaggle Playground Series](https://www.kaggle.com/competitions?searchQuery=playground+series) — Kaggle competitions team. A free practice ground, 10-25 hours per entry, for validation-design reps between capstone sessions.

## Before you move on

- You finished **one** branch's capstone, not three half-started ones.
- Your README states the metric, the result with a number, and what the system should not be used for.
- You can defend your capstone choice in one minute without mentioning salary.
- For Branch C: your write-up includes at least one thing that did not support your initial hypothesis.

---

[Previous: Running it in production](../06-production/README.md) &nbsp;·&nbsp; [Next: Finding the work](../08-finding-the-work/README.md)
