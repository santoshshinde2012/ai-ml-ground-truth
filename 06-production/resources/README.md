# Resources — Chapter 6: Running it in production

Resources for [the chapter](../README.md). Use selected documentation sections to finish the same
application within the 55-hour plan. Full courses and additional infrastructure are optional; hours
below are learner estimates rather than provider commitments.

Official guidance was checked on **9 October 2026**. Pin tool versions, record your workload and
consult current pricing before spending. Project/vendor benchmarks and feature announcements do not
establish reliability, cost or performance for your service.

**Browse:** [Start here](#start-here) &nbsp;·&nbsp; [Optional depth](#optional-depth) &nbsp;·&nbsp;
[Keep for reference](#keep-for-reference)

---

## Start here

### [Docker — Get started](https://docs.docker.com/get-started/)

_Docker documentation team_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 4–6 hours

Build and run the application's container, use a multi-stage build where useful, and inspect layers,
startup, health checks and secret injection. Record the image digest and deploy that artifact. A
working local container is the first deliverable; hosting credits are not assumed.

### [FastAPI — Testing](https://fastapi.tiangolo.com/tutorial/testing/)

_FastAPI maintainers_ &nbsp;·&nbsp; Official tutorial &nbsp;·&nbsp; 2–4 hours of selected
API/testing work

Use the request-validation and testing sections with your existing endpoint. Test normal and invalid
inputs, model readiness, timeouts and the chosen fallback. Keep a recorded request that links the
served output to the compatible feature/model release; endpoint availability alone does not
establish model quality. Use the [lifespan guide](https://fastapi.tiangolo.com/advanced/events/) for
loading and cleaning up model resources. Test that traffic reaches only a ready release and that
overload has a bounded deadline and fallback.

### [GitHub Actions — Building and testing Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)

_GitHub documentation team_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 3–5 hours

Pin Python and dependencies, run tests and save reports as artifacts. Add deterministic data and
permission checks plus a bounded evaluation job. A known broken schema or forbidden action should
fail reliably; stochastic quality comparisons need repeated runs and a declared decision rule.

### [MLflow — Experiment tracking](https://mlflow.org/docs/latest/ml/tracking/)

_MLflow project_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–3 hours

Track code/data/configuration identifiers, metrics and artifacts for the existing model. Use one run
to reconstruct its training and evaluation rather than treating a dashboard as lineage. Pin the
client/server versions and capture the exact data and split manifest.

### [MLflow — LLM and agent evaluation](https://mlflow.org/docs/latest/genai/eval-monitor/)

_MLflow project_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–3 hours

Use versioned cases, recorded traces and code-based or model-based scorers to compare two
application versions. Include retrieved evidence and tool actions when the final answer is not
enough. Verify a judge on human-labeled examples; an evaluation API does not validate the labels or
the rubric for you.

### [MLflow — Regression testing and CI/CD](https://mlflow.org/docs/latest/genai/eval-monitor/regression-testing/)

_MLflow project_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 1–2 hours

Connect a small evaluation suite to pytest and inspect the recorded failing case. Use exact
assertions for deterministic requirements and predeclared statistical gates for uncertain quality
measures. Keep a separate release set when failed cases are repeatedly added to the development
suite.

### [Langfuse documentation](https://langfuse.com/docs)

_Langfuse maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–3 hours

An alternative tracing and evaluation stack to inspect, not another mandatory platform. Trace one
request across retrieval, model and tools; join latency, tokens, cost and feedback. Set sampling,
redaction, access and retention explicitly. Compare hosted and self-hosted operation under current
terms without assuming any fixed free-tier quota.

### [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)

_OpenTelemetry project_ &nbsp;·&nbsp; Official specification repository &nbsp;·&nbsp; 1–2 hours

The current project repository defines GenAI spans, metrics and events; the old OpenTelemetry
`semconv/gen-ai` documentation page is marked moved and unmaintained. Use the repository to design
interoperable telemetry, and pin the convention/instrumentation version while the interfaces evolve.
Avoid recording raw prompts or tool arguments by default when they can contain sensitive data.

### [OpenAI — Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)

_OpenAI_ &nbsp;·&nbsp; Official developer documentation &nbsp;·&nbsp; 1 hour plus measurement

Study exact-prefix reuse and the minimum, retention and read/write pricing for the actual model.
Place reusable content where it can match and measure cache-hit usage, cost and latency. Caching
rules differ across model generations; a universal token threshold or discount is an unsafe budget
assumption. Use your provider's equivalent when the application uses another API.

### [OpenAI — Batch API](https://developers.openai.com/api/docs/guides/batch)

_OpenAI_ &nbsp;·&nbsp; Official developer documentation &nbsp;·&nbsp; 1 hour plus measurement

For supported asynchronous work, the current guide specifies a 50% discount and a 24-hour completion
window. A batch can expire with completed and unfinished requests. Reconcile output/error files by
`custom_id`, not position, and retry only unfinished work; measure actual turnaround. Batch requests
are suitable only when the product's deadline allows them. Record the model and price date in your
cost table.

## Optional depth

Add a tool when it resolves a requirement in your current system.

### [vLLM — Serving benchmark](https://docs.vllm.ai/en/stable/cli/bench/serve/)

_vLLM maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–4 hours with a load test

Measure the supported model on your hardware and representative input/output lengths. Record request
rate, concurrency, time to first token, time per output token, end-to-end latency, errors and
throughput at the service objective. Preserve runtime settings and warmup. The highest throughput at
an overloaded queue is not the capacity you can offer users.

### [PagedAttention](https://arxiv.org/abs/2309.06180)

_Woosuk Kwon and colleagues_ &nbsp;·&nbsp; Primary paper first released in September 2023
&nbsp;·&nbsp; 2–3 hours

Read the KV-cache memory-management design behind the original vLLM work. Explain why avoiding
wasted cache memory can allow more useful batching, then measure your current engine. Historical
speedups depend on the paper's baselines and hardware; they do not describe every current model or
deployment.

### [vLLM — Speculative decoding](https://docs.vllm.ai/en/stable/features/speculative_decoding/)

_vLLM maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 1–2 hours plus measurement

The current guide targets reducing inter-token latency for memory-bound, medium-to-low-QPS
workloads. Check supported methods and feature incompatibilities, then compare accepted draft
tokens, quality and latency under load. Extra draft work can fail to pay off; keep the baseline when
the measured workload does not benefit.

### [SGLang documentation](https://docs.sglang.io/)

_SGLang maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–4 hours of selected
sections

A serving-engine alternative to benchmark when its supported models and hardware fit. Read the
deployment and performance guidance, pin the runtime, and reuse the same load and quality tests used
for vLLM. Choose by measured task performance and operating requirements, rather than a project
headline.

### [Ray Serve](https://docs.ray.io/en/latest/serve/index.html)

_Ray maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 3–5 hours

Inspect deployment composition, scaling and request handling when the application needs several
services or replicas. Compare with the existing simple API before adding a distributed runtime.
Rehearse failure and recovery behavior; configuration that scales a demo does not establish capacity
or resilience under your workload.

### [Feast — Point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)

_Feast maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 1–2 hours

Read historical feature retrieval against entity timestamps and TTL. Construct one training snapshot
and verify it contains only information available at the decision. Point-in-time retrieval is
necessary but may also need explicit ingestion/availability timestamps and mature labels. A
warehouse query can implement the first version; a feature store is not a prerequisite.

### [DVC — Pipeline files](https://doc.dvc.org/user-guide/project-structure/dvcyaml-files)

_DVC maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–3 hours

Declare stages, inputs, parameters and outputs for a small reproducible pipeline. Record a data
artifact's actual version rather than only its path, and confirm another environment can retrieve
it. DVC is one option; an immutable-storage manifest can also be enough for a first project.

### [Dagster — Assets](https://dagster.io/docs/guides/build/assets)

_Dagster maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–3 hours

Model extraction, snapshots, training and scores as explicit dependencies with freshness and failure
handling. Run one deliberately failed upstream stage and ensure downstream actions do not silently
use stale outputs. Use the simplest scheduler that meets the project's recovery and lineage needs;
this is an optional implementation choice.

### [Evidently documentation](https://docs.evidentlyai.com/introduction)

_Evidently maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–3 hours

Create a report for feature/prediction changes and outcome quality once labels mature. Define a
reference period and useful slices, and interpret sample size and seasonality. Input drift is an
investigation signal; it neither proves reduced business value nor tells you that automatic
retraining will fix the cause.

### [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp)

_DataTalks.Club instructors and contributors_ &nbsp;·&nbsp; Free course repository &nbsp;·&nbsp;
Selected modules here

Use the tracking, deployment, monitoring and best-practices material to close a gap in the existing
classical-ML pipeline. Follow the repository's environment and project instructions, pin its commit,
and verify current dependency APIs. A full course project is extra work rather than an additional
requirement in these five weeks.

### [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)

_DataTalks.Club instructors and contributors_ &nbsp;·&nbsp; Free course repository &nbsp;·&nbsp;
Selected modules here

Use the evaluation, monitoring and application material for your existing LLM product. Adapt its
exercises to your documents and failure cases rather than opening another tutorial repository.
Cohort dates and hosted services change; the durable learning artifact is the versioned application,
evaluation and feedback loop.

## Keep for reference

### [MLflow — Model registry workflows](https://mlflow.org/docs/latest/ml/model-registry/workflow/)

_MLflow project_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 1–2 hours

Use versions and aliases when several releases need managed promotion. Keep a release manifest with
compatible preprocessing, feature contract, model, calibrator, policy and evaluation. Switching a
model alias alone is insufficient when the rest of the decision interface changed. Load a complete
compatible release and pin it for each request or batch. Artifact rollback still obeys current
access revocations and operating constraints. For write-capable extensions, the
[transactional-outbox guide](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)
explains the database/message consistency problem and duplicate-delivery handling; destination
idempotency and reconciliation remain necessary.
[Chapter 9's delivery plan](../../09-business-machine-learning/delivery-plan.md) supplies the
business-action and mature-outcome gates.

### [PyTorch — Reproducibility](https://docs.pytorch.org/docs/2.14/notes/randomness.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Versioned official documentation &nbsp;·&nbsp; 1 hour

Pin environment and device, control relevant random sources and declare the reproducibility
tolerance supported by repeated runs. Reproducibility across releases or platforms is not
guaranteed. Keep full training checkpoints and immutable data versions alongside code.

### [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems)

_D. Sculley and colleagues_ &nbsp;·&nbsp; Peer-reviewed NeurIPS 2015 paper &nbsp;·&nbsp; 1–2 hours

A foundational account of data dependencies, feedback loops and system maintenance. Map one
dependency and one feedback loop in your own product, then add a check or owner. Use it to reason
about current systems; it predates today's LLM tooling and does not prescribe a particular modern
stack.

### [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/)

_Google SRE authors_ &nbsp;·&nbsp; Free online book &nbsp;·&nbsp; 2–4 hours of selected chapters

Read service objectives, monitoring and incident response. Convert a product requirement into an
actionable latency/error target and rehearse the rollback. A model-quality signal with delayed
labels needs different evidence and timing from an immediate availability failure.

### [OWASP LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)

_OWASP GenAI Security Project_ &nbsp;·&nbsp; Official community guidance, 3 August 2026
&nbsp;·&nbsp; 2–3 hours

Select threats that match the application's tools and data boundaries, then implement attack cases
and check the recorded actions. Track both authorized-task completion and forbidden-action failures.
The risk list is guidance, not a certification that a system resists injection or misuse.

### [NIST AI RMF — Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

_NIST_ &nbsp;·&nbsp; Official July 2024 profile, NIST AI 600–1 &nbsp;·&nbsp; 1–2 hours of selected
sections

Use the profile to identify risks, owners and measurement gaps relevant to the actual application.
Connect the selected risks to evaluation and incident handling rather than copying a checklist into
a model card. This is risk-management guidance, not a substitute for applicable obligations.

### [European Commission — AI Act guidance](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)

_European Commission_ &nbsp;·&nbsp; Official guidance &nbsp;·&nbsp; Lookup reference

For an EU-facing product, check intended use, provider/deployer role and the current applicable text
and implementation schedule with the responsible owner. Distinguish an enacted obligation from a
proposal or political agreement. Record the assessment; a generic chapter summary cannot classify
every system or establish compliance.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
