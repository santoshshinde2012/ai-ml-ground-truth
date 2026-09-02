# Resources — Chapter 7: Choosing a specialisation

The resources for this chapter, grouped by how central each is, with a short note on what each one
is for. The shared list covers practice grounds and open-source paths. Each branch then has its own
depth section: start there once you have picked.

Prices and free tiers change often, so check a resource's own page before you plan around one.

---

## Start here

The resources on the main path for this chapter, in the order the chapter uses them. If you only do a few things, do these.

### [Kaggle Playground Series](https://www.kaggle.com/competitions?searchQuery=playground+series)

*Kaggle competitions team* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-25 hours

The correct entry point to Kaggle in 2026, and the one to use **instead** of Titanic. Competitions refresh roughly monthly, run a few weeks, use lightweight synthetic-from-real datasets, and let you iterate fast on features and models without competing against GPU-rich full-time Kagglers. The learning loop that matters: submit a baseline, then read the top public notebooks and winners' write-ups after the deadline. Treat Playground as deliberate practice, never as the centrepiece of your portfolio.

> **Worth knowing.** Playground datasets are synthetically generated from real-world data. Seasons rotate monthly, so any fixed season link goes stale — search Kaggle competitions for the current Playground Series.

### [scikit-learn Contributing Guide](https://scikit-learn.org/stable/developers/contributing.html)

*scikit-learn core maintainers* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3-4 hours

Read this **before** you plan an open-source-contribution path, because it is refreshingly honest and contradicts most career advice. The maintainers state they rarely use the 'good first issue' label because such issues 'often prove more complex than originally anticipated', and that contributing code 'generally requires advanced skills, and it may not be the best place to begin if you are new to open source contribution.' They point newcomers instead at bug triage, reviewing others' PRs, and documentation, and look at 'Easy', 'help wanted' and 'Needs Investigation' labels.

> **Worth knowing.** The project has explicitly hardened against low-effort and AI-assisted contributions: an LLM-generated PR will be closed and can burn goodwill. Read the guide, start with issue triage and docs, and expect a high bar.

### [PyTorch good-first-issue queue](https://github.com/pytorch/pytorch/contribute)

*PyTorch maintainers* &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 20-80 hours

Unlike most large ML repositories, PyTorch tends to keep a genuinely populated and labelled good-first-issue queue, spanning documentation clarifications, error-message improvements and small performance tasks. This is the most realistic large-repo entry point in the ML ecosystem. Start with a docs or error-message issue, not a Dynamo issue. Caveat: a merged PyTorch PR is a strong signal but a slow one — do it in parallel with shipping your own project, never instead of it.

> **Worth knowing.** A tool, not a lesson — and PyTorch "good first issues" are frequently C++/CUDA/compiler-internals work, not beginner-friendly in the way the label implies.

## Branch A — AI Engineer depth

There is no single course for this branch yet; its depth lives in the engineering literature and in
systems you instrument yourself. The plan is a full, careful re-read of the strongest
[Chapter 5](../../05-language-models/resources/README.md) and
[Chapter 6](../../06-production/resources/README.md) resources: the Anthropic engineering blog's
agent sequence end to end, *12-Factor Agents*, and Husain and Shankar's evals material applied to
your own traces.

## Branch B — ML Engineer depth

If you picked Branch B, start here rather than with the shared list above.

### [Stanford CS336: Language Modelling from Scratch (Spring 2026)](https://cs336.stanford.edu/)

*Percy Liang & Tatsunori Hashimoto* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40-60 hours for Assignment 1 only; 150-250 hours for the full course

