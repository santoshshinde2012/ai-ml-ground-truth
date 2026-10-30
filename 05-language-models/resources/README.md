# Resources — Chapter 5: Language models and AI engineering

Everything referenced in [the chapter](../README.md), grouped by purpose. **49 resources** are
listed. This is a catalogue, not a list to finish. The main chapter uses selected lessons and
readings within its 100-hour budget.

Hours below are suggested study budgets, not exact video runtimes or vendor estimates. “Free”
describes access to the material. API calls, hosted notebooks, hardware and certificates may cost
extra. Check current availability, prices and model/SDK versions before use.

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
exercises. An overview cannot show how reliable a particular model is or explain every later
post-training technique.

### [Building with the Claude API (Claude Academy)](https://academy.claude.com/courses/building-with-the-claude-api)

_Anthropic education team_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material &nbsp;·&nbsp; about 9
hours

Provider-written lessons on API requests, prompting/evaluation, tools, retrieval and agent
integrations. Pick request contracts, prompt evaluation and tool use for weeks 23-24. Exercises may
need an API key and paid usage. Check runnable examples against current docs. A course's model IDs
or MCP revision may not match your installed client.

### [Claude prompt engineering docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)

_Anthropic documentation team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3
hours

A signpost to model-specific guidance on clarity, examples, structure and context handling. Start
with clear success criteria and an evaluation, then test the techniques that fit your failure cases.
Reasoning and effort advice depends on the current model and endpoint. Older notebook prompting
instructions may not apply.

### [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

_Anthropic Applied AI team_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

The September 2025 essay connects instructions, tools, sources, history, compaction and memory. Use
it to plan a context budget and test what summaries keep. Its patterns come from vendor experience
with Claude agents. Compare them with your own tasks and the long-context research below.

### [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/)

_Eugene Yan_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

A useful 2023 taxonomy of evaluation, retrieval, tuning, caching, guardrails, defensive interfaces
and feedback, with links to its sources. Read it for architecture choices and failure modes. Check
current primary documentation before adopting its named models, costs or implementation examples.

### [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)

_Hamel Husain_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

The 2024 article presents assertions, human/model review and product experiments as separate
evaluation layers. Use it to start reading traces, instead of buying tooling before the task is
defined. Pair it with independent release data and agent final-state checks from this chapter.

### [AI Evals: Everything You Need to Know (Evals FAQ)](https://hamel.dev/blog/posts/evals-faq/)

_Hamel Husain & Shreya Shankar_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3–5 hours

Published and revised in September 2026. Detailed practical guidance on error analysis, rubrics,
annotation interfaces and judge validation across retrieval, agent and document tasks. Read selected
sections once you have development failures. Its workflow preferences and effort estimates are
advice from the authors' experience, not measured requirements for every project. Where a
requirement really has degrees, use a defined graded rubric.

### [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

_Erik Schluntz & Barry Zhang_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

The December 2024 workflow/agent taxonomy: chaining, routing, parallelisation, orchestrator-workers
and evaluator-optimiser. Use it to justify a fixed workflow or a bounded agent. It reports
Anthropic's observations. It does not prove that frameworks or multi-agent systems are always better
or worse. Pair it with the 2026 reliability and evaluation papers below.

### [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)

_Dex Horthy and contributors_ &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–4 hours

Opinionated principles on owning prompts, context and control flow, pause/resume, business state,
errors and focused agents. Useful for comparing an explicit loop with a framework. Turn each
relevant principle into an application requirement and a failure test. Popularity is not proof of
runtime reliability.

### [Model Context Protocol — official docs](https://modelcontextprotocol.io/docs/getting-started/intro)

_MCP maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6–10 hours

The official starting point for tools, resources, transport and authorisation. Before building,
identify the spec revision and SDK versions on both sides. Study discovery, schemas, errors,
cancellation and permissions for one read-only integration. The protocol standardises interaction.
It does not authorise users or guarantee safe tools.

### [MCP 2026-07-28 specification changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)

_MCP specification maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2
hours

Explains the stateless core, removed initialisation/protocol sessions, multi-round-trip requests and
feature lifecycle. Roots, sampling and logging are deprecated, not yet removed. Older tutorials can
still be right for an earlier deployed revision. Read it with client/server compatibility tests. A
transport retry is not business idempotency.

### [Anthropic Engineering blog](https://www.anthropic.com/engineering)

