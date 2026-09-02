# Resources — Chapter 4: Deep learning

Everything referenced in [the chapter](../README.md), grouped by how central it is, with a short
note on what each one is for.

Prices and free tiers change often, so check a resource's own page before you plan around one.

---

## Start here

The resources on the main path for this chapter, in the order the chapter uses them. If you only do a few things, do these.

### [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)

*Andrej Karpathy* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40-70 hours

This is the single best answer to 'how much maths do I actually need before writing code', because Karpathy states the prerequisite himself on the course page: 'Solid programming (Python), intro-level math (e.g. derivative, gaussian).' That is the whole gate. Lecture 1 builds micrograd — a ~100-line scalar autograd engine — from nothing, and in doing so it teaches you the chain rule by making you implement it, which is strictly more durable than watching a derivation. Lecture 5 ('Becoming a Backprop Ninja') forces you to hand-derive backward passes through matrix multiply, softmax, cross-entropy and BatchNorm, which is the real matrix-calculus exam.

> **Worth knowing.** Frozen since February 2024. Strong on backprop, MLPs and transformer intuition, but stops before post-training, RLHF and the scaling infrastructure behind a modern LLM.

### [PyTorch official tutorials — "Learn the Basics"](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)

*Suraj Subramanian, Seth Juarez, Cassie Breviu, Dmitry Soshnikov & Ari Bornstein* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 8-12 hours

The 8-part official path (Tensors, Datasets/DataLoaders, Transforms, Build Model, Autograd, Optimization Loop, Save/Load) using FashionMNIST. Non-negotiable: this is where you learn the idioms of the framework everyone actually uses, and how to read the docs when Stack Overflow fails. Every section opens in Colab. Do it in week 15, straight after the autograd exercise — or, if you took the fast.ai-first route, right after lesson 3 — so you can see what fastai is abstracting away. Docs currently track PyTorch 2.13.

### [CS231n course notes (Neural Networks + Convolutional Neural Networks modules)](https://cs231n.github.io/)

*Andrej Karpathy, Justin Johnson & Fei-Fei Li* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 15-20 hours

Still, in 2026, the clearest written treatment of backprop-as-computational-graph, weight initialisation, regularisation and the practical mechanics of CNNs — Karpathy's 'Backprop as a staged computation' and 'Neural Nets Part 3: Learning and Evaluation' notes are the ones every practitioner secretly re-reads. Free, no login. Use as reference alongside Karpathy's videos: the notes are the text version of what he says out loud. The parent course itself (cs231n.stanford.edu) is now Spring 2026 and its assignments reach transformers, self-supervised learning (CLIP/DINO) and diffusion models, but the *current-year* lecture videos are Canvas-only for enrolled Stanford students.

> **Worth knowing.** A decade old — good for backprop and CNN intuition only. The live 2026 CS231n syllabus covers considerably more than these notes do.

### [Dive into Deep Learning (d2l.ai)](https://d2l.ai/)

*Aston Zhang, Zachary C. Lipton, Mu Li & Alexander J. Smola* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 60-100 hours

The best 'math + code in the same cell' book: every concept appears as prose, equation, and a runnable implementation, with parallel PyTorch, JAX, TensorFlow and NumPy/MXNet versions — so you can literally diff how the same model looks in each framework, which settles the 'which framework' question empirically. Adopted at 500+ universities. Use it as the bottom-up spine if you hate fast.ai's top-down style, or as a per-topic supplement (its optimisation and CNN chapters are excellent). Note: the last tagged release is 1.0.3 (August 2024), so its coverage of 2025–2026 LLM practice is thin; the fundamentals chapters are unaffected and still excellent.

> **Worth knowing.** Author affiliations are as of the 2023 publication and are now out of date. Follow the PyTorch code path; the MXNet one is obsolete.

### [Practical Deep Learning for Coders (fast.ai)](https://course.fast.ai/)

*Jeremy Howard* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40-80 hours

