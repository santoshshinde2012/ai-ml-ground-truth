# Chapter 5: Language models and AI engineering

**Weeks 23-32 &nbsp;·&nbsp; about 100 hours.** &nbsp;·&nbsp; [Index](../README.md) &nbsp;·&nbsp; [Resources for this chapter](resources/README.md)

**The short version.** This is the centre of the book. You learn to treat a language model as a dependency: control what goes into its context, retrieve the right facts, and — above all — measure whether it works before trying to make it better. You finish by shipping a small, real product in two weeks, with an evaluation suite and a user who is not you.

**Same thread.** Build on documents from your Chapter 2 domain — ticket appeals, API docs you use at work, your exported notes. The eval discipline is the same as Chapter 3, applied to text.

---

## Your ten-week overview

Weeks 23-32, about ten hours a week. Weeks 27-28 are the **two-week product sprint** (detailed day plan below).

| Week | Focus | Do this | Done when |
|---|---|---|---|
| 23 | Model as dependency | Anthropic API course; one script calling the API with logging | Every call logs prompt id + latency |
| 24 | Context + tools | Structured output; tool call that returns real data | Tool result in trace |
| 25 | Retrieval | Chunk corpus; embed; on 20 hand-labelled queries measure recall at k (did the right chunk land in the top k?) | Two chunk strategies compared |
| 26 | Eval workflow | 50 gold pairs (inputs with the output you expect); read 30 traces; write failure notes | Failure modes listed |
| 27-28 | **Two-week product** | Follow day-by-day plan below | Public URL + pass-rate chart |
| 29 | Agents vs workflows | Write 60-line loop yourself; justify workflow in README | Can debug without framework |
| 30 | MCP or cost | MCP spec **or** caching + routing cost table | One measured optimisation |
| 31 | Fine-tuning (optional) | Honest before/after — include "not worth it" if true | Four-way comparison table |
| 32 | Buffer | CI eval gate; rehearse system-design story | Prompt change fails CI when quality drops |

