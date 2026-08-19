# Resources — Chapter 6: Running it in production

Everything referenced in [the chapter](../README.md), grouped by how central it is, with a short
note on what each one is for.

Prices and free tiers change often, so check a resource's own page before you plan around one.

---

## Start here

The resources on the main path for this chapter. If you only do a few things, do these.

### [AI Evals Free Email Course (17 parts)](https://ai.hamel.dev/eval-course)

*Hamel Husain & Shreya Shankar* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 5-6 hours

The free, paced version of Husain and Shankar's evals material: 17 email lessons on error analysis, synthetic data generation, custom evaluators and their trade-offs, human-in-the-loop annotation, and evals for RAG and multi-turn systems, plus two supplementary e-books. Use this as the structured on-ramp, and their Evals FAQ (in the Chapter 5 resources) as the reference you keep returning to. Between these two you get ~80% of the value of the $4,200 Maven course for $0.

> **Worth knowing.** Requires an email signup; it is the free distillation of, and lead capture for, a $4,200 Maven cohort course.

### [Eugene Yan — Start Here (LLM patterns, evals, ML in production)](https://eugeneyan.com/start-here/)

*Eugene Yan* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-15 hours

A curated index into a decade of genuinely good free writing by one identifiable senior practitioner. The highest-value pieces for this domain: 'Patterns for LLM Systems' (evals, RAG, finetuning, caching, guardrails, defensive UX), 'Product Evals in 3 Simple Steps', 'LLM-Evaluators', 'Challenges with ML in Production' and 'Testing ML'. Better signal-to-noise than any Medium/Substack MLOps aggregator, and it is one human you can cite in an interview.

### [FastAPI official documentation and tutorial](https://fastapi.tiangolo.com/)

*Sebastián Ramírez* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-15 hours

The default way to wrap a model in an HTTP API in 2026, and the docs are genuinely a course: request/response models with Pydantic, dependencies, background tasks, streaming JSON lines and Server-Sent Events (needed for token streaming from an LLM), testing, and bigger-application structure. Work through 'Tutorial - User Guide' up to Testing and Bigger Applications, plus the SSE/streaming pages. Do NOT skip the testing chapter — 'has tests for the API' is a visible differentiator on a portfolio repo.

### [GitHub Actions documentation (quickstart + workflows + deployment)](https://docs.github.com/en/actions)

*GitHub documentation team* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6-10 hours

The cheapest, most universal CI/CD you can demonstrate, and free for public repos. Learn: workflow YAML and events, running pytest on push, building and pushing a Docker image, using secrets, matrix builds, and scheduled (cron) workflows — the cron trigger doubles as a free batch-inference scheduler for a student project. Every serious portfolio repo in this domain should have a green CI badge; its absence raises questions about team experience.

### [Langfuse — open-source LLM observability (docs + pricing)](https://langfuse.com/pricing)

*Marc Klingen, Max Deichmann & Clemens Rawert* &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 4-6 hours

For a student this is the best free LLM-tracing option by a wide margin: 33k stars, MIT license, pushed daily, OpenTelemetry-based so it is framework-agnostic, and the hosted free tier (50k observations/mo) is 10x LangSmith's free tier (5k traces/mo). Self-hosting is real but needs Postgres + ClickHouse + Redis + S3, so use the cloud Hobby tier for a portfolio project and mention you know the self-host topology. Instrument your RAG project with this on day one — In an interview, 'I looked at 100 real traces' is one of the strongest sentences you can say.

> **Worth knowing.** Pricing pages change without notice, so the figures may already be out of date — and Langfuse can be self-hosted for free, which a pricing page alone does not make obvious.

### [LLM Zoomcamp (DataTalks.Club)](https://github.com/DataTalksClub/llm-zoomcamp)

*Alexey Grigorev, with Will Russell and Timur Kamaliev* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 60-80 hours

The 2026 edition (cohort started 8 June 2026, materials pushed as recently as July 2026) was restructured around what actually matters now: agentic RAG, vector search, orchestration (Kestra), a dedicated evaluation module, a monitoring module, best practices, plus a data-ingestion workshop with dlt and a capstone. This is the free course closest to what a 2026 'AI engineer, junior' job description asks for. Total API spend is only ~$1-5. Do this second, after Made With ML or MLOps Zoomcamp.