_Anthropic engineering teams_ &nbsp;·&nbsp; Article index &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Use single essays for particular design questions, not the rolling index as a curriculum. The
context and evaluation essays are linked directly in this catalogue. Keep vendor case studies apart
from independently measured results. Before transferring a recommendation, check the model, tool
permissions, budget and task behind it.

## Targeted research and implementation references

These sources explain specific decisions in the chapter. Read the linked abstract or documentation
section first. The full paper is optional. Dates show when the work was done, not that its tested
models are still current.

### [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

_Anthropic engineering team_ &nbsp;·&nbsp; Article, January 2026 &nbsp;·&nbsp; Free &nbsp;·&nbsp;
1–2 hours

Task, trial, grader, transcript and harness design, including deterministic and model-based grading
and repeatability. The useful distinction is between an agent's answer and what happened in the
environment. Use these sections in week 26. This is a vendor engineering account, so validate
graders and release criteria on your application's cases.

### [Eval awareness in Claude Opus 4.6's BrowseComp performance](https://www.anthropic.com/engineering/eval-awareness-browsecomp)

_Anthropic_ &nbsp;·&nbsp; Investigation, March 2026 &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

Documents leaked public answers and answer-key discovery in a web-enabled evaluation. It separates
runtime contamination from training contamination. Use it to design answer-key isolation, source
audits and fresh private tests. The observed rates apply only to its model, benchmark, budgets and
agent configurations.

### [Towards a Science of AI Agent Reliability](https://proceedings.mlr.press/v306/rabanser26a.html)

_Stephan Rabanser and coauthors_ &nbsp;·&nbsp; Peer-reviewed ICML 2026 paper &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 2–3 hours

A framework covering consistency, robustness, predictability and safety with explicit reliability
metrics. Its model/benchmark results argue for repeated trials, perturbations and error-severity
reporting over a single average. Choose a few metrics that matter for your task. Copy a full
benchmark profile into a small learner project only with a reason.

### [When Linguistic and Internal Confidence Diverge in Large Language Models](https://arxiv.org/abs/2608.28382)

_Hefan Zhang and coauthors_ &nbsp;·&nbsp; August 2026 preprint, revised 4 September; authors report
EMNLP Findings acceptance &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours of optional reading

Separates association, numerical agreement and calibration of reported confidence. Its open-model
experiments argue for checking confidence against task correctness before routing or abstention.
Logit and semantic-entropy measures are proxies too. Compare accepted-answer error with coverage and
cost on independent cases. A useful ranking signal is not automatically a probability of being
correct. These experiments do not show calibration for your current provider model.

### [Mid-Harness: Scaling Actions Between Model and Harness for Terminal Agents](https://arxiv.org/abs/2609.39982)

_Minki Kang and coauthors_ &nbsp;·&nbsp; Preprint, 30 September 2026 &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 1–2 hours

Studies sampling and verifying candidate actions before execution. Its terminal-agent experiments
show why verifier strength matters when spending extra inference compute. Treat the results as
recent experiments, not a production recipe. Compare against a bounded baseline at the same overall
budget. Verification cannot replace permission checks or safe execution.

### [Retrieval Augmented Generation or Long-Context LLMs?](https://aclanthology.org/2024.emnlp-industry.66/)

_Zhuowan Li and coauthors_ &nbsp;·&nbsp; EMNLP Industry 2024 paper &nbsp;·&nbsp; Free &nbsp;·&nbsp;
1–2 hours

Compares retrieval with long context and introduces a hybrid routing method. Read the quality/cost
trade-off and the experimental setup, then design your own comparison. Its tested models and tasks
are from 2024. Neither approach wins everywhere, and current models need a fresh evaluation on the
same permitted corpus and query families.

### [NoLiMa: Long-Context Evaluation Beyond Literal Matching](https://arxiv.org/abs/2502.05167)

_Ali Modarressi and coauthors_ &nbsp;·&nbsp; ICML 2025 paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2
hours

Tests long-context retrieval where matching words do not give away the answer. Use it to add
paraphrases and indirect evidence to your context tests. It shows a weakness of easy needle
evaluations. It does not set a safe context length for later models or your domain.

### [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)

_Kenneth Enevoldsen and coauthors_ &nbsp;·&nbsp; Research paper, 2025 &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 1–2 hours

