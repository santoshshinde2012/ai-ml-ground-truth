# Chapter 7: Choosing a specialisation

**Weeks 38-43 &nbsp;·&nbsp; about 70 hours.** &nbsp;·&nbsp; [Index](../README.md) &nbsp;·&nbsp; [Resources for this chapter](resources/README.md)

**The short version.** The shared path ends here. You pick one of three roles — AI Engineer, ML Engineer, or Data Scientist — spend about forty hours going deeper, and thirty building a capstone matched to that role's interviews. One branch done well beats three sampled.

---

Plan roughly 40 hours of depth and 30 on the capstone — and budget the capstone first. It is the
point of this chapter, and the depth sections should be cut to fit around it, not the other way
round.

Do one branch. The shared path you have finished is what makes the other two accessible later.

[Chapter 8: Finding the work](../08-finding-the-work/README.md) should already be running alongside
this chapter. If it is not open yet, open it today.

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

## Branch B — ML Engineer

**Go deeper on four things.**

- **The data layer.** Orchestration, warehouse modelling, data quality tests, and point-in-time
  correctness at scale.
- **Training at scale.** Data and model parallelism, mixed precision, gradient accumulation and
  checkpointing, profiling, and scaling laws.
- **Serving and inference optimisation.** Quantisation — storing weights in lower precision to
  shrink and speed up a model — plus distillation, compilation, batching strategies, and managing
  the KV cache.
- **Post-training.** Supervised fine-tuning, preference optimisation, and reinforcement learning
  from verifiable rewards.

[Stanford's CS336](https://cs336.stanford.edu/) is the rigorous free path here, and it is a graduate systems course rather than an
introduction. For six weeks, watch four lectures and do **Assignment 1 only**, timeboxed at forty to
sixty hours, treating it as your capstone. The rest is a second-year project.

**Capstone, pick one:** an end-to-end training and serving system with a documented retraining
trigger, keeping the model deliberately simple because the system is what is being assessed; a paper
reproduction with an honest account of where your numbers differ; or one from-scratch
language-model stage done to course standard.

**Interviews** centre on a machine learning systems design round covering data, training, evaluation,
serving and monitoring in forty-five minutes. Proposing the simple thing and saying what evidence
would justify escalating is usually the strongest move available.

## Branch C — Data Scientist

**Go deeper on four things.**

- **Experimentation.** Randomisation units, power calculations before you run, the peeking
  problem, multiple comparisons, novelty effects, interference in marketplaces, variance
  reduction, and guardrail metrics.
- **Causal inference.** Potential outcomes, confounders and colliders, difference-in-differences,
  instrumental variables, regression discontinuity, matching, and sensitivity analysis.
- **The classical statistics** deliberately deferred earlier in the book.
- **Communication** — the highest-leverage and least-taught part of the role.

One honest caveat: **experimentation and causal inference are the one area where the core references
sit outside the set of material this book leans on most heavily**, so vet whatever you pick here
with particular care. The names practitioners commonly give are Kohavi, Tang and Xu on trustworthy
online experiments, and Cunningham's *Causal Inference: The Mixtape* and Huntington-Klein's *The
Effect* for causal work, both free online.

**Capstone, pick one:** a full experiment analysis with a causal claim and a sensitivity analysis; a
metric system for a real product, with a decision memo; or a data engineering project with no machine
learning in it at all, which is a surprisingly strong and under-used signal.

**Interviews** include a live SQL screen, statistics, a product-sense case and an experimentation
case. A dashboard makes a weak capstone; a memo that leads to a decision makes a strong one.

## Resources

All 10 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [Kaggle Playground Series](https://www.kaggle.com/competitions?searchQuery=playground+series) — Kaggle competitions team. A free practice ground, 10-25 hours per entry.
- [PyTorch good-first-issue queue](https://github.com/pytorch/pytorch/contribute) — PyTorch maintainers. Free; the most realistic large-repository entry point.
- [scikit-learn contributing guide](https://scikit-learn.org/stable/developers/contributing.html) — scikit-learn core maintainers. Free; read it before planning an open-source path.
- [The Embedded Entrepreneur](https://www.amazon.com/Embedded-Entrepreneur-Build-Audience-Driven-Business/dp/3982195764) — Arvid Kahl. A paid book, 8-10 hours, on finding users before building.

---

[Previous: Running it in production](../06-production/README.md) &nbsp;·&nbsp; [Next: Finding the work](../08-finding-the-work/README.md)
