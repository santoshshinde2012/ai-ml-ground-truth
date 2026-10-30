# Chapter 6: Running it in production

**Weeks 33–37 &nbsp;·&nbsp; about 55 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** Your Chapter 5 product becomes a system: containerised, tested on every push,
deployed, watched, and cheap enough to defend in a budget conversation. Little here is glamorous,
but it separates a demo from something a team would trust.

**From this week, [Chapter 8: Finding the work](../08-finding-the-work/README.md) runs alongside
this chapter and the next.** Open it now. The search it describes takes longer to pay off than
anything left to build.

**In this chapter:** [Plan](#your-five-week-plan) &nbsp;·&nbsp; [Learn](#what-to-learn)
&nbsp;·&nbsp; [Build](#what-to-build) &nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp;
[Resources](#resources)

---

## Your five-week plan

About eleven hours a week. You are **finishing** the Chapter 5 app, not starting a new one. Bring
the [Chapter 3](../03-core-machine-learning/README.md) model along. Its saved bundle and API go
through the same container build, CI, release manifest, monitoring and rollback in these weeks. The
retraining, decision-tracing and stale-feature checks at the end of the chapter use that classical
model. If nothing needs a live decision, a scheduled batch-scoring job can replace its API.

| Week | Focus           | Do this                                                                      | Done when                                                          |
| ---- | --------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| 33   | Docker + deploy | Multi-stage Dockerfile; deploy to chosen platform; health/readiness check    | Image size and cold start measured; dependencies justified         |
| 34   | CI              | GitHub Actions: pytest + data tests + versioned eval cases and release gates | A known regression is caught; repeated runs show the uncertainty   |
| 35   | Observability   | Structured logs; trace viewer; two actionable alerts; delayed-outcome join   | A decision can be traced to its release and eventual outcome       |
| 36   | Cost + rollback | Measure request cost and serving load; rehearse compatible release rollback  | Previous release and fallback work on recorded requests            |
| 37   | Incident        | Break on purpose; write incident report; model card with **do not use for**  | Report in repo                                                     |

---

## What you will be able to do

Containerise, deploy, monitor, roll back, and say what your system costs per thousand requests.

Most of this will not set you apart. People notice its absence and assume its presence. That is why
it gets five weeks, not twelve. The exception is **cost engineering**, which very few people can
discuss with numbers from a system they built themselves.

## What to learn

### Worked lesson: a timeout is an unknown outcome

Your service asks a destination to issue a voucher with operation ID `retention-42`. The destination
issues it, but the acknowledgement is lost. Retrying with a new ID can issue another voucher. A
local timeout is a fact about the response, not proof that the remote action failed.

This tiny fake destination shows a business idempotency contract:

```python
issued = {}

def issue_voucher(operation_id, amount):
    if operation_id in issued:
        if issued[operation_id]["amount"] != amount:
            raise ValueError("same operation ID with different arguments")
        return issued[operation_id]
    result = {"voucher_id": f"voucher-{len(issued) + 1}", "amount": amount}
    issued[operation_id] = result
    return result

first = issue_voucher("retention-42", 10)
retry = issue_voucher("retention-42", 10)
assert first == retry and len(issued) == 1
```

The dictionary is for teaching only. Real delivery needs durable state, atomic handling of
concurrent requests, retained deduplication keys, and the destination's documented idempotency and
reconciliation behaviour. A transactional outbox closes the local gap between decision and dispatch.
On its own, it cannot deduplicate a remote service's effects.

**Try it yourself.** The worker crashes after the voucher is issued but before its local delivery
row is marked complete. What should it save before dispatch? Which key should it reuse? What
should happen if the destination cannot report or deduplicate the operation?

<details>
<summary>Hint and explained answer</summary>

Before dispatch, save the validated decision and pending delivery record atomically, with the
business operation ID and exact arguments. Retry or query with that same ID, and mark completion
after reconciliation. If the destination cannot deduplicate or show its state, stop automatic
retries and reconcile the unknown outcome. A new key, or treating the timeout as nondelivery, does
not make the operation safe. Rehearse both crash windows with a fake destination.

</details>

### Core operations and optional systems depth

Finish one deploy, regression command, monitored failure and rollback before trying distributed
serving or framework optimisations. The [reference lab](../labs/README.md) gives a deterministic
starting point. Production claims still need measurements from your own system.

**Containers, and about forty per cent of Docker.** Images and layers, why your build is slow,
multi-stage builds, `.dockerignore`, sensible Dockerfile hygiene for Python, volumes, environment
variables and secrets, and Compose for local work. Keep a small CPU/API application lean, and check
large layers for unused dependencies. GPU runtimes and model weights can genuinely need larger
images. Judge size alongside build time, cold start and deployment limits.

Choose one deployment environment you can run within your budget. A container service or serverless
API is enough for this chapter. If hosting is unavailable, a local container with a recorded load
test is a fair fallback. Learn Kubernetes when a target role or real requirement calls for it. A
first release does not need a cluster.

**Continuous integration that means something.** On every push, run your tests, your **data** tests
(schema assertions, range checks, point-in-time and label-maturity checks, group separation when the
evaluation needs unseen entities) and **evaluation assertions**. Put deterministic checks such as
output schemas, permissions and forbidden tool actions in the fast suite. Run a bounded quality
suite on pull requests and a larger one before release. Fix the dataset and scorer versions, and
compare against the current release on the same cases. Repeat stochastic runs, and report
uncertainty and important slices. Set the smallest useful quality difference and the release rule
before seeing the result. A noisy one-point judge wobble should not pass for a real regression.
[MLflow's regression-testing workflow](https://mlflow.org/docs/latest/genai/eval-monitor/regression-testing/)
shows how to record tests and traces. The scoring design is still your job.

Keep workflow permissions minimal. Checks get read-only repository access, and only the deployment
job gets deployment access. Run untrusted pull-request code without production secrets. Do not use a
privileged workflow trigger to check out and run a contributor's branch. Pin third-party actions to
reviewed commit SHAs, lock dependencies, and load model artifacts only from trusted, recorded
sources. A passing test suite cannot make an untrusted build artifact safe.

Loading an artifact can execute it. Pickle-based files, including `joblib` bundles and full PyTorch
checkpoints, can run arbitrary code on load. Check the recorded hash first, and never unpickle an
untrusted file. For weights, prefer [safetensors](https://huggingface.co/docs/safetensors/index), or
`torch.load` with `weights_only=True`, the default since PyTorch 2.6
([serialisation notes](https://docs.pytorch.org/docs/2.14/notes/serialization.html)). That narrows
the risk but does not remove it. scikit-learn's
[persistence guide](https://scikit-learn.org/stable/model_persistence.html) compares safer formats.

Version prompts, retrieval settings, tool schemas, decoding settings and model identifiers with the
application. Keep a held-out evaluation set for release decisions. Repeated tuning on the same
public benchmark or failure queue eventually fits that evaluation. Check automated judges against a
blinded human-labelled sample, track disagreement by failure type, and recalibrate when the judge or
task changes. Upgrading the judge's model is an evaluation change too. Once release cases shape
fixes or thresholds, treat them as development data and collect fresh, independent release cases. A
private holdout can be overfit just like a public benchmark.

**A rollback runbook.** Write it, then rehearse it. Define alert owners, the compatible previous
release, a fallback, and the signal that shows recovery worked. Fill the placeholders below from a
load test and the product's error tolerance, including minimum sample sizes for quality signals. An
immediate security or action-execution failure can need a different response from a slowly arriving
statistical quality signal.

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

**Serving.** FastAPI is a reasonable API starting point. Daily business decisions can use a
batch job. For self-hosted language models, compare a supported engine such as vLLM or SGLang on
your workload and hardware. Learn how KV-cache allocation, continuous batching and queueing affect
memory, throughput and latency. Record arrival rate, concurrency, input/output lengths, time to
first token, time per output token, p95 end-to-end latency, failures and cost per successful task.
Report the load at which the service still meets its objectives, not peak tokens per second at
unusable latency. [vLLM's serving benchmark](https://docs.vllm.ai/en/stable/cli/bench/serve/) gives
a starting harness. Include the warmup and runtime configuration in your report.

Separate process liveness from readiness to serve a compatible, loaded release. Load artifacts and
required resources before accepting traffic. FastAPI's
[lifespan guide](https://fastapi.tiangolo.com/advanced/events/) shows model startup and cleanup.
Bound queues and request deadlines under overload, and test that the fallback answers before the
caller's deadline. Retries on an overloaded service can add to its load, so count them in both
capacity and cost measurements.

A hosted model is a dependency that can fail. Set a client timeout inside the caller's deadline.
Retry only safe calls, with bounded backoff, and respect rate-limit responses. Decide what users see
during a provider outage: a cached or static answer, a queued job, or a clear "unavailable" message.
Rehearse it by blocking the provider endpoint, and record what the user actually saw.

Optimisation is conditional. Prefix caching needs reusable prefixes. Quantisation needs supported
kernels and a quality check. Speculative decoding adds draft work and depends on the workload. The
[current vLLM speculative-decoding guide](https://docs.vllm.ai/en/stable/features/speculative_decoding/)
targets memory-bound, medium-to-low request-rate workloads. Test one change under your load
before adopting it. Use distributed serving only when the simpler deployment cannot meet the
declared requirement.

**Monitoring.** For classical models, watch input distributions, prediction distributions and drift,
knowing that labels often arrive weeks late. For language-model applications, watch traces,
tool-call failure rates, evaluation pass rate on a live sample, cost and latency. Check upstream
freshness, schema changes and join coverage early, because a broken pipeline can look like model
drift. An input distribution alert shows a change, not its effect on prediction quality. Tie quality
alerts to outcomes once those outcomes are available.

An agent also needs repeated-task consistency, sensitivity to small input changes, correct
escalation, and checks for unauthorised actions. The peer-reviewed ICML 2026 paper
[Towards a Science of AI Agent Reliability](https://proceedings.mlr.press/v306/rabanser26a.html)
separates reliability from average task accuracy. Use that idea to build tests for your own
permissions and failure costs. A benchmark score is not a production guarantee.

For business ML, join outcomes to the original `decision_id` and report only mature cohorts. Track
feature freshness, missingness, calibration, precision at contact capacity, demand errors, margin,
budget use, opt-outs and action delivery. Compare the policy against its control group. A falling
input-drift score does not show rising business value. See
[Chapter 9's delivery plan](../09-business-machine-learning/delivery-plan.md) for the full feedback
path.

Alert on things that mean act now, and keep the list short. An alert nobody acts on trains everyone
to ignore the channel.

**Reproducibility.** Record code, immutable data/split versions, configuration, dependencies,
hardware/runtime, random state and checkpoints. A commit hash cannot rebuild a changing
customers table, a deleted API response or an unversioned prompt. Include query and snapshot
cutoffs, source licences and the commands needed to recover artifacts. For an API model, save the
provider model identifier, settings and recorded evaluation outputs. A changing hosted model may
not allow exact retraining or replay.

Be precise about which level you claim. _Rerunnable_ means the command works today. _Reproducible
within a declared tolerance_ means reruns land in a stated metric range on the same evaluation.
Report the runs that set that range. _Bit-identical_ needs tighter control, and even after seeding
it is not guaranteed across platforms or releases.
[PyTorch reproducibility notes](https://docs.pytorch.org/docs/2.14/notes/randomness.html).

**The classical ML lifecycle.** Schedule extraction, snapshot construction, training, evaluation and
batch scoring as explicit jobs with dependency checks and retries. Save preprocessing with the model
and compare batch and online features on recorded requests. Each release needs data/query
versions, training cutoff, feature schema, metrics and an immutable artifact identifier. A simple
manifest works at first. A registry adds managed versions and aliases when several models need them
([MLflow's registry workflow](https://mlflow.org/docs/latest/ml/model-registry/workflow/)).

Pin one complete release manifest to each request or batch, covering preprocessing, model,
calibrator, decision policy and any retrieval index. Prepare and validate the next release before
routing traffic to it. Workers should never mix separately refreshed components within one
decision. After retraining or changing score meaning, recheck calibration and decision thresholds on
data separate from model fitting before promotion. Rolling back artifacts still respects current
permissions, revocations, costs and operational constraints.

Serve risk scores in batch if a team acts once a day. Use an API where a session really needs a
decision. Either way, check authentication, request limits, fresh features and graceful fallback.
Shadow a new policy, check its outputs, then canary it with explicit stop conditions. On an alert,
inspect data and label freshness before retraining. Evaluate a challenger on recent mature cohorts
and the preserved benchmark. Promote only if the declared quality, business and latency gates
pass. Recalibration, data repair or rollback may be the right fix instead of a new model.

**Try it yourself.** Release `v8` of your Chapter 3 model went live at 09:00. At 11:00 an alert
fires: the share of requests above the decision threshold has doubled. The freshness check shows
the activity table behind its recency features last loaded at 02:00 yesterday. Outcome labels will
not mature for 30 days. Do you roll back to `v7`, retrain, or do something else?

<details>
<summary>Hint and explained answer</summary>

Look at the data before the model. A table that stopped loading before the release makes recent
activity look missing or zero, which can raise scores under either release. Rolling back to `v7`
would probably keep the symptom, and retraining would learn from broken inputs. Switch to the
stale-feature fallback now, then repair and reload the pipeline. Replay recorded requests through
`v7` and `v8` with fresh features. Roll back only if `v8` still falls outside its validated range.
The release timing is a lead to test, not a diagnosis, and waiting 30 days for labels is not an
option.

</details>

**Feedback is a data product.** Log eligibility, the chosen action, policy version, execution status
and, when randomised, the assignment probability. Then reconcile outcomes and label availability.
Keep training examples and evaluation cohorts separate as they mature. User ratings and model
judgements are useful diagnostic signals. But selected feedback is not an unbiased estimate of
product performance. Sending a retention offer or changing a price also changes later training
data. Keep a suitable control or exploration design to measure incremental effects. For LLM
applications, sample successful as well as failed traces, redact sensitive content, have a person
check proposed labels, and route approved cases into a versioned development set.

Keep access, retention and deletion rules with the trace pipeline. They need to reach every copy:
traces, evaluation cases drawn from them, training snapshots and derived artifacts. Record where
personal data flows and how long each store keeps it. Then rehearse one erasure request end to end,
including whether a model trained on the erased records needs retraining.

**Durable actions, when the application can write.** Commit the validated decision and a pending
delivery record together before dispatch. A transactional outbox is one way to close the gap
between database write and message send. The
[AWS design guide](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)
also requires handling duplicate delivery. Reuse the business operation ID, check the destination's
idempotency contract, and reconcile unknown outcomes after a timeout. If a destination cannot
deduplicate or report its state, stop and reconcile instead of promising exactly-once effects. Test
crashes before dispatch and after the remote effect but before its acknowledgement. This extension
is for action-capable systems. The Chapter 5 read-only sprint does not need an action worker.

**Cost.** Take one working feature and build a real table. Start with baseline cost per thousand
requests, then add the effect of restructuring the prompt so the static prefix caches, routing easy
requests to a cheaper model, and moving latency-tolerant work to a batch endpoint. Report the
evaluation pass rate beside each variant, because the classic trap is a cost cut that quietly lowers
quality.

| Variant                              | Cost / 1k requests | Eval pass rate | Notes                                                                   |
| ------------------------------------ | ------------------ | -------------- | ----------------------------------------------------------------------- |
| Baseline (single model, full prompt) | \$2.40              | 71%            | No caching                                                              |
| Cached static prefix (~2k tokens)    | \$1.10              | 71%            | Measure eligible tokens, hit rate and model-specific read/write charges |
| Route easy queries to smaller model  | \$0.85              | 68%            | Check quality drop before shipping                                      |
| Batch endpoint for async work        | \$0.55              | 71%            | Use the provider's asynchronous deadline; record observed turnaround    |

Fill in your own numbers from provider logs. Treat any figure in a tutorial, including this table,
as a placeholder until you measure.

Keep provider details in the experiment configuration. OpenAI's
[prompt-caching guide](https://developers.openai.com/api/docs/guides/prompt-caching) describes
exact-prefix reuse. Minimums, retention and read/write pricing depend on model generation and
settings, so do not budget with a universal discount. Its
[Batch API](https://developers.openai.com/api/docs/guides/batch) currently offers a 50% discount for
supported work with a 24-hour completion window. A batch can expire with partial results. Before
retrying unfinished work, reconcile successes and request-level errors by `custom_id`, not output
order. Measure turnaround instead of promising interactive latency. When comparing alternatives,
count retries, tool calls, judge usage, storage and idle compute.

For self-hosting, the answer is arithmetic, not preference. Compare monthly API cost with GPU
hours (including idle time) plus the engineering hours to run it. Then find the request volume
where the lines cross. Knowing how to do that sum matters more than which side you land on.

## Resources

Annotated resources are in **[resources/](resources/README.md)**. For the 55-hour plan, use the
selected sections. Full courses and deeper distributed-systems material are optional extras.

The ones to begin with:

- [Docker documentation — Get started, and the Python guide](https://docs.docker.com/get-started/) —
  Docker documentation team. Free documentation, 4–6 hours. Week 33.
- [FastAPI official documentation and tutorial](https://fastapi.tiangolo.com/) — Sebastián Ramírez.
  Free documentation, 2–4 hours of selected API/testing work. Use your existing endpoint.
- [GitHub Actions documentation](https://docs.github.com/en/actions) — GitHub documentation team.
  Free documentation, 3–5 hours of selected Python CI work. Week 34.
- [Prompt caching guide](https://developers.openai.com/api/docs/guides/prompt-caching) — OpenAI
  developer documentation. Free, 1–2 hours. Read your own provider's equivalent too. Week 36.

## What to build

Take the application from [Chapter 5](../05-language-models/README.md) and finish it properly: a
multi-stage Dockerfile, CI running tests and evaluations, deployment within a declared budget,
redacted structured request logs, a small dashboard, two alerts you would actually act on, a
rollback runbook, a cost table, and a model card. A model card is a one-page note on what the system
is for, what it was evaluated on, and what it should **not** be used for.

Deploy the [Chapter 3](../03-core-machine-learning/README.md) model beside it, as an API or a
batch-scoring job. Give it a release manifest (data/query versions, training cutoff, feature schema,
metrics and artifact hash) and a decision log that joins each `decision_id` to its features,
release and, once mature, its outcome. Add a freshness check that switches to the documented
fallback when inputs are stale. The reference lab's
[release manifest](../labs/reference/release-manifest.json) is a filled-in, simulated example.

Then break it on purpose and write a short incident report: what you injected, how long detection
took, what fired, how you rolled back, and what you would change. Set severity by user impact, such
as wrong decisions served versus a late dashboard. Write it blamelessly. Name the conditions and
missing safeguards that let the failure through, not a person to blame. The lab's [incident
rehearsal](../labs/reference/incident-report.md) is a filled-in example. Your own report is worth
more than another model in a portfolio, because very few people have one.

## Before you move on

- You can explain each Docker build stage and fix a build with a missing runtime dependency
  (documentation allowed). Show that the image starts and its readiness check catches a missing or
  incompatible model bundle.
- You can rerun training from the release manifest within a declared metric tolerance, or explain
  the limits of replaying a hosted model.
- You can show your dashboard and justify each alert.
- You can read your incident report and your cost table out loud.
- You can trace a decision to its features, model and eventual outcome, and rehearse a fallback on
  stale data.

## A few things worth knowing

- **Deploy on day one of the week, not day five.** The first deploy nearly always turns up
  something: a missing system library, a secret that was only in your shell, a port that is not
  exposed. Finding that on Monday leaves the week for fixing it.
- **Inspect image size.** `docker history` shows large layers. Separate required GPU runtimes and
  weights from unused build tools, caches or training data. Measure cold start after changing the
  image, since a smaller image does not always fix latency.
- **Secrets never go in the image.** Pass them in at run time as environment variables or from the
  platform's secret store. Keep a `.env.example` with the names but no values, and check that
  `.dockerignore` and `.gitignore` both exclude the real file.
- **Document applicable obligations with an owner.** Scope depends on the intended use, where the
  system is used, and your organisation's provider or deployer role. For an EU-facing release,
  check the
  [Commission's current AI Act guidance](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
  and the applicable enacted text when assessing classification, transparency and dates. Record the
  assessment and open questions. A model card alone does not show compliance. This book does not
  treat every application as high risk, or a proposed timeline change as enacted law.
  Data-protection law can apply as well, for example the EU's GDPR or India's Digital Personal Data
  Protection Act, 2023, depending on whose data you process and where. Record that assessment the
  same way. This book is not legal advice.

---

[Previous: Language models and AI engineering](../05-language-models/README.md) &nbsp;·&nbsp;
[Next: Choosing a specialisation](../07-specialisation/README.md)