Included here as the primary source for the entire 'just enough math' position, not as a maths course. Its official prerequisites page states the math requirement flatly: 'Just high school math is sufficient,' and it explicitly debunks the belief that deep learning requires 'lots of math.' Lesson 1 has you training a working image classifier before any theory appears; the math then arrives in context, chapter by chapter, as you need it. If you are paralysed by 'I need to finish maths first,' this course is the intervention.

> **Worth knowing.** The current course is the 2022 recording, so expect API drift in the notebooks. It is a deep-learning course, not a math resource.

### [fastbook — Deep Learning for Coders with fastai & PyTorch (free Jupyter notebooks)](https://github.com/fastai/fastbook)

*Jeremy Howard & Sylvain Gugger* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 20 hours

The book behind the course, released in full as runnable notebooks. Read chapter N after watching lesson N — the book contains the derivations and 'further research' questions the video skims. Chapter 4 ('MNIST basics'), where you build SGD from scratch, is the bridge to Karpathy. Note: the prettified web edition at fastai.github.io/fastbook2e only shows 6 of 20 chapters in full — use the GitHub notebooks, which are complete and free.

> **Worth knowing.** A 2020 book whose last commit is two years old: the fastai-specific APIs and environment pins are what rot, so expect dependency-resolution pain on a fresh install. The top-down pedagogy still holds up.

### [Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY)

*Andrej Karpathy* &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 8 hours

The canonical 'build a transformer with your own hands' lecture. Type it, don't watch it. This is the step that converts 'attention is a weighted average' from a phrase into something you can debug. Part of the Neural Networks: Zero to Hero series (https://karpathy.ai/zero-to-hero.html); if you have no backprop background, do the micrograd lecture (#1) first.

> **Worth knowing.** A from-scratch teaching build rather than the current state of the art — pair it with nanochat for how a modern model is actually assembled.

### [Let's build the GPT Tokenizer](https://youtu.be/zduSFxRajkE)

*Andrej Karpathy* &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4 hours

Tokenisation is the #1 source of weird LLM behaviour that beginners misattribute to 'the model is weak' — trailing whitespace bugs, non-English cost blowups, JSON key sensitivity, arithmetic failures. 2h13m building BPE from scratch. Stanford CS336 also opens with tokenisation for the same reason. Do this immediately after 'Let's build GPT'.

### [Understanding Deep Learning (UDL)](https://udlbook.github.io/udlbook/)

*Simon J.D. Prince* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 60-80 hours

This is the book that should have replaced Goodfellow as the default recommendation, and in 2026 it has. It is modern (transformers, diffusion, graph nets, self-supervised learning), ruthlessly curated rather than encyclopedic, and comes with free Colab notebooks, full slides for the early chapters, and answers to selected problems — so a self-learner can actually check themselves. For a beginner path: do not read it cover to cover first. Use it as the lookup layer under fast.ai and Karpathy — when a lesson says 'we use batch norm here', read the UDL chapter that night.

> **Worth knowing.** The book site alone is thin: the notebooks, slides, figures and answer booklet live in the GitHub repo at github.com/udlbook/udlbook.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

*Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser & Illia Polosukhin* &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3 hours

Read it once, mid-journey — after Karpathy's GPT video, not before. Reading it cold as your first resource is the classic beginner mistake: it's a 2017 machine-translation paper about an encoder-decoder model, and a 2026 LLM shares maybe half its design. Its lasting value is that it teaches you to read papers and shows you what has and hasn't survived nine years.

> **Worth knowing.** The primary source, not a tutorial — read it after the Illustrated Transformer and Karpathy's GPT lecture, or you will bounce off it.

### [Deep Learning Specialization (DeepLearning.AI / Coursera)](https://www.coursera.org/specializations/deep-learning)

*Andrew Ng* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 80-120 hours