### [Made With ML — MLOps Course](https://madewithml.com/courses/mlops/)

*Goku Mohandas* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40-60 hours

Still the single best free end-to-end walkthrough of taking ONE project from notebook to production: design, data, training, experiment tracking, testing (code, data, model), CI/CD, serving, monitoring. 49k GitHub stars. Its real value is the software-engineering discipline it forces (scripting, CLI, pre-commit, testing your data and your model, not just your code) — that discipline is exactly what hiring managers say junior candidates lack. That said, the repo's substantive commits stop at December 2023 (only a light touch in March 2026), and it is heavily Ray/Anyscale-flavoured. Learn the structure, not the exact library versions. Do this first, before any LLM-specific material.

> **Worth knowing.** A three-year-old MLOps curriculum, in the area where staleness hurts most — tooling, orchestration, serving and CI/CD have all turned over. Also vendor content for Ray/Anyscale. The systems-thinking and testing lessons transfer; the stack does not.

### [ML Observability Course (40 lessons)](https://www.evidentlyai.com/ml-observability-course)

*Emeli Dral & Elena Samuylova* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 15-20 hours

The only serious free course dedicated to the monitoring half of MLOps: 6 modules / 40+ video lessons on monitoring metrics (model quality, data quality, data drift), monitoring unstructured data including NLP and embeddings, **designing** a monitoring system, not just installing one, pipeline validation and testing, and deploying a dashboard with Evidently + MLflow + Airflow + Grafana. Monitoring and rollback is one of the things hiring managers name as the prototype/production dividing line. One caveat: the course repo was last pushed December 2023, so run the code against current Evidently (the library itself is actively maintained, pushed August 2026) and expect API drift.

> **Worth knowing.** Free and well-taught, but the code demos target a 2023 Evidently API with no version pin — expect breakage. Take the concepts (drift, data quality, test suites) and get the code from current Evidently docs.

### [MLflow documentation — tracking, model registry, and GenAI tracing](https://mlflow.org/docs/latest/genai/tracing/quickstart/)

*MLflow maintainers* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6-10 hours

27.5k stars, pushed daily as of August 2026. MLflow is the default answer for experiment tracking and it made the jump to the LLM era: MLflow 3 added the LoggedModel entity and MLflow Tracing, which auto-instruments 20+ GenAI libraries (OpenAI, LangChain, LlamaIndex, DSPy, Pydantic AI) and captures latency and token usage per step. That means one tool covers both halves of your portfolio. Learn tracking + model registry first (via MLOps Zoomcamp module 2), then the tracing quickstart. Self-hostable for free with a local sqlite backend.

> **Worth knowing.** The /docs/latest/ path floats: content shifts under the link without notice and no pinned version number is shown.

### [MLOps Zoomcamp (DataTalks.Club)](https://github.com/DataTalksClub/mlops-zoomcamp)

*Alexey Grigorev with Cristian Martinez and Emeli Dral* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 80-100 hours

The most complete free hands-on classical-MLOps curriculum: 6 modules + a graded final project covering MLflow experiment tracking and model registry, workflow orchestration, deployment (batch + streaming), monitoring with Evidently/Prometheus/Grafana, and best practices (testing, linting, GitHub Actions CI/CD, Terraform). The repo is actively maintained (commits as recent as August 2026) even though there is NO live 2026 cohort — it is explicitly positioned as self-paced now. Pick this over Made With ML if you want breadth of tools; pick Made With ML if you want depth on ONE project. Doing the final project and putting it on GitHub is the highest-ROI portfolio move in classical MLOps.

> **Worth knowing.** No 2026 cohort — the live deadlines and peer review that made the course work are gone, and it is now self-paced only. The stack is classical MLOps with no LLMOps or GenAI coverage.

### [Modal — serverless GPU/CPU platform (examples + pricing)](https://modal.com/docs/examples)

*Modal* &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 6-10 hours

THE cheapest realistic deployment target for a student in 2026. $30/month free covers roughly 187 hours of T4 or 27 hours of A10G, plus CPU web endpoints, cron jobs and autoscaling. The examples gallery is a working library: 'Deploy an OpenAI-compatible LLM service with vLLM', batched Whisper transcription, LoRA finetuning, Slackbots. Because it scales to zero, an idle demo costs nothing. Limitations to know: no custom domains and 1-day log retention on Starter.

