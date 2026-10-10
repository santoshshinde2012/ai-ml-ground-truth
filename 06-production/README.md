# Chapter 6: Running it in production

**Weeks 33–37 &nbsp;·&nbsp; about 55 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** Your Chapter 5 product becomes a system: containerised, tested on every push,
deployed, watched, and cheap enough to defend in a budget conversation. Little here is glamorous,
and its absence is what separates a demo from something a team would trust.

**From this week, [Chapter 8: Finding the work](../08-finding-the-work/README.md) runs alongside
this chapter and the next.** Open it now; the search it describes has a longer lead time than
anything left to build.

**In this chapter:** [Plan](#your-five-week-plan) &nbsp;·&nbsp; [Learn](#what-to-learn)
&nbsp;·&nbsp; [Build](#what-to-build) &nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp;
[Resources](#resources)

---

## Your five-week plan

About eleven hours a week. You are **finishing** the Chapter 5 app, not starting a new one.

| Week | Focus           | Do this                                                                      | Done when                                                          |
| ---- | --------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 33   | Docker + deploy | Multi-stage Dockerfile; deploy to chosen platform; health/readiness check    | Image size and cold start measured; dependencies justified         |
| 34   | CI              | GitHub Actions: pytest + data tests + versioned eval cases and release gates | A known regression is detected; repeated runs quantify uncertainty |
| 35   | Observability   | Structured logs; trace viewer; two actionable alerts; delayed-outcome join   | A decision can be traced to its release and eventual outcome       |
| 36   | Cost + rollback | Measure request cost and serving load; rehearse compatible release rollback  | Previous release and fallback work on recorded requests            |
| 37   | Incident        | Break on purpose; write incident report; model card with **do not use for**  | Report in repo                                                     |

---

## What you will be able to do

Containerise, deploy, monitor, roll back, and say what your system costs per thousand requests.

Most of this is expected rather than distinguishing. Its absence is noticed; its presence is
assumed. That is why it gets five weeks rather than twelve. The exception is **cost engineering**,
which very few people can discuss with numbers from a system they built themselves.

## What to learn

**Containers, and about forty per cent of Docker.** Images and layers, why your build is slow,
multi-stage builds, `.dockerignore`, sensible Dockerfile hygiene for Python, volumes, environment
variables and secrets, and Compose for local work. Keep a small CPU/API application lean, and
inspect large layers for unused dependencies. GPU runtimes and model weights can legitimately
require larger images; judge size alongside build time, cold start and deployment constraints.

Choose one deployment environment you can operate within your budget. A container service or
serverless API is enough for this chapter; a local container with a recorded load test is an honest
fallback when hosting is unavailable. Learn Kubernetes when a target role or an actual requirement
calls for it, rather than making a cluster a prerequisite for the first release.

**Continuous integration that means something.** Run your tests, your **data** tests (schema
assertions, range checks, point-in-time/label-maturity checks, group separation when the evaluation
requires unseen entities) and **evaluation assertions** on every push. Put deterministic checks such
as output schemas, permissions and forbidden tool actions in the fast suite. Run a bounded quality
suite on pull requests and a larger suite before release. Fix the dataset and scorer versions,
compare against the current release on the same cases, repeat stochastic runs, and report
uncertainty and important slices. Set a minimum useful quality difference and the release rule
before seeing the result; a noisy one-point judge fluctuation should not masquerade as a reliable
regression.
[MLflow's regression-testing workflow](https://mlflow.org/docs/latest/genai/eval-monitor/regression-testing/)
shows how to record tests and traces, but the scoring design remains your responsibility.

Version prompts, retrieval settings, tool schemas, decoding settings and model identifiers with the
application. Keep a held-out evaluation set for release decisions: continually tuning on the same
public benchmark or failure queue eventually fits that evaluation. Validate automated judges against
a blinded human-labeled sample, track disagreement by failure type, and recalibrate when either the
judge or task changes. A judge's model upgrade is an evaluation change too. Once release cases
influence fixes or thresholds, treat them as development evidence and acquire fresh independent
release cases; a private holdout can be overfit just like a public benchmark.

**A rollback runbook.** Write it, then rehearse it. Define alert ownership, the compatible previous
release, a fallback, and the evidence that tells you recovery succeeded. Fill the placeholders below
using a load test and the product's error tolerance, including minimum sample sizes for quality
signals. Immediate security or action-execution failures can need a different response from a slowly
arriving statistical quality signal.

```markdown
# Rollback runbook — [service name]

## When to use this

- Alert: [quality measure] crosses [declared bound] with [minimum sample/window]
- Alert: p95 latency above [service objective] for [window] at [minimum traffic]
- Immediate stop: [unauthorized action / invalid price / duplicate delivery condition]
- Manual: user reports systematic wrong answers

## Roll back application

1. Redeploy previous immutable image: `[registry]/app:[last-good-tag-or-digest]`
2. Confirm readiness and replay [recorded smoke cases]; verify feature and output schemas

## Roll back decision release

1. Select [previous release manifest]: compatible model, features, calibrator and policy
2. Load and validate the complete release; route requests after its readiness check passes
3. Replay [recorded decisions]; preserve current access/revocations, constraints and freshness checks
4. Confirm fallback and idempotency before resuming actions

## Kill switch

- Disable new model-driven actions with [delivery feature flag]; pause action workers/outbox consumers
- Reconcile in-flight actions before retrying or resuming; a timeout does not prove nondelivery
- For read-only LLM responses, disable `LLM_ENABLED` or route to the approved static fallback

## Who to notify

- [Your name / on-call channel]

## After rollback

- Open incident doc; attach traces from first failing request
```

**Serving.** FastAPI is a reasonable API starting point; daily business decisions can use a batch
job. For self-hosted language models, compare a supported engine such as vLLM or SGLang against your
workload and hardware. Learn how KV-cache allocation, continuous batching and queueing affect
memory, throughput and latency. Record arrival rate, concurrency, input/output lengths, time to
first token, time per output token, p95 end-to-end latency, failures and cost per successful task.
Define the load at which the service still meets its objectives, rather than reporting maximum
tokens per second with unusable latency.
[vLLM's serving benchmark](https://docs.vllm.ai/en/stable/cli/bench/serve/) provides a starting
harness; include the warmup and runtime configuration in your report.

Separate process liveness from readiness to serve a compatible, loaded release. Load artifacts and
required resources before accepting traffic; FastAPI's
[lifespan guide](https://fastapi.tiangolo.com/advanced/events/) demonstrates model startup and
cleanup. Bound queues and request deadlines under overload, and test the fallback before the
caller's deadline. Adding retries to an already overloaded service can increase its load; count them
in both capacity and cost measurements.

Optimization is conditional. Prefix caching needs reusable prefixes; quantization needs supported
kernels and a quality check; speculative decoding adds draft work and is workload dependent. The
[current vLLM speculative-decoding guide](https://docs.vllm.ai/en/stable/features/speculative_decoding/)
targets memory-bound, medium-to-low request-rate workloads. Test a single change under your load
before adopting it. Distributed serving belongs here only when the simpler deployment cannot meet
the declared requirement.

**Monitoring.** For classical models: input distributions, prediction distributions and drift, with
the awareness that labels often arrive weeks late. For language-model applications: traces,
tool-call failure rates, evaluation pass rate on a live sample, cost and latency. Check upstream
freshness, schema changes and join coverage early: a broken pipeline can look like model drift. An
input distribution alert diagnoses a change, not its effect on prediction quality. Tie quality
alerts to outcomes once those outcomes are available.

An agent also needs repeated-task consistency, sensitivity to small input changes, correct
escalation, and unauthorized-action checks. The peer-reviewed ICML 2026 paper
[Towards a Science of AI Agent Reliability](https://proceedings.mlr.press/v306/rabanser26a.html)
separates reliability from average task accuracy; use that framing to build tests for your own
permissions and failure costs, rather than adopting a benchmark score as a production guarantee.

For business ML, join outcomes to the original `decision_id` and report only mature cohorts. Track
feature freshness, missingness, calibration, precision at contact capacity, demand errors, margin,
budget use, opt-outs and action delivery. Compare the policy against its control group. A falling
input-drift score is not evidence of improving business value. See
[Chapter 9's delivery plan](../09-business-machine-learning/delivery-plan.md) for the full feedback
path.

Alert on things that mean act now, and keep the list short. An alert nobody acts on trains everyone
to ignore the channel.

**Reproducibility.** Record code, immutable data/split versions, configuration, dependencies,
hardware/runtime, random state and checkpoints. A commit hash cannot reconstruct a changing
customers table, a deleted API response or an unversioned prompt. Include query and snapshot
cutoffs, source licenses and the commands needed to recover artifacts. For an API model, save the
provider model identifier, settings and recorded evaluation outputs; exact retraining or replay of a
changing hosted model may be unavailable.

Be precise about which level you are claiming. _Rerunnable_ means the command works today.
_Reproducible within a declared tolerance_ means reruns meet a specified metric range on the same
evaluation; report the runs that establish that range. _Bit-identical_ requires stronger control and
is not guaranteed across platforms or releases even after seeding.
[PyTorch reproducibility notes](https://docs.pytorch.org/docs/2.14/notes/randomness.html).

**The classical ML lifecycle.** Schedule extraction, snapshot construction, training, evaluation and
batch scoring as explicit jobs with dependency checks and retries. Persist preprocessing with the
model and compare batch and online features on recorded requests. Each release needs data/query
versions, training cutoff, feature schema, metrics and an immutable artifact identifier. A simple
manifest works first; a registry adds managed versions and aliases when several models need it
([MLflow's registry workflow](https://mlflow.org/docs/latest/ml/model-registry/workflow/)).

Pin one complete release manifest for each request or batch, including preprocessing, model,
calibrator, decision policy and any retrieval index. Prepare and validate the next release before
routing traffic to it; workers must not mix independently refreshed components within one decision.
After retraining or changing score semantics, recheck calibration and decision thresholds on data
separate from model fitting before promotion. Rolling back artifacts still obeys current
permissions, revocations, costs and operational constraints.

Serve risk scores in batch if a team acts once a day; use an API where a session genuinely needs a
decision. Check authentication, request limits, fresh features and graceful fallback in either case.
Shadow a new policy, verify outputs, then canary it with explicit stop conditions. On an alert,
inspect data and label freshness before retraining. Evaluate a challenger on recent mature cohorts
and the preserved benchmark, then promote only if the declared quality, business and latency gates
pass. Recalibration, data repair or rollback may be the right fix instead of a new model.

**Feedback is a data product.** Log eligibility, the chosen action, policy version, execution status
and assignment probability when randomized, then reconcile outcomes and label availability. Keep
training examples and evaluation cohorts separate as they mature. User ratings and model judgments
are useful diagnostic signals, but selected feedback is not an unbiased estimate of product
performance. Sending a retention offer or changing a price also changes later training data;
maintain an appropriate control or exploration design to measure incremental effects. For LLM
applications, sample successful as well as failed traces, redact sensitive content, have a person
verify proposed labels, and route approved cases into a versioned development set. Keep access,
retention and deletion rules with the trace pipeline.

**Durable actions, when the application can write.** Commit the validated decision and a pending
delivery record together before dispatch. A transactional outbox is one pattern for avoiding a
database-write/message-send gap; the
[AWS design guide](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)
also requires handling duplicate delivery. Reuse the business operation ID, check the destination's
idempotency contract, and reconcile unknown outcomes after a timeout. If a destination cannot
deduplicate or report its state, stop for reconciliation rather than promising exactly-once effects.
Test crashes before dispatch and after the remote effect but before its acknowledgement. This is an
extension for action-capable systems; the Chapter 5 read-only sprint does not need an action worker.

**Cost.** Take one working feature and produce a real table: baseline cost per thousand requests,
then the effect of restructuring the prompt so the static prefix caches, routing easy requests to a
cheaper model, and moving latency-tolerant work to a batch endpoint. Report the evaluation pass rate
alongside each variant, because a cost reduction that quietly degrades quality is the classic trap.

| Variant                              | Cost / 1k requests | Eval pass rate | Notes                                                                   |
| ------------------------------------ | ------------------ | -------------- | ----------------------------------------------------------------------- |
| Baseline (single model, full prompt) | $2.40              | 71%            | No caching                                                              |
| Cached static prefix (~2k tokens)    | $1.10              | 71%            | Measure eligible tokens, hit rate and model-specific read/write charges |
| Route easy queries to smaller model  | $0.85              | 68%            | Check quality drop before shipping                                      |
| Batch endpoint for async work        | $0.55              | 71%            | Use the provider's asynchronous deadline; record observed turnaround    |

Fill in your own numbers from provider logs — treat any figure in a tutorial, including this table,
as a placeholder until you measure.

Provider details belong in the experiment configuration. OpenAI's
[prompt-caching guide](https://developers.openai.com/api/docs/guides/prompt-caching) describes
exact-prefix reuse, but minimums, retention and read/write pricing depend on model generation and
settings. Do not budget using a universal discount. Its
[Batch API](https://developers.openai.com/api/docs/guides/batch) currently offers a 50% discount for
supported work with a 24-hour completion window. A batch can expire with partial results; reconcile
successes and request-level errors by `custom_id`, not output order, before retrying unfinished
work. Measure turnaround rather than promising interactive latency. Count retries, tool calls, judge
usage, storage and idle compute when comparing alternatives.

For self-hosting, the honest answer is arithmetic rather than preference: compare API cost per month
against GPU hours including idle time plus the engineering hours to run it, and find the request
volume where the lines cross. Knowing how to do that calculation matters more than which side you
land on.

## Resources

The annotated resources are in **[resources/](resources/README.md)**. Use the selected sections for
the 55-hour plan; full courses and distributed systems depth are optional extensions.

The ones to begin with:

- [Docker documentation — Get started, and the Python guide](https://docs.docker.com/get-started/) —
  Docker documentation team. Free documentation, 4–6 hours. Week 33.
- [FastAPI official documentation and tutorial](https://fastapi.tiangolo.com/) — Sebastián Ramírez.
  Free documentation, 2–4 hours of selected API/testing work; use your existing endpoint.
- [GitHub Actions documentation](https://docs.github.com/en/actions) — GitHub documentation team.
  Free documentation, 3–5 hours of selected Python CI work. Week 34.
- [Prompt caching guide](https://developers.openai.com/api/docs/guides/prompt-caching) — OpenAI
  developer documentation. Free, 1–2 hours; read your own provider's equivalent too. Week 36.

## What to build

Take the application from [Chapter 5](../05-language-models/README.md) and finish it properly: a
multi-stage Dockerfile, CI running tests and evaluations, deployment within a declared budget,
redacted structured request logs, a small dashboard, two alerts you would actually act on, a
rollback runbook, a cost table, and a model card. A model card is a one-page note on what the system
is for, what it was evaluated on, and what it should **not** be used for.

Then break it on purpose and write a short incident report: what you injected, how long detection
took, what fired, how you rolled back, and what you would change. That document is worth more than
another model in a portfolio, because very few people have one.

## Before you move on

- You can write a multi-stage Dockerfile from memory.
- You can rerun training from the release manifest within a declared metric tolerance, or explain
  the limits of replaying a hosted model.
- You can show your dashboard and justify each alert.
- You can read your incident report and your cost table out loud.
- You can trace a decision to its features, model and eventual outcome, and rehearse a fallback on
  stale data.

## A few things worth knowing

- **Deploy on day one of the week, not day five.** The first deploy always surfaces something: a
  missing system library, a secret that was only in your shell, a port that is not exposed. Finding
  that on Monday leaves the week for fixing it.
- **Inspect image size.** `docker history` identifies large layers; distinguish required GPU
  runtimes and weights from unused build tools, caches or training data. Measure cold start after
  changing the image rather than assuming a smaller image always fixes latency.
- **Secrets never go in the image.** Pass them in at run time as environment variables or from the
  platform's secret store, keep a `.env.example` with the names but no values, and check that
  `.dockerignore` and `.gitignore` both exclude the real file.
- **Document applicable obligations with an owner.** Scope depends on the intended use, where the
  system is used, and the organization's provider/deployer role. For an EU-facing release, consult
  the
  [Commission's current AI Act guidance](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
  and applicable enacted text when assessing classification, transparency and dates. Record the
  assessment and unresolved questions; a model card alone does not establish compliance. The roadmap
  does not treat every application as high risk or a proposed timeline change as enacted law.

---

[Previous: Language models and AI engineering](../05-language-models/README.md) &nbsp;·&nbsp;
[Next: Choosing a specialisation](../07-specialisation/README.md)