5 courses: Neural Networks and Deep Learning; Improving Deep NNs (hyperparameters/regularisation/optimisation); Structuring ML Projects; CNNs; Sequence Models. Ng's explanations of bias/variance, regularisation and the practical 'what do I do when my model is bad' workflow (Course 2 and Course 3) remain the best in any course anywhere, and Course 3 has essentially no competitor. But be honest about 2026: the assignments are Python + TensorFlow, and the last substantial refresh was April 2021 (when TF2, MobileNet, U-Net and a transformer lesson were added). For someone targeting 2026 jobs, doing all 5 courses in TensorFlow is time spent learning a framework the field left.

> **Worth knowing.** Five years since its last refresh and taught in TensorFlow, which is likely not the framework you will use — take it for conceptual grounding. Enrolment needs a paid Coursera subscription.

### [fast.ai Part 2: Deep Learning Foundations to Stable Diffusion](https://course.fast.ai/Lessons/part2.html)

*Jeremy Howard with Jonathan Whitaker, Tanishq Abraham & Wasim Lorgat, plus Stability.ai and Hugging Face contributors* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 30 hours

You rebuild a modern deep learning framework and Stable Diffusion from the ground up — matrix multiplication, backprop, ResNets, U-Nets, transformers, optimisers, mixed precision, DDPM/DDIM. This is fast.ai's answer to the criticism that it hides too much, and it is the ideal 'act three' after Part 1 + Karpathy. Not a beginner resource: it explicitly assumes Part 1 or equivalent PyTorch/Kaggle competence.

> **Worth knowing.** The headline deliverable — implementing Stable Diffusion from scratch — targets a deprecated model generation, and DDPM-style formulations have largely given way to flow matching. Strongest as a foundations course.

### [Learn PyTorch for Deep Learning: Zero to Mastery](https://www.learnpytorch.io/)

*Daniel Bourke* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40-60 hours

The most beginner-tolerant *pure PyTorch* course: 10 notebook-modules running from tensors through classification, computer vision, custom datasets, transfer learning, experiment tracking and paper replication to deployment. Its transfer-learning and 'replicate a paper' modules are exactly the gap fast.ai leaves (fast.ai teaches transfer learning through its own API; Bourke teaches it in raw torchvision, which is what a job requires). Note: the site's last major update was April 2023, so its PyTorch 2.x coverage is an add-on section rather than integrated; the APIs used still work but check the docs for anything torch.compile-related.

> **Worth knowing.** Unchanged since April 2023 by its own admission. Core PyTorch APIs still work, but the "PyTorch 2.0" framing is now historical and nothing covers torch.compile maturity, modern distributed training or current deployment paths.

### [Machine Learning with PyTorch and Scikit-Learn](https://www.amazon.com/Machine-Learning-PyTorch-Scikit-Learn-learning/dp/1801819319)

*Sebastian Raschka, PhD, with Yuxi Liu and Vahid Mirjalili* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 60-90 hours

The best single bridge from classical ML to deep learning in one PyTorch-native volume — you get scikit-learn fundamentals (evaluation, regularisation, feature engineering) and then PyTorch NNs, CNNs, RNNs, transformers and graph NNs from the same author with consistent notation. Valuable specifically for people who skipped classical ML and would otherwise never learn cross-validation or proper evaluation. Published February 2022, so its transformer chapter predates the LLM boom; Raschka's own *Build a Large Language Model (From Scratch)* is the sequel to reach for after.

> **Worth knowing.** 2022 content, substantially superseded on current tooling by Géron's December 2025 Scikit-Learn and PyTorch book; the runnable code lives in the rasbt/machine-learning-book GitHub repo.

### [MIT 6.S191: Introduction to Deep Learning (2026 edition)](https://introtodeeplearning.com/)

*Alexander Amini & Ava Amini* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 15-25 hours

The best short on-ramp in the field: 9 fast, well-produced lectures covering sequence modelling, CNNs, generative modelling, RL, LLMs, AI ethics and parallel training, all re-recorded and open-sourced each January — the 2026 edition is already public. Labs are Colab notebooks (repo carries both TensorFlow and PyTorch material). Use it as a one-week orientation *before* committing 3 months to fast.ai or Karpathy: it gives you the map of the territory cheaply. Not deep enough to be your main course.