> **Worth knowing.** This URL is examples only; pricing lives at modal.com/pricing, which is the load-bearing half if you are deciding whether you can afford GPU time. Vendor documentation, not a course — it teaches Modal, not portable deployment skills.

### [Prompt caching guide (OpenAI API docs)](https://developers.openai.com/api/docs/guides/prompt-caching)

*OpenAI developer documentation* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1-2 hours

Cost control is a named 2026 hiring criterion and this is the primary source for the single biggest lever. Concrete numbers you should be able to quote: cached input bills at 0.1x the uncached rate (a 90% discount); the minimum cacheable prefix is 1,024 tokens, so a 900-token system prompt never caches at all; on newer models cache writes cost 1.25x. Combine with batch endpoints (~50% off) for latency-tolerant work and cheap-model-first routing. Read the equivalent page for whatever provider you actually use — the mechanics differ in detail. One hour here changes how you structure every prompt you write.

### [Rules of Machine Learning: Best Practices for ML Engineering](https://developers.google.com/machine-learning/guides/rules-of-ml)

*Martin Zinkevich* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2-3 hours

43 rules, readable in an afternoon, and still the highest wisdom-per-minute document in the field. Rule #1 ('don't be afraid to launch a product without ML'), Rule #4 ('keep the first model simple and get the infrastructure right'), and the training/serving-skew sections are what separate someone who has thought about production from someone who has only trained models. It predates transformers entirely and that does not matter — it is about metrics, infrastructure, and organisational failure modes. Read it in week one, then re-read after your first deployment.

> **Worth knowing.** Timeless on process discipline but silent on anything LLM-related; its recent date stamp reflects a docs-platform refresh, not a rewrite.

### [vLLM documentation — quickstart and OpenAI-compatible server](https://docs.vllm.ai/en/stable/getting_started/quickstart.html)

*vLLM project* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 5-8 hours

89k stars and under very active development — the de facto open-model inference engine. The two things to learn: offline batched inference with the LLM class, and `vllm serve` producing an OpenAI-compatible /v1/chat/completions endpoint, which lets you swap a paid API for a self-hosted model without changing client code. Understanding PagedAttention and continuous batching well enough to explain WHY throughput improves is a strong interview signal. Requires Linux + GPU — do not try this on a Mac.

> **Worth knowing.** The /en/latest/ docs track the development preview rather than the shipped release; /en/stable/ matches the version you have installed.

### [What We Learned from a Year of Building with LLMs](https://applied-llms.org/)

*Eugene Yan, Bryan Bischof, Charles Frye, Hamel Husain, Jason Liu & Shreya Shankar* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-5 hours

Six practitioners, three parts: tactical (prompting, RAG, structured output), operational (data, team, workflow), strategic (when to build, when not to). Published June 2024, so treat the tooling references as historical — but the failure modes it names (skipping evals, over-abstracting with frameworks, no data inspection habit) are precisely the failure modes still killing 2026 projects. Free, and the fastest way to inherit a year of other people's scar tissue.

