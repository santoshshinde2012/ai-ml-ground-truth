# Resources — Chapter 5: Language models and AI engineering

Everything referenced in [the chapter](../README.md), grouped by purpose. **50 resources** are
listed; this is a catalogue, not a requirement to complete them all. The main chapter uses selected
lessons and readings within its 100-hour budget.

Hours below are suggested study budgets, not guaranteed video runtimes or vendor estimates. “Free”
describes access to the material; API calls, hosted notebooks, hardware and certificates may have
separate charges. Check current availability, prices and model/SDK versions before use.

**Browse:** [Start here](#start-here) &nbsp;·&nbsp;
[Targeted research and implementation references](#targeted-research-and-implementation-references)
&nbsp;·&nbsp; [Optional depth](#optional-depth) &nbsp;·&nbsp;
[Keep for reference](#keep-for-reference)

---

## Start here

Use the first API, context and evaluation readings to build the baseline. MCP is an optional week-30
branch. Read vendor examples as implementations to test, not neutral comparisons.

### [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)

_Andrej Karpathy_ &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 4 hours

A broad introduction to tokenisation, model training, post-training and model behaviour. Useful for
connecting the API to what the model learned. Watch selected sections alongside the chapter
exercises; a conceptual overview does not establish the reliability of a particular model or explain
every later post-training technique.

### [Building with the Claude API (Claude Academy)](https://academy.claude.com/courses/building-with-the-claude-api)

_Anthropic education team_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material &nbsp;·&nbsp; about 9
hours

Provider-authored lessons on API requests, prompting/evaluation, tools, retrieval and agent
integrations. Select request contracts, prompt evaluation and tool use for weeks 23-24. Exercises
may require an API key and paid usage. Cross-check executable examples against current docs rather
than assuming a course's model IDs or MCP revision match your installed client.

### [Claude prompt engineering docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)

_Anthropic documentation team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3
hours

A signpost to model-specific guidance on clarity, examples, structure and context handling. Begin
with explicit success criteria and an evaluation, then test the techniques relevant to your failure
cases. Reasoning and effort recommendations depend on the current model and endpoint; older notebook
prompting instructions are not automatically applicable.

### [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

_Anthropic Applied AI team_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

The September 2025 essay connects instructions, tools, sources, history, compaction and memory. Use
it to plan a context budget and test what summaries preserve. Vendor experience with Claude agents
motivates its patterns; compare those patterns with your own tasks and the long-context research
below.

### [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/)

_Eugene Yan_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

A useful 2023 taxonomy of evaluation, retrieval, tuning, caching, guardrails, defensive interfaces
and feedback, with links to its evidence. Read for architecture choices and failure modes. Check
current primary documentation before adopting its named models, costs or implementation examples.

### [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)

_Hamel Husain_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

The 2024 article introduces assertions, human/model review and product experiments as different
evaluation layers. Use it to start inspecting traces rather than buying tooling before defining the
task. Pair it with independent release data and agent final-state checks from this chapter.

### [AI Evals: Everything You Need to Know (Evals FAQ)](https://hamel.dev/blog/posts/evals-faq/)

_Hamel Husain & Shreya Shankar_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3–5 hours

Published and revised in September 2026. Detailed practitioner guidance on error analysis, rubrics,
annotation interfaces and judge validation across retrieval, agent and document tasks. Read selected
sections after you have development failures. Its workflow preferences and effort estimates are
advice from the authors' experience, not measured requirements for every project; use a defined
graded rubric where the requirement genuinely has degrees.

### [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

_Erik Schluntz & Barry Zhang_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

The December 2024 workflow/agent taxonomy: chaining, routing, parallelisation, orchestrator-workers
and evaluator-optimiser. Use it to justify a fixed workflow or a bounded agent. It describes
Anthropic's observations; it does not prove that frameworks or multi-agent systems are always better
or worse. Pair with the 2026 reliability and evaluation papers below.

### [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)

_Dex Horthy and contributors_ &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–4 hours

Opinionated principles about owning prompts, context and control flow; pause/resume; business state;
errors and focused agents. Useful for comparing an explicit loop with a framework. Turn each
relevant principle into an application requirement and a failure test. Repository popularity is not
evidence of runtime reliability.

### [Model Context Protocol — official docs](https://modelcontextprotocol.io/docs/getting-started/intro)

_MCP maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6–10 hours

The canonical starting point for tools, resources, transport and authorization. Identify the spec
revision and SDK versions implemented on both sides before building. Study discovery, schemas,
errors, cancellation and permissions for one read-only integration. The protocol standardises
interaction; it does not authorize users or guarantee safe tools.

### [MCP 2026-07-28 specification changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)

_MCP specification maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2
hours

Explains the stateless core, removed initialization/protocol sessions, multi-round-trip requests and
feature lifecycle. Roots, sampling and logging are deprecated, not immediately removed. Earlier
tutorials can still describe an earlier deployed revision correctly. Read alongside client/server
compatibility tests; a transport retry is not a business idempotency guarantee.

### [Anthropic Engineering blog](https://www.anthropic.com/engineering)

_Anthropic engineering teams_ &nbsp;·&nbsp; Article index &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Use individual essays for particular design questions rather than reading the rolling index as a
curriculum. The context and evaluation essays are linked directly in this catalogue. Separate vendor
case studies from independently measured results, and check the model, tool permissions, budget and
task used before transferring a recommendation.

## Targeted research and implementation references

These sources explain specific decisions in the chapter. Read the linked abstract or relevant
documentation section first; full-paper study is optional. Dates indicate the evidence's period, not
a promise that its tested models remain current.

### [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

_Anthropic engineering team_ &nbsp;·&nbsp; Article, January 2026 &nbsp;·&nbsp; Free &nbsp;·&nbsp;
1–2 hours

Task, trial, grader, transcript and harness design, including deterministic and model-based grading
and repeatability. The useful distinction is between an agent's answer and what happened in the
environment. Select these sections for week 26. This is a vendor engineering account, so validate
graders and release criteria on your application's cases.

### [Eval awareness in Claude Opus 4.6's BrowseComp performance](https://www.anthropic.com/engineering/eval-awareness-browsecomp)

_Anthropic_ &nbsp;·&nbsp; Investigation, March 2026 &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

Documents leaked public answers and answer-key discovery in a web-enabled evaluation. It
distinguishes runtime contamination from training contamination. Use it to design answer-key
isolation, source audits and fresh private tests; the observed rates are specific to its model,
benchmark, budgets and agent configurations.

### [Towards a Science of AI Agent Reliability](https://proceedings.mlr.press/v306/rabanser26a.html)

_Stephan Rabanser and coauthors_ &nbsp;·&nbsp; Peer-reviewed ICML 2026 paper &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 2–3 hours

A framework covering consistency, robustness, predictability and safety with explicit reliability
metrics. Its model/benchmark results motivate repeated trials, perturbations and error-severity
reporting rather than a single average. Choose a few metrics meaningful for your task; do not copy a
complete benchmark profile into a small learner project without a reason.

### [When Linguistic and Internal Confidence Diverge in Large Language Models](https://arxiv.org/abs/2608.28382)

_Hefan Zhang and coauthors_ &nbsp;·&nbsp; August 2026 preprint, revised 4 September; authors report
EMNLP Findings acceptance &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours of optional reading

Separates association, numerical agreement and calibration of reported confidence. Its open-model
experiments motivate checking confidence against task correctness before routing or abstention;
logit and semantic-entropy measures are proxies too. Compare accepted-answer error against coverage
and cost on independent cases. A useful ranking signal is not automatically a correctness
probability, and these experiments do not establish calibration for your current provider model.

### [Mid-Harness: Scaling Actions Between Model and Harness for Terminal Agents](https://arxiv.org/abs/2609.39982)

_Minki Kang and coauthors_ &nbsp;·&nbsp; Preprint, 30 September 2026 &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 1–2 hours

Studies sampling and verifying candidate actions before execution. Its terminal-agent experiments
show why verifier strength matters when allocating extra inference compute. Treat the results as
recent experimental evidence, not a production recipe. Compare against a bounded baseline at the
same overall budget; verification cannot replace permission checks or safe execution.

### [Retrieval Augmented Generation or Long-Context LLMs?](https://aclanthology.org/2024.emnlp-industry.66/)

_Zhuowan Li and coauthors_ &nbsp;·&nbsp; EMNLP Industry 2024 paper &nbsp;·&nbsp; Free &nbsp;·&nbsp;
1–2 hours

Compares retrieval and long context and introduces a hybrid routing method. Read the quality/cost
trade-off and experimental setup to design your own comparison. Its tested models and tasks are from
2024; neither approach is universally superior, and current models need a new evaluation on the same
permitted corpus and query families.

### [NoLiMa: Long-Context Evaluation Beyond Literal Matching](https://arxiv.org/abs/2502.05167)

_Ali Modarressi and coauthors_ &nbsp;·&nbsp; ICML 2025 paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2
hours

Tests long-context retrieval where matching words do not give away the answer. Use it to add
paraphrases and indirect evidence to your context tests. It exposes a limitation of easy needle
evaluations; it does not determine a universal safe context length for later models or your domain.

### [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)

_Kenneth Enevoldsen and coauthors_ &nbsp;·&nbsp; Research paper, 2025 &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 1–2 hours

Broadens embedding evaluation across tasks and languages. Useful for narrowing a candidate list by
language and task rather than treating one English retrieval leaderboard as universal. Finish
selection using domain-labelled retrieval queries, query/document prefixes, serving latency,
embedding/index size and permitted model use.

### [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352)

_Edoardo Debenedetti and coauthors_ &nbsp;·&nbsp; Research paper, 2024 &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 1–2 hours

A tool-agent environment for studying malicious instructions in otherwise useful external data. Use
its threat model to build harmless injection tests and check both task success and unwanted effects.
A benchmark defence result does not establish complete protection for another tool environment;
application permissions and isolation remain necessary.

### [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948)

_DeepSeek-AI_ &nbsp;·&nbsp; Research paper, 2025 &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

Primary evidence on reasoning-oriented RL, staged post-training and distillation in the paper's
setting. Read to distinguish supervised examples, preference training, verifiable rewards and
distillation. These results do not imply RL is the best next step for a document assistant; your
reward validity, data, compute budget and held-out task outcomes govern that decision.

### [TRL — GRPO trainer documentation](https://huggingface.co/docs/trl/grpo_trainer)

_Hugging Face TRL contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–4
hours

The executable reference for reward functions, configuration, generation and training metrics. For
an optional bounded task, inspect reward correctness and gaming before running training. Pin the
library version and distinguish optimization reward from independent quality, safety and deployment
cost. It is a reference, not a mandatory experiment in the 100-hour chapter.

### [Sentence Transformers — retrieve and rerank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

_Sentence Transformers contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp;
1–2 hours

A practical two-stage example: retrieve candidates, then score query-document pairs with a
cross-encoder. Compare relevance gain against added latency and cost. The reranker cannot recover a
relevant source excluded by retrieval or access filtering; evaluate candidate coverage separately
from final ordering.

### [MCP — official security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)

_MCP specification maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2
hours

Reference for token audience, authorization, confused-deputy/token-passthrough risks, redirect
validation, SSRF and scope management. Apply the controls relevant to your transport and deployment.
Inspect permissions at the resource/action boundary; protocol interoperability and a successful
connection do not grant business authorization.

### [Claude pricing and prompt-cache documentation](https://platform.claude.com/docs/en/about-claude/pricing)

_Anthropic documentation team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1
hour

Use the current pricing page with
[cache behaviour](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) to model
input/output, cache writes/reads, batch and tool charges. Then measure actual usage, hit rates and
retries. Rates and features vary by model and endpoint; a cached-input discount is not a discount on
every component of a request. Check
[thinking usage and billing](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost):
thinking-token details are part of the output total, rather than an additional token bill.

## Optional depth

Choose one branch after the application works. Full courses and books below extend the schedule;
their study budgets are not included in the chapter's 100 hours.

### [a smol course — post-training](https://huggingface.co/learn/smol-course/en/unit0/1)

_Hugging Face education team_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material &nbsp;·&nbsp; 20–35
hours

Hands-on instruction tuning, evaluation, preference alignment and vision-language examples using the
Hugging Face training ecosystem. Check the live unit list: the introduction still lists RL and
synthetic-data units as forthcoming. The release months have no year there, so do not infer
availability from an old schedule. Use current TRL docs for a specific RL experiment.

### [AI Engineering: Building Applications with Foundation Models](https://huyenchip.com/books/)

_Chip Huyen_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 25–35 hours

An architectural view of evaluation, datasets, retrieval, tuning, inference and product choices.
Useful for connecting this chapter to production. A book's examples are a snapshot; verify live tool
interfaces and prices in their documentation. Select the chapters answering your current design
question rather than reading another complete survey before shipping.

### [AI Evals for Engineers & Product Managers](https://maven.com/parlance-labs/evals)

_Hamel Husain & Shreya Shankar_ &nbsp;·&nbsp; Cohort course &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 30–40
hours

An optional structured route with instructor feedback and cohort exercises. Check the current
syllabus, dates, price and access terms on the course page. Read the instructors' free FAQ first and
decide whether feedback/accountability adds enough value for your situation; the roadmap does not
require purchasing a course.

### [Anthropic's Interactive Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)

_Anthropic education team_ &nbsp;·&nbsp; Interactive repository &nbsp;·&nbsp; Free material
&nbsp;·&nbsp; 5–8 hours

Exercises on instruction clarity, examples and structure. Check notebook model IDs, dependencies and
API availability before running. Compare historical techniques with the current prompting docs;
retain an exercise only when its change improves your measured task. Executable API practice may
incur charges.

### [Build a Large Language Model (From Scratch)](https://www.manning.com/books/build-a-large-language-model-from-scratch)

_Sebastian Raschka_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 40–60 hours

Step-by-step transformer implementation, training and tuning for readers wanting the mechanisms
underneath the API. The [companion repository](https://github.com/rasbt/LLMs-from-scratch) can be
used independently. Treat optional architecture implementations as additional study, not a reason to
delay the application chapter or a verified list of the newest model releases.

### [Build a Reasoning Model (From Scratch)](https://www.manning.com/books/build-a-reasoning-model-from-scratch)

_Sebastian Raschka_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 35–50 hours

The publisher lists **June 2026** publication. Covers reasoning evaluation, inference-time
techniques, reinforcement learning and distillation. The
[free code](https://github.com/rasbt/reasoning-from-scratch) supports practical study. Requires
PyTorch and transformer familiarity; this is an optional post-training branch, not an additional
prerequisite for building a reliable API-backed application.

### [Hands-On Large Language Models](https://www.llm-book.com/)

_Jay Alammar & Maarten Grootendorst_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 25–35 hours

A visual practical introduction to embeddings, transformers, search, retrieval and tuning. The
[notebooks](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models) are public. Use the
illustrations for concepts; update dependencies and model choices before reproducing applied
examples. Complement it with current evaluation and security references.

### [Hugging Face Agents Course](https://huggingface.co/learn/agents-course)

_Hugging Face education team_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material &nbsp;·&nbsp; 25–40
hours

Agent foundations and examples using smolagents, LangGraph and LlamaIndex, followed by practical
tasks. Useful for examining different execution/persistence abstractions after writing a bounded
loop. It is not a controlled comparison proving which framework suits your task; make that
comparison using identical cases, tool permissions and budgets.

### [Hugging Face Context Course](https://huggingface.co/learn/context-course)

_Hugging Face and contributing instructors_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material
&nbsp;·&nbsp; 12–20 hours

Coding-agent context practice involving skills, tool integrations and agent execution. Choose the
sections matching your environment and check version-specific instructions before running them. Test
retrieval, memory and compaction against task constraints. Coding-agent examples do not replace
application access checks or a reliability evaluation.

### [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)

_Hugging Face education team_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material &nbsp;·&nbsp; 70–90
hours

A substantial route through Transformers, datasets, tokenizers, fine-tuning and later reasoning
topics. Chapters 1–4 provide library foundations; choose advanced units when pursuing open-weight
training. Completing the whole course is a separate study branch, not part of this chapter's
100-hour application path.

### [Hugging Face MCP Course](https://huggingface.co/learn/mcp-course/en/unit0/introduction)

_Hugging Face and MCP contributors_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material &nbsp;·&nbsp;
15–25 hours

A guided protocol introduction with practical integrations. Check which revision the exercise
client/server implement. Session and initialization examples can be correct for older revisions; the
2026-07-28 changelog identifies removed versus deprecated features. Do not mix lifecycle
instructions from different revisions without compatibility testing.

### [Lil'Log — research archive](https://lilianweng.github.io/archives/)

_Lilian Weng_ &nbsp;·&nbsp; Research surveys &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–4 hours

Use the archive to find a survey for a concrete question, then follow its primary papers.
[Harness Engineering for Self-Improvement (July 2026)](https://lilianweng.github.io/posts/2026-07-04-harness/)
is relevant to feedback and evaluation loops. These are research surveys, often denser than the main
path; experimental self-improvement techniques need independent validation.

### [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)

_Lilian Weng_ &nbsp;·&nbsp; Article, 2023 &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Planning, memory, tool use and reflection provide a useful conceptual decomposition. The named
systems and techniques are historical examples. Compare them with your bounded workflow and current
tool APIs; age alone does not prove a technique is obsolete or that a later protocol solves its
reliability problems.

### [LLMs-from-scratch — companion repository](https://github.com/rasbt/LLMs-from-scratch)

_Sebastian Raschka and contributors_ &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 20–30
hours

Executable model-building lessons and optional architecture examples. Read attention, positional
representations and normalization alongside a working implementation. Check each example's
dependencies and scope. Pick one architecture to understand deeply rather than treating a rapidly
changing model directory or star count as a course completion target.

### [The Annotated Transformer — source and notebook](https://github.com/harvardnlp/annotated-transformer)

_Alexander Rush and contributors_ &nbsp;·&nbsp; Interactive repository &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 4–6 hours

An annotated implementation of the original encoder-decoder Transformer, connecting equations with
PyTorch. The repository provides the notebook source if the hosted article is unavailable. Use it
for attention and training mechanics; it is not a complete template for every modern decoder-only or
multimodal architecture.

### [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

_Jay Alammar_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

A visual introduction to attention and the original encoder-decoder architecture. Follow with a
modern implementation for positional representations, grouped-query attention, cache behaviour or
mixture-of-experts where your chosen model uses them. Modern architectures differ; none of those
mechanisms is mandatory in every language model.

## Keep for reference

Look these up when a specific task needs them rather than reading each one end to end.

### [Ahead of AI — newsletter/archive](https://magazine.sebastianraschka.com/archive)

_Sebastian Raschka_ &nbsp;·&nbsp; Articles &nbsp;·&nbsp; Free/paid access varies &nbsp;·&nbsp; 1–2
hours

Architecture and training explanations that link to underlying work. Select a topic relevant to your
experiment and verify model/release facts against the primary paper or model card. An archive is a
moving index, not a reproducible source for an unspecified “latest best model”.

### [DeepLearning.AI Short Courses](https://www.deeplearning.ai/short-courses/)

_DeepLearning.AI and partner instructors_ &nbsp;·&nbsp; Courses &nbsp;·&nbsp; Access terms vary
&nbsp;·&nbsp; 1–3 hours each

Short introductions to individual tools and methods. Select a relevant evaluation, retrieval or
deployment course before its exercise, not the entire catalogue. Check current access terms and SDK
versions; course access, duration and syllabus vary. Use the live course page when deciding whether
it fits your schedule and budget.

### [llama.cpp](https://github.com/ggml-org/llama.cpp)

_Georgi Gerganov and contributors_ &nbsp;·&nbsp; Inference repository &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 5–15 hours

Useful for understanding quantisation, batching, context/KV-cache memory and hardware-specific
inference. Benchmark the actual model, quantisation, context and concurrency you intend to serve.
Include hardware and operating costs in comparisons with an API; a local inference lever is not
automatically a saving in a provider's token-priced bill.

### [Ollama](https://ollama.com/)

_Ollama team_ &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Local software free; cloud terms vary &nbsp;·&nbsp;
2–4 hours

A convenient local model runtime with cloud features as well. The official
[FAQ](https://docs.ollama.com/faq) distinguishes local and cloud processing and documents local-only
configuration. Verify the endpoint, web-search/tools and logging path before claiming data stays
local. RAM/VRAM needs depend on weights, quantisation, context and concurrency; measure on your
machine rather than promising that a model size always runs comfortably.

### [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

_OpenAI and community contributors_ &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free material
&nbsp;·&nbsp; 3–8 hours

Provider-maintained executable examples for selected API patterns and evaluation methods. Use the
recipe matching the task, then verify its dependencies, supported model and current endpoint.
Identify portable design ideas separately from provider-specific interfaces and charges. Reading a
recipe does not require adopting its entire application architecture.

### [Simon Willison's blog](https://simonwillison.net/)

_Simon Willison_ &nbsp;·&nbsp; Articles and experiments &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Hands-on reports about model tools, local experiments and security. Useful for finding a concrete
experiment or failure case to reproduce. Distinguish tested behaviour, commentary and predictions; a
forecast about sandboxing or coding capability is not evidence that a security boundary is solved.

### [Unsloth — fine-tuning docs and notebooks](https://unsloth.ai/docs)

_Unsloth team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free material &nbsp;·&nbsp; 6–12 hours

A practical option for adapter/quantised training with supported notebooks. Check the current
model-specific requirements, licence, sequence length, batch and GPU availability before budgeting.
There is no universal free-Colab guarantee, memory figure or fixed quality loss for QLoRA. Compare
adapters against the untuned model on independent cases and include serving costs.

### [OWASP — Prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

_OWASP GenAI Security Project_ &nbsp;·&nbsp; Reference &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

Read before attaching private retrieval or write-capable tools. Use the threat model to test hostile
retrieved instructions, cross-user access and unauthorized effects with harmless data. Combine
prompt-level defences with application permissions and isolation; a model instruction alone cannot
enforce authorization. Pair with Anthropic's
[August 2026 evaluation-containment incident account](https://www.anthropic.com/news/improving-alignment-security-efforts).
Use fake credentials and verify network boundaries in the learner harness. Its vendor-reported cyber
evaluation incidents motivate testing containment; they are not a controlled estimate of failure in
ordinary application deployments.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