### [NYU Deep Learning (DS-GA 1008), Spring 2021 edition](https://atcold.github.io/NYU-DLSP21/)

*Yann LeCun* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40 hours

The only place a beginner can hear the person who invented convolutional nets and the energy-based-model framing explain them personally, with Canziani's genuinely outstanding PyTorch notebooks and multi-language transcripts. Canziani has continued to teach and redesign DS-GA 1008 through Fall 2025, and is writing an accompanying book (atcold.github.io/book.html), but SP21 is the last fully public, self-contained edition — treat it as a perspective supplement (self-supervised learning, energy-based models) rather than your primary curriculum, and expect the framing to be more idiosyncratic than fast.ai's.

> **Worth knowing.** Explicitly a 2021 archive. Valuable for LeCun's energy-based and self-supervised framing, which is taught nowhere else, but treat it as a supplement rather than a starting point.

### [Stanford CS231n 2025 lecture videos (YouTube playlist)](https://www.youtube.com/playlist?list=PLoROMvodv4rOmsNzYBMe0gJY2XS8AQg16)

*Stanford Online / CS231n teaching staff* &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 25 hours

The most recent publicly-released CS231n video set. Use this rather than the widely-circulated 2016/2017 playlist, which is now a genuine trap: the 2017 lectures predate transformers, use TensorFlow-era framing, and spend time on architectures nobody trains anymore.

> **Worth knowing.** Videos only — the assignments and lecture notes that make the course work live separately at cs231n.stanford.edu.

### [Stanford CS231n: Deep Learning for Computer Vision — official site and Spring 2026 schedule](https://cs231n.stanford.edu/schedule.html)

*Fei-Fei Li, Justin Johnson, Ehsan Adeli, Zane Durante & Tiange Xiang* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 60 hours

Where to get the current syllabus, slides (PDFs are public, e.g. the 2026 lecture decks) and the three programming assignments. Worth doing assignment 1–2 by hand after Karpathy: implementing a fully-connected net and a CNN in raw NumPy is the single best test of whether you actually understood backprop. Flag honestly: because current-year videos are not public, do not expect a self-contained video course here — pair the 2026 materials with the publicly posted prior-year playlist.

> **Worth knowing.** Slides and notes are public, but the current-year lecture videos link into Canvas and are Stanford-only. The most recent freely watchable set is the 2025 YouTube playlist listed above.

### [The Little Book of Deep Learning](https://fleuret.org/public/lbdl.pdf)

*François Fleuret* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3-6 hours

A ~160-page phone-readable PDF (500,000+ downloads in its first year) that does something no other resource here does: it shows you how little maths you actually need, in one sitting, at correct professional density. Fleuret explicitly limits himself 'to the background necessary to understand a few important models' — tensor shapes, the chain rule, gradient descent, cross-entropy, and the layer zoo — rather than being exhaustive. Read it in a weekend after Karpathy lecture 1 as a sanity check on scope: if you can follow this book, your maths is sufficient to proceed, and any remaining gaps can be closed just-in-time. Written for readers with a STEM background, so it is terse, not gentle.

> **Worth knowing.** A compressed deep-learning primer that assumes linear algebra, calculus and probability rather than teaching them.

### [UMich EECS 498-007 / 598-005: Deep Learning for Computer Vision](https://web.eecs.umich.edu/~justincj/teaching/eecs498/FA2020/)

*Justin Johnson* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 30 hours

Johnson re-taught CS231n at Michigan with the full lecture set publicly posted on YouTube (playlist: youtube.com/playlist?list=PL5-TkQAfAZFbzxjBHtzdVCWE0Zbhomg7r), including the excellent 'Backpropagation', 'Training Neural Networks I/II', and 'Convolutional Networks' lectures. This is effectively a complete public-video CS231n, at greater depth than the single 2025 Stanford playlist. Best single video source for CNNs and training dynamics if you prefer a lecturer to a book.

