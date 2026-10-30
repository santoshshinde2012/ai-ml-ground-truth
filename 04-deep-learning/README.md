# Chapter 4: Deep learning

**Weeks 14–22 &nbsp;·&nbsp; about 90 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** Build a tiny autograd engine, learn an explicit PyTorch training loop, debug
a model that fails to learn, and implement attention. Finish with a trained model, a fair evaluation
and a measured quality, memory and runtime trade-off. Modern tools speed this up, but you still
need to understand the data, gradients and evaluation.

**Same thread, new skill.** You already know tabular ML from Chapter 3. Here you learn _how neural
nets learn_ — the machinery behind LLMs. The first build option below keeps your Chapter 3 data,
split and baseline.

**In this chapter:** [Plan](#your-nine-week-plan) &nbsp;·&nbsp; [Learn](#what-to-learn)
&nbsp;·&nbsp; [Build](#what-to-build) &nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp;
[Resources](#resources)

---

## Your nine-week plan

About ten hours a week. Start with Karpathy, or with fast.ai lessons 1–3 if you need an early win
(see below).

| Week | Focus                   | Do this                                                                                                               | Done when                                                       |
| ---- | ----------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 14   | Autograd                | Karpathy micrograd / Zero to Hero 1–2; rebuild `Value` from an empty file                                             | Backward pass on paper + code                                   |
| 15   | PyTorch basics          | Official PyTorch tutorial; write a training loop and explain it                                                       | Loop runs; you can diagnose a planted mode or gradient bug      |
| 16   | Debug training          | Overfit 10 samples; learning-rate sweep; loss curves                                                                  | Can name 3 failure modes                                        |
| 17   | MLP / CNN               | Dive into Deep Learning or CS231n notes; one small classifier                                                         | Baseline comparison and loss curves explained                   |
| 18   | Transfer learning       | fast.ai lessons 1–4 **or** fastbook ch 1–4; train the head, then compare unfreezing the backbone                      | Demo on **your** images or domain                               |
| 19   | Attention intuition     | Karpathy build-GPT video; type along                                                                                  | Can draw the attention block                                    |
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

- **Top-down** (fast.ai): train a working model in lesson one, then come back to the mechanics.
  This can keep you engaged, though it is a teaching choice, not a proven cure for giving up.
- **Bottom-up** (Karpathy, d2l.ai): start from a single derivative and build up to a transformer.
  The argument is that nothing else produces real understanding of what is happening.
- **Maths first**: foundations before code. This is the one ordering I would gently steer you away
  from, for the reasons in [Chapter 3](../03-core-machine-learning/README.md).

I suggest **bottom-up first, top-down alongside**: build the autograd engine, then learn PyTorch,
then use fast.ai for transfer learning and momentum. If you know that you lose interest without an
early win, invert it and do fast.ai's first three lessons before the autograd exercise. Both work.

**On frameworks.** Use PyTorch here so the exercises share one implementation. Choose another
framework later when a project or team needs one. Keras supports custom PyTorch training steps
([Keras custom-training-step guide](https://keras.io/guides/custom_train_step_in_torch/)), so it
still lets you learn the loop. JAX is useful beyond very large training runs too. The point is a
consistent first project.

The official [PyTorch 2.14 release](https://pytorch.org/blog/pytorch-2-14-release-blog/), published
2 September 2026, adds compiler, hardware and distributed-runtime work. Pin a supported release and
use its docs. A release-note speedup on one kernel or device does not predict your model's
end-to-end speed. Several new features are marked experimental.

## What to learn

### Worked lesson: gradients must accumulate

Let `x = 3`, `a = x × x` and `y = a + a`. The forward pass gives `a = 9` and `y = 18`.
`a` is used twice, and each use contributes 1 to `dy/da`, so its accumulated gradient is 2.
The two inputs to `x × x` then each contribute `x × 2 = 6` to `dy/dx`. The final gradient is 12.
Assigning a gradient with `=` instead of accumulating with `+=` silently loses a path.

```python
def objective(x):
    a = x * x
    return a + a

x, epsilon = 3.0, 1e-5
numeric_gradient = (objective(x + epsilon) - objective(x - epsilon)) / (2 * epsilon)
assert abs(numeric_gradient - 12.0) < 1e-6
```

This numerical gradient is a small, independent check on your backward pass, for debugging rather
than training. It needs many forward evaluations and can be unstable near non-differentiable points
or with a badly chosen step size.

**Try it yourself.** Change the graph to `y = a × a`, keeping `a = x × x`. At `x = 3`, predict
the value and derivative before running the numerical check. Which reused nodes need accumulation?

<details>
<summary>Hint and explained answer</summary>

The objective is `x⁴`, so its value is 81 and its derivative is `4x³ = 108`. Each use of `a`
contributes 9, giving `dy/da = 18`. Each use of `x` then contributes `3 × 18 = 54`, adding up to
108. Test this graph as well as plain addition and multiplication. A backward pass that only works
on a simple chain is incomplete.

</details>

### Core concepts

**Backpropagation, by building it.** Write a scalar autograd engine: a `Value` class with the
arithmetic operations, a topological sort for the backward pass, and correct gradient accumulation
when a node is used more than once. That last detail is where most people's bug lives, and finding
it is the moment the chain rule stops being a formula.

**PyTorch as a language.** Tensors, `Dataset` and `DataLoader`, and the explicit training loop you
should be able to implement and explain. Know why `model.train()` and `model.eval()` differ, why
`zero_grad()` exists, what `torch.no_grad()` saves you, and why both the model and the data need to
be on the same device.

Start with this explicit loop and inspect each state change:

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
`torch.inference_mode()`. Evaluation mode changes dropout and batch-normalisation behaviour.
Turning off autograd avoids building a backward graph. Neither does the other's job. When
debugging, check mode and gradient state separately rather than guessing. After
validation, switch back to training mode at the start of each epoch.
[PyTorch's optimisation tutorial](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
shows separate training and evaluation loops.

Check the loss contract too. For ordinary multiclass classification, pass unnormalised logits to
`CrossEntropyLoss`, with class-index targets of the expected shape and dtype. Applying softmax first
changes the objective. Use valid probability targets only when the task calls for them. The
[loss documentation](https://docs.pytorch.org/docs/2.14/generated/torch.nn.CrossEntropyLoss.html)
also explains ignored targets and reduction. For epoch loss, sum the loss numerator and its
intended denominator across batches, then divide. A plain average of batch means can overweight a
short last batch or a sequence with few supervised tokens.

**Training dynamics, and how to break them.** This is the part that separates people who can debug
training from people who change the architecture and hope. Instrument your runs with loss curves for
both splits, gradient norms per layer, and activation histograms.

Five habits fix most problems:

1. **Try to overfit ten clean samples with regularisation and augmentation turned off.** An
   unexpected failure is a clue, though noisy labels, a constrained model or the loss can limit the
   fit. Check shapes, target encoding and gradient flow before adding complexity.
2. Compare against a trivial baseline.
3. Sweep the learning rate across orders of magnitude and plot it.
4. Turn off every extra (augmentation, scheduler, dropout), get a working baseline, then add one
   thing at a time.
5. **Look at the data.** Print ten samples as the model sees them, after transforms. A surprising
   share of "it will not learn" turns out to be inverted labels or a normalisation applied twice.

**When it still will not learn, work down this checklist.** Change one thing per run and log it.

- **Overfit one small batch.** If a few examples cannot reach near-zero training loss, suspect the
  loss, targets or update step before the architecture.
- **Data, labels and shapes.** Assert shapes and dtypes where the loss is computed, and check label
  values against the output layer. `(B, 1)` outputs against `(B,)` targets broadcast to `(B, B)` in
  a regression loss, as in the Chapter 2 exercise.
- **Loss at initialisation.** With near-uniform initial predictions, multiclass cross-entropy starts
  near `ln(C)`, about 2.30 for ten classes. Much higher suggests overconfident initialisation. An
  output bias matching the class prior or target mean is a cheap fix.
- **Learning rate, then warmup and schedule.** Find a working constant rate by sweeping orders of
  magnitude. Only then add a short warmup for early instability, and a decay schedule.
- **AdamW and weight decay.** `Adam` with `weight_decay` adds an L2 term to the gradient by default.
  `AdamW` decouples the decay from the adaptive update. Check which one you use, and whether biases
  and normalisation weights are excluded from decay.
- **Gradient norms and clipping.** Log the global norm each step (`clip_grad_norm_` returns it).
  Clip to cap occasional spikes, calling `scaler.unscale_(optimizer)` first if you use a gradient
  scaler. Clipping on most steps acts as a smaller learning rate.
- **Vanishing or exploding gradients.** Early-layer gradient norms orders of magnitude below later
  ones, with a flat loss, suggest vanishing. Growing norms, loss spikes or NaNs suggest exploding.
  Check initialisation for the activation, normalisation, residual paths and the learning rate.

Karpathy's [recipe for training neural networks](https://karpathy.github.io/2019/04/25/recipe/) and
Google's [Deep Learning Tuning Playbook](https://github.com/google-research/tuning_playbook) expand
these steps. Both have notes in [resources/](resources/README.md#keep-for-reference).

**Transfer learning.** When suitable pretrained weights exist, adapt them and compare against a
small from-scratch baseline. For tiny datasets, freeze the backbone and train a new head. Unfreeze
more as you get more data, and try lower learning rates for earlier layers. CNNs make weight sharing
and local inductive bias concrete. Vision transformers and self-supervised encoders are useful
challengers when their data, memory and latency needs fit. Avoid claiming one family wins every
small-data or edge task. Augment training data only, deduplicate before splitting, and hold out
whole subjects or capture sessions when deployment needs that generalisation.

Freezing parameters with `requires_grad_(False)` does not freeze batch-normalisation buffers. Decide
whether to keep the pretrained running statistics or adapt them on training data. To keep them,
return the relevant backbone modules to evaluation mode after each outer `model.train()` call,
leaving the new head in training mode. Record the choice, and keep validation data out of
statistics updates.
[PyTorch's BatchNorm documentation](https://docs.pytorch.org/docs/2.14/generated/torch.nn.BatchNorm2d.html)
describes running statistics. Evaluation mode and gradient freezing are separate controls.

**Attention, built by hand.** Follow Karpathy's
[build-a-GPT lecture](https://www.youtube.com/watch?v=kCc8FmEb1nY), typing rather than watching,
then build a byte-pair tokeniser. Inspect how it splits whitespace, numbers and several languages.
Tokenisation affects the input and token cost, but is only one possible cause of reasoning
failures. Add tests for causal masking, padding, position handling and encode/decode round trips.
Split a language corpus by source document before making token windows, so neighbouring or
duplicated text cannot leak into validation. Learn BPE merges and any fitted preprocessing from
training text only, then keep them fixed for validation and the final test.

The scale has a useful derivation. Suppose the `d` query and key components are independent, with
zero mean and unit variance. Then each product has variance 1 and the dot product, their sum, has
variance `d`. Dividing by `sqrt(d)` restores variance 1 under those assumptions. This helps stop dot
products growing with head dimension and over-concentrating the softmax. Learned components need not
meet those assumptions exactly, so this explains the scale rather than proving exact normalisation
for every trained head. Apply a causal mask before softmax, so a masked future token gets no
attention weight, however large its unmasked score.

To test causal masking, change a future token and check earlier logits stay the same within
numerical tolerance, in evaluation mode. Shift targets correctly for next-token prediction, checking
whether the model already shifts them internally. Exclude padding from the loss too. Masking it in
attention alone leaves its training targets in place.

Read [_Attention Is All You Need_](https://arxiv.org/abs/1706.03762) **after** this, not before. It
is a 2017 machine-translation paper describing an encoder-decoder model. Compare its attention
mechanism with your decoder-only model. There is no useful percentage for how much of its design a
current model shares. Read cold as a first resource, it tends to discourage people. Read after you
have built the thing, it is easier to connect to the code. Its notes are in
[resources/](resources/README.md).

**Efficient training, after correctness.** Profile an eager baseline, then change one thing at a
time. Automatic mixed precision can cut memory and runtime on supported hardware. Choose the dtype
for the device, check loss and gradients stay finite, and use a gradient scaler when your
precision and setup need one
([PyTorch AMP recipe](https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html)).

Gradient accumulation changes the effective batch size. Scale the loss correctly and step the
optimiser at the intended interval. With variable-length sequences, divide the summed token loss by
all non-ignored prediction targets in the accumulation window, including a short final window.
Averaging each microbatch's mean equally changes token weighting. Check your pinned trainer's
handling so you do not divide twice. The
[Transformers accumulation guide](https://huggingface.co/docs/transformers/grad_accumulation)
documents this denominator. Accumulation does not reproduce a large batch's batch-normalisation
statistics. Activation checkpointing trades recomputation for activation memory. These are different
controls, not interchangeable fixes.

Try `torch.compile` once the model is correct. Record first-run compilation separately from
steady-state time, because changing shapes and graph breaks can erase the benefit. Report peak
memory, examples or tokens per second, and the same validation metric as the eager model. A slower
or less stable result is still a useful experiment
([official compile tutorial](https://docs.pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)).

**Where recent research fits.** The material below was checked on 9 October 2026. It is
orientation and optional depth within the 90 hours. Reproducing a frontier model is extra work.

| Source and evidence                                                                                                                                                     | What to learn                                                                                                 | Bounded exercise                                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| [CS336 Spring 2026](https://cs336.stanford.edu/), official course                                                                                                       | Architecture/resource accounting, data filtering and evaluation precede mid/post-training                     | Read the schedule, then trace one tiny model from corpus to checkpoint; reserve full assignments for Chapter 7                                        |
| [FlashAttention-4](https://proceedings.mlsys.org/paper_files/paper/2026/hash/ae8b0b5838ba510daff1198474e7b984-Abstract-Conference.html), peer-reviewed MLSys 2026 paper | Attention performance depends on memory movement, kernel scheduling and hardware                              | Explain why the reported hardware result does not transfer automatically to your laptop; use a supported attention backend and profile it             |
| [DeepSeek-R1](https://www.nature.com/articles/s41586-025-09422-z), peer-reviewed Nature paper published 17 September 2025                                               | Reinforcement learning with verifiable rewards is a separate stage from pretraining and supervised adaptation | Describe a reliable task verifier, then one way a model could exploit it; reasoning benchmarks alone show no general retention or pricing benefit   |

For adaptation, tell full fine-tuning apart from LoRA, which trains low-rank weight updates, and
QLoRA, which trains adapters on a quantised base model. Neither guarantees lower serving latency or
unchanged task quality. Supervised fine-tuning learns from demonstrations and preference
optimisation from comparisons. RL with verifiable rewards needs a real verifier. Learn these
distinctions here. Run one bounded adaptation experiment only when it addresses a measured failure
in your project: optionally in Chapter 5's week 31 fine-tuning decision, or as Chapter 7 depth work.
The primary papers and current implementation guides are in the resource list.

## Resources

All 30 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.
The main path uses selected sections, so the full-course hour estimates are not extra work.

The ones to begin with:

- [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) — Andrej Karpathy. A free
  course, 40–70 hours; lecture 1 (micrograd) is week 14.
- [PyTorch official tutorials — "Learn the Basics"](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)
  — PyTorch documentation team. Free documentation, 8–12 hours.
- [Practical Deep Learning for Coders](https://course.fast.ai/) — Jeremy Howard. A free course,
  40–80 hours; lessons 1 to 4 are what this chapter uses.
- [Understanding Deep Learning](https://udlbook.github.io/udlbook/) — Simon J. D. Prince. A free
  book, 60–80 hours, used for lookup, not read cover to cover.

## What to build

**A model you trained yourself,** with an honest ablation — retraining with one component removed
or swapped at a time, to measure what each one contributes. Pick one:

- **Same thread:** a small network on your Chapter 3 features, in raw PyTorch. Tune on the same
  training and validation data, then compare once on the same test with your Chapter 3 baseline and
  boosted tree. Losing to the trees is worth reporting. The
  [reference lab](../labs/README.md#follow-the-project-through-the-book) sets up the same experiment
- A classifier on 200-plus photos **you took**, in raw PyTorch, deployed as a small demo
- A character-level language model on a corpus that means something to you, with the modern
  architecture pieces swapped in one at a time
- A reproduction of one bounded paper component, implemented from the paper and compared against a
  reference

Whichever you pick, save the split and data versions, configuration, environment, seed and a full
training checkpoint: model, optimiser, scheduler and scaler if used, random-generator states and
progress. Save preprocessing and tokeniser versions too. Resuming mid-epoch can also need the
sampler or data-loader position. Practise resuming from it. To judge whether an
ablation helped, record how results vary across repeated runs. A seed does not guarantee identical
results across releases or devices
([PyTorch reproducibility notes](https://docs.pytorch.org/docs/2.14/notes/randomness.html)).

Keep a final test untouched until model selection is done. Include a real ablation, failed runs,
one diagnosed failure, and a demo with its inference settings recorded. If hosting is unavailable,
a reproducible local demo is fine, but do not present a screenshot as a live service.

The ablation is where most of the value sits. A table showing that one change mattered and three
were within noise, with wall-clock times alongside, says more about you than a good final number.

**Handoff to Chapter 5.** Carry these habits forward: an untouched test, replayable runs and a fair
baseline comparison. [Chapter 5](../05-language-models/README.md) applies them to documents
from your Chapter 2 domain, starting from a pretrained model rather than one you trained.

## Before you move on

- Your autograd engine passes a numerical gradient check on a graph with a reused node, and you can
  explain and fix a deliberately broken accumulation rule.
- You can write a training and validation loop, find a wrong mode or gradient setting, and show
  that validation does not update the model. Documentation is allowed.
- Given an unhealthy loss curve, you can name a likely cause and the instrument that confirms it.
- You can label a causal attention matrix with its shapes and mask, and explain the variance reason
  for dividing by the square root of the head dimension.
- You can reload a checkpoint and explain what would be lost by saving only model weights.
- You can compare a precision or compile change on quality, memory and measured runtime.

## A few things worth knowing

- **The Goodfellow, Bengio and Courville book** is free, famous, and where a lot of people stall.
  Published in 2016 with only minor corrections since, it has no transformer chapter and its
  sequence and generative sections are well out of date. Chapters 2 to 9 are still a clean rigorous
  treatment of the mathematics. Simon Prince's
  [_Understanding Deep Learning_](https://udlbook.github.io/udlbook/), also free, is the more useful
  modern choice.
- **Check the date on course materials.** The older CS231n recordings teach basic training
  mechanics. The [Spring 2026 schedule](https://cs231n.stanford.edu/schedule.html) adds current
  vision topics. Its slides and assignments are public, but the current lecture videos may not be.
- **Rewrite one fast.ai exercise in an explicit PyTorch loop.** This checks your grasp of
  transforms, optimiser updates and validation behaviour under the convenience API.
- **Use materials that contain working exercises.** Read
  [microgpt](https://karpathy.github.io/2026/02/12/microgpt/), a compact pure-Python teaching
  implementation, and inspect [nanochat](https://github.com/karpathy/nanochat), an
  author-maintained training pipeline. Pin its commit and compute assumptions before running it.
  Neither a tiny names model nor a repository headline shows production capability.

---

[Previous: Core machine learning](../03-core-machine-learning/README.md) &nbsp;·&nbsp;
[Next: Language models and AI engineering](../05-language-models/README.md)