The most rigorous free language-model curriculum there is, and the natural depth path for this branch. Seventeen lectures: tokenisation, resource accounting, architectures, attention alternatives and mixture-of-experts, GPUs and TPUs, Triton kernels, parallelism, scaling laws, inference, evaluation, data sourcing and filtering, post-training (SFT, RLHF, RLVR) and alignment. Five assignments: Basics, Systems, Scaling, Data, and Alignment and Reasoning RL. For this chapter, timebox it: watch the first four lectures, do **Assignment 1 only**, and treat that as your capstone. You will touch tokenisation, a from-scratch training stack, and the systems thinking interviews test. Skip the paid certificate; the [lecture recordings](https://www.youtube.com/playlist?list=PLoROMvodv4rMqXOcazWaTUHhq-yembLCV) and [assignment repositories](https://github.com/stanford-cs336) are public.

> **Worth knowing.** A graduate systems course, not an introduction: it assumes fluent PyTorch and comfort with GPUs. Assignment 1 alone is forty to sixty hours if done honestly. The rest is a second-year project, not a six-week sprint.

## Branch C — Data Scientist depth

If you picked Branch C, start here. These three references sit outside the rest of this book's curated set — vet them with particular care, but practitioners name them constantly for good reason.

### [Trustworthy Online Controlled Experiments (companion site)](https://www.experimentguide.com/)

*Ron Kohavi, Diane Tang & Ya Xu* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid book; free companion materials &nbsp;·&nbsp; 20-30 hours

The standard reference for A/B testing at scale, written by experimentation leaders from Microsoft,
Google and LinkedIn. The book itself is paid; the companion site at experimentguide.com carries
slides, FAQs, and supplementary material worth reading before you buy. Read it for the mechanics
that actually matter in interviews: randomisation units, guardrail metrics, peeking, carryover,
validity checks, and why a surprising positive result should make you suspicious first. Pair with
your capstone — an experiment write-up with a sensitivity analysis is exactly what this prepares.

> **Worth knowing.** Not free in full. Use the companion site and library access, and buy the book
> only if experimentation is the branch you are committing to.

### [The Effect: An Introduction to Research Design and Causality](https://theeffectbook.net/)

*Nicholas Huntington-Klein* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free online &nbsp;·&nbsp; 25-40 hours

A gentler complement to the Mixtape: research design and identification first, regression mechanics
second. Part 1 uses causal diagrams to make confounding and identification intuitive; Part 2 covers
implementation with controls, matching and regression discontinuity. The free Bookdown version stays
on theeffectbook.net; a print edition exists if you prefer paper. Best for someone who finds the
Mixtape's pace fast, or who needs to explain a design choice to a non-technical stakeholder in a
decision memo — which is most of the Data Scientist job.

> **Worth knowing.** Examples lean econometric. The `causaldata` package (R, Stata, Python) holds
> the book's datasets if you want to run the code alongside the prose.

### [Causal Inference: The Mixtape (2nd edition, online)](https://mixtape.scunning.com/)

*Scott Cunningham* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free online &nbsp;·&nbsp; 30-50 hours

The most approachable free introduction to causal inference for social-science-style questions.
Cunningham walks difference-in-differences, matching, regression discontinuity, instrumental
variables and sensitivity analysis with plain language and worked examples in R and Stata. The
online second edition is still being polished — expect typos — but it is readable now and costs
nothing. Use it when your capstone needs a causal claim, not just a correlation with a good p-value.

> **Worth knowing.** The 2nd-edition web version is explicitly a work-in-progress. Code is in R/Stata,
> not Python — translate the ideas, not the syntax, unless your capstone is in R.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [Photo AI by Pieter Levels — $0 to $132K MRR case study](https://www.indiehackers.com/post/photo-ai-by-pieter-levels-complete-deep-dive-case-study-0-to-132k-mrr-in-18-months-3a9a2b1579)

*Indie Hackers community post about Pieter Levels, solo founder of NomadList, RemoteOK and PhotoAI* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1-2 hours

The canonical existence proof that one person can ship and monetise an AI product, and a useful corrective to the mythology. Real numbers: PhotoAI launched Feb 2023, ~$5.4K MRR in week one, ~$132-138K MRR by Nov 2025. But read the caveats hiring managers and founders both note — it came after roughly 70 failed projects, and it launched into an audience of ~350K followers. The transferable lessons are narrow scope, boring stack (vanilla PHP), ship daily, tweet every ship and every revenue milestone; the non-transferable part is the pre-existing distribution.

> **Worth knowing.** Anonymous user-generated content with no editorial review; every revenue number is a third-party estimate — Levels publishes his own figures on his open startup pages. One extreme outlier is not a template, and its PHP/SQLite/one-VPS stack is not what this book teaches.

### [The Embedded Entrepreneur: How to Build an Audience-Driven Business](https://www.amazon.com/Embedded-Entrepreneur-Build-Audience-Driven-Business/dp/3982195764)

*Arvid Kahl* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 8-10 hours

The best structured antidote to the beginner failure mode of building a technically impressive AI thing nobody wants. Kahl's sequence — Audience Discovery, Audience Exploration, Problem Discovery, then Audience Building — inverts the usual order: find the customers first, build the solution with them. For an AI portfolio this is what converts 'RAG over documents' into 'RAG over the 2,400-page regulation that 40 people in this Slack complain about weekly', which is exactly the specificity hiring managers reward. The book itself was written this way with 500+ alpha readers.

> **Worth knowing.** A bootstrapping and audience-building book, the weakest topical fit in an AI/ML learning path. Sold through a commerce listing with no free preview.

## Keep for reference

Not for reading end to end. Useful to have when you need to look something up.

### [Best AI Projects to Build in 2026 (Sequenced for Hiring)](https://www.dataquest.io/blog/ai-projects/)

*Anishta Purrahoo* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

A reasonable secondary source for the sequencing argument — that projects should be ordered to map onto skills that actually appear in job descriptions (RAG, evals, model serving, MLOps), and that three strong projects beat ten generic ones. Included for the sequencing frame only; no named practitioner behind it, so verify any specific claim against a primary source before repeating it in an interview.

> **Worth knowing.** Vendor content marketing for a paid learning platform; its hiring claims are assertions, not evidence. Usable as a project-idea list, not as a source on the job market.

### [How to become a Kaggle Competitions Grandmaster](https://towardsdatascience.com/how-to-become-a-kaggle-competitions-grandmaster-9d77431c5b7d/)

*Agnis Liukis* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

A first-person account of the real requirements and timeline: Competitions Grandmaster needs 5 gold medals including at least one solo gold, and it took the author roughly two years of sustained effort. Read it precisely to calibrate expectations downward — the honest conclusion for a beginner is that Kaggle is a superb modelling gym and a poor career shortcut, and that the ROI is in reading winning solution write-ups, not in chasing tiers. Concentrate on one competition at a time rather than several.

> **Worth knowing.** Five-year-old competition tactics, published on Towards Data Science behind a metered paywall.

### [Hugging Face Transformers contribution guide and queue](https://github.com/huggingface/transformers/contribute)

*Hugging Face Transformers maintainers* &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 15-50 hours

Transformers is the friendliest large ML repo culturally — the contributing guide explicitly maintains 'Good First Issue' and the harder 'Good Second Issue' lists, and the norm is to comment claiming the issue before you start. The good-first-issue list is often empty — these queues drain within hours. The practical tactic is to watch the repo, filter issues by the label directly, and move fast; or contribute to the surrounding ecosystem (datasets, diffusers, accelerate, evaluate, the HF course repos) where the queues are less contested. Documentation fixes are the highest-success-rate first contribution.

> **Worth knowing.** The good-first-issue queue is often empty, so it may deliver nothing as a starting point — read CONTRIBUTING.md and filter the issue tracker yourself.

### [The 2025 AI Engineering Reading List](https://www.latent.space/p/2025-papers)

*swyx* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Paywalled &nbsp;·&nbsp; an hour as a map

~50 curated papers/posts/model families, roughly one per week for a year, spanning frontier LLMs, RAG, agents, benchmarks and evals — built by updating the a16z 2023 list with Latent Space paper-club picks and NeurIPS 'best of' recommendations. Use it as a menu, not a syllabus: pick the 5 items adjacent to the project you're building. Reading papers is a supplement to shipping, never a substitute, and a beginner who reads 50 papers but ships nothing has little to show a hiring manager.

> **Worth knowing.** A paid Substack post (7-day free trial), and a late-2024 snapshot that misses roughly two model generations. The free normcore-llm-reads list in the Chapter 8 resources covers similar ground.

### [What Titanic, Iris, and House Prices Say About Your Portfolio](https://www.statology.org/what-titanic-iris-and-house-prices-say-about-your-portfolio/)

*Vinod Chugani* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

Useful mainly as a blunt statement of the consensus: these datasets tell an experienced reviewer very little, because when every bootcamp graduate has an identical Titanic notebook, the notebook carries zero signal — it confirms you can follow a tutorial, not that you can formulate a problem, source data, build a system and measure impact. Its constructive fix is the right one: add at least one project where you sourced your own data, defined your own question and made your own decisions. Read it once for the framing, then move on.

> **Worth knowing.** SEO-oriented content marketing on a stats-tutorial site: thin sourcing, and no data behind its hiring claims. Read it as framing, not as evidence.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