> **Worth knowing.** The host has a broken TLS certificate chain, so some browsers warn on the URL, and the Fall 2020 material is six years stale. The YouTube lecture playlist is the more reliable route in.

## Keep for reference

Not for reading end to end. Useful to have when you need to look something up.

### [Deep Learning (the "Goodfellow book")](https://www.deeplearningbook.org/)

*Ian Goodfellow, Yoshua Bengio & Aaron Courville* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-20 hours

Published 2016 and, by the authors' own statement, only minor corrections since. Parts I–II (linear algebra, probability, numerical computation, feedforward nets, regularisation, optimisation, CNNs — roughly chapters 2–9) are still the cleanest rigorous treatment of the mathematics. Everything about sequence models and generative models is pre-transformer and pre-diffusion and should be skipped. **The trap:** it is the most-recommended and least-finished book in the field. Treat it as an encyclopedia you open for one rigorous explanation (vanishing gradients, why L2 regularisation does what it does), never as a beginner's reading plan.

> **Worth knowing.** A decade old and structurally missing the transformer architecture, so it cannot serve as a 2026 deep-learning text on its own. Dense and notation-heavy graduate reference that beginners reliably bounce off.

### [Kaggle Notebooks — free GPU/TPU quota](https://www.kaggle.com/docs/notebooks)

*Kaggle* &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free &nbsp;·&nbsp; 30 hours

Kaggle is the clear answer for a learner with no money. Kaggle gives a visible, predictable weekly quota (one P100 16GB or two T4s, plus TPU access) rather than Colab's undisclosed, demand-dependent allocation that can silently drop you to CPU at peak times. Two extra advantages for a beginner: datasets are already mounted (no download bandwidth cost) and public notebooks let you read how strong practitioners structure real training code. Practical rule: prototype in Colab because it starts faster, run anything that matters on Kaggle because the quota is honest. Colab free (T4, ~15–30 GPU-hours/week depending on demand) is the fallback, not the plan.

> **Worth knowing.** Kaggle changes its weekly GPU/TPU allowance, so treat any printed hours figure as approximate and check the current limits.

### [Lightning AI Studios — free tier](https://lightning.ai/pricing)

*Lightning AI* &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free &nbsp;·&nbsp; varies

The best free option when Kaggle's 9-hour session cap starts hurting: a persistent VS Code-style cloud dev environment with SSH and CLI, so your work survives between sessions (Colab and Kaggle both wipe state). Step 2 on the no-money compute ladder. Check the student program if you have a .edu address.

> **Worth knowing.** The free-tier allowance and terms change; check the pricing page before planning around them.

### [LLM101n syllabus (archived) + fast.ai/Eureka Labs status check](https://github.com/karpathy/LLM101n)

*Andrej Karpathy / Eureka Labs* &nbsp;·&nbsp; Repository &nbsp;·&nbsp; Free &nbsp;·&nbsp; 20 hours

Include this only so you do not waste time chasing it. The repo was archived on 1 August 2024 and contains a README and an image — no lessons, no code. The 17-chapter syllabus (bigram LM, transformers, tokenisation, optimisation, distributed training, inference, finetuning, deployment, multimodal) is still the best free curriculum *outline* in existence and is worth reading as a checklist of what you should eventually know. But with Karpathy at Anthropic since May 2026 and Eureka Labs paused, do not wait for the course: nanochat plus Raschka's books cover the same ground today.

> **Worth knowing.** Teaches nothing: an archived 17-chapter syllabus for a course that was never shipped. Historical interest only — Karpathy's nanochat is the material that actually exists.

### [Modal — serverless GPU with a standing free credit allowance](https://modal.com/pricing)

*Modal Labs* &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Paid &nbsp;·&nbsp; varies

Where to go once you need a real GPU for a few hours (fine-tuning, a paper replication) and want to pay nothing while idle. Its Python-decorator model means you deploy a training job without learning Docker or Kubernetes — the right escape hatch for a beginner who has outgrown notebooks but has not learned infra. Student credit programs also exist.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
