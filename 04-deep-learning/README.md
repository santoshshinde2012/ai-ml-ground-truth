# Chapter 4: Deep learning

**Weeks 14-22 &nbsp;·&nbsp; about 90 hours.** &nbsp;·&nbsp; [Index](../README.md) &nbsp;·&nbsp; [Resources for this chapter](resources/README.md)

**The short version.** You build a tiny neural network engine from an empty file, learn PyTorch properly, practise diagnosing training that quietly fails, and build attention with your own hands. You finish with a model you trained yourself and can explain — which is what separates you from someone who only calls APIs.

**Same thread, new skill.** You still know tabular ML from Chapter 3. Here you learn *how neural nets learn* — the machinery behind LLMs.

---

## Your nine-week plan

About ten hours a week. Karpathy first unless you need an early win (fast.ai lesson 1-3), as noted below.

| Week | Focus | Do this | Done when |
|---|---|---|---|
| 14 | Autograd | Karpathy micrograd / Zero to Hero 1-2; rebuild `Value` from empty file | Backward pass on paper + code |
| 15 | PyTorch basics | Official PyTorch tutorial; training loop from memory | Loop runs on toy data |
| 16 | Debug training | Overfit 10 samples; learning-rate sweep; loss curves | Can name 3 failure modes |
| 17 | MLP / CNN | Dive into Deep Learning or CS231n notes; one small classifier | Validation loss decreases |
| 18 | Transfer learning | fast.ai lessons 1-4 **or** fastbook ch 1-4; freeze/unfreeze head | Demo on **your** images or domain |
| 19 | Attention intuition | Karpathy build-GPT video; type along | Can draw attention block |
| 20 | Tokeniser | Karpathy tokeniser video; byte-level on small corpus | Encode/decode round-trip works |
| 21 | Your model | Pick capstone option from What to build; config file | Training reproducible from config |
| 22 | Ablation + deploy | Ablation table (incl. failed runs); public demo link | README + honest ablation |

---

## What you will be able to do

Write backpropagation from an empty file, train a network in PyTorch without a template, and take a
model that is quietly not learning and work out why.

## On the order to do this in

You will be told three incompatible things about how to start deep learning, and all three come from
people worth listening to.

- **Top-down** (fast.ai): train a working model in lesson one, and earn the theory afterwards. The
  argument is that motivation collapses without early wins, and the dropout data supports them.
- **Bottom-up** (Karpathy, d2l.ai): start from a single derivative and build up to a transformer.
  The argument is that nothing else produces real understanding of what is happening.
- **Maths first**: foundations before code. This is the one ordering I would gently steer you away
  from, for the reasons in [Chapter 3](../03-core-machine-learning/README.md).

I suggest **bottom-up first, top-down alongside**: build the autograd engine, then learn PyTorch,
then use fast.ai for transfer learning and momentum. If you know that you lose interest without an
early win, invert it and do fast.ai's first three lessons before the autograd exercise. Both work.

The heat in this argument mostly comes from people who did one and not the other. Both authors have
said versions of "learn it, then learn why".

**On frameworks:** PyTorch, and only PyTorch, for at least a year. TensorFlow's own release notes
now point new generative-AI users elsewhere. JAX is aimed at people optimising very large training
runs. Keras is a reasonable production tool and a poor teaching one, because it hides the training
loop, which is the thing you most need to see.

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
model.train()
for epoch in range(num_epochs):
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        loss = criterion(model(x), y)
        loss.backward()
        optimizer.step()
