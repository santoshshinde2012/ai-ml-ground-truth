# Chapter 7: Choosing a specialisation

**Weeks 38–43 &nbsp;·&nbsp; about 70 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** The shared path ends here. You pick one of three roles — AI Engineer, ML
Engineer, or Data Scientist — spend about forty hours going deeper, and thirty building a capstone
matched to that role's interviews. One branch done well beats three sampled.

**Extend the same thread.** Your capstone should build on the dataset, model, or LLM app from
Chapters 2–6 — not a new tutorial project. One coherent story beats three unrelated repos.

**In this chapter:** [AI Engineer](#branch-a--ai-engineer) &nbsp;·&nbsp;
[ML Engineer](#branch-b--ml-engineer) &nbsp;·&nbsp; [Data Scientist](#branch-c--data-scientist)
&nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp; [Resources](#resources)

---

Plan roughly 40 hours of depth and 30 on the capstone — and budget the capstone first. It is the
point of this chapter, and the depth sections should be cut to fit around it, not the other way
round.

Do one branch. The shared path you have finished is what makes the other two accessible later.

[Chapter 8: Finding the work](../08-finding-the-work/README.md) should already be running alongside
this chapter. If it is not open yet, open it today.

**For offer, pricing or churn work, use [Chapter 9](../09-business-machine-learning/README.md) as
your applied track.** Its shared delivery work plus one guide is about 40 hours. You can use the 30
capstone hours here for a bounded prototype, then spend about ten additional hours on the remaining
shared checks. ML Engineers should emphasise data/serving/feedback; Data Scientists should emphasise
identification, experiment design and the decision memo. Both need the basic experiment checks
before recommending an intervention.

## What you will be able to do

Go deep on one role, finish a capstone that matches its interviews, and explain in writing why you
did not sample the other two.

## Branch A — AI Engineer

**Go deeper on four things.**

- **Agent harnesses.** State, tool contracts, durable execution, bounded retries and verification.
  Use sub-agents or memory when a measured task needs them; make external actions idempotent and put
  human review at the decisions that require it.
- **Evaluation as a speciality.** Judging the whole trajectory, not just the final answer; tool-call
  correctness; multi-turn evaluation; keeping a judge calibrated over time.
- **Reliability and safety.** Prompt injection — hostile instructions hidden in content the model
  reads — privilege boundaries, escalation, rate limits and per-user cost caps. Test allowed and
  forbidden actions together: a system that refuses every task is safe from execution mistakes but
  does not meet the product goal.
- **The product layer.** Designing for a component that is sometimes wrong, and capturing user
  feedback that feeds your evaluation set.

The depth material is a deliberate return to the strongest of the
[Chapter 5](../05-language-models/resources/README.md) and
[Chapter 6](../06-production/resources/README.md) resources, applied to your capstone within the
depth budget: the Anthropic engineering blog's agent sequence end to end,
[12-Factor Agents](https://github.com/humanlayer/12-factor-agents), and Husain and Shankar's evals
material applied to your own traces. Add the dated primary research and official security guidance
in this chapter's resource list. These are complementary evidence sources, not a claim that a
particular agent framework guarantees reliability.

The ICML 2026 paper
[Towards a Science of AI Agent Reliability](https://proceedings.mlr.press/v306/rabanser26a.html),
with an [arXiv version](https://arxiv.org/abs/2602.16666) submitted 18 February and revised 2 June
2026, organizes reliability around consistency, robustness, predictability and safety. For the
capstone, repeat representative tasks, perturb inputs, test escalation and permissions, and measure
recovery after tool failures. Report completion, action errors, latency and cost together. Record
harness, model and evaluator versions; the same final answer can hide a very different sequence of
tool actions. Use the
[OWASP LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/), published 3
August 2026, to derive relevant attack cases; a risk checklist is not evidence that the defense
works.

**Capstone, pick one:** a reproducible evaluation of one important failure mode; an agentic system
with trajectory evaluation and a bounded user pilot; or an open-source tool/contribution with a
reproduced problem and documented validation. Scope the artifact to 30 hours. Record actual pilot
feedback when available; adoption, novelty and a maintainer's merge decision are separate outcomes.

**Interview preparation:** practise an AI systems design discussion, then confirm the employer's
rounds and tool rules using [Chapter 8](../08-finding-the-work/README.md). Useful prompts include a
triage system for ten thousand tickets a day, evidence that it works, a cost-halving target,
recovery from a high error rate, and whether the task warrants an agent. Use your artifacts to
support the tradeoffs; these prompts are practice examples, not a universal interview format.

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
- **Serving and inference optimisation.** Quantisation reduces representation precision and can save
  memory; speed depends on supported kernels and the workload. Compare quality and latency before
  adopting it. Also learn distillation, compilation, batching strategies, and management of the KV
  cache, the memory a model keeps of the tokens it has already processed.
- **Post-training.** Supervised fine-tuning, preference optimisation, and reinforcement learning
  from verifiable rewards.

Choose a **production path** or a **language-model implementation path** before spending the 70
hours. The default production path below uses selected systems readings for about 40 hours and one
capstone for 30. It does not require a from-scratch language model.

For the alternative, [CS336 Spring 2026](https://cs336.stanford.edu/) has public materials and five
assignments spanning basics, systems, scaling, data and alignment/reasoning. It assumes strong
programming, deep-learning and mathematical preparation. Use about ten hours of selected lectures,
fifty for Assignment 1, and ten for tests, profiling and documentation. **That assignment replaces
the production capstone and its depth work.** These are learner planning estimates; extend the
schedule if correctness needs more time. The full graduate course is outside this chapter's budget.
See **Branch B — ML Engineer depth** in [resources/](resources/README.md).

Current efficient-training depth should use the official FSDP2, AMP and compiler guides against your
pinned framework version. Explain the memory/communication tradeoff of sharding before renting
multiple GPUs. Read the MLSys 2026
[FlashAttention-4 paper](https://proceedings.mlsys.org/paper_files/paper/2026/hash/ae8b0b5838ba510daff1198474e7b984-Abstract-Conference.html)
about hardware-aware attention kernels alongside its
[March arXiv version](https://arxiv.org/abs/2603.05451). Its hardware-specific results require a
workload comparison. For adaptation, compare a no-training baseline with one justified SFT or
adapter run. Separate demonstrations, preference data and verifiable rewards, reserve a held-out
task evaluation, and include memory and serving cost. A successful fine-tuning loss does not
establish improvement on the product task.

**Capstone, pick one:** an end-to-end training and serving system with a documented retraining
trigger, keeping the model deliberately simple because the system is what is being assessed; a paper
reproduction with an honest account of where your numbers differ; or one from-scratch language-model
stage done to course standard.

**Interview preparation:** rehearse a 45-minute machine learning systems design discussion covering
data, training, evaluation, serving and monitoring. That is a practice allocation; employers vary
the format and may also assess coding or statistics. Explain a simple starting design and the
evidence that would justify adding complexity, then adapt to the actual round instructions.

**A six-week production plan** (about 12 hours a week; choose the separate CS336 allocation above if
the implementation path is your capstone):

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

- **Experimentation.** Estimands, randomisation units, power/minimum detectable effect before you
  run, sample-ratio mismatch, multiple comparisons, novelty/carryover, interference in marketplaces,
  variance reduction and guardrail metrics. Repeated observations from one user are not independent
  experimental units.
- **Causal inference.** Potential outcomes, confounders and colliders, difference-in-differences,
  instrumental variables, regression discontinuity, matching, and sensitivity analysis.
- **The classical statistics** deliberately deferred earlier in the book.
- **Communication.** Turn a metric, its uncertainty and its limitations into a clear decision memo.

For applied work, distinguish prediction from treatment effects before choosing a causal method.
[Chapter 9](../09-business-machine-learning/README.md) adds primary research, identification
assumptions and a shared experiment protocol for the three business cases. The annotated list is in
[resources/](resources/README.md) under **Branch C — Data Scientist depth**: Kohavi, Tang and Xu on
trustworthy online experiments (companion site at experimentguide.com), Cunningham's _Causal
Inference: The Remix_ online edition, and Huntington-Klein's _The Effect_, both free online.

For each experiment, declare who is eligible, the unit randomized, treatment and control, assignment
logging, outcome window, intended estimand and stopping rule. Analyze by assignment for an
intent-to-treat effect; excluding failed deliveries or nonresponders after assignment can break the
comparison. Reconcile assignment, exposure and outcomes; investigate sample-ratio mismatch before
interpreting a lift. Align uncertainty with clustered or repeated units. Use a fixed analysis
horizon or a justified sequential method: repeatedly checking ordinary p-values and stopping when
one crosses 0.05 changes the error rate.

Make one variance-reduction experiment part of the depth work. Compare unadjusted estimates with
CUPED using only covariates unaffected by treatment, then run simulated A/A tests to check interval
coverage.
[Ensuring Trustworthy Online A/B Testing: Addressing Five Key Questions on CUPED](https://arxiv.org/abs/2606.18750),
a preprint submitted 17 June 2026, examines adjustment and variance-estimation choices, including
multi-arm and two-stage sampling. It is recent methodological evidence, not a guarantee that an
arbitrary adjustment makes every business experiment more precise.

For observational work, state the identification argument before selecting an estimator.
Difference-in-differences requires a credible comparison and trend assumptions; instruments need
relevance and exclusion; regression discontinuity needs a defensible cutoff design. An uplift model,
a doubly robust learner or a flexible predictor cannot create missing randomization, overlap or
unmeasured-confounding control. Use sensitivity checks appropriate to the design and write down what
remains unidentifiable. Chapter 9 connects these choices to offer, price and retention actions.

**Capstone, pick one:** an experiment analysis with a justified causal claim and sensitivity checks;
a metric system for a real product, with a decision memo; or a data engineering project showing
validated SQL, lineage and reliable metric delivery. Choose the artifact that demonstrates the
target role's actual responsibilities.

**Interview preparation:** practise live SQL, statistics, product reasoning and experiment design,
prioritizing the target employer's actual rounds. Pair a dashboard with a memo that connects its
metrics, uncertainty and limitations to a decision.

**A simple six-week plan** (about 12 hours a week):

| Week | Depth (about 7 h)                                                                            | Capstone (about 5 h)                                                                 |
| ---- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| 1    | Experiment companion materials; estimand, power and stopping rule                            | Pick capstone question; declare design and one-page memo outline                     |
| 2    | _The Remix_ or _The Effect_ Part 1 — identification and diagrams                             | SQL + point-in-time query for your dataset                                           |
| 3    | Assignment/exposure checks, clustering and A/A coverage; selected CUPED research             | First analysis draft; distinguish randomized evidence from observational assumptions |
| 4    | Sensitivity analysis and overlap or design diagnostics relevant to your claim                | Revise memo; report uncertainty, guardrails and a decision boundary                  |
| 5    | [Chapter 2](../02-data-foundations/README.md) SQL drills or DataLemur if interviews are near | Practise live SQL screen out loud                                                    |
| 6    | Rehearse experimentation and product-sense cases                                             | Publish memo or experiment write-up; link from portfolio                             |

## Resources

The annotated resources are in **[resources/](resources/README.md)**, grouped by branch. The hours
on full books and courses are alternatives, not requirements to add to the 70-hour plan.

The ones to begin with depend on the branch you chose:

- **Branch A** — choose relevant sections from the "Start here" lists of
  [Chapter 5](../05-language-models/resources/README.md) and
  [Chapter 6](../06-production/resources/README.md), then
  [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) — Dex Horthy. Free, 3–5 hours.
  For the security week, the
  [OWASP Top 10 for LLM Applications](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
  — OWASP GenAI Security Project. Free, 3–4 hours.
- **Branch B** — the training, data and serving guides in the branch resource list for the default
  production path; [Stanford CS336](https://cs336.stanford.edu/) for the alternative implementation
  capstone.
- **Branch C** —
  [Trustworthy Online Controlled Experiments (companion site)](https://www.experimentguide.com/) —
  Ron Kohavi, Diane Tang & Ya Xu. Free companion materials to a paid book, 20–30 hours. Then
  [The Effect](https://theeffectbook.net/) — Nicholas Huntington-Klein. A free book, 25–40 hours.
- **Any branch** —
  [Kaggle Playground Series](https://www.kaggle.com/competitions?searchQuery=playground+series) —
  Kaggle competitions team. A free practice ground, 10–25 hours per entry, for validation-design
  reps between capstone sessions.

## Before you move on

- You finished **one** branch's capstone, not three half-started ones.
- Your README states the metric, the result with a number, and what the system should not be used
  for.
- You can defend your capstone choice in one minute without mentioning salary.
- For Branch C: your write-up distinguishes the prespecified hypothesis from the observed result and
  includes a relevant sensitivity or robustness check.
- For Branch A: you can show repeated-task results, a permission-boundary test and recovery from a
  failed tool call, including the cost of successful completion.
- For Branch B's production path: your release links data, model and serving configuration; load and
  checkpoint/rollback checks support your claims. For the CS336 alternative: correctness tests,
  checkpoint resume, profiling and the documented implementation are the completion evidence.
- For Branch C: the estimand, assignment/design checks, uncertainty and limits of the causal claim
  appear in the decision memo; synthetic data or a simulation is labeled as such.

---

[Previous: Running it in production](../06-production/README.md) &nbsp;·&nbsp;
[Next: Finding the work](../08-finding-the-work/README.md)
