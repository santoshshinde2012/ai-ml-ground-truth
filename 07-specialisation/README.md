# Chapter 7: Choosing a specialisation

**Weeks 38–43 &nbsp;·&nbsp; about 70 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** The shared path ends here. Pick one of three roles: AI Engineer, ML Engineer
or Data Scientist. Spend about forty hours going deeper and thirty on a capstone matched to that
role's interviews. One branch done well beats three sampled.

**Extend the same thread.** Build your capstone on the dataset, model or LLM app from Chapters 2–6,
not a new tutorial project. One connected story beats three unrelated repos.

**In this chapter:** [AI Engineer](#branch-a--ai-engineer) &nbsp;·&nbsp;
[ML Engineer](#branch-b--ml-engineer) &nbsp;·&nbsp; [Data Scientist](#branch-c--data-scientist)
&nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp; [Resources](#resources)

---

Plan about 40 hours of depth and 30 on the capstone, and budget the capstone first. It is the point
of this chapter, so fit the depth work around it.

Do one branch. The shared path you have finished keeps the other two open for later.

You do not need to master every topic below. Think in three levels of depth:

| Branch | Build in your capstone | Explain using your results | Recognise, and defer unless needed |
| --- | --- | --- | --- |
| AI Engineer | One scoped workflow, a checked tool boundary and an independent evaluation | A failure taxonomy, judge limits, recovery and running cost | Multi-agent coordination or advanced memory, unless you have measured a need |
| ML Engineer | One reproducible data/model/serving path with a load test and rollback | Bottlenecks, feature consistency and release artifacts that work together | Distributed training, custom kernels and post-training beyond the chosen project |
| Data Scientist | One randomised analysis or a well-argued observational design, with uncertainty and a decision memo | Assignment, estimand, missing outcomes, sensitivity and limits | The full catalogue of causal estimators. Choose the design first, then its estimator |

These hours assume the project and environment from earlier chapters. Record your actual time, and
shrink the capstone if integration or getting data eats the budget. The goal is one finished system,
not familiarity with every research direction listed.

[Chapter 8: Finding the work](../08-finding-the-work/README.md) should already be running alongside
this chapter. If it is not, start it today.

**For offer, pricing or churn work, use [Chapter 9](../09-business-machine-learning/README.md) as
your applied track.** Its shared delivery work plus one guide is about 40 hours. Use the 30 capstone
hours here for a small prototype, then about ten more for the remaining shared checks. ML Engineers
should stress data, serving and feedback. Data Scientists should stress identification, experiment
design and the decision memo. Both need the basic experiment checks before recommending an
intervention.

## What you will be able to do

Go deep on one role, finish a capstone that matches its interviews, and explain in writing why you
did not sample the other two.

## Branch A — AI Engineer

**Go deeper on four things.**

- **Agent harnesses.** State, tool contracts, durable execution, limited retries and verification.
  Add sub-agents or memory when a measured task needs them. Make external actions idempotent (safe
  to repeat), and put human review at the decisions that need it.
- **Evaluation as a speciality.** Judge the whole trajectory as well as the final answer. Check
  tool-call correctness and multi-turn behaviour, and keep a judge calibrated over time.
- **Reliability and safety.** Prompt injection (hostile instructions hidden in content the model
  reads), privilege boundaries, escalation, rate limits and per-user cost caps. Test allowed and
  forbidden actions together. A system that refuses every task avoids execution mistakes but fails
  the product goal.
- **The product layer.** Design for a component that is sometimes wrong, and capture user feedback
  that feeds your evaluation set.

For depth, apply the strongest [Chapter 5](../05-language-models/resources/README.md) and
[Chapter 6](../06-production/resources/README.md) resources to your capstone, within the depth
budget. Read the Anthropic engineering blog's agent sequence end to end, then
[12-Factor Agents](https://github.com/humanlayer/12-factor-agents). Apply Husain and Shankar's evals
material to your own traces. Add the dated research and official security guidance from this
chapter's resource list. Recommending these sources is not a claim that any agent framework
guarantees reliability.

The ICML 2026 paper
[Towards a Science of AI Agent Reliability](https://proceedings.mlr.press/v306/rabanser26a.html)
organises reliability around consistency, robustness, predictability and safety. Its
[arXiv version](https://arxiv.org/abs/2602.16666) was submitted 18 February and revised 2 June 2026.
For your capstone, repeat typical tasks, perturb inputs, test escalation and permissions, and
measure recovery after tool failures. Report completion, action errors, latency and cost together.
Record harness, model and evaluator versions, because the same final answer can hide a very
different sequence of tool actions. Use the
[OWASP LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/), published 3
August 2026, to choose relevant attack cases. A risk checklist alone does not show that your defence
works.

**Capstone, pick one:**

- A reproducible evaluation of one important failure mode.
- An agentic system with trajectory evaluation and a small user pilot.
- An open-source tool or contribution, with a reproduced problem and documented validation. Start
  from a bug or gap you hit in a library your Chapter 5–6 app uses, and show the change working in
  that app.

Keep the work to 30 hours. Record real pilot feedback when available. Adoption, novelty and a
maintainer's merge decision are separate outcomes.

**Interview preparation:** practise an AI systems design discussion, then confirm each employer's
rounds and tool rules using [Chapter 8](../08-finding-the-work/README.md). Good practice prompts: a
triage system for ten thousand tickets a day, showing it works, halving its cost, recovering from a
high error rate, and whether the task needs an agent. Use your artifacts to support the tradeoffs.
These prompts are practice. Real formats vary.

**A simple six-week plan** (about 12 hours a week):

| Week | Depth (about 7 h)                                                                                                   | Capstone (about 5 h)                                                              |
| ---- | ------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| 1    | Re-read [Chapter 5](../05-language-models/resources/README.md) eval resources; instrument one live trace end to end | Pick capstone; write README with success metric                                   |
| 2    | Anthropic agent sequence + [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)                       | Ship rough version; collect and label a small diverse trace sample                |
| 3    | Reliability paper and eval material applied to your traces                                                          | Check trajectory scorer against human labels; repeat tasks and report uncertainty |
| 4    | Relevant injection cases from OWASP 2026; least-privilege tools                                                     | Test permissions, idempotency and recovery; fix top failure mode and re-measure   |
| 5    | Cost and latency table from [Chapter 6](../06-production/README.md)                                                 | Harden deploy; add kill switch                                                    |
| 6    | Write interview stories from the capstone                                                                           | Polish README; publish write-up                                                   |

## Branch B — ML Engineer

**Go deeper on four things.**

- **The data layer.** Orchestration, warehouse modelling, data quality tests, and point-in-time
  correctness at scale.
- **Training at scale.** Data and model parallelism, mixed precision, gradient accumulation and
  checkpointing, profiling, and scaling laws.
- **Serving and inference optimisation.** Quantisation stores numbers at lower precision and can
  save memory. Any speed-up depends on the supported kernels and the workload, so compare quality
  and latency before adopting it. Also learn distillation, compilation, batching strategies and
  management of the KV cache, the memory a model keeps of tokens it has already processed.
- **Post-training.** Supervised fine-tuning, preference optimisation, and reinforcement learning
  from verifiable rewards.

Before spending the 70 hours, choose a **production path** or a **language-model implementation
path**. The default production path below spends about 40 hours on selected systems readings and 30
on one capstone, with no from-scratch language model.

For the alternative, [CS336 Spring 2026](https://cs336.stanford.edu/) has public materials and five
assignments covering basics, systems, scaling, data and alignment/reasoning. It assumes strong
programming, deep learning and maths. Plan about ten hours of selected lectures, fifty for
Assignment 1, and ten for tests, profiling and documentation. **That assignment replaces the
production capstone and its depth work.** It also steps off the project thread, which is fine when
model implementation is your target role. Your Chapter 2–6 project stays your portfolio's production
story. These are planning estimates, so allow more time if correctness needs it. The full graduate
course is beyond this chapter's budget. See **Branch B — ML Engineer depth** in
[resources/](resources/README.md).

For efficient training, use the official FSDP2, AMP and compiler guides for your pinned framework
version. Explain the memory and communication tradeoff of sharding before renting several GPUs. Read
the MLSys 2026
[FlashAttention-4 paper](https://proceedings.mlsys.org/paper_files/paper/2026/hash/ae8b0b5838ba510daff1198474e7b984-Abstract-Conference.html)
on hardware-aware attention kernels, alongside its
[March arXiv version](https://arxiv.org/abs/2603.05451). Its results are hardware-specific, so test
them on your own workload. For adaptation, compare a no-training baseline with one well-chosen SFT
or adapter run. Keep demonstrations, preference data and verifiable rewards separate, hold out a
task evaluation, and include memory and serving cost. A good fine-tuning loss does not show that the
product task improved.

**Capstone, pick one:**

- An end-to-end training and serving system with a documented retraining trigger. Keep the model
  simple on purpose, since the system is what is assessed.
- A paper reproduction with a frank account of where your numbers differ. Pick a method that applies
  to your Chapter 3–4 model, and finish by running it on your own dataset.
- One from-scratch language-model stage, done to course standard.

**Interview preparation:** rehearse a 45-minute machine learning systems design discussion covering
data, training, evaluation, serving and monitoring. The length is for practice. Formats vary, and
some employers also test coding or statistics. Explain a simple starting design and what results
would justify more complexity, then adapt to the real round.

**A six-week production plan** (about 12 hours a week). If the implementation path is your capstone,
use the CS336 hours above instead:

| Week | Depth (about 7 h)                                                    | Capstone (about 5 h)                                                     |
| ---- | -------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| 1    | Data contracts, immutable snapshots and point-in-time joins          | Pick capstone; pin data, splits, environment and release manifest        |
| 2    | Profile training; selected AMP/compile/FSDP2 material                | Baseline trains and resumes from a full checkpoint                       |
| 3    | One justified precision, adapter or model experiment                 | Report quality, memory and runtime against the baseline                  |
| 4    | [Chapter 6](../06-production/resources/README.md) serving benchmarks | Batch or API release; measure load, latency and cost per successful task |
| 5    | Mature-label feedback and challenger promotion gates                 | Inject stale data or a serving failure; rehearse compatible rollback     |
| 6    | Re-read one systems-design interview guide                           | README + honest numbers; rehearse 45-min design                          |

## Branch C — Data Scientist

**Go deeper on four things.**

- **Experimentation.** Estimands, randomisation units, power and minimum detectable effect before
  you run, sample-ratio mismatch, multiple comparisons, novelty and carryover, interference in
  marketplaces, variance reduction and guardrail metrics. Repeated observations from one user are
  not independent experimental units.
- **Causal inference.** Potential outcomes, confounders and colliders, difference-in-differences,
  instrumental variables, regression discontinuity, matching, and sensitivity analysis.
- **The classical statistics** the book deliberately left for later.
- **Communication.** Turn a metric, its uncertainty and its limitations into a clear decision memo.

In applied work, separate prediction from treatment effects before choosing a causal method.
[Chapter 9](../09-business-machine-learning/README.md) adds primary research, identification
assumptions and a shared experiment protocol for the three business cases. The annotated list is in
[resources/](resources/README.md) under **Branch C — Data Scientist depth**: Kohavi, Tang and Xu on
trustworthy online experiments (companion site at experimentguide.com), and two books free online,
Cunningham's _Causal Inference: The Remix_ and Huntington-Klein's _The Effect_.

For each experiment, write down in advance who is eligible, the unit randomised, treatment and
control, assignment logging, the outcome window, the intended estimand and the stopping rule.
Analyse by assignment for an intent-to-treat effect. Dropping failed deliveries or non-responders
after assignment can break the comparison. Reconcile assignment, exposure and outcomes, and look
into any sample-ratio mismatch before reading a lift. Match the uncertainty to clustered or repeated
units. Use a fixed analysis horizon or a well-founded sequential method. Checking ordinary p-values
repeatedly and stopping when one crosses 0.05 changes the error rate.

Include one variance-reduction experiment in the depth work. Compare unadjusted estimates with
CUPED, using only covariates the treatment cannot affect. Then run simulated A/A tests to check
interval coverage.
[Ensuring Trustworthy Online A/B Testing: Addressing Five Key Questions on CUPED](https://arxiv.org/abs/2606.18750),
a preprint submitted 17 June 2026, examines choices of adjustment and variance estimation, including
multi-arm and two-stage sampling. It is recent method research, not a promise that any adjustment
makes every business experiment more precise.

For observational work, state the identification argument before choosing an estimator.
Difference-in-differences needs a credible comparison and trend assumptions. Instruments need
relevance and exclusion. Regression discontinuity needs a cutoff design you can defend. An uplift
model, a doubly robust learner or a flexible predictor cannot supply missing randomisation, overlap
or control of unmeasured confounding. Use sensitivity checks that suit the design, and write down
what remains unidentifiable. Chapter 9 connects these choices to offer, price and retention actions.

**Capstone, pick one:**

- An experiment analysis with a well-supported causal claim and sensitivity checks.
- A metric system for a real product, with a decision memo.
- A data engineering project on your Chapter 2 sources and snapshots, showing validated SQL, lineage
  and reliable metric delivery.

Choose the one closest to your target role's actual work.

If you have no randomised data of your own, run the [reference lab](../labs/README.md). It writes a
simulated experiment to `data/assignments.csv` and `data/experiment_outcomes.csv` in its output
directory, with assignment probabilities and failed deliveries kept in their assigned arm. Practise
the intent-to-treat analysis, sample-ratio check and uncertainty there, and label the result as
simulated.

**Interview preparation:** practise live SQL, statistics, product reasoning and experiment design,
putting the target employer's actual rounds first. Pair a dashboard with a memo that links its
metrics, uncertainty and limitations to a decision.

**A simple six-week plan** (about 12 hours a week):

| Week | Depth (about 7 h)                                                                            | Capstone (about 5 h)                                                                 |
| ---- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| 1    | Experiment companion materials; estimand, power and stopping rule                            | Pick capstone question; declare design and one-page memo outline                     |
| 2    | _The Remix_ or _The Effect_ Part 1 — identification and diagrams                             | SQL + point-in-time query for your dataset                                           |
| 3    | Assignment/exposure checks, clustering and A/A coverage; selected CUPED research             | First analysis draft; distinguish randomised evidence from observational assumptions |
| 4    | Sensitivity analysis and overlap or design diagnostics relevant to your claim                | Revise memo; report uncertainty, guardrails and a decision boundary                  |
| 5    | [Chapter 2](../02-data-foundations/README.md) SQL drills or DataLemur if interviews are near | Practise live SQL screen out loud                                                    |
| 6    | Rehearse experimentation and product-sense cases                                             | Publish memo or experiment write-up; link from portfolio                             |

## Resources

The annotated resources are in **[resources/](resources/README.md)**, grouped by branch. Hours for
full books and courses are alternatives, not additions to the 70-hour plan.

The ones to begin with depend on the branch you chose:

- **Branch A.** The relevant sections of the "Start here" lists in
  [Chapter 5](../05-language-models/resources/README.md) and
  [Chapter 6](../06-production/resources/README.md), then
  [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) by Dex Horthy (free, 3–5
  hours). For the security week, the
  [OWASP Top 10 for LLM Applications](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
  from the OWASP GenAI Security Project (free, 3–4 hours).
- **Branch B.** For the default production path, the training, data and serving guides in the branch
  resource list. For the alternative implementation capstone,
  [Stanford CS336](https://cs336.stanford.edu/).
- **Branch C.**
  [Trustworthy Online Controlled Experiments (companion site)](https://www.experimentguide.com/) by
  Ron Kohavi, Diane Tang & Ya Xu: free companion materials to a paid book. Plan 6–10 hours of
  selected reading here, or 20–30 for the full book. Then [The Effect](https://theeffectbook.net/)
  by Nicholas Huntington-Klein, a free book: 6–10 hours of selected reading here, or 25–40 for the
  whole book.
- **Any branch.** The
  [Kaggle Playground Series](https://www.kaggle.com/competitions?searchQuery=playground+series) from
  the Kaggle competitions team is free validation-design practice between capstone sessions, 10–25
  hours per entry.

## Before you move on

- You finished **one** branch's capstone, not three half-started ones.
- Your README states the metric, the result with a number, and what the system should not be used
  for.
- You can defend your capstone choice in one minute without mentioning salary.
- For Branch A: you can show repeated-task results, a permission-boundary test and recovery from a
  failed tool call, with the cost of successful completion.
- For Branch B's production path: your release links data, model and serving configuration. Load and
  checkpoint/rollback checks support your claims. For the CS336 alternative, the completion evidence
  is correctness tests, checkpoint resume, profiling and the documented implementation.
- For Branch C: the decision memo states the estimand, assignment or design checks, uncertainty and
  the limits of the causal claim. It separates the hypothesis set in advance from the observed
  result, includes a relevant sensitivity or robustness check, and labels synthetic data or a
  simulation as such.

---

[Previous: Running it in production](../06-production/README.md) &nbsp;·&nbsp;
[Next: Finding the work](../08-finding-the-work/README.md)
