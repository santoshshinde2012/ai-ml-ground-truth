# Resources — Chapter 4: Deep learning

Resources for [the chapter](../README.md), grouped by purpose. The main path uses selected lectures
and sections within 90 hours. Finishing everything below would take far longer. Hours are planning
estimates, not course-provider promises.

Current course and tool guidance was checked on **9 October 2026**. Foundations stay useful when
their APIs need updating. Recent papers are labelled by evidence type. Reported benchmark gains hold
under the authors' setup, not necessarily on your project.

**Browse:** [Start here](#start-here) &nbsp;·&nbsp; [Optional depth](#optional-depth) &nbsp;·&nbsp;
[Keep for reference](#keep-for-reference)

---

## Start here

### [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)

_Andrej Karpathy_ &nbsp;·&nbsp; Free course &nbsp;·&nbsp; 40–70 hours for the full sequence;
selected lectures here

Start with micrograd, then the makemore training and backpropagation exercises. Rebuild the scalar
engine, check a reused node's gradient accumulation, and derive one small matrix backward pass. The
course builds autoregressive models up to a teaching GPT. It is not a full curriculum for current
post-training or distributed systems.

### [PyTorch — Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Free documentation &nbsp;·&nbsp; 8–12 hours

After micrograd, work through the tensor, data-loader, autograd, optimisation and save/load
sequence. Write an explicit training and validation loop with device placement, keeping evaluation
mode and turning off autograd distinct. Restore training mode after validation. Use docs matching
your pinned version rather than trusting an old notebook's API. Check the
[loss contract](https://docs.pytorch.org/docs/2.14/generated/torch.nn.CrossEntropyLoss.html) and
[BatchNorm buffers](https://docs.pytorch.org/docs/2.14/generated/torch.nn.BatchNorm2d.html):
softmax before cross-entropy, or validation updates to running statistics, can each give a
misleading training result.

### [CS231n foundational notes](https://cs231n.github.io/)

_Stanford CS231n teaching staff_ &nbsp;·&nbsp; Free notes &nbsp;·&nbsp; 6–10 hours of selected
sections

Read the notes on computational graphs, initialisation, regularisation, and learning and evaluation
beside your training exercises. Implement one gradient check and diagnose a loss curve. For later
vision architectures and assignments, use the current course schedule below.

### [Dive into Deep Learning](https://d2l.ai/)

_Aston Zhang, Zachary C. Lipton, Mu Li and Alexander J. Smola_ &nbsp;·&nbsp; Free interactive book
&nbsp;·&nbsp; 10–15 hours of selected sections

Use the PyTorch path for MLPs, optimisation and CNNs, with equations and runnable examples side by
side. Pick chapters that solve a problem in your current model. The public book states its version.
Pin its notebook dependencies and use current framework docs for implementation changes. It
supplements the chapter rather than adding a full book to your plan.

### [Practical Deep Learning for Coders](https://course.fast.ai/)

_Jeremy Howard_ &nbsp;·&nbsp; Free course &nbsp;·&nbsp; 40–80 hours for the full course; lessons 1–4
here

A useful top-down route: train an image model, then inspect what the convenience API does.
Use the first lessons for transfer learning and data inspection. Rewrite one exercise in an explicit
PyTorch loop. Check the installation and notebook dependencies, because the recorded course and the
current library docs may use different releases.

### [fastbook](https://github.com/fastai/fastbook)

_Jeremy Howard and Sylvain Gugger_ &nbsp;·&nbsp; Free notebook book &nbsp;·&nbsp; 6–10 hours of
selected chapters

Read chapters 1–4 alongside the course, especially where it builds an optimisation loop. Use the
repository notebooks for the complete source, and reproduce one exercise in a pinned environment.
Image-collection services have their own access rules and pricing. A course example does not make
them free.

### [Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY)

_Andrej Karpathy_ &nbsp;·&nbsp; Free video and teaching code &nbsp;·&nbsp; 8–12 hours with
implementation

Build the decoder, causal attention and training loop on a small corpus. Test tensor shapes and the
causal mask, and explain how teacher-forced loss differs from generation. The small model is an
implementation exercise, not a reproduction of a frontier model.

### [Let's build the GPT Tokenizer](https://youtu.be/zduSFxRajkE)

_Andrej Karpathy_ &nbsp;·&nbsp; Free video &nbsp;·&nbsp; 4–6 hours with exercises

Implement byte-pair encoding and inspect whitespace, digits and several languages. Check
encode/decode round trips and special tokens. Split the source corpus first, then learn BPE merges
on training text and create windows. Keep the tokeniser fixed on held-out text. Tokenisation
changes the representation and token cost. Run a controlled experiment before blaming a reasoning
failure on it.

### [Understanding Deep Learning](https://udlbook.github.io/udlbook/)

_Simon J. D. Prince_ &nbsp;·&nbsp; Free online book and companion materials &nbsp;·&nbsp; 6–10 hours
of lookup reading here

Use the chapters on losses, optimisation, convolution and attention when a lesson needs a deeper
derivation. The author's site links the book and companion notebooks. Try a selected problem and
compare your answer with the available solutions. Solving one tests shapes and gradients in a way
reading cannot.

## Optional depth

Choose one topic close to your capstone. These are alternatives, not another required syllabus.

### [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

_Ashish Vaswani and colleagues_ &nbsp;·&nbsp; Peer-reviewed NeurIPS 2017 paper &nbsp;·&nbsp; 3–4
hours

Read it after implementing attention. Compare its encoder-decoder translation architecture
with your decoder-only model, and explain masking, positional information and scaled dot products.
Its historical benchmark does not mean current language models should copy every design choice.

### [MIT 6.S191 — 2026 edition](https://introtodeeplearning.com/)

_Alexander Amini, Ava Amini and course staff_ &nbsp;·&nbsp; Free course materials &nbsp;·&nbsp;
15–25 hours

The official online 2026 schedule runs from 30 March to 25 May and links lectures and labs,
including language models and fine-tuning. Use it for orientation or as an alternative short
course. Check the lab environment and framework before running it. Doing both this course and the
main path takes extra time.

### [CS231n — Spring 2026 schedule](https://cs231n.stanford.edu/schedule.html)

_Stanford CS231n teaching staff_ &nbsp;·&nbsp; Official course materials &nbsp;·&nbsp; 8–15 hours of
selected work

Use the public slides and programming assignments to extend your vision capstone into transformers,
self-supervised representations or generative modelling. Current lecture videos may need Stanford
access, even though the slides are public. Pick one assignment section that fills a gap in your
implementation.

### [CS336 — Spring 2026](https://cs336.stanford.edu/)

_Tatsunori Hashimoto, Percy Liang and course staff_ &nbsp;·&nbsp; Official graduate course
&nbsp;·&nbsp; Selected orientation here

The current schedule links lectures and assignments on architecture, systems, scaling, data and
post-training. Read resource accounting and evaluation before treating model size as the goal. Full
assignments need more time and preparation. Chapter 7 sets aside separate time for an
implementation capstone.

### [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)

_Edward J. Hu and colleagues_ &nbsp;·&nbsp; Foundational paper first released in 2021 &nbsp;·&nbsp;
2–3 hours

Understand a frozen base weight plus a trainable low-rank update. Count trainable parameters
and compare optimiser memory with full fine-tuning. Rank, target modules and how you serve the
adapter are choices to evaluate. Fewer trainable parameters alone do not prove task quality or
faster inference. For implementation, use the current PEFT guide below.

### [QLoRA: Efficient Finetuning of Quantized LLMs](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1feb87871436031bdc0f2beaa62a049b-Abstract-Conference.html)

_Tim Dettmers, Artidoro Pagnoni, Ari Holtzman and Luke Zettlemoyer_ &nbsp;·&nbsp; Peer-reviewed
NeurIPS 2023 paper &nbsp;·&nbsp; 2–3 hours

Tell quantising the frozen base apart from training its adapters. Read about NF4, double
quantisation and optimiser-memory handling. Reproduce a small memory measurement with a supported
stack. The paper's specific models, devices and chatbot evaluations do not promise quality or
hardware capacity in general today.

### [Direct Preference Optimization](https://proceedings.neurips.cc/paper_files/paper/2023/hash/a85b405ed65c6477a4fe8302b5e06ce7-Abstract.html)

_Rafael Rafailov and colleagues_ &nbsp;·&nbsp; Peer-reviewed NeurIPS 2023 paper &nbsp;·&nbsp; 2–3
hours

Compare training on preferred and rejected response pairs with supervised demonstrations and
on-policy reinforcement learning. Inspect response-pair quality, the reference-policy choice and
a held-out task evaluation. Optimising for preferences does not, by itself, check
factuality, permission boundaries or a business outcome.

### [DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning](https://www.nature.com/articles/s41586-025-09422-z)

_Daya Guo and colleagues_ &nbsp;·&nbsp; Peer-reviewed Nature paper, published 17 September 2025
&nbsp;·&nbsp; 2–3 hours

Note how R1-Zero's reinforcement-learning experiment differs from R1's multistage pipeline. Design
a toy verifier, then an adversarial answer that exposes its weakness. This is a study by the model's
developer. Its reasoning benchmarks neither prove it works on every task nor replace a reliable
reward signal.

### [FlashAttention-4](https://proceedings.mlsys.org/paper_files/paper/2026/hash/ae8b0b5838ba510daff1198474e7b984-Abstract-Conference.html)

_Ted Zadouri and colleagues_ &nbsp;·&nbsp; Peer-reviewed MLSys 2026 paper &nbsp;·&nbsp; 2–3 hours

Study hardware-aware kernel scheduling and memory movement. Compare the attention algorithm with its
implementation, and identify the device assumptions. Profile a supported backend on your own
workload. Avoid copying the paper's hardware result into an end-to-end speed estimate.

## Keep for reference

Use these while debugging or measuring a run.

### [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/)

_Andrej Karpathy_ &nbsp;·&nbsp; Free author's article, 25 April 2019 &nbsp;·&nbsp; 1–2 hours

For a model that trains without errors but does not learn well. Read the end-to-end skeleton
section first and apply it in week 16. It covers a fixed seed, loss at initialisation, a
well-initialised output bias, an input-independent baseline, overfitting one batch and visualising
data just before the network. The later stages (overfit, regularise, tune) suit the capstone
ablation. These are one practitioner's 2019 heuristics, drawn mostly from image classification, not
a measured comparison. Starting points such as Adam at 3e-4 with a constant rate are for
baselining, not settings to keep.

### [Deep Learning Tuning Playbook](https://github.com/google-research/tuning_playbook)

_Varun Godbole, George E. Dahl, Justin Gilmer, Christopher J. Shallue and Zachary Nado_
&nbsp;·&nbsp; Free guide, version 1.0 (2023) &nbsp;·&nbsp; 3–5 hours of selected sections

For tuning a pipeline that already works, especially in weeks 21–22. Read the guide to starting a
new project (architecture, optimiser, batch size, initial configuration) and the incremental-tuning
sections on scientific, nuisance and fixed hyperparameters. Use the FAQ on
schedules, warmup and gradient clipping for lookup. The authors present it as their opinions, not
an officially supported Google product. Its multi-trial studies assume more compute than this
chapter's budget, so borrow the process and keep runs few.

### [Automatic Mixed Precision recipe](https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 1–2 hours plus
measurement

Check supported device and dtype combinations, and where autocast and gradient scaling belong.
Compare a correct full-precision baseline with one supported setting on quality, finite gradients,
peak memory and runtime. Mixed precision does a different job from gradient accumulation or
activation checkpointing. For token-level accumulation, use the
[Transformers loss-normalisation guide](https://huggingface.co/docs/transformers/grad_accumulation)
to check the non-ignored-target denominator across the whole update, including a partial final
window. Check your pinned trainer's behaviour before adding manual scaling.

### [torch.compile tutorial](https://docs.pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 1–2 hours plus
measurement

Record eager time, compilation and warmup time, and steady-state time separately. Try the input
shapes your application really uses, and look for graph breaks or recompilation. Keep the same
evaluation, and report a slower result if your workload does not benefit.

### [PyTorch 2.14 release notes](https://pytorch.org/blog/pytorch-2-14-release-blog/)

_PyTorch project_ &nbsp;·&nbsp; Official release published 2 September 2026 &nbsp;·&nbsp; 30–60
minutes

Use the release notes to pick supported compiler, hardware and distributed features for your
environment. Separate experimental features from stable interfaces, and pin your chosen
version. A vendor or project benchmark is a lead worth testing, not a promised speedup for your
project.

### [Saving and loading models](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Official tutorial &nbsp;·&nbsp; 1–2 hours

Practise saving and resuming a full training checkpoint, including optimiser state and
training progress. Add scheduler, scaler and random state when your run needs them. Save
preprocessing, tokeniser and configuration with the inference weights. Load only artefacts you
trust, and follow the serialisation guidance for your installed version.

### [Reproducibility notes](https://docs.pytorch.org/docs/2.14/notes/randomness.html)

_PyTorch documentation team_ &nbsp;·&nbsp; Versioned official documentation &nbsp;·&nbsp; 1 hour

Control the relevant random sources, and record deterministic settings, device and environment. Set
a metric tolerance and repeat the ablation, because a seed does not guarantee identical results
across releases or platforms. Write down which reproducibility claim your artefacts support.

### [PEFT documentation](https://huggingface.co/docs/peft/index)

_Hugging Face PEFT maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–4 hours

After reading LoRA, use the guide for adapter configuration, saving and loading, and supported
methods. Pin PEFT, Transformers and quantisation dependencies together. Check trainable parameter
counts, the base-model revision and the deployed adapter, then evaluate the real task.

### [TRL documentation](https://huggingface.co/docs/trl/index)

_Hugging Face TRL maintainers_ &nbsp;·&nbsp; Official documentation &nbsp;·&nbsp; 2–4 hours of
selected sections

Compare the SFT, DPO and reward-based trainer interfaces as distinct tools. Check
dataset formats, masking, reference models and reward functions. Implement only the trainer your
capstone's results justify. Large-scale post-training is beyond this chapter's budget.

### [microgpt](https://karpathy.github.io/2026/02/12/microgpt/)

_Andrej Karpathy_ &nbsp;·&nbsp; Author's teaching article, 12 February 2026 &nbsp;·&nbsp; 3–5 hours

A compact pure-Python implementation that connects tokenisation, autograd, a GPT, optimisation and
sampling. Trace one parameter from the forward pass to its update, and explain every stage. Its tiny
names dataset and scalar code are for understanding, not deployment or efficient language-model
training.

### [nanochat](https://github.com/karpathy/nanochat)

_Andrej Karpathy and contributors_ &nbsp;·&nbsp; Author-maintained repository &nbsp;·&nbsp; 2–4
hours to inspect; running it is separate

Trace the data, tokeniser, training, evaluation and serving configuration in one repository. Pin a
commit and work out the compute you need before launching a run. Compare the repository's
demonstration with your own budget and evaluation. A headline training cost is not a full
production-cost estimate.

### [Deep Learning](https://www.deeplearningbook.org/)

_Ian Goodfellow, Yoshua Bengio and Aaron Courville_ &nbsp;·&nbsp; Free online 2016 book
&nbsp;·&nbsp; Lookup reference

Use the sections on linear algebra, probability, optimisation and backpropagation when you need a
rigorous foundation. It predates transformers and current post-training practice, so use the later
sources above for those topics. You can do the chapter's implementation exercises without reading
the whole book.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