> **Worth knowing.** A 2024 retrospective being read in 2026: the strategy and operations material holds up, but the tactical layer is dated.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [aie-book — free companion resources for AI Engineering](https://github.com/chiphuyen/aie-book)

*Chip Huyen* &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-6 hours

17k stars, last pushed July 2026. Contains resources.md (a curated AI-engineering reading list), chapter summaries, study notes, prompt examples, case studies, and notes on hallucination mitigation. Use this to decide whether to buy the book, and as a living link-farm that is curated by a working practitioner, which keeps the signal high.

### [BentoML documentation](https://docs.bentoml.com/en/latest/)

*BentoML team* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 5-8 hours

8.8k stars, pushed August 2026. The Python-first, least-Kubernetes-flavoured way to package a model into a reproducible service with adaptive batching, model composition and one-command containerization. Worth 5-8 hours as the 'nicer developer experience' comparison point against a hand-rolled FastAPI + Dockerfile — being able to argue why you chose one over the other is more valuable than knowing either in depth. Lower priority than FastAPI and vLLM.

> **Worth knowing.** Vendor docs with a commercial funnel — much of the scaling material routes to the paid BentoCloud product.

### [DeepLearning.AI short courses: LLMOps, and Evaluating & Debugging Generative AI](https://www.deeplearning.ai/short-courses/evaluating-debugging-generative-ai/)

*Carey Phelps* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1-3 hours

Two production-specific picks from the catalogue introduced in the Chapter 5 resources, useful for the instrumentation habits (tracking, versioning, tracing training runs). Do not let them substitute for Hamel Husain and Shreya Shankar on evals.

> **Worth knowing.** Largely a Weights & Biases product tutorial; an hour of vendor tooling will not supply genuine LLM-evaluation methodology.

### [Full Stack Deep Learning 2022 + LLM Bootcamp 2023](https://fullstackdeeplearning.com/course/)

*Charles Frye, Sergey Karayev & Josh Tobin* &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 25-35 hours

Historically the best-credentialed production-ML course in existence, and the lectures on troubleshooting deep learning, ML project management, testing, and data-centric development are still excellent viewing. Note: the latest course iteration is 2022 and the LLM Bootcamp is April 2023 — the course-materials repo's last commit is 2021 and there has been no new iteration. Its LLMOps content predates modern agents, structured outputs, the entire evals literature, and current serving stacks. Watch the 'why' lectures (troubleshooting, project management, data-centric AI); ignore every tool recommendation. Replaced in practice by LLM Zoomcamp + Hamel/Shreya for the LLM half.

> **Worth knowing.** The 2023 LLM Bootcamp is a time capsule — its LLMOps and deployment sections are substantially superseded.

### [Introduction to Machine Learning Interviews Book](https://huyenchip.com/ml-interviews-book/)

*Chip Huyen* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-20 hours

Free, web-readable, and the deployment/production sections are more honest about what real interviews probe than most paid material. Good complement to the ByteByteGo book if you cannot spend money. Note it predates the LLM era, so supplement its modelling questions with current material.

> **Worth knowing.** Good for classical ML fundamentals and interview logistics, but it will not prepare you for an LLM/AI-engineering interview loop — pair it with something current if that is your target.

### [Machine Learning System Design Interview](https://www.amazon.com/Machine-Learning-System-Design-Interview/dp/1736049127)

*Ali Aminian & Alex Xu* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 15-20 hours

~280 pages, 211 diagrams, a 7-step framework and 10 worked ML system design problems (video recommendation, ad click prediction, visual search, harmful-content detection etc.). This is interview-shaped rather than job-shaped, and that is exactly why it earns a place: ML system design rounds are where junior candidates with good projects still fail. Use it as drilling material **after** *Designing Machine Learning Systems*, not instead of it — Huyen teaches you to think, Aminian/Xu teach you to perform under 45 minutes of pressure.

> **Worth knowing.** Three-year-old interview prep. Strong on classical ML system design, but it predates the GenAI and LLM topics that now make up half a modern interview loop.

### [Ray Serve documentation](https://docs.ray.io/en/latest/serve/index.html)

*Ray project* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6-10 hours

43.5k stars, pushed daily. The right tool once you need to **compose** models — multi-model pipelines, typed inter-service calls, autoscaling on queue depth — rather than serve one. Correct sequencing for a beginner: FastAPI or vLLM for a single model; Ray Serve only when you actually have branching or multiple models. Made With ML uses Ray throughout, so you will meet it there anyway. Learning it 'because it's on a roadmap' before you have a composition problem is wasted time.

> **Worth knowing.** The /en/latest/ path is the nightly development documentation and can describe APIs that do not exist in your installed release — use the stable, versioned docs instead.

### [Weights & Biases free courses (Effective MLOps, Model CI/CD, LLM Apps: Evaluation, RAG++)](https://wandb.ai/site/courses/)

*Weights & Biases AI Academy* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3-6 hours

Short, free, genuinely useful for specific gaps: 'Model CI/CD' and 'CI/CD for Machine Learning (GitOps)' fill the automation gap most self-taught people have; 'LLM Apps: Evaluation' and 'RAG++: From POC to Production' are decent second passes after Hamel/Shreya. Be clear-eyed that these are vendor courses designed to teach you W&B — the concepts transfer, the tool lock-in is real, and MLflow is the more common answer in job listings. Cherry-pick 2-3 courses; don't collect the set.

> **Worth knowing.** The MLOps courses are 2022-era and heavily tied to W&B tooling; the LLM-track courses (evaluation, RAG++, structured outputs) are the ones worth a beginner's time.

## Keep for reference

Not for reading end to end. Useful to have when you need to look something up.

### [DVC — Data Version Control](https://dvc.org)

*DVC maintainers* &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-6 hours

15.8k stars and still actively pushed (August 2026). The mental model is what matters: version tiny pointer files in Git, keep the actual data in object storage, and link each model artefact to its exact training data, params and pipeline. That lineage story answers 'how would you reproduce a model from three months ago?'. Many teams get 80% of the benefit from immutable, date-partitioned paths in S3 plus MLflow artefact logging.

> **Worth knowing.** The project has changed owners — treeverse/dvc is the current canonical repo — which is worth weighing as a stability consideration before adopting DVC.

### [Feast — the open source feature store (docs)](https://docs.feast.dev/)

*Feast maintainers / Feast open-source community* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-6 hours

7.2k stars, pushed daily, definitively not dead. But be honest about when it applies: the practical break-even for adopting a feature store is roughly 3-5 production models or 2+ ML teams sharing features — below that the operational overhead exceeds the consistency benefit. So for a beginner, spend 4-6 hours understanding the problem (training/serving skew, point-in-time correctness, online vs offline stores) and be able to discuss it; do not build your portfolio around Feast. Demonstrating point-in-time-correct feature joins by hand in Postgres is more impressive than a Feast tutorial.

> **Worth knowing.** A feature store is specialist infrastructure that a beginner shipping an AI MVP will never need, and Feast's commercial backing has thinned since Tecton's involvement wound down. Advanced, optional material.

### [Hugging Face Spaces documentation (hardware, pricing, lifecycle)](https://huggingface.co/docs/hub/en/spaces-overview)

*Hugging Face* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 1-2 hours

Included specifically as a **reality check**, because most 2023-2024 tutorials are now wrong. Per the current official docs: static Spaces are free for everyone, but 'Gradio and Docker Spaces run on compute and require a paid plan to create: PRO for personal accounts, Team or Enterprise for organisations', with the sole free exception that a personal account in good standing may host up to 2 Gradio Spaces on ZeroGPU. CPU Basic hardware still shows a $0.00 hourly rate, but you need a paid plan to **create** the compute-backed Space. Free hardware also sleeps when idle. Plan your $0 deployment around this, not around a blog post from 2023.

> **Worth knowing.** Deploying an MVP free on Spaces no longer holds for Gradio or Docker Spaces; the free paths are ZeroGPU (two Spaces) and Static Spaces only, so expect a paywall at the deploy step otherwise.

### [MLOps: Continuous delivery and automation pipelines in machine learning](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

*Google Cloud Architecture Center* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2 hours

The canonical 'MLOps level 0 / 1 / 2' maturity article that half the industry's slide decks are copied from. Two hours, and you will be able to place any team's practice on a shared scale and articulate what the next increment of automation would be — a very effective interview answer.

> **Worth knowing.** Two years old and classical-ML-shaped: it teaches the right vocabulary for training pipelines and the wrong mental model for LLM applications. Also vendor-framed toward Google Cloud and Vertex.

### [Practitioners Guide to MLOps (Google Cloud whitepaper)](https://cloud.google.com/resources/mlops-whitepaper)

*Google Cloud AI/ML team* &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-6 hours

The clearest vendor-published framing of the MLOps lifecycle, capability model, and the processes (experimentation, training operationalization, continuous training, model deployment, prediction serving, continuous monitoring, data & model management). Read it to acquire the vocabulary that appears in enterprise job descriptions. It is a reference document, not a tutorial — skim the capability model and the diagrams, don't grind it. Pair with the companion architecture article on MLOps maturity levels 0/1/2 (docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning).

> **Worth knowing.** Five years old and pre-LLM, and likely behind a lead-capture form. Useful only as canonical vocabulary for classical MLOps maturity levels, not as 2026 practice.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
