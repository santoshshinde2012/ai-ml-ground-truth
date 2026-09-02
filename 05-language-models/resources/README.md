# Resources — Chapter 5: Language models and AI engineering

Everything referenced in [the chapter](../README.md), grouped by how central it is, with a short
note on what each one is for.

Prices and free tiers change often, so check a resource's own page before you plan around one.

---

## Start here

The resources on the main path for this chapter, in the order the chapter uses them. If you only do a few things, do these.

### [Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)

*Andrej Karpathy* &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4 hours

The single best first artefact in the entire domain. 3h31m, general-audience but technically honest, and it is the only free resource that walks the entire training stack in one sitting: pretraining data, tokenisation, the transformer, SFT, RLHF, RLVR, plus mental models for hallucination, tool use and 'why the model can't count letters'. Watch this before touching any code — it gives you the map that makes everything else legible. Beats DeepLearning.AI intros because it explains mechanism, not API surface.

> **Worth knowing.** Pair it with a 2026 reasoning/RL source: the post-training section is the part that has aged.

### [Anthropic Courses (API fundamentals, real-world prompting, prompt evaluations, tool use)](https://github.com/anthropics/courses)

*Anthropic education team* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 12-18 hours

Five sequenced free courses. The two that matter most and that beginners skip: 'prompt evaluations' (writing production evals) and 'tool use' — tool use is the primitive that agents, MCP, structured output and RAG are all built on, so learn it directly from the provider before touching any framework. Pair with the Claude Cookbooks repo (github.com/anthropics/claude-cookbooks) for runnable recipes.

> **Worth knowing.** The notebooks still default to Claude 3 Haiku, which may no longer be callable — swap in a current model string. The prompting techniques, not the model choices, are what has aged well.

### [Claude prompt engineering docs and best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)

*Anthropic documentation team* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3 hours

The living reference, kept current per model generation — clarity, examples/multishot, XML structuring, role prompting, extended thinking, prompt chaining, long-context handling. Crucially it opens by telling you not to prompt-engineer until you have success criteria and a way to test empirically, which is the correct ordering that most prompt courses invert. Pair with claude.com/blog/best-practices-for-prompt-engineering for provider-agnostic craft.

> **Worth knowing.** The overview page is now mostly a signpost; the actual model-current guidance lives in the Claude prompting best-practices pages.

### [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

*Anthropic Applied AI team* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The clearest statement of the field's central 2026 shift from prompt engineering to context engineering, i.e. curating the whole token budget (system prompt, tools, examples, history, retrieved docs, compaction) rather than wordsmithing one prompt. If you only read one industry post about how the job changed, read this one. It reframes RAG, memory and tool design as one problem.

> **Worth knowing.** Vendor-authored: an Anthropic engineering post framed around Claude-family agent patterns. Useful and honest, but read it alongside a non-vendor source rather than as neutral guidance.

### [Patterns for Building LLM-based Systems & Products](https://eugeneyan.com/writing/llm-patterns/)

*Eugene Yan* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3-4 hours

Seven durable patterns — evals, RAG, fine-tuning, caching, guardrails, defensive UX, collect user feedback — each with the research behind it and the failure mode it addresses. The best free 'system design for LLM apps' reference, and unusually well-cited. His start-here page (eugeneyan.com/start-here/) is the guided entry point; 'Patterns for Building Cybersecurity Evals' (21 Jun 2026) is a good recent worked example of domain-specific eval design.

> **Worth knowing.** Strong on evals, RAG, fine-tuning, caching and guardrails as patterns, but every named model and leaderboard reference is 2023-vintage. Read it for the taxonomy, not the recommendations.

### [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)

*Hamel Husain* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The origin post (Mar 2024) that defined the now-standard three-level framework: L1 cheap assertion-style unit tests run constantly, L2 human + LLM-judge review of traces with a custom viewer, L3 A/B tests for mature products. Read this first, then the FAQ. Also see hamel.dev/notes/llm/ai-product-engineering/ for the broader notes.

> **Worth knowing.** 2024 post, partly superseded by Husain's own later free email course, which formalises the Analyze–Measure–Improve lifecycle. Read this first as the foundation, then the newer course.

### [LLM Evals: Everything You Need to Know (Evals FAQ)](https://hamel.dev/blog/posts/evals-faq/)

*Hamel Husain & Shreya Shankar* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-6 hours

