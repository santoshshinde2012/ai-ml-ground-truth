# Chapter 4: Deep learning

**Weeks 14–22 &nbsp;·&nbsp; about 90 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** Build a tiny autograd engine, learn an explicit PyTorch training loop, debug
a model that fails to learn, and implement attention. Finish with a trained model, an honest
evaluation and a measured quality/memory/runtime tradeoff. Current training tools make this work
more efficient; they do not replace the need to understand the data, gradients and evaluation.

**Same thread, new skill.** You still know tabular ML from Chapter 3. Here you learn _how neural
nets learn_ — the machinery behind LLMs.

**In this chapter:** [Plan](#your-nine-week-plan) &nbsp;·&nbsp; [Learn](#what-to-learn)
&nbsp;·&nbsp; [Build](#what-to-build) &nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp;
[Resources](#resources)

---

## Your nine-week plan

About ten hours a week. Karpathy first unless you need an early win (fast.ai lesson 1–3), as noted
below.

| Week | Focus                   | Do this                                                                                                               | Done when                                                       |
| ---- | ----------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 14   | Autograd                | Karpathy micrograd / Zero to Hero 1–2; rebuild `Value` from empty file                                                | Backward pass on paper + code                                   |
| 15   | PyTorch basics          | Official PyTorch tutorial; training loop from memory                                                                  | Loop runs on toy data                                           |
| 16   | Debug training          | Overfit 10 samples; learning-rate sweep; loss curves                                                                  | Can name 3 failure modes                                        |
| 17   | MLP / CNN               | Dive into Deep Learning or CS231n notes; one small classifier                                                         | Baseline comparison and loss curves explained                   |
| 18   | Transfer learning       | fast.ai lessons 1–4 **or** fastbook ch 1–4; train the head, then compare unfreezing the backbone                      | Demo on **your** images or domain                               |
| 19   | Attention intuition     | Karpathy build-GPT video; type along                                                                                  | Can draw attention block                                        |
| 20   | Tokeniser               | Karpathy tokeniser video; byte-level on small corpus                                                                  | Encode/decode round-trip works                                  |
| 21   | Your model + efficiency | Pick capstone; profile eager training; save and resume a full checkpoint; try one supported precision/compile setting | Config reproduces the run and the bottleneck is measured        |
| 22   | Ablation + deploy       | Report quality, memory and runtime; include failed runs; finish demo                                                  | Untouched test, checkpoint replay and honest ablation in README |

---

## What you will be able to do

Write backpropagation from an empty file, train a network in PyTorch without a template, and take a
model that is quietly not learning and work out why.

## On the order to do this in

You will be told three incompatible things about how to start deep learning, and all three come from
people worth listening to.

- **Top-down** (fast.ai): train a working model in lesson one, then return to the mechanics. This
  can help you stay engaged; it is a teaching choice, not a measured guarantee about dropout.
- **Bottom-up** (Karpathy, d2l.ai): start from a single derivative and build up to a transformer.
  The argument is that nothing else produces real understanding of what is happening.
- **Maths first**: foundations before code. This is the one ordering I would gently steer you away
  from, for the reasons in [Chapter 3](../03-core-machine-learning/README.md).

I suggest **bottom-up first, top-down alongside**: build the autograd engine, then learn PyTorch,
then use fast.ai for transfer learning and momentum. If you know that you lose interest without an
early win, invert it and do fast.ai's first three lessons before the autograd exercise. Both work.

**On frameworks.** Use PyTorch for this chapter so the exercises share one implementation. Choose
another framework later when a project or team needs it. Keras supports custom PyTorch training
steps, so it does not inherently prevent learning the loop; JAX is useful beyond very large training
runs too. The recommendation is about keeping your first project coherent.
[Keras custom-training-step guide](https://keras.io/guides/custom_train_step_in_torch/).

The official [PyTorch 2.14 release](https://pytorch.org/blog/pytorch-2-14-release-blog/), published
2 September 2026, adds compiler, hardware and distributed-runtime work. Pin a supported release and
use its matching docs. A release-note speedup on one kernel or device is not a prediction of your
model's end-to-end speed; several new features are explicitly experimental.

## What to learn

**Backpropagation, by building it.** Write a scalar autograd engine: a `Value` class with the
arithmetic operations, a topological sort for the backward pass, and correct gradient accumulation
when a node is used more than once. That last detail is where most people's bug lives, and finding
it is the moment the chain rule stops being a formula.

**PyTorch as a language.** Tensors, `Dataset` and `DataLoader`, and the explicit training loop you
should be able to type from nothing. Know why `model.train()` and `model.eval()` differ, why
`zero_grad()` exists, what `torch.no_grad()` saves you, and why both the model and the data need to
be on the same device.

The loop you should be able to type from an empty file:

```python
for epoch in range(num_epochs):
    model.train()
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        loss = criterion(model(x), y)
        loss.backward()
        optimizer.step()
```

For validation, call `model.eval()` and run the forward pass inside `torch.no_grad()` or
`torch.inference_mode()`. Evaluation mode changes dropout and batch-normalization behavior;
disabling autograd avoids building a backward graph. Neither substitutes for the other. If you
cannot write this without looking, you are not ready to debug someone else's training code. Restore
training mode at the start of each epoch after validation has changed it.
[PyTorch's optimization tutorial](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
shows separate training and evaluation loops.

Check the loss contract too. For ordinary multiclass classification, pass unnormalized logits to
`CrossEntropyLoss` and class-index targets with the expected shape and dtype; applying softmax first
changes the objective. Use valid probability targets only when the task calls for them. The
[loss documentation](https://docs.pytorch.org/docs/2.14/generated/torch.nn.CrossEntropyLoss.html)
also explains ignored targets and reduction. When reporting epoch loss, aggregate the loss numerator
and its intended denominator across batches; equally averaging batch means can overweight a short
last batch or a sequence with few supervised tokens.

**Training dynamics, and how to break them.** This is the part that separates people who can debug
training from people who change the architecture and hope. Instrument your runs with loss curves for
both splits, gradient norms per layer, and activation histograms.

Five habits fix most problems:

1. **Try to overfit ten clean samples with regularization and augmentation disabled.** Unexpected
   failure is a debugging signal; noisy labels, a constrained model or the loss may limit the
   achievable fit. Check shapes, target encoding and gradient flow before adding complexity.
2. Compare against a trivial baseline.
3. Sweep the learning rate across orders of magnitude and plot it.
4. Turn off every extra (augmentation, scheduler, dropout), get a working baseline, then add one
   thing at a time.
5. **Look at the data.** Print ten samples as the model sees them, after transforms. A surprising
   share of "it will not learn" turns out to be inverted labels or a normalisation applied twice.

**Transfer learning.** When suitable pretrained weights exist, compare adapting them to a small
from-scratch baseline. Take a pretrained model and adapt it: freeze the backbone and train a new
head for tiny datasets, unfreeze progressively as you have more data, and compare lower learning
rates for earlier layers. CNNs make weight sharing and local inductive bias concrete; vision
transformers and self-supervised encoders are useful challengers when their data, memory and latency
requirements fit. Do not assert that one family dominates every small-data or edge task. Keep
augmentations in training only, deduplicate before splitting, and hold out subjects or capture
sessions when deployment needs that generalization.

Freezing parameters with `requires_grad_(False)` does not freeze batch-normalization buffers. Decide
whether to preserve the pretrained running statistics or adapt them using training data. To preserve
them, restore evaluation mode on the relevant backbone modules after each outer `model.train()` call
while keeping the new head in training mode. Record that choice and keep validation data out of
statistics updates.
[PyTorch's BatchNorm documentation](https://docs.pytorch.org/docs/2.14/generated/torch.nn.BatchNorm2d.html)
describes the running-statistics behavior; evaluation mode and gradient freezing are separate
controls.

**Attention, built by hand.** Follow Karpathy's
[build-a-GPT lecture](https://www.youtube.com/watch?v=kCc8FmEb1nY), typing rather than watching,
then build a byte-pair tokeniser. Inspect how whitespace, numbers and several languages are split;
tokenization affects input representation and token cost, but is not the sole explanation for
reasoning failures. Add tests for causal masking, padding, position handling and encode/decode round
trips. Split a language corpus by source document before making token windows, so adjacent or
duplicated text cannot leak into validation. Learn BPE merges and any fitted preprocessing only from
training text; keep them fixed for validation and the final test.

Check causal masking by changing a future token and verifying that earlier logits stay unchanged
within numerical tolerance in evaluation mode. Shift targets correctly for next-token prediction;
check whether the model already shifts them internally. Exclude padding from the loss; masking
padding in attention alone does not exclude its training targets.

Read [_Attention Is All You Need_](https://arxiv.org/abs/1706.03762) **after** this, not before. It
is a 2017 machine-translation paper describing an encoder-decoder model. Compare its attention
mechanism to your decoder-only model; there is no useful percentage for how much of its design a
current model shares. Read cold as a first resource, it tends to discourage people; read after you
have built the thing, it is easier to connect to the code. Its annotated entry is in
[resources/](resources/README.md).

**Efficient training, after correctness.** Profile an eager baseline, then change one thing at a
time. Automatic mixed precision can reduce memory and runtime on supported hardware; choose the
dtype for the device, check finite loss/gradients, and use a gradient scaler when the precision and
training setup require it. Gradient accumulation changes effective batch size; scale the loss
correctly and step the optimizer at the intended cadence. With variable-length sequences, normalize
the summed token loss by all non-ignored prediction targets in the accumulation window, including a
short final window; averaging each microbatch's mean equally changes token weighting. Check the
pinned trainer's handling rather than dividing twice. The
[Transformers accumulation guide](https://huggingface.co/docs/transformers/grad_accumulation)
documents this denominator. Accumulation does not reproduce a large batch's batch-normalization
statistics. Activation checkpointing trades recomputation for activation memory. These are different
controls, not interchangeable fixes.
[PyTorch AMP recipe](https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html).

Try `torch.compile` on an already correct model. Record first-run compilation separately from
steady-state time; changing shapes and graph breaks can erase the benefit. Report peak memory,
examples/tokens per second and the same validation metric as the eager model. A slower or less
stable result is still a useful experiment.
[Official compile tutorial](https://docs.pytorch.org/tutorials/intermediate/torch_compile_tutorial.html).

**Where recent research fits.** The material below was checked on 9 October 2026. These are
orientation and optional depth within the 90 hours; reproducing a frontier model is extra work.

| Source and evidence                                                                                                                                                     | What to learn                                                                                                 | Bounded exercise                                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| [CS336 Spring 2026](https://cs336.stanford.edu/), official course                                                                                                       | Architecture/resource accounting, data filtering and evaluation precede mid/post-training                     | Read the schedule, then trace one tiny model from corpus to checkpoint; reserve full assignments for Chapter 7                                        |
| [FlashAttention-4](https://proceedings.mlsys.org/paper_files/paper/2026/hash/ae8b0b5838ba510daff1198474e7b984-Abstract-Conference.html), peer-reviewed MLSys 2026 paper | Attention performance depends on memory movement, kernel scheduling and hardware                              | Explain why the reported hardware result does not transfer automatically to your laptop; use a supported attention backend and profile it             |
| [DeepSeek-R1](https://www.nature.com/articles/s41586-025-09422-z), peer-reviewed Nature paper published 17 September 2025                                               | Reinforcement learning with verifiable rewards is a separate stage from pretraining and supervised adaptation | Describe a reliable task verifier, then one way a model could exploit it; do not infer general retention or pricing benefit from reasoning benchmarks |

For adaptation, distinguish full fine-tuning from LoRA, which trains low-rank weight updates, and
QLoRA, which combines adapter training with a quantized base model. Neither guarantees lower serving
latency or preserved task quality. Supervised fine-tuning learns from demonstrations; preference
optimization learns from comparisons; RL with verifiable rewards needs an actual verifier. Learn
these distinctions here and implement one bounded adaptation experiment in Chapter 7 only when it
answers your project's measured failure. The primary papers and current implementation guides are in
the resource list.

## Resources

The annotated resources for this chapter are in **[resources/](resources/README.md)**. The main path
uses selected sections; the full-course hour estimates are not extra requirements.

The ones to begin with:

- [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) — Andrej Karpathy. A free
  course, 40–70 hours; lecture 1 (micrograd) is week 14.
- [PyTorch official tutorials — "Learn the Basics"](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)
  — PyTorch documentation team. Free documentation, 8–12 hours.
- [Practical Deep Learning for Coders](https://course.fast.ai/) — Jeremy Howard. A free course,
  40–80 hours; lessons 1 to 4 are what this chapter uses.
- [Understanding Deep Learning](https://udlbook.github.io/udlbook/) — Simon J. D. Prince. A free
  book, 60–80 hours as a lookup layer, not a read-through.

## What to build

**A model you trained yourself,** with an honest ablation — the model retrained with one component
removed or swapped at a time, to measure what each one contributed. Pick one:

- A classifier on 200-plus photos **you took**, in raw PyTorch, deployed as a small demo
- A character-level language model on a corpus that means something to you, with the modern
  architecture pieces swapped in one at a time
- A reproduction of one bounded paper component, implemented from the paper and compared against a
  reference

Whichever you pick, save the split and data versions, configuration, environment, seed and full
training checkpoint: model, optimizer, scheduler/scaler where used, random-generator states and
progress. Save preprocessing/tokenizer versions too; mid-epoch resume can also need sampler or
data-loader progress. Rehearse loading it and resuming. Record differences across repeated runs when
deciding whether an ablation helped; setting a seed does not guarantee identical results across
releases or devices.
[PyTorch reproducibility notes](https://docs.pytorch.org/docs/2.14/notes/randomness.html).

Keep a final test untouched until model selection is done. Include a real ablation and failed runs,
one diagnosed failure, and a demo with its inference settings recorded. A local reproducible demo is
acceptable when hosting is unavailable; do not claim that a screenshot is a live service.

The ablation is where most of the value sits. A table showing that one change mattered and three
were within noise, with wall-clock times alongside, says more about you than a good final number.

## Before you move on

- You can rebuild the autograd engine from an empty file, in under an hour.
- You can write a training loop from nothing.
- Given an unhealthy loss curve, you can name a likely cause and the instrument that confirms it.
- You can draw attention from memory and explain why we divide by the square root of the head
  dimension.
- You can reload a checkpoint and explain what would be lost by saving only model weights.
- You can compare a precision or compile change on quality, memory and measured runtime.

## A few things worth knowing

- **The Goodfellow, Bengio and Courville book** is free, famous, and where a lot of people stall.
  Published in 2016 with only minor corrections since, it has no transformer chapter and its
  sequence and generative sections are well out of date. Chapters 2 to 9 are still a clean rigorous
  treatment of the mathematics. Simon Prince's
  [_Understanding Deep Learning_](https://udlbook.github.io/udlbook/), also free, is the more useful
  modern choice.
- **Date course materials explicitly.** The older CS231n recordings teach foundational training
  mechanics; the [Spring 2026 schedule](https://cs231n.stanford.edu/schedule.html) adds current
  vision topics. Public slides and assignments do not imply public access to the current lecture
  videos.
- **Rewrite one fast.ai exercise in an explicit PyTorch loop.** This checks your understanding of
  transforms, optimizer updates and validation behavior underneath the convenience API.
- **Use materials that contain working exercises.** Read
  [microgpt](https://karpathy.github.io/2026/02/12/microgpt/) as a compact pure-Python teaching
  implementation and [nanochat](https://github.com/karpathy/nanochat) as an author-maintained
  training pipeline to inspect. Pin the commit and compute assumptions before running it; neither a
  tiny names model nor a repository headline establishes production capability.

---

[Previous: Core machine learning](../03-core-machine-learning/README.md) &nbsp;·&nbsp;
[Next: Language models and AI engineering](../05-language-models/README.md)
