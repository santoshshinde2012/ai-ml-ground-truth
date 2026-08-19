# Chapter 6: Running it in production

**Weeks 33-37 &nbsp;·&nbsp; about 55 hours.** &nbsp;·&nbsp; [Index](../README.md) &nbsp;·&nbsp; [Resources for this chapter](resources/README.md)

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

For self-hosting, the honest answer is arithmetic rather than preference: compare API cost per month
against GPU hours including idle time plus the engineering hours to run it, and find the request
volume where the lines cross. Knowing how to do that calculation matters more than which side you
land on.

## Resources

All 28 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [AI Evals Free Email Course (17 parts)](https://ai.hamel.dev/eval-course) — Hamel Husain & Shreya Shankar. A free course, 5-6 hours.
- [Eugene Yan — Start Here (LLM patterns, evals, ML in production)](https://eugeneyan.com/start-here/) — Eugene Yan. A free article, 10-15 hours.
- [FastAPI official documentation and tutorial](https://fastapi.tiangolo.com/) — Sebastián Ramírez. Free documentation, 10-15 hours.
- [GitHub Actions documentation (quickstart + workflows + deployment)](https://docs.github.com/en/actions) — GitHub documentation team. Free documentation, 6-10 hours.

## What to build

Take the application from [Chapter 5](../05-language-models/README.md) and finish it properly: a multi-stage Dockerfile, CI running tests
and evaluations, deployment to a free tier, structured logging of every request, a small dashboard,
two alerts you would actually act on, a rollback runbook, a cost table, and a model card that
includes what the system should **not** be used for.

Then break it on purpose and write a short incident report: what you injected, how long detection
took, what fired, how you rolled back, and what you would change. That document is worth more than
another model in a portfolio, because very few people have one.

## Before you move on

- You can write a multi-stage Dockerfile from memory.
- You can reproduce a model from a commit hash.
- You can show your dashboard and justify each alert.
- You can read your incident report and your cost table out loud.

---

[Previous: Language models and AI engineering](../05-language-models/README.md) &nbsp;·&nbsp; [Next: Choosing a specialisation](../07-specialisation/README.md)