Last updated 18 July 2026 and the most useful free document in applied LLM work. Distilled from teaching 700+ practitioners. The load-bearing claims a beginner must absorb: error analysis (manually reading 20–50 traces, open coding then axial coding) comes **before** any eval infrastructure; use binary pass/fail not 1–5 scales; appoint one domain expert as benevolent dictator; build a custom annotation viewer rather than adopting a generic eval platform; and expect evals to be 60–80% of your effort, not a testing afterthought. Covers RAG, agentic, multi-turn and document-processing evals specifically.

### [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)

*Erik Schluntz & Barry Zhang* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The reference taxonomy the whole industry now uses: workflows (prompt chaining, routing, parallelisation, orchestrator-workers, evaluator-optimiser) versus true agents. Its core finding is the most useful anti-hype sentence a beginner can internalise: the most successful implementations used simple composable patterns, not complex frameworks. Published Dec 2024 and still the correct starting frame; read it alongside the newer harness-design posts.

> **Worth knowing.** Nearly two years old and flagged as partly superseded by its own publisher. Valuable for the conceptual taxonomy — workflows vs agents, routing, orchestrator-workers, evaluator-optimiser — but its tooling advice is not current.

### [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)

*Dex Horthy* &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3-5 hours

25.4k stars, and the most useful anti-framework antidote for beginners. Twelve concrete principles, among them: own your prompts, own your context window, own your control flow, tools are just structured outputs, unify execution and business state, launch/pause/resume, contact humans with tool calls, compact errors into context, small focused agents, make your agent a stateless reducer. Read it right after you get frustrated by your first framework abstraction; it will explain why.

### [Model Context Protocol — official docs](https://modelcontextprotocol.io/docs/getting-started/intro)

*Anthropic and the MCP open-source maintainer group* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-15 hours

MCP is now a genuine cross-vendor standard — supported by Claude, ChatGPT, VS Code, Cursor and others — so it is one of the few 2026 'hot' skills that is safe to invest in. Learn it from the spec site, not from tutorials, because the 2026-07-28 release changed the fundamentals: stateless protocol core, server-minted handles instead of sessions, multi-round-trip requests, header-based routing, cacheable list results, hardened authorisation, and a formal extensions framework.

### [MCP 2026-07-28 specification changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)

*MCP specification maintainers* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2 hours

Read this specifically to avoid learning MCP wrong. Almost every MCP tutorial published in 2025 teaches the stateful session model that 2026-07-28 removed. The changelog also documents the new feature lifecycle policy (Active, Deprecated, Removed — minimum 12 months between deprecation and removal), which is the signal that MCP is now stable enough to build a career skill on. Context: blog.modelcontextprotocol.io/posts/2026-07-28/ and the 2026 roadmap post.

### [Anthropic Engineering blog](https://www.anthropic.com/engineering)

*Anthropic engineering and applied AI teams* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1-2 hours

The highest signal-to-noise industry feed for agent builders in 2026. Key entries to read in order: 'Building effective agents' (Dec 2024), 'How we built our multi-agent research system' (Jun 2025), 'Effective context engineering' (Sep 2025), 'Code execution with MCP: building more efficient agents' (Nov 2025), 'Demystifying evals for AI agents' (Jan 2026), 'Harness design for long-running application development' (Mar 2026), 'Scaling managed agents: decoupling the brain from the hands' (Apr 2026). That sequence is effectively a free graduate course in agent engineering.

