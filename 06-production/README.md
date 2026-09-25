# Chapter 6: Running it in production

**Weeks 33-37 &nbsp;·&nbsp; about 55 hours.** &nbsp;·&nbsp; [Index](../README.md) &nbsp;·&nbsp; [Resources for this chapter](resources/README.md)

**The short version.** Your Chapter 5 product becomes a system: containerised, tested on every push, deployed, watched, and cheap enough to defend in a budget conversation. Little here is glamorous, and its absence is what separates a demo from something a team would trust.

**From this week, [Chapter 8: Finding the work](../08-finding-the-work/README.md) runs alongside
this chapter and the next.** Open it now; the search it describes has a longer lead time than
anything left to build.

---

## Your five-week plan

About eleven hours a week. You are **finishing** the Chapter 5 app, not starting a new one.

| Week | Focus | Do this | Done when |
|---|---|---|---|
| 33 | Docker + deploy | Multi-stage Dockerfile; deploy to Modal or similar; public URL | Image under 500 MB |
| 34 | CI | GitHub Actions: pytest + data tests + **eval assertions** | Bad prompt fails build |
| 35 | Observability | Structured logs; trace viewer; two real alerts | Dashboard shows last 100 requests |
| 36 | Cost + rollback | Cost table (see template below); rollback runbook filled in | Can read both out loud |
| 37 | Incident | Break on purpose; write incident report; model card with **do not use for** | Report in repo |

---

## What you will be able to do

Containerise, deploy, monitor, roll back, and say what your system costs per thousand requests.

Most of this is expected rather than distinguishing. Its absence is noticed; its presence is
assumed. That is why it gets five weeks rather than twelve. The exception is **cost engineering**,
which very few people can discuss with numbers from a system they built themselves.

## What to learn

**Containers, and about forty per cent of Docker.** Images and layers, why your build is slow,
multi-stage builds, `.dockerignore`, sensible Dockerfile hygiene for Python, volumes, environment
variables and secrets, and Compose for local work. Aim for an image well under 500 MB; if yours is
several gigabytes you are shipping build tools, unused CUDA libraries or your training data.

Kubernetes appears on every MLOps diagram, and for someone at this point it is a long detour with
little portfolio payoff. Learn Docker properly and one CI system properly, and deploy somewhere
serverless. This is contested, and worth knowing that it is: plenty of postings do ask for
Kubernetes, and the "own your service in production" argument is a real one. The common advice for
people entering the field is still Docker deeply, Kubernetes on the job.

**Continuous integration that means something.** Run your tests, your **data** tests (schema
assertions, range checks, a check that no group appears in both splits) and **your evaluation
assertions** on every push. That last one is the differentiator: a prompt change that makes things
worse should fail the build, exactly like a broken test. Prompts are code, and they belong in version
control with an identifier logged on every call.

**A rollback runbook.** Five minutes to write, and it answers "can you explain monitoring and
rollback?" before anyone asks. What the alert looks like, the command that rolls back, how to switch
models without redeploying, the kill switch, and who to tell.

```markdown
# Rollback runbook — [service name]

## When to use this
- Alert: eval pass rate below 70% for 15 minutes (link: [dashboard URL])
- Alert: p95 latency above 3s for 10 minutes
- Manual: user reports systematic wrong answers

## Roll back application
1. `git checkout [last-good-tag]` or redeploy previous image: `[registry]/app:[tag]`
2. Confirm health: `curl https://[url]/health`

## Roll back model (no full redeploy)
1. Set env `MODEL_ID=[previous-model]` or switch config in [config path]
2. Restart workers: `[your command]`

## Kill switch
- Disable feature flag `LLM_ENABLED=false` or route to static fallback message

## Who to notify
- [Your name / on-call channel]