```

`model.eval()` and `torch.no_grad()` replace `model.train()` when you are measuring validation loss.
If you cannot write this without looking, you are not ready to debug someone else's training code.

**Training dynamics, and how to break them.** This is the part that separates people who can debug
training from people who change the architecture and hope. Instrument your runs with loss curves for
both splits, gradient norms per layer, and activation histograms.

Five habits fix most problems:

1. **Overfit a single batch of ten samples to near-zero loss first.** If you cannot, something is
   broken in the model, the loss or the data pipeline. It takes thirty seconds and saves hours.
2. Compare against a trivial baseline.
3. Sweep the learning rate across orders of magnitude and plot it.
4. Turn off every extra (augmentation, scheduler, dropout), get a working baseline, then add one
   thing at a time.
5. **Look at the data.** Print ten samples as the model sees them, after transforms. A surprising
   share of "it will not learn" turns out to be inverted labels or a normalisation applied twice.

**Transfer learning.** Almost nobody trains from scratch. Take a pretrained model and adapt it:
freeze everything and train a new head for tiny datasets, unfreeze progressively as you have more
data, and use lower learning rates for earlier layers. Two weeks is the right budget here.
Convolutional networks are no longer the frontier, but they remain the cheapest concrete way to
understand weight sharing, inductive bias and feature hierarchies, and they still dominate
small-data and edge deployment.

**Attention, built by hand.** Follow Karpathy's [build-a-GPT lecture](https://www.youtube.com/watch?v=kCc8FmEb1nY), typing rather than watching,
then build a byte-pair tokeniser. Tokenisation looks like the boring part and is responsible for a
disproportionate share of confusing model behaviour: arithmetic mistakes, letter counting, whitespace
sensitivity and the higher cost of non-English text. Both Karpathy and Stanford's CS336 open with it,
which is not a coincidence.

Read [*Attention Is All You Need*](https://arxiv.org/abs/1706.03762) **after** this, not before. It is a 2017 machine-translation paper
describing an encoder-decoder model, and a current language model shares perhaps half its design.
Read cold as a first resource it tends to discourage people; read after you have built the thing it
is genuinely enjoyable. Its annotated entry is in [resources/](resources/README.md).

## Resources

All 25 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) — Andrej Karpathy. A free course, 40-70 hours; lecture 1 (micrograd) is week 14.
- [PyTorch official tutorials — "Learn the Basics"](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) — PyTorch documentation team. Free documentation, 8-12 hours.
- [Practical Deep Learning for Coders](https://course.fast.ai/) — Jeremy Howard. A free course, 40-80 hours; lessons 1 to 4 are what this chapter uses.
- [Understanding Deep Learning](https://udlbook.github.io/udlbook/) — Simon J.D. Prince. A free book, 60-80 hours as a lookup layer, not a read-through.

## What to build

**A model you trained yourself,** with an honest ablation — the model retrained with one component
removed or swapped at a time, to measure what each one contributed. Pick one:

- A classifier on 200-plus photos **you took**, in raw PyTorch, deployed as a small demo
- A character-level language model on a corpus that means something to you, with the modern
  architecture pieces swapped in one at a time
- A paper reproduction, implemented from the paper alone and compared against a reference

Whichever you pick, four things matter: it reproduces from a config file, it has a real ablation
reported honestly including the runs that failed, it documents one failure you diagnosed, and it is
deployed somewhere a stranger can click.

The ablation is where most of the value sits. A table showing that one change mattered and three
were within noise, with wall-clock times alongside, says more about you than a good final number.

## Before you move on

- You can rebuild the autograd engine from an empty file, in under an hour.
- You can write a training loop from nothing.
- Given an unhealthy loss curve, you can name a likely cause and the instrument that confirms it.
- You can draw attention from memory and explain why we divide by the square root of the head
  dimension.

## A few things worth knowing

- **The Goodfellow, Bengio and Courville book** is free, famous, and where a lot of people stall.
  Published in 2016 with only minor corrections since, it has no transformer chapter and its
  sequence and generative sections are well out of date. Chapters 2 to 9 are still a clean rigorous
  treatment of the mathematics. Simon Prince's [*Understanding Deep Learning*](https://udlbook.github.io/udlbook/), also free, is
  the more useful modern choice.
- **The 2016-17 CS231n video playlist** is the most linked deep learning course on the internet and
  predates transformers entirely. Use the recent recordings instead.
- **fast.ai's own API is not PyTorch.** Its abstractions are excellent for learning and rare in
  industry, so plan to rewrite at least one project in plain PyTorch.
- **Do not wait for a course that has not shipped.** Karpathy's LLM101n repository has been archived
  since 2024 with a syllabus and no materials. The syllabus is a good checklist;
  [nanochat](https://github.com/karpathy/nanochat) is the working artefact to read instead.

---

[Previous: Core machine learning](../03-core-machine-learning/README.md) &nbsp;·&nbsp; [Next: Language models and AI engineering](../05-language-models/README.md)