New words in this chapter — context engineering, retrieval, gold set, pass rate, trace, judge — are
explained where they first appear below, and collected in [Terms in plain English](../README.md#glossary).

---

## What you will be able to do

Ship a language-model application with an evaluation suite you built **before** you started
optimising, an error taxonomy taken from real traces, and a cost per thousand requests you measured.

## The one idea to take from this chapter

Almost every practitioner who writes about this arrives at the same conclusion: **the main reason AI
products fail is the absence of an evaluation system**. It is also, encouragingly, the thing hiring
managers name as the clearest signal that someone has really built with these models rather than
watched videos.

An application with a good interface and no labelled examples is hard to improve, because there is
no way to tell whether a change helped. The same application with a hundred hand-labelled traces, a
documented set of failure modes, and a judge you have checked against your own labels is a different
proposition entirely. A trace is the saved record of one request — input, intermediate steps,
output. A judge is a model prompted to grade another model's answers against criteria you wrote.
Few people do this, which is exactly why it is worth doing.

## What to learn

**The model as a dependency.** Treat it like a database: a stochastic function with a latency budget,
a token bill and a schema contract. Learn tool use first, since agents, retrieval and structured
output are all built on it. Learn structured output properly, and remember that constrained decoding — forcing each generated
token to fit your schema — guarantees the **shape** of the answer, not its truth.

Learn the economics, because they come up in interviews and in budget conversations. Caching a
static prompt prefix can reduce input cost by around ninety per cent, but there is a minimum
cacheable prefix length, so a short system prompt may never cache at all. Batch endpoints are
substantially cheaper for work that can wait. Routing easy requests to a smaller model behind a
confidence check often does more than any of it. These figures are provider-specific and they move,
so check the current pricing pages rather than trusting a number in any document, including this one.

Reasoning models add one more dial. They think in extra tokens before they answer, mostly hidden
from you, and those tokens are billed as output and take up context. The major providers now let you
set an effort level on each request. Treat it like model choice: start at low effort, and raise it only
where your evaluations show it helps. You build those evaluations later in this chapter.

**Context engineering.** The context window is a budget you allocate, not a bucket you fill. Order it
so the stable parts (system prompt, tool definitions, examples) come first and can be cached, and the
dynamic parts (retrieved documents, history) come after. The harder problems are all about time:
compacting history as it grows, deciding what persists across sessions, compressing errors before
they enter the context, and noticing that a long context window does not mean the model attends
usefully to all of it.

This is the shift the field made over the last two years, from wordsmithing one prompt to curating
the whole token budget. It is also why "prompt engineer" is not really a job title any more.

**Retrieval that survives contact.** Chunk, embed, take the top few, put them in the prompt: that is
a prototype rather than an architecture. The current bar adds hybrid retrieval (dense embeddings for
meaning, keyword search for exact tokens like product codes), reranking, chunking that respects
document structure, metadata filters, citations back to source spans, an explicit path for "I do not
have that information", and routing by query complexity.

The most important habit: **measure retrieval separately from generation**. If you only measure
end-to-end, you cannot tell whether to fix the retriever or the prompt, and you can lose a week
rewording a prompt when the document was never fetched.

**Evaluation, which is most of the work.** The order matters more than the tooling, and most people
get it backwards.

1. Ship a deliberately rough first version, so you have real traces
2. Collect a hundred or more of them
3. **Read them yourself**, by hand
4. Write a free-text note on each failure
5. Cluster those notes into a handful of failure modes
6. **Now** write pass/fail assertions, one per failure mode
7. Add a model-based judge only for what assertions cannot reach
8. Check the judge against your own labels, and report agreement properly
9. Wire it into CI
10. Fix the most common failure first, then measure again

Steps three to five are the stage. Prefer binary pass/fail criteria to a one-to-five scale, since
nobody applies a five-point scale consistently and the disagreement swamps the signal. If something
genuinely needs gradation, split it into several binary checks.

Build your own small trace viewer rather than adopting a general platform. A hundred lines that show
input, retrieved chunks, prompt, output and two label buttons will get you through a hundred traces
in an hour. A tool that takes six clicks per trace means you will look at twelve and stop.

**Agents and workflows.** Most things called agents would be better as workflows, and the judgement
about when not to use one is itself worth demonstrating.

| Pattern | Use when |
|---|---|
| One call with tools | Most tasks, genuinely |
| Prompt chaining | The task decomposes and each step can be evaluated separately |
| Routing | There are distinct input categories |
| Parallel calls, then aggregate | Subtasks are independent, or you want a vote |
| Orchestrator and workers | Subtasks are not known until runtime |
| Generate, critique, revise | There are clear quality criteria |
| A true agent | You cannot hardcode the path, but you can verify progress |

Write the loop yourself before reaching for a framework. It is about sixty lines, or two hundred with
error compaction, context management, a turn limit and a human-approval step for anything
destructive. Once you have written it you can debug any framework; if you start with a framework you
may struggle to debug your own application.

**MCP**, the Model Context Protocol, is an open standard for connecting a model to tools and data. It
is one of the few current "hot skills" that looks safe to invest in, because it has reached a
versioned specification with a formal deprecation policy. Learn it from the specification and the
changelog rather than from tutorials: the 2026-07-28 release moved to a stateless core, and most
2025 tutorials teach the session model it removed.

**Agent skills** are a smaller idea worth knowing next to MCP. A skill is a folder holding a
`SKILL.md` file of instructions, plus optional scripts and reference files. The agent reads only each
skill's name and description at first, and loads the rest when a task calls for it. That is context
engineering in a reusable form. The format began at Anthropic, is now an
[open standard](https://agentskills.io/home), and coding agents from several vendors support it.
Writing one skill for a task you repeat is a quick way to see how loading on demand saves context.

**Fine-tuning, considered fourth.** The order that works is a good prompt, then examples, then
retrieval, and only then fine-tuning. It is the right tool for style and format consistency, for
moving work to a smaller and cheaper model, and for narrow domain tasks. It is the wrong tool for
adding facts, which belong in retrieval where they can be updated and cited. Roughly half the time
the honest conclusion is that it was not worth it, and publishing that comparison shows more
judgement than a successful fine-tune does.

## Resources

All 35 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) — Andrej Karpathy. A free video, 4 hours. Watch it in week 23 for the map.
- [Building with the Claude API (Claude Academy)](https://academy.claude.com/courses/building-with-the-claude-api) — Anthropic education team. A free course, 9 hours.
- [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) — Hamel Husain. A free article, 1 hour. Then the Evals FAQ by the same authors.
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Erik Schluntz & Barry Zhang. A free article, 1 hour.

## What to build

**Warm up first, in about three hours.** Deploy any pretrained model behind a public URL. It proves
nothing about you, and that is the point: its only job is to remove the fear of deploying before
the real work starts.

**Next, the evaluation-first application.** Pick a narrow task you personally care about and can judge:
extracting fields from your own documents, triaging your own issue tracker, drafting first-pass
replies. Follow the ten steps above in order.

The output is a repository where the evaluation suite predates the optimisation, plus a chart of the
pass rate across versions. This is, in my view, the single most useful thing you can build in this
whole book.

Then re-scope it into a small product with a public URL, following the two-week plan below.

## Before you move on

- You can explain why error analysis comes before evaluation tooling.
- You can explain how you checked your judge, and which two numbers you report.
- You can show a CI run that failed because a prompt change made things worse.
- You can state your cost per thousand requests and three ways to reduce it.

## A few things worth knowing

- **`nanoGPT` is marked "very old and deprecated" by its own author**, whose README points readers to
  [nanochat](https://github.com/karpathy/nanochat) instead. It is still recommended by many current roadmaps, which makes it a quick way to
  tell whether a list has been re-checked.
- **Frameworks after the raw loop, not before.** Provider APIs have converged enough that the
  abstraction hides less than it used to, and teams have reported real reductions in code and
  maintenance after moving back to raw SDKs. Both sides of this argument agree on the learning order.
- **Model names age quickly.** Everything specific in this chapter will be superseded. Tokenisation,
  attention, cache economics, retrieval, evaluation and context management will not, so that is where
  the study time is best spent.

---

## Your first AI product: a two-week plan

One user, one job, one screen, one metric. If you cannot phrase it as "this person does X in
Z seconds instead of W minutes", it is not scoped yet.

**Write the non-goals down on day one.** No authentication, no payments, no autonomous agent, no
fine-tuning, no custom vector store, no mobile app. Each is a week you are choosing not to spend, and
having the list written down is what stops you spending it anyway late on day nine.

| Day | What you do | What exists at the end |
|---|---|---|
| 1 | Name the person and the task. Write the README first: problem, user, success metric, non-goals | A scoped problem |
| 2 | **Hand-write 30-50 real input and expected-output pairs** | Your gold set: the evaluation set, and the specification |
| 3 | The roughest possible end-to-end path: hardcoded input, one call, printed output | You have hit every part of the pipeline once |
| 4 | Evaluation harness, version one: assertion checks over the gold set | **A single pass-rate number.** Everything after this is measured |
| 5 | Data layer: ingest, chunk, embed, index | Retrieval works |
| 6 | Retrieval evaluation: recall at k, two chunking strategies compared | The numbers that make your best interview story |
| 7 | Generation: structured output, citations to source spans, a path for "I do not know" | Grounded answers |
| - | **Weekend check: a pass-rate number exists, or reduce scope now** | An honest decision point |
| 8 | A thin interface. Do not build authentication | Something usable |
| 9 | Logging of every request, and the crudest possible trace viewer | You can see what is happening |
| 10 | **Read 100 traces. Cluster the failures. Add them to the gold set** | An error taxonomy |
| 11 | Fix only the most common failure, then re-measure | The pass rate moves, or you fixed the wrong thing |
| 12 | Deploy and harden: container, secrets, rate limit, per-user cost cap, graceful degradation | **A public URL** |
| 13 | A judge for the subjective part, checked against your labels. Evaluations in CI | Regressions fail the build |
| 14 | Ship the story: short demo, before-and-after metric, decisions, known failures, cost table | Something you can show people |

Day 10 is the one people skip, and it is the day that makes the difference. It also feels the least
like progress, which is presumably why.

Days 12 and 13 ask for skills this book has not taught yet — containers, secrets, CI. That is
deliberate: [Chapter 6](../06-production/README.md) teaches them properly, and takes this exact
application as its starting point. For now the crudest deploy that produces a public URL is enough.
The old free Hugging Face route is now paid, but the compute table in
[Chapter 1](../01-getting-oriented/README.md) still holds: Modal's free credits cover a deployed demo.

It is a product rather than a demo when there is a public URL, a number that moved, evaluations in
CI, an honest list of known failures, a cost table, and at least one user who is not you.

---

[Previous: Deep learning](../04-deep-learning/README.md) &nbsp;·&nbsp; [Next: Running it in production](../06-production/README.md)
