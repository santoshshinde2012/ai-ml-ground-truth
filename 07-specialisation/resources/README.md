# Resources — Chapter 7: Choosing a specialisation

Choose one branch of [the chapter](../README.md). The 70 hours cover depth and a capstone. The
full-course and book estimates below are alternatives, not extra reading. For ML Engineers, CS336
Assignment 1 replaces the default production path and capstone.

Sources were checked on **9 October 2026**. For technical claims, prefer a primary paper, course or
maintainer guide. Recent preprints, peer-reviewed research and vendor engineering accounts are
labelled separately. Popularity, a competition rank or a founder's revenue does not show hiring
outcomes or technical soundness.

**Browse:** [Start here](#start-here) &nbsp;·&nbsp;
[Branch A — AI Engineer depth](#branch-a--ai-engineer-depth) &nbsp;·&nbsp;
[Branch B — ML Engineer depth](#branch-b--ml-engineer-depth) &nbsp;·&nbsp;
[Branch C — Data Scientist depth](#branch-c--data-scientist-depth)

---

## Start here

### [Kaggle Playground Series](https://www.kaggle.com/competitions?searchQuery=playground+series)

_Kaggle_ &nbsp;·&nbsp; Practice competitions &nbsp;·&nbsp; 10–25 hours for a bounded entry

Use one competition to practise validation design. Set a baseline, keep an internal holdout, and
explain why your split matches the competition. Check the current rules and dataset description,
since the season, metric and data-generating process vary. A synthetic competition can test
implementation skills. It cannot show production performance or the causal benefit of a business
intervention.

### [scikit-learn contributing guide](https://scikit-learn.org/stable/developers/contributing.html)

_scikit-learn maintainers_ &nbsp;·&nbsp; Official guidance &nbsp;·&nbsp; 2–3 hours to assess a
suitable contribution

Start with issue reproduction or documentation in an area you use. The current policy requires
careful review of the issue and documentation, manual review and an explanation of your reasoning.
Shallow automated submissions are restricted. The full Automated Contributions Policy requires AI
tool disclosure, with an extra disclosure rule for paid-platform work. Read the current policy
before opening anything, and keep human responsibility for the change. An issue label does not
guarantee a beginner-sized task.

### [PyTorch contributing guide](https://github.com/pytorch/pytorch/blob/main/CONTRIBUTING.md)

_PyTorch maintainers_ &nbsp;·&nbsp; Official guidance &nbsp;·&nbsp; 2–3 hours to assess scope;
implementation is separate

Read the current contribution and review workflow, find a problem you can reproduce, and inspect the
relevant subsystem. Documentation, tests and error explanations count when they fix a real issue.
Avoid promising a merge date or assuming the good-first-issue queue is stocked. Your capstone need
not wait for a maintainer's review.

### [Transformers contributing guide](https://github.com/huggingface/transformers/blob/main/CONTRIBUTING.md)

_Hugging Face Transformers maintainers_ &nbsp;·&nbsp; Official guidance &nbsp;·&nbsp; 2–3 hours to
assess scope

The current guide welcomes coordinated, scoped and verified AI-assisted contributions. It requires
human review, relevant tests, and disclosure with evidence of coordination and testing. It rejects
pure-agent submissions with no human taking responsibility. Skip isolated busywork, and coordinate
as the guide describes before implementing. Policies differ, so read each project's current
instructions.

## Branch A — AI Engineer depth

Use these with the evaluation and deployment material in
[Chapter 5](../../05-language-models/resources/README.md) and
[Chapter 6](../../06-production/resources/README.md).

### [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

_Anthropic engineering_ &nbsp;·&nbsp; Vendor engineering account, 9 January 2026 &nbsp;·&nbsp; 2–3
hours

Tell the transcript apart from the final environment state. Combine code, human and model graders,
isolate each trial's state, and check judges against human labels. The article separates `pass@k`,
at least one success, from `pass^k`, success on every trial. Use the metric that fits the product,
and include retry cost. An agent's claim that an action succeeded is not the recorded outcome.

### [Towards a Science of AI Agent Reliability](https://arxiv.org/abs/2602.16666)

_Stephan Rabanser, Sayash Kapoor and colleagues_ &nbsp;·&nbsp; Peer-reviewed ICML 2026 paper; arXiv
submitted 18 February, revised 2 June 2026 &nbsp;·&nbsp; 2–3 hours

The [published paper](https://proceedings.mlr.press/v306/rabanser26a.html) describes reliability as
consistency, robustness, predictability and safety, instead of average benchmark accuracy alone.
Turn those into tests for your system: repeated tasks, perturbed inputs, escalation and permission
boundaries. Keep harness and evaluator versions fixed, and report uncertainty. Its benchmark results
do not give universal production failure rates.

### [OWASP LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)

_OWASP GenAI Security Project_ &nbsp;·&nbsp; Official community guidance, 3 August 2026
&nbsp;·&nbsp; 3–4 hours

Pick attack cases that match your application's retrieved content, tools and privileges. Test what
the agent actually executes, including escalation, malicious retrieved instructions, data exposure
and repeated delivery. Test useful allowed tasks too, not only attacks. The threat list guides
tests. It does not certify their coverage or prove a complete defence.

### [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)

_Dex Horthy and contributors_ &nbsp;·&nbsp; Author's engineering guide &nbsp;·&nbsp; 3–5 hours

Read the principles beside your own agent loop, especially explicit state/control flow and
recoverable execution. Apply one principle to a recorded failure, then re-measure the task. Treat
the repository as design proposals to test, not a formal standard. Twelve rules do not mean every
task needs an agent.

## Branch B — ML Engineer depth

Choose the default production capstone or the alternative implementation path first.

### [CS336 — Language Modeling from Scratch, Spring 2026](https://cs336.stanford.edu/)

_Tatsunori Hashimoto, Percy Liang and course staff_ &nbsp;·&nbsp; Official graduate course
&nbsp;·&nbsp; Alternative 70-hour allocation in the chapter

The official schedule links public lectures and five assignments. Assignment 1 is the alternative
implementation capstone. It replaces the production system rather than adding to it. Budget selected
lectures, implementation, tests and profiling together, and extend the schedule when needed. The
course assumes strong programming, deep learning and maths.

### [PyTorch — Fully Sharded Data Parallel, FSDP2](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Official tutorial &nbsp;·&nbsp; 2–4 hours to study;
multi-GPU execution is separate

Learn how sharding parameters, gradients and optimiser state trades memory for communication.
Estimate single-device memory first. If a supported multi-GPU experiment is justified, measure GPU
usage and checkpoint/restart behaviour. Follow the tutorial for your pinned release. Reading the API
is useful depth work, even without rented hardware.

### [torchao documentation](https://docs.pytorch.org/ao/stable/)

_PyTorch/torchao maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–4 hours with one
experiment

Read the supported quantisation formats, hardware and integration limits. Quantise one small model
only if your device and runtime support it, then compare quality, resident memory and latency at the
same batch and input lengths. Lower weight precision does not guarantee lower end-to-end latency or
unchanged task behaviour.

### [PEFT](https://huggingface.co/docs/peft/index) and [TRL](https://huggingface.co/docs/trl/index)

_Hugging Face maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 4–8 hours of selected
work

Before choosing a trainer, use the primary LoRA, QLoRA and DPO papers in
[Chapter 4](../../04-deep-learning/resources/README.md) to understand the method. Build one small
adaptation experiment against a no-training baseline. Record the base-model revision, data
provenance, masking, adapter configuration, reward or preference construction, and the held-out
evaluation. Serving the correct adapter is part of finishing.

### [FlashAttention-4](https://arxiv.org/abs/2603.05451)

_Ted Zadouri and colleagues_ &nbsp;·&nbsp; Peer-reviewed MLSys 2026 paper; arXiv submitted 5 March
2026 &nbsp;·&nbsp; 2–3 hours

Read the
[published kernel and scheduling design](https://proceedings.mlsys.org/paper_files/paper/2026/hash/ae8b0b5838ba510daff1198474e7b984-Abstract-Conference.html),
then check which attention backend your framework actually selects. Keep the paper's device
assumptions separate from your project's measurements. Explain a bottleneck before trying a kernel
optimisation. Benchmark speed-ups may not carry over to a different device, model or sequence
length.

## Branch C — Data Scientist depth

Start with the design and decision, then choose an estimator.

### [Trustworthy Online Controlled Experiments — companion site](https://experimentguide.com/)

_Ron Kohavi, Diane Tang and Ya Xu_ &nbsp;·&nbsp; 2020 book; free companion materials, paid full book
&nbsp;·&nbsp; 6–10 hours of selected reading

Read about experiment ingredients, metric design and validity checks alongside your capstone
protocol. The author site offers a sample chapter, errata and extra materials, not the full free
book. Before analysing a result, declare the unit, eligibility, treatment and control, metric,
outcome window, minimum detectable effect and stopping rule.

### [The Effect](https://theeffectbook.net/)

_Nicholas Huntington-Klein_ &nbsp;·&nbsp; Free online book &nbsp;·&nbsp; 6–10 hours of selected
reading

Read the identification and causal-diagram sections before implementing a method. Draw the
data-generating argument, mark what is observed, and explain which assumption allows the
counterfactual comparison. Write a memo that separates the estimate from the decision, with its
uncertainty and the observations that could change it.

### [Causal Inference: The Remix](https://mixtape.scunning.com/)

_Scott Cunningham_ &nbsp;·&nbsp; Free online second edition; paid print edition &nbsp;·&nbsp; 8–12
hours of selected reading

The
[author's release announcement](https://causalinf.substack.com/p/online-version-of-the-remix-is-now)
names Yale University Press and a 25 August 2026 publication date. The online edition is marked a
work in progress. Use its expanded difference-in-differences and synthetic-control material when the
design fits your question. Check the cohort and timing assumptions instead of adding a regression by
rote. Examples and syntax cannot replace a credible untreated comparison.

### [Diagnosing Sample Ratio Mismatch in Online Controlled Experiments](https://www.microsoft.com/en-us/research/publication/diagnosing-sample-ratio-mismatch-in-online-controlled-experiments-a-taxonomy-and-rules-of-thumb-for-practitioners/)

_Aleksander Fabijan and colleagues_ &nbsp;·&nbsp; Peer-reviewed KDD 2019 paper; Microsoft Research
publication page &nbsp;·&nbsp; 2–3 hours

Read the taxonomy of assignment, execution and data-processing problems that can produce unexpected
group ratios. Inject a missing-event or eligibility-filter bug, and look at the diagnostic. A
significant mismatch is a symptom to investigate. Deleting inconvenient users until the ratio looks
right does not repair the experiment.

### [CUPED — Improving the Sensitivity of Online Controlled Experiments](https://doi.org/10.1145/2433396.2433413)

_Alex Deng, Ya Xu, Ron Kohavi and Toby Walker_ &nbsp;·&nbsp; Peer-reviewed WSDM 2013 paper, ACM
Digital Library DOI &nbsp;·&nbsp; 2–3 hours

Learn variance reduction with covariates the treatment cannot affect. Compare a simple difference in
means with an adjusted estimate, and document the coefficient estimation and standard error you
used. Read the later research below for extensions. The original inference may not carry over to
every adjustment or sampling design.

### [Ensuring Trustworthy Online A/B Testing: Addressing Five Key Questions on CUPED](https://arxiv.org/abs/2606.18750)

_Yu Zhang, Bokui Wan, Yongli Qin, Jinyong Ma and Yifan Guo_ &nbsp;·&nbsp; Preprint submitted 17 June
2026 &nbsp;·&nbsp; 2–3 hours

The paper examines adjustment choices and variance estimation, including multi-arm experiments and
two-stage sampling, under stated design assumptions. Use it to audit the estimator and uncertainty
calculation in your capstone. Run simulated A/A experiments to check interval coverage, and compare
power under a known effect. It is a methods preprint, not a general guarantee of unbiased estimates
or lower variance.

### [Time-uniform, nonparametric, nonasymptotic confidence sequences](https://arxiv.org/abs/1810.08240)

_Steven R. Howard, Aaditya Ramdas, Jon McAuliffe and Jasjeet Sekhon_ &nbsp;·&nbsp; Peer-reviewed
Annals of Statistics, April 2021 &nbsp;·&nbsp; 2–4 hours

An optional primary source for inference that allows repeated monitoring, under its assumptions. In
simulation, compare a fixed-horizon analysis with a well-founded sequential method. Updating
ordinary fixed-horizon intervals every day does not make them valid for optional stopping. Choose
the stopping and estimation framework before looking at results.

### [EconML — Doubly robust learning](https://www.pywhy.org/EconML/spec/estimation/dr.html)

_PyWhy/EconML maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 3–5 hours with a small
example

Study the outcome and propensity nuisance models, cross-fitting and treatment-effect estimation.
State the consistency, overlap and no-unmeasured-confounding assumptions, or the randomised design.
Cross-fitting can reduce overfitting in estimation. It cannot identify an effect when the causal
assumptions fail. Evaluate a treatment policy on a suitable held-out experiment.

### [Metalearners for estimating heterogeneous treatment effects](https://www.pnas.org/doi/10.1073/pnas.1804597116)

_Sören R. Künzel, Jasjeet S. Sekhon, Peter J. Bickel and Bin Yu_ &nbsp;·&nbsp; Peer-reviewed PNAS
2019 paper &nbsp;·&nbsp; 2–3 hours

Compare the S-, T- and X-learner constructions and the data situations they target. Use a randomised
or clearly simulated treatment dataset, hold out the policy evaluation, and compare with a
constant-effect baseline. A predictive fit or uplift curve alone does not show incremental profit on
a new population.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
