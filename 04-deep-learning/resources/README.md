# Resources — Chapter 4: Deep learning

Resources for [the chapter](../README.md), grouped by purpose. The main path uses selected lectures
and sections within 90 hours; completing every resource below would be a much longer programme.
Hours are learner planning estimates, not course-provider promises.

Current course and tool guidance was checked on **9 October 2026**. Foundations remain useful when
their APIs need updating. Recent papers are labeled by evidence type; reported benchmark gains are
results under the authors' setup, not guaranteed gains on your project.

**Browse:** [Start here](#start-here) &nbsp;·&nbsp; [Optional depth](#optional-depth) &nbsp;·&nbsp;
[Keep for reference](#keep-for-reference)

---

## Start here

### [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)

_Andrej Karpathy_ &nbsp;·&nbsp; Free course &nbsp;·&nbsp; 40–70 hours for the full sequence;
selected lectures here

Start with micrograd, then the makemore training and backpropagation exercises. Rebuild the scalar
engine, check a reused node's gradient accumulation, and derive one small matrix backward pass. The
course develops autoregressive models up to a teaching GPT; it is not a complete curriculum for
current post-training or distributed systems.

### [PyTorch — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Free documentation &nbsp;·&nbsp; 8–12 hours

Use the tensor, data-loader, autograd, optimization and save/load sequence after micrograd. Write an
explicit training and validation loop, including device placement and the distinction between
evaluation mode and disabling autograd; restore training mode after validation. Use documentation
matching your pinned installation rather than copying an old notebook's API without checking it.
Check the
[loss contract](https://docs.pytorch.org/docs/2.14/generated/torch.nn.CrossEntropyLoss.html) and
[BatchNorm buffers](https://docs.pytorch.org/docs/2.14/generated/torch.nn.BatchNorm2d.html): softmax
before cross-entropy and validation updates to running statistics can both produce a misleading
training result.

### [CS231n foundational notes](https://cs231n.github.io/)

_Stanford CS231n teaching staff_ &nbsp;·&nbsp; Free notes &nbsp;·&nbsp; 6–10 hours of selected
sections

Read computational graphs, initialization, regularization and learning/evaluation beside your
training exercises. Implement one gradient check and diagnose a loss curve. These are foundational
notes; use the current course schedule below for later vision architectures and assignments.

### [Dive into Deep Learning](https://d2l.ai/)

_Aston Zhang, Zachary C. Lipton, Mu Li and Alexander J. Smola_ &nbsp;·&nbsp; Free interactive book
&nbsp;·&nbsp; 10–15 hours of selected sections

Use the PyTorch path for MLPs, optimization and CNNs, with equations and executable examples in the
same place. Choose chapters that resolve a problem in your current model. The public book identifies
its version; pin its notebook dependencies and use current framework docs for implementation
changes. It supplements the chapter rather than adding a full book to the plan.

### [Practical Deep Learning for Coders](https://course.fast.ai/)

_Jeremy Howard_ &nbsp;·&nbsp; Free course &nbsp;·&nbsp; 40–80 hours for the full course; lessons 1–4
here

A useful top-down route: train an image model and then inspect what the convenience API does. Use
the initial lessons for transfer learning and data inspection. Rewrite one exercise in an explicit
PyTorch loop. Check installation and notebook dependencies; the published course recordings and
current library documentation need not use the same release.

### [fastbook](https://github.com/fastai/fastbook)

_Jeremy Howard and Sylvain Gugger_ &nbsp;·&nbsp; Free notebook book &nbsp;·&nbsp; 6–10 hours of
selected chapters

Read chapters 1–4 alongside the course, especially the construction of an optimization loop. Use the
repository notebooks for the complete source and reproduce one exercise in a pinned environment.
External services used for collecting images have their own access and pricing; a course example is
not an entitlement to a free data source.

### [Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY)

_Andrej Karpathy_ &nbsp;·&nbsp; Free video and teaching code &nbsp;·&nbsp; 8–12 hours with
implementation

Build the decoder, causal attention and training loop on a small corpus. Test tensor shapes and the
causal mask, and explain the difference between teacher-forced loss and generation. The small model
is an implementation exercise, not a frontier-model reproduction.

### [Let's build the GPT Tokenizer](https://youtu.be/zduSFxRajkE)

_Andrej Karpathy_ &nbsp;·&nbsp; Free video &nbsp;·&nbsp; 4–6 hours with exercises

Implement byte-pair encoding and inspect whitespace, digits and several languages. Check
encode/decode round trips and handling of special tokens. Split the source corpus before learning
BPE merges on training text and creating windows; keep the tokenizer fixed on held-out text.
Tokenization changes representation and token cost; use a controlled experiment before attributing a
reasoning failure to it.

### [Understanding Deep Learning](https://udlbook.github.io/udlbook/)

_Simon J. D. Prince_ &nbsp;·&nbsp; Free online book and companion materials &nbsp;·&nbsp; 6–10 hours
of lookup reading here

Use the chapters on losses, optimization, convolution and attention when a lesson needs a deeper
derivation. The author's site links the book and companion notebooks. Attempt a selected problem and
compare your answer with the available solutions; reading alone does not check your grasp of shapes
and gradients.

## Optional depth

Choose one topic adjacent to the capstone. These are alternatives, not another required syllabus.

### [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

_Ashish Vaswani and colleagues_ &nbsp;·&nbsp; Peer-reviewed NeurIPS 2017 paper &nbsp;·&nbsp; 3–4
hours

Read after implementing attention. Compare the encoder-decoder translation architecture with your
decoder-only model and explain masking, positional information and scaled dot products. Its
historical benchmark is not evidence that a current language-model architecture should match every
design choice.

### [MIT 6.S191 — 2026 edition](https://introtodeeplearning.com/)

_Alexander Amini, Ava Amini and course staff_ &nbsp;·&nbsp; Free course materials &nbsp;·&nbsp;
15–25 hours

The official online 2026 schedule runs from 30 March to 25 May and links lectures and labs,
including language models and fine-tuning. Use it as an orientation or an alternative short course.
Inspect the lab environment and framework before running it; completing both this course and the
main path is extra time.

### [CS231n — Spring 2026 schedule](https://cs231n.stanford.edu/schedule.html)

_Stanford CS231n teaching staff_ &nbsp;·&nbsp; Official course materials &nbsp;·&nbsp; 8–15 hours of
selected work

Use public slides and programming assignments to extend your vision capstone into transformers,
self-supervised representations or generative modeling. Current lecture-video links may require
Stanford access; public slides do not imply that the full current video course is freely available.
Select one assignment section that answers a gap in your implementation.

### [CS336 — Spring 2026](https://cs336.stanford.edu/)

_Tatsunori Hashimoto, Percy Liang and course staff_ &nbsp;·&nbsp; Official graduate course
&nbsp;·&nbsp; Selected orientation here

The current schedule links lectures and assignments on architecture, systems, scaling, data and
post-training. Read resource accounting and evaluation before treating model size as the objective.
Full assignments need more time and preparation; Chapter 7 provides a separate implementation
capstone allocation.

### [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)

_Edward J. Hu and colleagues_ &nbsp;·&nbsp; Foundational paper first released in 2021 &nbsp;·&nbsp;
2–3 hours

Understand a frozen base weight plus a trainable low-rank update. Count trainable parameters and
compare optimizer memory with full fine-tuning. Rank, target modules and adapter serving strategy
are choices to evaluate; fewer trainable parameters alone do not establish task quality or faster
inference. Use the current PEFT guide below for implementation.

### [QLoRA: Efficient Finetuning of Quantized LLMs](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1feb87871436031bdc0f2beaa62a049b-Abstract-Conference.html)

_Tim Dettmers, Artidoro Pagnoni, Ari Holtzman and Luke Zettlemoyer_ &nbsp;·&nbsp; Peer-reviewed
NeurIPS 2023 paper &nbsp;·&nbsp; 2–3 hours

Distinguish quantizing the frozen base from training its adapters; read NF4, double quantization and
optimizer-memory handling. Reproduce a small memory measurement with a supported stack. The paper's
specific model, device and chatbot evaluations are not a current universal quality or
hardware-capacity promise.

### [Direct Preference Optimization](https://proceedings.neurips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract.html)

_Rafael Rafailov and colleagues_ &nbsp;·&nbsp; Peer-reviewed NeurIPS 2023 paper &nbsp;·&nbsp; 2–3
hours

Contrast training on preferred/rejected response pairs with supervised demonstrations and on-policy
reinforcement learning. Inspect response-pair quality, reference-policy choices and a held-out task
evaluation. Optimizing preferences does not by itself validate factuality, permission boundaries or
a business outcome.

### [DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning](https://www.nature.com/articles/s41586-025-09422-z)

_Daya Guo and colleagues_ &nbsp;·&nbsp; Peer-reviewed Nature paper, published 17 September 2025
&nbsp;·&nbsp; 2–3 hours

Read the distinction between R1-Zero's reinforcement-learning experiment and R1's multistage
pipeline. Design a toy verifier, then an adversarial answer that exposes its weakness. This is a
model-developer study; its reasoning benchmarks do not establish effectiveness on every task or
substitute for a reliable reward signal.

### [FlashAttention-4](https://proceedings.mlsys.org/paper_files/paper/2026/hash/ae8b0b5838ba510daff1198474e7b984-Abstract-Conference.html)

_Ted Zadouri and colleagues_ &nbsp;·&nbsp; Peer-reviewed MLSys 2026 paper &nbsp;·&nbsp; 2–3 hours

Study hardware-aware kernel scheduling and memory movement. Compare the attention algorithm with its
implementation and identify the device assumptions. Profile a supported backend on your own
workload; the paper's hardware result should not be copied into an end-to-end speed estimate.

## Keep for reference

Use these while debugging or measuring a run.

### [Automatic Mixed Precision recipe](https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 1–2 hours plus
measurement

Check supported device/dtype combinations and where autocast and gradient scaling belong. Compare a
correct full-precision baseline against one supported setting on quality, finite gradients, peak
memory and runtime. Mixed precision is not a replacement for gradient accumulation or activation
checkpointing. For token-level accumulation, use the
[Transformers loss-normalization guide](https://huggingface.co/docs/transformers/grad_accumulation)
to check the non-ignored-target denominator across the whole update, including a partial final
window. Verify the trainer's pinned behavior before adding manual scaling.

### [torch.compile tutorial](https://docs.pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 1–2 hours plus
measurement

Record eager time, compilation/warmup time and steady-state time separately. Try the actual input
shapes the application uses and inspect graph breaks or recompilation. Keep the same evaluation and
include a slower result if the workload does not benefit.

### [PyTorch 2.14 release notes](https://pytorch.org/blog/pytorch-2-14-release-blog/)

_PyTorch project_ &nbsp;·&nbsp; Official release published 2 September 2026 &nbsp;·&nbsp; 30–60
minutes

Use the release notes to select supported compiler, hardware and distributed features for your
environment. Distinguish experimental features from stable interfaces and pin the selected version.
A vendor/project benchmark is an adoption lead to test, not a promised project speedup.

### [Saving and loading models](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Official tutorial &nbsp;·&nbsp; 1–2 hours

Practice a full training checkpoint and resume, including optimizer state and training progress;
include scheduler, scaler and random state when your run needs them. Save preprocessing, tokenizer
and configuration with inference weights. Only load trusted artifacts and follow the serialization
guidance for your installed version.

### [Reproducibility notes](https://docs.pytorch.org/docs/2.14/notes/randomness.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Versioned official documentation &nbsp;·&nbsp; 1 hour

Control relevant random sources and document deterministic settings, device and environment. Set a
metric tolerance and repeat the ablation; a seed does not guarantee identical results across
releases or platforms. Record which reproducibility claim your artifacts support.

### [PEFT documentation](https://huggingface.co/docs/peft/index)

_Hugging Face PEFT maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–4 hours

Use the guide to adapter configuration, saving/loading and supported methods after reading LoRA. Pin
PEFT, Transformers and quantization dependencies together. Verify trainable parameter counts, the
correct base-model revision and the deployed adapter, then evaluate the actual task.

### [TRL documentation](https://huggingface.co/docs/trl/index)

_Hugging Face TRL maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–4 hours of
selected sections

Compare SFT, DPO and reward-based trainer interfaces without treating them as interchangeable. Check
dataset formats, masking, reference models and reward functions. Implement only the trainer your
capstone's evidence justifies; large-scale post-training is outside this chapter's budget.

### [microgpt](https://karpathy.github.io/2026/02/12/microgpt/)

_Andrej Karpathy_ &nbsp;·&nbsp; Author's teaching article, 12 February 2026 &nbsp;·&nbsp; 3–5 hours

A compact pure-Python implementation connecting tokenization, autograd, a GPT, optimization and
sampling. Trace one parameter from forward pass to update and explain every stage. Its tiny names
dataset and scalar implementation are for understanding, not a useful deployment or efficient
language-model training pipeline.

### [nanochat](https://github.com/karpathy/nanochat)

_Andrej Karpathy and contributors_ &nbsp;·&nbsp; Author-maintained repository &nbsp;·&nbsp; 2–4
hours to inspect; running it is separate

Trace the data, tokenizer, training, evaluation and serving configuration in one repository. Pin a
commit and calculate compute requirements before launching a run. Compare the repository's
demonstration with your own budget and evaluation; a headline training cost is not a complete
production-cost estimate.

### [Deep Learning](https://www.deeplearningbook.org/)

_Ian Goodfellow, Yoshua Bengio and Aaron Courville_ &nbsp;·&nbsp; Free online 2016 book
&nbsp;·&nbsp; Lookup reference

Use the linear algebra, probability, optimization and backpropagation sections when you need a
rigorous foundation. It predates transformers and current post-training practice, so pair it with
the later sources above for those topics. Reading the whole book is not a prerequisite for the
chapter's implementation exercises.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