Broadens embedding evaluation across tasks and languages. Useful for narrowing a candidate list by
language and task, instead of treating one English retrieval leaderboard as universal. Make the
final choice with domain-labelled retrieval queries, query/document prefixes, serving latency,
embedding/index size and permitted model use.

### [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352)

_Edoardo Debenedetti and coauthors_ &nbsp;·&nbsp; Research paper, 2024 &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 1–2 hours

A tool-agent environment for studying malicious instructions in otherwise useful external data. Use
its threat model to build harmless injection tests and check both task success and unwanted effects.
A benchmark defence result does not fully protect another tool environment. Application permissions
and isolation are still needed.

### [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948)

_DeepSeek-AI_ &nbsp;·&nbsp; Research paper, 2025 &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

Primary results on reasoning-oriented RL, staged post-training and distillation in the paper's
setting. Read it to tell apart supervised examples, preference training, verifiable rewards and
distillation. These results do not make RL the best next step for a document assistant. Your reward
validity, data, compute budget and held-out task outcomes decide that.

### [TRL — GRPO trainer documentation](https://huggingface.co/docs/trl/grpo_trainer)

_Hugging Face TRL contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–4
hours

The runnable reference for reward functions, configuration, generation and training metrics. For an
optional bounded task, check the reward for correctness and gaming before training. Pin the library
version. Keep the optimisation reward separate from independent quality, safety and deployment cost.
It is a reference, not a required experiment in the 100-hour chapter.

### [Sentence Transformers — retrieve and rerank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)

_Sentence Transformers contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp;
1–2 hours

A practical two-stage example: retrieve candidates, then score query-document pairs with a
cross-encoder. Compare relevance gain with added latency and cost. The reranker cannot recover a
relevant source that retrieval or access filtering excluded. Evaluate candidate coverage separately
from final ordering.

### [MCP — official security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)

_MCP specification maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2
hours

Reference for token audience, authorisation, confused-deputy/token-passthrough risks, redirect
validation, SSRF and scope management. Apply the controls that fit your transport and deployment.
Check permissions at the resource/action boundary. Interoperability and a successful connection do
not grant business authorisation.

### [Claude pricing and prompt-cache documentation](https://platform.claude.com/docs/en/about-claude/pricing)

_Anthropic documentation team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1
hour

Use the current pricing page with
[cache behaviour](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) to model
input/output, cache writes/reads, batch and tool charges. Then measure actual usage, hit rates and
retries. Rates and features vary by model and endpoint. A cached-input discount does not discount
every part of a request. Check
[thinking usage and billing](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost).
Thinking-token details are part of the output total, not a separate token bill.

## Optional depth

Choose one branch after the application works. The full courses and books below add to the
schedule. Their study budgets are outside the chapter's 100 hours.

### [a smol course — post-training](https://huggingface.co/learn/smol-course/en/unit0/1)

_Hugging Face education team_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material &nbsp;·&nbsp; 20–35
hours

Hands-on instruction tuning, evaluation, preference alignment and vision-language examples using the
Hugging Face training ecosystem. Check the live unit list. Its introduction still lists RL and
synthetic-data units as forthcoming, and the release months have no year, so check availability
yourself. Use current TRL docs for a specific RL experiment.

### [AI Engineering: Building Applications with Foundation Models](https://huyenchip.com/books/)

_Chip Huyen_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 25–35 hours

An architectural view of evaluation, datasets, retrieval, tuning, inference and product choices.
Useful for connecting this chapter to production. A book's examples are a snapshot, so check live
tool interfaces and prices in their documentation. Pick the chapters that answer your current design
question, rather than reading another complete survey before shipping.

### [AI Evals for Engineers & Product Managers](https://maven.com/parlance-labs/evals)

_Hamel Husain & Shreya Shankar_ &nbsp;·&nbsp; Cohort course &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 30–40
hours

An optional structured route with instructor feedback and cohort exercises. Check the current
syllabus, dates, price and access terms on the course page. Read the instructors' free FAQ first and
decide whether feedback and accountability are worth it for you. The roadmap does not require buying
a course.

### [Anthropic's Interactive Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)

_Anthropic education team_ &nbsp;·&nbsp; Interactive repository &nbsp;·&nbsp; Free material
&nbsp;·&nbsp; 5–8 hours

Exercises on instruction clarity, examples and structure. Check notebook model IDs, dependencies and
API availability before running. Compare older techniques with the current prompting docs. Keep an
exercise's change only when it improves your measured task. Running API exercises may cost money.