## After rollback
- Open incident doc; attach traces from first failing request
```

**Serving.** FastAPI for one model. vLLM if you are serving an open-weights model yourself; it is
worth understanding paged attention and continuous batching well enough to explain why throughput
improves, since that is a good interview answer and you now know enough to actually follow it. Ray
Serve only once you genuinely need to compose several models.

**Monitoring.** For classical models: input distributions, prediction distributions and drift, with
the awareness that labels often arrive weeks late. For language-model applications: traces, tool-call
failure rates, evaluation pass rate on a live sample, cost and latency. In both cases the most common
"drift" turns out to be a broken upstream pipeline rather than a changing world, so check that first.

Alert on things that mean act now, and keep the list short. An alert nobody acts on trains everyone
to ignore the channel.

**Reproducibility.** A model is a function of four things: code, data, configuration and environment.
Pin all four. Data is the one people lose, because "the customers table" is not a version and it
changed yesterday. Immutable date-partitioned storage plus artefact lineage gets you most of the
benefit with modest machinery.

Be precise about which level you are claiming. *Rerunnable* means the command works today.
*Reproducible* means the same inputs give a statistically equivalent model, and is the right target.
*Bit-identical* is expensive on GPUs and rarely worth it.

**Cost.** Take one working feature and produce a real table: baseline cost per thousand requests,
then the effect of restructuring the prompt so the static prefix caches, routing easy requests to a
cheaper model, and moving latency-tolerant work to a batch endpoint. Report the evaluation pass rate
alongside each variant, because a cost reduction that quietly degrades quality is the classic trap.

| Variant | Cost / 1k requests | Eval pass rate | Notes |
|---|---|---|---|
| Baseline (single model, full prompt) | $2.40 | 71% | No caching |
| Cached static prefix (~2k tokens) | $1.10 | 71% | Prefix must exceed provider minimum |
| Route easy queries to smaller model | $0.85 | 68% | Check quality drop before shipping |
| Batch endpoint for async work | $0.55 | 71% | Adds minutes of latency |

Fill in your own numbers from provider logs — treat any figure in a tutorial, including this table,
as a placeholder until you measure.

For self-hosting, the honest answer is arithmetic rather than preference: compare API cost per month
against GPU hours including idle time plus the engineering hours to run it, and find the request
volume where the lines cross. Knowing how to do that calculation matters more than which side you
land on.

## Resources

All 29 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [Docker documentation — Get started, and the Python guide](https://docs.docker.com/get-started/) — Docker documentation team. Free documentation, 4-6 hours. Week 33.
- [FastAPI official documentation and tutorial](https://fastapi.tiangolo.com/) — Sebastián Ramírez. Free documentation, 10-15 hours; do not skip the testing chapter.
- [GitHub Actions documentation](https://docs.github.com/en/actions) — GitHub documentation team. Free documentation, 6-10 hours. Week 34.
- [Prompt caching guide](https://developers.openai.com/api/docs/guides/prompt-caching) — OpenAI developer documentation. Free, 1-2 hours; read your own provider's equivalent too. Week 36.

## What to build

Take the application from [Chapter 5](../05-language-models/README.md) and finish it properly: a multi-stage Dockerfile, CI running tests
and evaluations, deployment to a free tier, structured logging of every request, a small dashboard,
two alerts you would actually act on, a rollback runbook, a cost table, and a model card. A model
card is a one-page note on what the system is for, what it was evaluated on, and what it should
**not** be used for.

Then break it on purpose and write a short incident report: what you injected, how long detection
took, what fired, how you rolled back, and what you would change. That document is worth more than
another model in a portfolio, because very few people have one.

## Before you move on

- You can write a multi-stage Dockerfile from memory.
- You can reproduce a model from a commit hash.
- You can show your dashboard and justify each alert.
- You can read your incident report and your cost table out loud.

## A few things worth knowing

- **Deploy on day one of the week, not day five.** The first deploy always surfaces something: a
  missing system library, a secret that was only in your shell, a port that is not exposed. Finding
  that on Monday leaves the week for fixing it.
- **Your first image will be huge.** Everyone's is. `docker history` shows which layer is to blame;
  it is usually build tools, unused CUDA libraries or training data, and the image tends to halve in
  twenty minutes once you look.
- **Secrets never go in the image.** Pass them in at run time as environment variables or from the
  platform's secret store, keep a `.env.example` with the names but no values, and check that
  `.dockerignore` and `.gitignore` both exclude the real file.
- **Regulation is now part of production.** If your system is offered to people in the EU,
  [the AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) is likely
  to apply to it. Its transparency rules, such as telling people when they are dealing with an AI,
  apply from August 2026. The stricter rules for high-risk uses, such as hiring, education and
  critical infrastructure, start on 2 December 2027, after a 2026 amendment moved them back. You do
  not need to be a lawyer. Your model card should simply say whether the system could fall into a
  high-risk use, and why.

---

[Previous: Language models and AI engineering](../05-language-models/README.md) &nbsp;·&nbsp; [Next: Choosing a specialisation](../07-specialisation/README.md)
