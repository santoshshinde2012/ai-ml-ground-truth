# Chapter 5: Language models and AI engineering

**Weeks 23–32 &nbsp;·&nbsp; about 100 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** Treat a language model as a dependency: control its context, retrieve the
right facts, constrain its actions, and measure whether it works. Finish with a small application,
an independent release evaluation, measured operating costs, and a user who is not you.

**Same thread.** Build on documents from your Chapter 2 domain — ticket appeals, API docs you use at
work, your exported notes. The eval discipline is the same as Chapter 3, applied to text.

**In this chapter:** [Plan](#your-ten-week-overview) &nbsp;·&nbsp; [Learn](#what-to-learn)
&nbsp;·&nbsp; [Product sprint](#your-first-ai-product-a-two-week-plan) &nbsp;·&nbsp;
[Completion](#before-you-move-on) &nbsp;·&nbsp; [Resources](#resources)

---

## Your ten-week overview

Weeks 23–32, about ten hours a week. Read selected lessons rather than every resource. Weeks 27–28
reserve about 20 hours for the **two-week product sprint**; its days are work sessions, not fourteen
full working days. Reuse the cases, pipeline and deployment from weeks 23-26.

| Week  | Focus                | Do this                                                                         | Done when                                                            |
| ----- | -------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 23    | Model as dependency  | Selected API lessons; one call with structured output and logging               | Model/version, prompt ID, usage, errors and latency recorded         |
| 24    | Context + tools      | One read-only tool; compare context variants; test malformed arguments          | Tool schema and application permission checks in a trace             |
| 25    | Retrieval            | Label 20 query families; compare keyword, dense and one hybrid/reranked variant | Relevant-source recall and latency reported                          |
| 26    | Eval workflow        | 50 cases; separate development/release families; read 30 development traces     | Failure modes and release criteria written down                      |
| 27–28 | **Two-week product** | Follow the session plan below                                                   | Usable URL + quality/cost report + known failures                    |
| 29    | Agents vs workflows  | Build a bounded loop or explicit workflow; test recovery                        | Deadline, step limit, permissions and retry behaviour demonstrated   |
| 30    | MCP or cost          | Current MCP revision **or** measured caching/routing comparison                 | Compatible versions or a quality-preserving cost result              |
| 31    | Fine-tuning decision | Compare prompt-only, examples and retrieval; optionally an adapter              | Keep the simplest acceptable approach; report a null result honestly |
| 32    | Release + buffer     | CI regression checks; independent release run; design story                     | Evidence supports release or a decision to defer                     |

New words in this chapter — context engineering, retrieval, gold set, pass rate, trace, judge — are
explained where they first appear below, and collected in
[Terms in plain English](../README.md#glossary).

---

## What you will be able to do

Ship a language-model application with an evaluation suite you built **before** you started
optimising, an error taxonomy taken from real traces, and a cost per thousand requests you measured.

## The one idea to take from this chapter

**A plausible answer is an observation, not proof that the system works.** You need examples with
criteria you can check, traces that reveal how answers were produced, and a release decision that
was not tuned to the test answers. This applies to document extraction and to an agent that can
change files or call services.

An application with a good interface and no labelled examples is hard to improve, because there is
no way to tell whether a change helped. The same application with a hundred hand-labelled traces, a
documented set of failure modes, and a judge you have checked against your own labels is a different
proposition entirely. A trace is the saved record of one request — input, intermediate steps,
output. A judge is a model prompted to grade another model's answers against criteria you wrote.
These records let you explain failures and compare changes. Neither a trace nor a model judge
replaces a domain expert or application-enforced permissions.

## What to learn

**The model as a dependency.** Treat it like a database: a stochastic function with a latency
budget, a token bill and a schema contract. Learn structured output, tool calls, streaming,
cancellation and error handling. Where an endpoint enforces a schema, it controls the **shape**, not
the truth. Validate values, references and tool arguments in application code. Record the model
identifier, sampling/effort settings, prompt version and API/SDK version for reproducible
comparisons.

Choose a current general-purpose model supporting your required interface as the baseline. Compare a
smaller model and a stronger or reasoning model on your own tasks. Effort controls, reasoning
visibility and billing differ by endpoint; raise the budget only when evaluations justify it.
Self-reported model confidence is not a calibrated routing score. Validate a router against labelled
outcomes and include escalation calls in the comparison.

The [2026 linguistic-confidence study](https://arxiv.org/abs/2608.28382), whose authors report
acceptance to EMNLP Findings, distinguishes useful score ordering from calibrated probabilities. For
your router, measure error among accepted answers against the fraction accepted, then freeze its
threshold before the release test. Recheck calibration after changing model, prompt or domain; token
probabilities and agreement between sampled answers are also signals requiring validation.

**Economics you can measure.** Record input, cached input, output and separately exposed reasoning
usage; retrieval, tool, storage and hosting charges; retries; and failed requests. Compare cold and
warm caches. Cache minimums, lifetimes, write charges and batch discounts depend on provider and
model. Check dated [pricing](https://platform.claude.com/docs/en/about-claude/pricing) and
[cache documentation](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) rather
than assuming a fixed saving applies to the whole bill. Reconcile usage fields with the provider's
billing schema rather than summing every breakdown. Claude's
[thinking-cost guide](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost)
explains that thinking usage is already included in billed output tokens; adding it again
double-counts cost.

If 1,000 attempted requests cost $8 and 800 pass task checks, the observed cost is $0.01 per
successful request. Report cost per attempt and per success, p50/p95 latency and timeout rate. A
cheaper model requiring frequent escalation can cost more for the task. Set a spending limit and a
fallback before public deployment. Enforce request and aggregate application limits, including
retries and concurrent calls; verify whether a provider budget setting stops requests or only
alerts.

**Context engineering.** The context window is a budget you allocate, not a bucket you fill. Order
it so the stable parts (system prompt, tool definitions, examples) come first and can be cached, and
the dynamic parts (retrieved documents, history) come after. The harder problems are all about time:
compacting history as it grows, deciding what persists across sessions, compressing errors before
they enter the context, and noticing that a long context window does not mean the model attends
usefully to all of it.

Give sources identifiers and dates. Preserve unresolved tasks, decisions and source references when
compacting history; test whether compaction drops a constraint or promotes an unverified claim to a
fact. Stored memory needs an owner, access permissions, update rules and deletion.
[NoLiMa (2025)](https://arxiv.org/abs/2502.05167) tests long-context retrieval without easy literal
matches, illustrating why a simple needle test can miss failures. Its results concern the tested
models and tasks. Include paraphrases, distant evidence and conflicting versions in your own tests.

**Choose the information path.** Retrieval-augmented generation (RAG) fetches selected sources; long
context supplies a larger body directly; search fetches external information when freshness or
coverage requires it. Compare them rather than assuming every application needs a vector store.

| Situation                                                      | Start with                             | Measure before expanding                                             |
| -------------------------------------------------------------- | -------------------------------------- | -------------------------------------------------------------------- |
| A small, stable, permitted document fits comfortably           | Direct context with source IDs         | Correctness, source use, cost and irrelevant-context sensitivity     |
| A changing/large corpus; exact IDs or access boundaries matter | Filtered keyword/dense retrieval       | Relevant-source coverage, stale versions, access leakage and latency |
| Mixed exact and semantic queries                               | Hybrid candidates, optionally reranked | Gain over each retriever alone at the same context budget            |
| Current information outside the corpus is needed               | Bounded search/fetch with provenance   | Source quality, freshness, injection exposure and reproducibility    |
| Questions need different information paths                     | Tested routing between paths           | Router errors and total quality/cost, including fallbacks            |

The [EMNLP 2024 RAG/long-context study](https://aclanthology.org/2024.emnlp-industry.66/) compares
both and hybrid routing. It supports a task-specific comparison, not a ranking of 2026 models. Hold
the permitted corpus, source versions, query set and answer criteria constant.

**Retrieval that you can diagnose.** Start with keyword and dense baselines. Choose embeddings by
language, domain, length, deployment cost and licensing; follow their query-prefix and similarity
conventions. Changing the embedding model usually requires re-embedding the index.
[MMTEB (2025)](https://arxiv.org/abs/2502.13595) broadens multilingual evaluation, but your own
domain queries still decide. Chunk around document structure; retain source/version/parent IDs;
deduplicate chunks. Apply user access before retrieval and verify it again before returning sources,
including caches. A cross-encoder reranker scores retrieved query-document pairs more expensively
and cannot recover a missing candidate. See the official
[retrieve-then-rerank example](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html).

Deploy the query encoder, document embeddings, chunk/source manifest and retrieval configuration as
a compatible version. A new query encoder against an old index can silently change results. Test
source updates, deletions and permission revocations as well as ingestion; a cached answer must not
restore access to a source the user can no longer read.

The most important habit: **measure retrieval separately from generation**. If you only measure
end-to-end, you cannot tell whether to fix the retriever or the prompt, and you can lose a week
rewording a prompt when the document was never fetched. Label relevant source spans and measure
recall at k, ordering and latency; count source families rather than duplicate chunks as successes.
Then score answer correctness, whether cited passages support claims, and suitable abstention for
missing/conflicting evidence. Citation presence alone is not support. Twenty query families are a
debugging exercise, not a precise production quality estimate.

**Evaluation as a development loop.** Establish a small task specification first, then improve it
using real development traces. An efficient order is:

1. Write representative cases and acceptance criteria; reserve independent release cases.
2. Build the smallest complete version and collect development traces.
3. Read failures, write free-text notes, and group recurring failure modes.
4. Add deterministic assertions where outputs or final state can be checked directly.
5. Add a judge only for criteria needing interpretation; ask for evidence and a rubric decision.
6. Validate the judge on separately labelled examples before relying on its measurements.
7. Put regression cases in CI; fix one failure mode and compare on development cases.
8. Run the independent release evaluation after fixing the candidate and decision thresholds.

**Keep test answers out of development.** Split by source document, customer/session, time or
question family as appropriate, then check duplicates and paraphrases across splits. Split before
generating synthetic variants. A RAG question may legitimately refer to an accessible source
document; its expected answer and grading notes must remain inaccessible to the application and its
tools. Prompt-tuned cases are development cases. A CI regression set catches known failures;
repeated optimisation against it cannot provide an independent release claim. Periodically acquire a
fresh, independently labelled holdout.

Web agents can retrieve leaked benchmark answers during evaluation even when they were absent from
training. Anthropic's
[March 2026 BrowseComp investigation](https://www.anthropic.com/engineering/eval-awareness-browsecomp)
documents leaked answers and evaluation-aware answer-key searches in its tested setup. Audit
provenance, isolate grading assets and use fresh private cases. Public benchmark scores are
supporting evidence, not your release test.

Use binary criteria for binary requirements; use a defined graded rubric when quality has degrees,
and check human-rater agreement. Choose a viewer that makes inputs, sources, calls and outputs easy
to inspect. Read the task/trial/grader sections of
[Demystifying evals for AI agents (January 2026)](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).
Its examples describe Anthropic's experience rather than universal performance guarantees.

| What you evaluate         | Evidence to save                                                          |
| ------------------------- | ------------------------------------------------------------------------- |
| Extraction/classification | Per-field/class metrics, whole-record correctness, invalid outputs        |
| Grounded answers          | Correctness, supported claims, citations, answerable/unanswerable slices  |
| Judge quality             | Human/judge confusion matrix; failure sensitivity and false-alarm rate    |
| Multi-step actions        | Final environment state, forbidden side effects, permissions, completion  |
| Reliability               | Independent repeated trials, perturbations, recovery and failure severity |
| Operations                | Cost per attempt/success, p50/p95 latency, deadlines and retry counts     |

Blind reviewers to candidate identity where practical; test answer-order and verbosity sensitivity.
Overall agreement can hide a judge passing nearly everything. If failure is the positive label,
failure sensitivity is `TP/(TP+FN)` and false-alarm rate is `FP/(FP+TN)`. Missing labels and grader
errors are explicit outcomes, not passes. Reset files, databases and tools between independent agent
trials; disclose retry/attempt budgets. Report sample size, uncertainty and meaningful slices;
respect task/session grouping rather than treating correlated trials as new users.
[Towards a Science of AI Agent Reliability (ICML 2026)](https://proceedings.mlr.press/v306/rabanser26a.html)
organises reliability around consistency, robustness, predictability and safety: one average success
score is insufficient for an action-capable system.

**Agents and workflows.** Start with a fixed workflow when the steps are known. Give an agent
discretion where its next step depends on observed evidence and you can verify progress and
constrain effects. Compare the flexibility with the added calls and failure modes.

| Pattern                                    | Use when                                                      |
| ------------------------------------------ | ------------------------------------------------------------- |
| One call, optionally with a read-only tool | One bounded task has a checkable output                       |
| Prompt chaining                            | The task decomposes and each step can be evaluated separately |
| Routing                                    | There are distinct input categories                           |
| Parallel calls, then aggregate             | Subtasks are independent, or you want a vote                  |
| Orchestrator and workers                   | Subtasks are not known until runtime                          |
| Generate, critique, revise                 | There are clear quality criteria                              |
| A true agent                               | You cannot hardcode the path, but you can verify progress     |

Build one small loop or state machine before choosing a framework; there is no production-ready
line-count target. Make control flow explicit: allowed tools, argument validation, deadline,
token/cost/step limits, bounded retries, cancellation, checkpoints and stop/handoff conditions. Use
idempotency keys and reconcile actual service state before retrying writes. A timeout does not tell
you whether a remote action happened. Multi-agent designs also need bounded fan-out, shared-state
ownership and evidence reconciliation; compare with a single-worker baseline.

For a write-capable extension, persist the validated action and its status before dispatch; use the
same business idempotency key on retries. Bind any user confirmation to the exact action, arguments,
recipient and validity interval. If those change, obtain a new confirmation where the product
requires one. Recheck authorization at execution; a saved approval is not a permanent access grant.
Chapter 6 covers durable delivery and recovery.

Test tool failure and context-compaction recovery. The
[September 2026 Mid-Harness preprint](https://arxiv.org/abs/2609.39982) investigates sampling and
verifying candidate actions before executing one in terminal-agent benchmarks. After a bounded
baseline, optionally compare action verification with extra generation at the same total budget. Its
results do not establish verifier reliability for your actions; application authorization still
decides whether an action may run.

**Access and tool boundaries belong in the first product.** Authenticate users when documents or
actions are private, and apply their document permissions before retrieval. Treat retrieved text and
tool output as untrusted input. Validate tool arguments and enforce permissions in application code;
the model does not grant its own access. Add timeouts, bounded retries, idempotency for writes, and
a confirmation step for consequential actions. Redact secrets and personal data from traces. Test
cross-user retrieval and documents that try to override instructions. The
[OWASP prompt-injection reference](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) explains
the threat and layered mitigations; the [AgentDojo benchmark](https://arxiv.org/abs/2406.13352)
provides tool-agent attack and defence examples. Use harmless canary data for exfiltration tests.
Downloaded skills are also untrusted. Use narrowly scoped service credentials, network/file
allowlists and isolated execution where relevant. Keep grading secrets and other users' data outside
the tool environment, recheck access at execution, and define trace retention. A public, read-only
demo can keep controls small because its data and permitted effects are small.

Verify the evaluation boundary itself: use fake credentials and harmless services, test outbound
access restrictions, and keep production secrets outside the harness. Anthropic's
[August 2026 incident account](https://www.anthropic.com/news/improving-alignment-security-efforts)
reports evaluation-environment misconfigurations that allowed unauthorized access. This is a vendor
incident report about intentionally less-protected cyber evaluations, not an estimate of your
application's failure rate. Test safe stopping when a task or tool cannot be completed.

**MCP**, the Model Context Protocol, is an open standard connecting clients to tools and data. Learn
the specification revision your client and server implement. The
[2026-07-28 changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
introduces a stateless core without the earlier initialization handshake or protocol sessions, and
adds multi-round-trip requests. Stateful business operations use explicit handles whose access the
server must enforce. Roots, sampling and logging are deprecated, still functional during their
deprecation window. Earlier-version tutorials may remain useful for those versions; test
compatibility rather than assuming it.

Learn request/version metadata, discovery, schemas, results/errors and cancellation. Transport
retries are not exactly-once business transactions. For remote servers, validate token audience,
avoid token passthrough, protect OAuth redirects and restrict outbound fetches against SSRF; follow
the
[official MCP security practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices).
Installing a server does not grant access to every connected user.

**Agent skills** are a smaller idea worth knowing next to MCP. A skill is a folder holding a
`SKILL.md` file of instructions, plus optional scripts and reference files. The agent reads only
each skill's name and description at first, and loads the rest when a task calls for it. That is
context engineering in a reusable form. The format began at Anthropic, is now an
[open standard](https://agentskills.io/home), and coding agents from several vendors support it.
Writing one skill for a repeated task lets you compare loading on demand with inline instructions.
Read its scripts/references and enforce normal tool permissions. Loading a skill does not raise its
trust level.

**Fine-tuning and RL when the error warrants them.** There is no fixed requirement to add RAG before
training. Match the intervention to the failure and available evidence.

| Need                                                          | First comparison                                   | Evidence to justify training                                          |
| ------------------------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------- |
| Clearer instructions or recurring output mistakes             | Prompt, schema checks, labelled examples           | Persistent held-out errors despite the simple baseline                |
| Current, attributable or private facts                        | Permitted context, retrieval or search             | Training is not a source-update or access-control mechanism           |
| Consistent narrow behaviour or a smaller model                | Supervised fine-tuning, often LoRA/QLoRA           | Clean examples, independent evaluation, acceptable serving costs      |
| Well-defined response preferences                             | DPO or another preference-training method          | Reliable preference labels and unwanted trade-off checks              |
| Verifiable outcomes such as unit-tested code or bounded maths | Optional RL, such as GRPO, with a validated reward | Reward integrity, task coverage, compute budget, reward-hacking tests |

The [DeepSeek-R1 paper](https://arxiv.org/abs/2501.12948) studies reasoning post-training and
distillation; it is not a prescription to run RL for a document assistant. The official
[TRL GRPO documentation](https://huggingface.co/docs/trl/grpo_trainer) exposes reward and training
controls for an optional experiment. Validate reward against human/task outcomes; increased reward
alone does not establish quality.

Split by document/customer/task family and time where appropriate, deduplicate before training, and
keep teacher-generated examples and evaluation labels independent. Verify synthetic labels, record
provenance and permitted data use, and compare at the same deployment budget. Quantised adapter
tuning reduces some memory costs; sequence length, batches, optimizer state and serving context also
matter. If training adds no useful benefit, retain the baseline and report that result.

## Resources

All 50 resources, with notes and a targeted research section, are in
**[resources/](resources/README.md)**. Optional resource study budgets are not added to the
chapter's 100 hours. Start with selected lessons and sections:

- [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) — Andrej Karpathy.
  A free video, 4 hours. Watch it in week 23 for the map.
- [Building with the Claude API (Claude Academy)](https://academy.claude.com/courses/building-with-the-claude-api)
  — Anthropic education team. A free course, 9 hours.
- [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) — Hamel Husain. A free article,
  1 hour. Then the Evals FAQ by the same authors.
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) —
  Erik Schluntz & Barry Zhang. A free article, 1 hour.
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
  — Anthropic. Task, trial and grader sections for week 26.

## What to build

**Warm up in about three hours.** Put a pretrained model or read-only API function behind a URL
using non-sensitive data. Measure one request and one failure; reuse this deployment path.

**Next, the evaluation-first application.** Pick a narrow task you personally care about and can
judge: extracting fields from your own documents, triaging your own issue tracker, drafting
first-pass replies. Follow the evaluation loop above. Retrieval is optional when the input already
contains all required information.

The output is a repository where the evaluation suite predates optimisation, with evaluation
history, failure examples, the development/release split and a measured operating-cost table.

Then re-scope it into a small product with a public URL, following the
[two-week plan below](#your-first-ai-product-a-two-week-plan).

## Your first AI product: a two-week plan

One user, one job, one screen, one main quality metric plus cost, latency and access checks.
Allocate about 20 hours across these sessions, reusing weeks 23–26 work. Reduce a task requiring
complex integration or a custom authentication system before this sprint.

**Write the non-goals on day one.** No payments, autonomous writes, custom vector store, mobile app
or model training. Use public/non-sensitive data, or platform authentication with verified per-user
access for a private application. Optional agents and tuning experiments come later.

| Day | What you do                                                                                    | What exists at the end                                              |
| --- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| 1   | Name the person and the task. Write the README first: problem, user, success metric, non-goals | A scoped problem                                                    |
| 2   | Review the 30–50 cases already collected; split independent families                           | Development cases + reserved release cases; grading assets isolated |
| 3   | The roughest possible end-to-end path: hardcoded input, one call, printed output               | You have hit every part of the pipeline once                        |
| 4   | Assertions on development cases; record versions and settings                                  | Quality and cost baseline                                           |
| 5   | If sources are needed, ingest/index with source IDs and access metadata                        | Small retrieval path; otherwise improve input validation            |
| 6   | Compare two retrieval/context variants on labelled queries                                     | Source coverage, quality and latency comparison                     |
| 7   | Generation: structured output, citations to source spans, a path for "I do not know"           | Grounded answers                                                    |
| —   | **Weekend check: a pass-rate number exists, or reduce scope now**                              | An honest decision point                                            |
| 8   | A thin interface; public data or platform authentication with per-user access checks           | Something usable with its intended data permissions                 |
| 9   | Redacted request logs, restricted access and the crudest possible trace viewer                 | You can inspect failures without exposing private inputs            |
| 10  | Read development failures; group them; add development cases                                   | Error taxonomy; release holdout untouched                           |
| 11  | Fix one common failure and compare on development                                              | Measured change, including no improvement if that is the result     |
| 12  | Deploy and harden: container, secrets, rate limit, per-user cost cap, graceful degradation     | **A public URL**                                                    |
| 13  | Validate a judge if needed; regression checks in CI; fix candidate and release criteria        | Reproducible evaluation and declared decision rules                 |
| 14  | Run reserved release cases; save demo, costs and known failures                                | Release or defer decision supported by results                      |

Use deterministic checks for objective tasks; a model judge is optional. Run selected repeated
trials for stochastic/tool-heavy cases within the budget and disclose the count. Do not rerun a
failed release until it happens to pass. Investigate on development data and acquire fresh release
evidence if changes have been tuned to the old holdout.

Days 12 and 13 ask for skills this book has not taught yet — containers, secrets, CI. That is
deliberate: [Chapter 6](../06-production/README.md) teaches them properly, and takes this exact
application as its starting point. For now the crudest deploy that produces a public URL is enough.
Check current hosting eligibility and charges before choosing a route.
[Hugging Face Spaces](https://huggingface.co/docs/hub/spaces-overview) still offers free Static
Spaces; creating Gradio/Docker Spaces has account-plan requirements and some ZeroGPU exceptions.
Free CPU hardware and permission to create a Space are separate issues.
[Modal pricing](https://modal.com/pricing) distinguishes compute credits from Shared Endpoints,
whose per-token charges are not covered by those credits. Neither route guarantees free model API
calls or a free running demo.

Completion means a usable URL, an honest independent quality report, regression checks, access and
spending controls, known failures, a cost table and feedback from at least one other user. A
measured lack of improvement is a valid result; release claims need independent evidence.

After release, model/SDK upgrades, prompt changes and corpus refreshes are separate versioned
changes. Recheck retrieval coverage, access filtering, task quality and cost before rollout; retain
the compatible previous configuration and index for rollback, subject to current permissions and
deletions. A rollback must not restore revoked access or withdrawn sources. Observe sampled real
failures and user corrections under the trace-retention policy. Chapter 6 develops this operating
loop. If the sprint's release results guide later changes, acquire fresh release cases for week 32
and keep the earlier cases for regression testing.

## Before you move on

- You can explain why error analysis comes before evaluation tooling.
- You can validate deterministic graders; if you use a model judge, you can show its confusion
  matrix, failure sensitivity and false-alarm rate.
- You can distinguish CI regression cases from an independent release evaluation.
- You can demonstrate a denied tool action, timeout and tested fallback.
- You can state cost per attempt/success and the limits of the quality estimate.

## A few things worth knowing

- **Tutorial code ages.** Check repository status, dependencies, available models and endpoint
  versions before reproducing it; preserve the conceptual lesson while updating executable details.
- **Frameworks are a choice.** They can help persistence, tracing and integration; a small explicit
  workflow can be easier to inspect. Compare what your application actually needs.
- **Model names age quickly.** Everything specific in this chapter will be superseded. Tokenisation,
  attention, cache economics, retrieval, evaluation and context management will not, so that is
  where the study time is best spent.

---

[Previous: Deep learning](../04-deep-learning/README.md) &nbsp;·&nbsp;
[Next: Running it in production](../06-production/README.md)