### [Build a Large Language Model (From Scratch)](https://www.manning.com/books/build-a-large-language-model-from-scratch)

_Sebastian Raschka_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 40–60 hours

Step-by-step transformer implementation, training and tuning for readers who want the mechanisms
under the API. The free [companion repository](https://github.com/rasbt/LLMs-from-scratch) works on
its own. Read attention, positional representations and normalisation alongside its working code,
and check each example's dependencies and scope. Pick one architecture to understand deeply. A
fast-changing model directory or star count is not a completion target. The optional architecture
implementations are extra study, not a reason to delay the application chapter or a verified list of
the newest model releases.

### [Build a Reasoning Model (From Scratch)](https://www.manning.com/books/build-a-reasoning-model-from-scratch)

_Sebastian Raschka_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 35–50 hours

The publisher lists **June 2026** publication. Covers reasoning evaluation, inference-time
techniques, reinforcement learning and distillation. The
[free code](https://github.com/rasbt/reasoning-from-scratch) supports practical study. It needs
PyTorch and transformer familiarity. This is an optional post-training branch, not a prerequisite for
building a reliable API-backed application.

### [Hands-On Large Language Models](https://www.llm-book.com/)

_Jay Alammar & Maarten Grootendorst_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 25–35 hours

A visual, practical introduction to embeddings, transformers, search, retrieval and tuning. The
[notebooks](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models) are public. Use the
illustrations for concepts. Update dependencies and model choices before reproducing applied
examples. Pair it with current evaluation and security references.

### [Hugging Face Agents Course](https://huggingface.co/learn/agents-course)

_Hugging Face education team_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material &nbsp;·&nbsp; 25–40
hours

Agent foundations and examples using smolagents, LangGraph and LlamaIndex, followed by practical
tasks. Useful for exploring execution/persistence abstractions after you write a bounded loop. It is
not a controlled comparison of which framework suits your task. Make that comparison with identical
cases, tool permissions and budgets.

### [Hugging Face Context Course](https://huggingface.co/learn/context-course)

_Hugging Face and contributing instructors_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material
&nbsp;·&nbsp; 12–20 hours

Context practice for coding agents, covering skills, tool integrations and agent execution. Choose
sections matching your environment and check version-specific instructions before running them. Test
retrieval, memory and compaction against task constraints. Coding-agent examples do not replace
application access checks or a reliability evaluation.

### [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)

_Hugging Face education team_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material &nbsp;·&nbsp; 70–90
hours

A substantial route through Transformers, datasets, tokenizers, fine-tuning and later reasoning
topics. Chapters 1–4 give the library foundations. Choose advanced units if you pursue open-weight
training. The whole course is a separate study branch, not part of this chapter's 100-hour
application path.

### [Hugging Face MCP Course](https://huggingface.co/learn/mcp-course/en/unit0/introduction)

_Hugging Face and MCP contributors_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free material &nbsp;·&nbsp;
15–25 hours

A guided protocol introduction with practical integrations. Check which revision the exercise
client/server implement. Session and initialisation examples can be correct for older revisions. The
2026-07-28 changelog shows removed versus deprecated features. Mix lifecycle instructions from
different revisions only after compatibility testing.

### [Lil'Log — research archive](https://lilianweng.github.io/archives/)

_Lilian Weng_ &nbsp;·&nbsp; Research surveys &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–4 hours

Use the archive to find a survey for a concrete question, then follow its primary papers.
[Harness Engineering for Self-Improvement (July 2026)](https://lilianweng.github.io/posts/2026-07-04-harness/)
is relevant to feedback and evaluation loops. These are research surveys, often denser than the main path. Experimental
self-improvement techniques need independent validation.

### [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)

_Lilian Weng_ &nbsp;·&nbsp; Article, 2023 &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Planning, memory, tool use and reflection give a useful conceptual breakdown. The named systems and
techniques are historical examples. Compare them with your bounded workflow and current tool APIs.
Age alone does not make a technique obsolete, nor does a later protocol solve its reliability
problems.

### [The Annotated Transformer — source and notebook](https://github.com/harvardnlp/annotated-transformer)

_Alexander Rush and contributors_ &nbsp;·&nbsp; Interactive repository &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 4–6 hours

An annotated implementation of the original encoder-decoder Transformer, connecting equations with
PyTorch. The repository has the notebook source if the hosted article is unavailable. Use it for
attention and training mechanics. It is not a complete template for every modern decoder-only or
multimodal architecture.

### [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

_Jay Alammar_ &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

A visual introduction to attention and the original encoder-decoder architecture. Follow it with a
modern implementation for positional representations, grouped-query attention, cache behaviour or
mixture-of-experts, where your chosen model uses them. Modern architectures differ. Not every
language model needs each of those mechanisms.

## Keep for reference

Look these up when a specific task needs them rather than reading each one end to end.

### [Ahead of AI — newsletter/archive](https://magazine.sebastianraschka.com/archive)

_Sebastian Raschka_ &nbsp;·&nbsp; Articles &nbsp;·&nbsp; Free/paid access varies &nbsp;·&nbsp; 1–2
hours

Architecture and training explanations that link to underlying work. Pick a topic that fits your
experiment and check model/release facts against the primary paper or model card. An archive is a
moving index, not a reproducible source for an unnamed “latest best model”.

### [DeepLearning.AI Short Courses](https://www.deeplearning.ai/short-courses/)

_DeepLearning.AI and partner instructors_ &nbsp;·&nbsp; Courses &nbsp;·&nbsp; Access terms vary
&nbsp;·&nbsp; 1–3 hours each

Short introductions to single tools and methods. Before an exercise, pick one relevant evaluation,
retrieval or deployment course, not the whole catalogue. Check current access terms and SDK
versions, because access, duration and syllabus vary. Use the live course page to decide whether it
fits your schedule and budget.

### [llama.cpp](https://github.com/ggml-org/llama.cpp)

_Georgi Gerganov and contributors_ &nbsp;·&nbsp; Inference repository &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 5–15 hours

Useful for understanding quantisation, batching, context/KV-cache memory and hardware-specific
inference. Benchmark the exact model, quantisation, context and concurrency you plan to serve.
Include hardware and running costs when you compare with an API. Faster local inference does not
automatically lower a provider's token-priced bill.

### [Ollama](https://ollama.com/)

_Ollama team_ &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Local software free; cloud terms vary &nbsp;·&nbsp;
2–4 hours

A convenient local model runtime that also has cloud features. The official
[FAQ](https://docs.ollama.com/faq) explains local versus cloud processing and documents local-only
configuration. Check the endpoint, web-search/tools and logging path before claiming data stays
local. RAM/VRAM needs depend on weights, quantisation, context and concurrency. Measure on your
machine instead of promising that a model size always runs comfortably.

### [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

_OpenAI and community contributors_ &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free material
&nbsp;·&nbsp; 3–8 hours

Provider-maintained runnable examples for selected API patterns and evaluation methods. Use the
recipe that matches your task, then check its dependencies, supported model and current endpoint.
Separate portable design ideas from provider-specific interfaces and charges. You can use a recipe
without adopting its whole application architecture.

### [Simon Willison's blog](https://simonwillison.net/)

_Simon Willison_ &nbsp;·&nbsp; Articles and experiments &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Hands-on reports about model tools, local experiments and security. Useful for finding a concrete
experiment or failure case to reproduce. Separate tested behaviour from commentary and predictions.
A forecast about sandboxing or coding ability does not show a security boundary is solved.

### [Unsloth — fine-tuning docs and notebooks](https://unsloth.ai/docs)

_Unsloth team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free material &nbsp;·&nbsp; 6–12 hours

A practical option for adapter/quantised training with supported notebooks. Before budgeting, check
current model-specific requirements, licence, sequence length, batch and GPU availability. Free
Colab is not guaranteed, and QLoRA has no universal memory figure or fixed quality loss. Compare
adapters with the untuned model on independent cases, including serving costs.

### [OWASP — Prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

_OWASP GenAI Security Project_ &nbsp;·&nbsp; Reference &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

Read this before attaching private retrieval or write-capable tools. Use the threat model to test
hostile retrieved instructions, cross-user access and unauthorised effects with harmless data.
Combine prompt-level defences with application permissions and isolation. A model instruction alone
cannot enforce authorisation. Pair it with Anthropic's
[August 2026 evaluation-containment incident account](https://www.anthropic.com/news/improving-alignment-security-efforts).
Use fake credentials and check network boundaries in the learner harness. The vendor-reported cyber evaluation incidents
motivate testing containment. They are not a controlled estimate of failure in ordinary application
deployments.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