> **Worth knowing.** A rolling blog index rather than a stable reference — specific essays drift down the feed over time.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [a smol course (post-training)](https://huggingface.co/learn/smol-course/en/unit0/1)

*Ben Burtenshaw* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 25-35 hours

The cheapest legitimate route into supervised fine-tuning and preference alignment. Units: instruction tuning, evaluation, preference alignment (DPO and friends), vision-language models, and — still marked forthcoming — RL and synthetic data. Built on TRL/PEFT/transformers, ~3–4h per unit, free certification. This is the practical counterpart to CS336's theory-heavy alignment lectures, and it's how you learn DPO without renting a cluster.

> **Worth knowing.** The RL and synthetic-data units — the post-training core — are still marked forthcoming on a two-year-old schedule, and four of seven units are SFT, eval, DPO and VLM basics. It does not cover modern post-training.

### [AI Engineering: Building Applications with Foundation Models](https://huyenchip.com/books/)

*Chip Huyen* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 25-35 hours

The best single map of the AI-Engineer job as a *discipline*: evaluation methodology, dataset engineering, RAG vs agents, inference optimisation, and product architecture. Deliberately light on code, heavy on decision frameworks, and notably less hype-driven than the flood of 'agentic AI' books. Honest caveat repeated across reviews: the breadth means several topics are surface-level, and being a 2024-written book it predates the 2026 agent-harness/MCP consolidation — pair it with Anthropic's engineering blog for the current layer.

### [AI Evals for Engineers & Product Managers (cohort course)](https://maven.com/parlance-labs/evals)

*Hamel Husain & Shreya Shankar* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 30-40 hours

The most respected paid course in applied LLM engineering, 700+ alumni. Listed here mainly so you can make an informed decision: for a beginner, the free FAQ and blog posts contain most of the intellectual content, and the premium you pay is for cohort accountability and office hours. Do the free writing first; only pay if your employer is funding it or you're already shipping an AI product that's failing.

> **Worth knowing.** $4,200 cohort course — by far the most expensive item here. The same instructors' free 17-part email course covers the same Analyze–Measure–Improve lifecycle.

### [Anthropic's Interactive Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)

*Anthropic applied AI / education team* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6-9 hours

9 chapters plus an advanced appendix, with an executable playground at the bottom of every lesson so you see the delta from each change immediately. It is written by the lab that trained the model, and it teaches structure — XML delimiters, examples, thinking, chaining — rather than incantations.

> **Worth knowing.** Every model ID in the notebooks needs updating before the code runs, and several Claude-3-era techniques are no longer best practice. The pedagogy transfers; pair it with current Anthropic prompt-engineering docs.

### [Build a Large Language Model (From Scratch)](https://www.manning.com/books/build-a-large-language-model-from-scratch)

*Sebastian Raschka, PhD* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 40-60 hours

The best paced, most complete text version of what Karpathy does on video. Where the book earns its money over free alternatives: it explains *why* each design choice exists at a beginner-appropriate speed, and the free companion repo has been kept current far beyond the book — it now includes standalone from-scratch implementations of Llama 3.2, Qwen3 dense + MoE, Qwen3.5, Gemma 3 and Gemma 4, and Olmo 3. If you buy one LLM book for the 'how does it work' half, buy this.

### [Build a Reasoning Model (From Scratch)](https://www.manning.com/books/build-a-reasoning-model-from-scratch)

*Sebastian Raschka, PhD* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 35-50 hours

Published 11 August 2026 — the newest serious book in the domain and the one that closes the biggest gap in every older curriculum. Starts from a pretrained LLM and builds evaluation harnesses, inference-time scaling (best-of-n, verifiers), reinforcement learning (RLVR-style), and distillation. This is exactly the post-o1/DeepSeek-R1 material that every 2024-era roadmap is missing. Free code at github.com/rasbt/reasoning-from-scratch.

> **Worth knowing.** Paid, and "from scratch" here presumes comfort with PyTorch and transformer internals — a sequel in spirit to his Build a Large Language Model (From Scratch). Not a starting point.

### [Hands-On Large Language Models](https://www.llm-book.com/)

*Jay Alammar & Maarten Grootendorst* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 25-35 hours

The best *illustrated* practitioner book — nearly 300 custom diagrams. Covers tokens/embeddings, transformer internals, prompt engineering, semantic search, RAG, multimodal, and fine-tuning, all runnable. It is the visual complement to Chip Huyen's more architectural AI Engineering. Code is free at github.com/handsOnLLM/Hands-On-Large-Language-Models — run the notebooks even if you don't buy it.

> **Worth knowing.** A solid 2024 visual introduction to the concepts, but treat its applied and tooling chapters as dated.

### [Hugging Face Agents Course](https://huggingface.co/learn/agents-course)

*Ben Burtenshaw & Sergio Paniego* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 25-40 hours

Free, certificate-bearing, and structured as an intro, then smolagents, LangGraph, LlamaIndex, observability & evals, and a capstone. Its real value in 2026 is comparative: it makes you build the same agent three ways so you can form your own opinion in the framework-vs-raw-SDK debate rather than inheriting one. Repo: github.com/huggingface/agents-course.

### [Hugging Face Context Course (context engineering for code agents)](https://huggingface.co/learn/context-course)

*Ben Burtenshaw & Atin Kumar Singh, with Claude Code sections by Maya Nielan and Ryan Whitehead* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 12-20 hours

The most 2026-current free course on this list and the one nobody's roadmap mentions yet. Six units — onboarding, agent skills, MCP servers, plugins, sub-agents, lifecycle hooks — capped by building a minimal agent loop from scratch. This is the actual day-job of an AI engineer in 2026 — structuring knowledge so an agent finds the right thing at the right time. Do the final 'minimal agent loop from scratch' unit even if you skip everything else.

### [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)

*Hugging Face education team* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 70-90 hours

The best free hands-on bridge between theory and the actual ecosystem you'll be paid to use. 12 chapters: transformers library, datasets, tokenizers, fine-tuning, Gradio demos, classic NLP tasks, then chapters 10–12 on modern fine-tuning, dataset curation and reasoning models. Ad-free, no signup wall. Do chapters 1–4 early; chapters 10–12 only after you've shipped something.

### [Hugging Face MCP Course](https://huggingface.co/learn/mcp-course/en/unit0/introduction)

*Ben Burtenshaw & Alex Notov* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 15-25 hours

The best free structured path into MCP, and it's co-authored with the people who own the spec. Units: fundamentals and architecture, an end-to-end use case, a deployed use case, and bonus units (including Tiny Agents). Free certification. Cross-check anything you build against the current spec, because MCP moved to a stateless core in 2026-07-28.

> **Worth knowing.** Predates the 2026-07-28 MCP spec: what it teaches about sessions, the initialize handshake, roots, sampling and logging has since been removed or deprecated.

### [Lil'Log — Scaling Laws, Carefully (Jun 2026) and Harness Engineering for Self-Improvement (Jul 2026)](https://lilianweng.github.io/archives/)

*Lilian Weng* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4 hours

Her two 2026 posts are the current frontier, not the 2023 agent post everyone still links. 'Harness Engineering for Self-Improvement' (4 Jul 2026) is directly about the 2026 shift toward the harness — feedback loops where the system improves its own training/deployment pipeline. Also read 'Why We Think' (May 2025) for the reasoning-model era and 'Extrinsic Hallucinations in LLMs' (2024), still the best treatment of hallucination.

> **Worth knowing.** The linked archive index drifts as new posts appear. Dense research-survey writing aimed at ML researchers — the two posts are 25–31 minute reads and belong in an advanced tier, not a beginner one.

### [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)

*Lilian Weng* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2 hours

The post that gave the field its vocabulary: planning, memory, tool use, reflection. A caution for 2026: the specific techniques (ReAct, Reflexion, MRKL, early AutoGPT-style scaffolds) are dated and partly superseded by native tool-calling, RLVR-trained reasoning models and MCP. Read it for the conceptual decomposition, then get current practice from Anthropic's harness-design posts. Recognising this post's age is itself a useful 2026 skill.

> **Worth knowing.** A 2023 post: the conceptual taxonomy is still useful, but the examples are historical and not how agents are built now.

### [LLMs-from-scratch (companion repo)](https://github.com/rasbt/LLMs-from-scratch)

*Sebastian Raschka, PhD* &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 30 hours

103k stars, and usable entirely without buying the book. The bonus directory is the real 2026 asset: reading a from-scratch Qwen3 MoE or Gemma 4 implementation next to a from-scratch GPT-2 is the fastest way to see what actually changed in architectures (RoPE, GQA, RMSNorm, SwiGLU, MoE routing, sliding-window attention).

> **Worth knowing.** A reasoning-model sequel covers the newer follow-on material.

### [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/)

*Alexander 'Sasha' Rush* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-6 hours

Line-by-line PyTorch implementation interleaved with the paper text — the bridge from mathematical notation to running code. The 2022 community refresh modernised the PyTorch. Note: like the paper, it implements the original encoder-decoder architecture, so treat it as a companion to the paper rather than a template for building a modern decoder-only LLM. Source: github.com/harvardnlp/annotated-transformer.

> **Worth knowing.** Four-year-old code implementing a nine-year-old architecture. Instructive as history, but not how a 2026 LLM is built — pair it with a decoder-only from-scratch implementation such as nanochat.

### [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

*Jay Alammar* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

Still the best 90-minute visual on-ramp to attention, used in courses at Stanford, MIT, Harvard, Princeton and CMU. Note: it describes the original 2017 encoder-decoder Transformer, not a 2026 decoder-only LLM — no RoPE, no GQA, no MoE, no KV cache, learned absolute position embeddings. Read it for intuition, then get the modern deltas from Raschka's repo or CS336 Lecture 3/4. Alammar himself notes the updated/expanded treatment is now in his book.

> **Worth knowing.** Eight years old and architecturally dated where it now matters: modern LLMs are decoder-only with RoPE/GQA. Still the best first picture of attention; follow it with the author's updated Chapter 3.

## Keep for reference

Not for reading end to end. Useful to have when you need to look something up.

### [Ahead of AI (newsletter/archive)](https://magazine.sebastianraschka.com/archive)

*Sebastian Raschka, PhD* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 2 hours

The best 'keep current without drowning' subscription for architecture-level readers. His annual architecture-comparison posts and pieces like 'Controlling Reasoning Effort in LLMs' (18 Jul 2026, covering the GPT-5.6 family's reasoning-effort settings and the RLVR lineage from o1 and DeepSeek-R1) are the fastest way to understand what actually changed this quarter. Use this instead of Twitter/X for architecture news.

### [DeepLearning.AI Short Courses](https://www.deeplearning.ai/courses)

*DeepLearning.AI, with Andrew Ng and instructors from OpenAI, Anthropic, LangChain, Hugging Face, Microsoft, Pinecone, NVIDIA and 30+ partners* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1-2 hours

Best used surgically, not sequentially. Each is 1–2 hours, taught by a practitioner from the vendor whose tool it covers — which is both the strength (authoritative, current) and the weakness (each is effectively a guided tour of one company's SDK). Worth doing: 'Evaluating AI Agents' (trajectory evaluation, not just final answers), and the MCP and agent-memory courses. Not a substitute for building: treat these as 90-minute orientations before you write your own version.

### [llama.cpp](https://github.com/ggml-org/llama.cpp)

*Georgi Gerganov and contributors* &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 5-15 hours

The C/C++ inference engine underneath most of the local-AI ecosystem — Ollama and LM Studio are both built on its ggml tensor library. Worth going one level down from Ollama once you care about inference cost: this is where you learn what quantisation formats (Q4_K_M vs Q8), KV cache size, batching and context length actually do to memory and throughput. Those are the same levers that determine your API bill at scale.

### [Ollama](https://ollama.com/)

*Ollama team* &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3-5 hours

The fastest path to running models locally, which matters for beginners for three reasons: zero marginal cost while you iterate, no data leaving your machine, and it forces you to confront quantisation and VRAM tradeoffs. 100+ quantised models available. Rule of thumb from 2026 guides: a modern AVX2 CPU with 16GB RAM runs an 8B model at Q4 comfortably. Use Ollama for convenience; drop to llama.cpp directly when you need control over build flags, quantisation and sampling.

> **Worth knowing.** Ollama has expanded into a paid cloud product, so "run models locally for free" is no longer the whole story.

### [OpenAI Cookbook](https://github.com/openai/openai-cookbook)

*OpenAI developer relations and community contributors* &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-20 hours

Runnable reference implementations straight from the provider, browsable at developers.openai.com/cookbook. Use it as a lookup, not a curriculum — grep for the pattern you need (structured outputs, embeddings, agents SDK, evals). 2026 additions lean heavily agentic, e.g. 'Building Governed AI Agents: A Practical Guide to Agentic Scaffolding' (Feb 2026). Reading both the OpenAI cookbook and Anthropic's cookbooks teaches you which parts of your knowledge are portable versus vendor-specific.

> **Worth knowing.** Single-vendor: every recipe assumes the OpenAI API. Valuable as executable patterns, but they need translating for any other provider.

### [Simon Willison's blog](https://simonwillison.net/)

*Simon Willison* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2 hours

The best daily 'what actually happened and does it actually work' feed, written by a working engineer who tests claims rather than repeating press releases. His annual reviews (Dec 2023/2024/2025) and 'LLM predictions for 2026' (simonwillison.net/2026/Jan/8/llm-predictions-for-2026/) are the fastest way to compress a year. His 2026 predictions worth internalising: RL-trained reasoning models now produce work experts rely on; sandboxing finally maturing; and a major coding-agent security incident is likely because people run these with excessive permissions. Use his llm CLI to experiment cheaply across providers.

### [Unsloth — fine-tuning docs and notebooks](https://unsloth.ai/docs)

*Daniel & Michael Han* &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-20 hours

The lowest-friction way to actually run LoRA/QLoRA in 2026, and the practical answer to 'do I need an H100'. Free-tier Colab handles a 7–8B QLoRA; 4-bit base + LoRA adapter puts a 70B in ~48GB instead of ~140GB at 1–2% quality cost. Their model directory doubles as a useful census of the current open-weight frontier (Qwen3.8, DeepSeek V4, Kimi K3, Gemma 4, GLM-5.2, Meta Muse). Sensible starting hyperparameters: r=16, alpha=16, all-linear target modules. Alternatives: HF TRL (most standard/portable) and Axolotl (YAML-driven pipelines).

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
