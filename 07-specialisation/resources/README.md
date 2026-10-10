# Resources — Chapter 7: Choosing a specialisation

Choose one branch of [the chapter](../README.md). The 70 hours include depth and a capstone; the
full-course and book estimates below are alternatives, not an additional reading requirement. For ML
Engineers, CS336 Assignment 1 replaces the default production path and capstone.

Sources were checked on **9 October 2026**. Prefer a primary paper, course or maintainer guide for
technical claims. Recent preprints, peer-reviewed research and vendor engineering accounts are
labeled separately. Resource popularity, competition rank or a founder's revenue does not establish
hiring outcomes or technical validity.

**Browse:** [Start here](#start-here) &nbsp;·&nbsp;
[Branch A — AI Engineer depth](#branch-a--ai-engineer-depth) &nbsp;·&nbsp;
[Branch B — ML Engineer depth](#branch-b--ml-engineer-depth) &nbsp;·&nbsp;
[Branch C — Data Scientist depth](#branch-c--data-scientist-depth)

---

## Start here

### [Kaggle Playground Series](https://www.kaggle.com/competitions?searchQuery=playground+series)

_Kaggle_ &nbsp;·&nbsp; Practice competitions &nbsp;·&nbsp; 10–25 hours for a bounded entry

Use one competition for validation-design practice: establish a baseline, keep an internal holdout,
and explain why the split matches the competition. Read the current dataset description and rules
rather than assuming a fixed season, metric or data-generating process. A synthetic competition can
test implementation skills; it cannot establish production performance or the causal benefit of a
business intervention.

### [scikit-learn contributing guide](https://scikit-learn.org/stable/developers/contributing.html)

_scikit-learn maintainers_ &nbsp;·&nbsp; Official guidance &nbsp;·&nbsp; 2–3 hours to assess a
suitable contribution

Start with issue reproduction or documentation in an area you use. The current policy requires
careful review of the issue and documentation, manual review and an explanation of the rationale;
shallow automated submissions are restricted. The full Automated Contributions Policy requires AI
tool disclosure; paid-platform work has an additional disclosure rule. Read the current policy
before opening anything and retain human responsibility for the change. A label on an issue is not a
guarantee of a beginner-sized task.

### [PyTorch contributing guide](https://github.com/pytorch/pytorch/blob/main/CONTRIBUTING.md)

_PyTorch maintainers_ &nbsp;·&nbsp; Official guidance &nbsp;·&nbsp; 2–3 hours to assess scope;
implementation is separate

Read the current contribution and review workflow, find a problem you can reproduce and inspect the
relevant subsystem. Documentation, tests and error explanations can be meaningful when they resolve
an actual issue. Do not promise a merge date or assume a good-first-issue queue is populated; your
capstone can proceed independently of a maintainer's review.

### [Transformers contributing guide](https://github.com/huggingface/transformers/blob/main/CONTRIBUTING.md)

_Hugging Face Transformers maintainers_ &nbsp;·&nbsp; Official guidance &nbsp;·&nbsp; 2–3 hours to
assess scope

The current guide welcomes coordinated, scoped and verified AI-assisted contributions. It requires
human review, relevant tests and disclosure with coordination and test evidence, and rejects
pure-agent submissions without that responsibility. Avoid isolated busywork and coordinate according
to the guide before taking on implementation. This policy differs from other projects; read each
project's current instructions.

## Branch A — AI Engineer depth

Use these with the evaluation and deployment material in
[Chapter 5](../../05-language-models/resources/README.md) and
[Chapter 6](../../06-production/resources/README.md).

### [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

_Anthropic engineering_ &nbsp;·&nbsp; Vendor engineering account, 9 January 2026 &nbsp;·&nbsp; 2–3
hours

Distinguish the transcript from the final environment state. Combine code, human and model graders,
isolate trial state, and check judges against human labels. The article distinguishes `pass@k`, at
least one success, from `pass^k`, success on every trial. Use the metric that fits the product and
include retry cost; an agent's claim that an action succeeded is not the recorded action outcome.

### [Towards a Science of AI Agent Reliability](https://arxiv.org/abs/2602.16666)

_Stephan Rabanser, Sayash Kapoor and colleagues_ &nbsp;·&nbsp; Peer-reviewed ICML 2026 paper; arXiv
submitted 18 February, revised 2 June 2026 &nbsp;·&nbsp; 2–3 hours

The [published paper](https://proceedings.mlr.press/v306/rabanser26a.html) organizes reliability as
consistency, robustness, predictability and safety rather than average benchmark accuracy alone.
Translate those dimensions into repeated tasks, input perturbations, escalation and
permission-boundary tests for your system. Keep harness and evaluator versions fixed and report
uncertainty. Its experimental benchmark results do not establish universal production failure rates.

### [OWASP LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)

_OWASP GenAI Security Project_ &nbsp;·&nbsp; Official community guidance, 3 August 2026
&nbsp;·&nbsp; 3–4 hours

Select attack cases relevant to the application's retrieved content, tools and privileges. Test what
the agent actually executes, including escalation, malicious retrieved instructions, data exposure
and repeated delivery. Check useful authorized-task completion as well as attacks. The threat list
guides tests; it does not certify their coverage or prove a complete defense.

### [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)

_Dex Horthy and contributors_ &nbsp;·&nbsp; Author's engineering guide &nbsp;·&nbsp; 3–5 hours

Read the principles beside your own agent loop, especially explicit state/control flow and
recoverable execution. Apply one principle to a recorded failure, then re-measure the task. Treat
the repository as a set of design proposals to evaluate, rather than a formal standard or evidence
that twelve rules make every task require an agent.

## Branch B — ML Engineer depth

Choose the default production capstone or the alternative implementation path first.

### [CS336 — Language Modeling from Scratch, Spring 2026](https://cs336.stanford.edu/)

_Tatsunori Hashimoto, Percy Liang and course staff_ &nbsp;·&nbsp; Official graduate course
&nbsp;·&nbsp; Alternative 70-hour allocation in the chapter

The official schedule links public lectures and five assignments. Assignment 1 is the implementation
capstone alternative, not homework to add to a separate production system. Budget selected lectures,
implementation, tests and profiling together; extend the schedule when necessary. Strong
programming, deep-learning and mathematical preparation are assumed.

### [PyTorch — Fully Sharded Data Parallel, FSDP2](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Official tutorial &nbsp;·&nbsp; 2–4 hours to study;
multi-GPU execution is separate

Understand how sharding parameters, gradients and optimizer state trades memory for communication.
Estimate single-device memory first, then measure utilization and checkpoint/restart behavior if a
supported multi-GPU experiment is justified. Follow the tutorial for your pinned release; reading
the API is a useful depth exercise even without rented hardware.

### [torchao documentation](https://docs.pytorch.org/ao/stable/)

_PyTorch/torchao maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–4 hours with one
experiment

Read supported quantization formats, hardware and integration constraints. Quantize one small model
only when the device/runtime support it, then compare quality, resident memory and latency at the
same batch and input lengths. Reduced weight precision does not guarantee reduced end-to-end latency
or unchanged task behavior.

### [PEFT](https://huggingface.co/docs/peft/index) and [TRL](https://huggingface.co/docs/trl/index)

_Hugging Face maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 4–8 hours of selected
work

Use the primary LoRA, QLoRA and DPO papers in
[Chapter 4](../../04-deep-learning/resources/README.md) to understand the method before selecting a
trainer. Build one bounded adaptation experiment against a no-training baseline. Record base-model
revision, data provenance, masking, adapter configuration, reward or preference construction and
held-out evaluation; serving the correct adapter is part of completion.

### [FlashAttention-4](https://arxiv.org/abs/2603.05451)

_Ted Zadouri and colleagues_ &nbsp;·&nbsp; Peer-reviewed MLSys 2026 paper; arXiv submitted 5 March
2026 &nbsp;·&nbsp; 2–3 hours

Read the
[published kernel and scheduling design](https://proceedings.mlsys.org/paper_files/paper/2026/hash/ae8b0b5838ba510daff1198474e7b984-Abstract-Conference.html),
then inspect the attention backend your framework actually selects. Keep the paper's device
assumptions separate from the project's measurements. Explain a bottleneck before attempting a
kernel optimization; benchmark-derived speedups need not transfer to a different device, model or
sequence length.

## Branch C — Data Scientist depth

Start with the design and decision, then choose an estimator.

### [Trustworthy Online Controlled Experiments — companion site](https://experimentguide.com/)

_Ron Kohavi, Diane Tang and Ya Xu_ &nbsp;·&nbsp; 2020 book; free companion materials, paid full book
&nbsp;·&nbsp; 6–10 hours of selected reading

Read experiment ingredients, metric design and validity checks alongside the capstone protocol. The
author site provides a sample chapter, errata and additional materials; do not describe it as the
full free book. Declare the unit, eligibility, treatment/control, metric, outcome window, minimum
detectable effect and stopping rule before analyzing a result.

### [The Effect](https://theeffectbook.net/)

_Nicholas Huntington-Klein_ &nbsp;·&nbsp; Free online book &nbsp;·&nbsp; 6–10 hours of selected
reading

Use the identification and causal-diagram sections before implementing a method. Draw the
data-generating argument, identify what is observed and explain which assumption allows the
counterfactual comparison. Write a memo that separates the estimate from the decision, including
uncertainty and the observations that could change it.

### [Causal Inference: The Remix](https://mixtape.scunning.com/)

_Scott Cunningham_ &nbsp;·&nbsp; Free online second edition; paid print edition &nbsp;·&nbsp; 8–12
hours of selected reading

The
[author's release announcement](https://causalinf.substack.com/p/online-version-of-the-remix-is-now)
identifies Yale University Press and a 25 August 2026 publication date. The author's online edition
is marked a work in progress. Use its expanded difference-in-differences and synthetic-control
material when the design fits your question; inspect cohort/time assumptions rather than
mechanically adding a regression. Examples and syntax do not substitute for a credible untreated
comparison.

### [Diagnosing Sample Ratio Mismatch in Online Controlled Experiments](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/)

_Aleksander Fabijan and colleagues_ &nbsp;·&nbsp; Peer-reviewed KDD 2019 paper; Microsoft Research
publication page &nbsp;·&nbsp; 2–3 hours

Read the taxonomy of assignment, execution and data-processing problems that can produce unexpected
group ratios. Inject a missing-event or eligibility-filter bug and inspect the diagnostic. A
significant mismatch is a symptom to investigate; deleting inconvenient users until the ratio looks
right does not repair the experiment.

### [CUPED — Improving the Sensitivity of Online Controlled Experiments](https://ai.stanford.edu/~ronnyk/2013-02CUPEDImprovingSensitivityOfControlledExperiments.pdf)

_Alex Deng, Ya Xu, Ron Kohavi and Toby Walker_ &nbsp;·&nbsp; Peer-reviewed WSDM 2013 paper,
author-hosted PDF &nbsp;·&nbsp; 2–3 hours

Understand variance reduction with covariates unaffected by treatment. Compare a simple difference
in means with an adjusted estimate, documenting coefficient estimation and the standard error used.
Read the later research below for extensions; do not assume all adjustment or sampling designs
inherit the original setup's inference.

### [Ensuring Trustworthy Online A/B Testing: Addressing Five Key Questions on CUPED](https://arxiv.org/abs/2606.18750)

_Yu Zhang, Bokui Wan, Yongli Qin, Jinyong Ma and Yifan Guo_ &nbsp;·&nbsp; Preprint submitted 17 June
2026 &nbsp;·&nbsp; 2–3 hours

The paper examines adjustment specifications and variance estimation, including multi-arm
experiments and two-stage sampling, under stated design assumptions. Use it to audit the estimator
and uncertainty calculation in the capstone. Run simulated A/A experiments to check interval
coverage and compare power under a known effect. This is methodological preprint evidence, not a
universal guarantee of unbiasedness or variance reduction.

### [Time-uniform, nonparametric, nonasymptotic confidence sequences](https://arxiv.org/abs/1810.08240)

_Steven R. Howard, Aaditya Ramdas, Jon McAuliffe and Jasjeet Sekhon_ &nbsp;·&nbsp; Peer-reviewed
Annals of Statistics, April 2021 &nbsp;·&nbsp; 2–4 hours

An optional primary source for inference that allows repeated monitoring under its assumptions.
Compare a fixed-horizon analysis with a justified sequential method in simulation. Ordinary
fixed-horizon intervals do not become valid for optional stopping by updating them every day; choose
the stopping/estimation framework before looking at results.

### [EconML — Doubly robust learning](https://www.pywhy.org/EconML/spec/estimation/dr.html)

_PyWhy/EconML maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 3–5 hours with a small
example

Inspect outcome and propensity nuisance models, cross-fitting and treatment-effect estimation. State
consistency, overlap and no-unmeasured-confounding assumptions or the randomized design.
Cross-fitting can reduce overfitting in estimation; it does not identify an effect when the causal
assumptions fail. Evaluate a treatment policy on an appropriate held-out experiment.

### [Metalearners for estimating heterogeneous treatment effects](https://www.pnas.org/doi/10.1073/pnas.1804597116)

_Sören R. Künzel, Jasjeet S. Sekhon, Peter J. Bickel and Bin Yu_ &nbsp;·&nbsp; Peer-reviewed PNAS
2019 paper &nbsp;·&nbsp; 2–3 hours

Compare the S-, T- and X-learner constructions and the data situations they target. Use a randomized
or explicitly simulated treatment dataset, hold out the policy evaluation, and compare with a
constant-effect baseline. A predictive fit or uplift curve alone does not establish incremental
profit on a new population.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
