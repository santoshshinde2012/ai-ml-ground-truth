# Resources — Chapter 3: Core machine learning

Everything referenced in [the chapter](../README.md), grouped by how central it is, with a short
note on what each one is for.

Prices and free tiers change often, so check a resource's own page before you plan around one.

**Browse:** [Start here](#start-here) &nbsp;·&nbsp; [Optional depth](#optional-depth) &nbsp;·&nbsp;
[Keep for reference](#keep-for-reference) &nbsp;·&nbsp;
[Decisions, forecasts and current research](#decisions-forecasts-and-current-research)

---

## Start here

The resources on the main path for this chapter, in the order the chapter uses them. If you only do
a few things, do these.

### [An Introduction to Statistical Learning (ISLP — Python edition, 2023; ISLR 2nd ed. — R, 2021, corrected June 2023)](https://www.statlearning.com/)

_Gareth James, Daniela Witten, Trevor Hastie & Robert Tibshirani, with Jonathan Taylor on the Python
edition_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 60–90 hours

Probably the most valuable free text in the field, and the one that makes you _statistically_
literate rather than just API-literate. The bias-variance decomposition,
resampling/cross-validation, the bootstrap, regularisation (ridge/lasso) and tree ensembles are
explained here by the people who invented several of them. Take the Python edition (ISLP, 2023, adds
the `ISLP` pip package) unless you have a reason to want R. Do not confuse it with _The Elements of
Statistical Learning_ (ESL) by Hastie/Tibshirani/Friedman. ESL has the same authors but is the
graduate-level maths version, and a classic beginner trap. Start ISL in your first week and read it
through the middle weeks of this chapter, alongside Ng's courses if you take that track. Chapters
2–6 and 8 (statistical learning, linear regression, classification, resampling, regularisation and
trees) map onto this chapter. The rest can wait.

> **Worth knowing.** A statistics text built on tidy teaching datasets. The availability-time
> checks, deployment-matched splits and serving work in this chapter are yours to add.

### [scikit-learn MOOC — Machine learning in Python with scikit-learn (Inria)](https://inria.github.io/scikit-learn-mooc/)

_scikit-learn community with Inria Learning Lab, Inria Academy and probabl_ &nbsp;·&nbsp; Course
&nbsp;·&nbsp; Free &nbsp;·&nbsp; 35–50 hours

A free, structured route through pipelines, model selection, tuning, linear and tree models, and
evaluation. Use it as an alternative to the book-first route, following its stated environment and
adapting examples to your deployment split. Maintainer authorship helps, but a notebook may not
match the scikit-learn version you install.

> **Worth knowing.** The hosted cohort run is on fun-mooc.fr. The GitHub Pages version is the
> always-open self-study copy.

### [scikit-learn: Common Pitfalls and Recommended Practices](https://scikit-learn.org/stable/common_pitfalls.html)

_scikit-learn core developer team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3
hours

Read it in Week 7 for side-by-side examples of inconsistent preprocessing, leakage and randomness.
Fit preprocessing within training folds, and learn how seeds and estimator state behave in repeated
fits. Pair it with the chapter's availability-time and label-maturity checks. A pipeline cannot
repair a feature that was already extracted from the future.

### [scikit-learn User Guide — Model Selection and Evaluation](https://scikit-learn.org/stable/user_guide.html)

_scikit-learn core developers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10–15
hours

Most beginners use the sklearn docs only for API lookup and never read the prose. The User Guide
repays reading as a real textbook, with the maths and the failure modes written by the people who
implemented them. Read the model-selection/cross-validation chapter (why KFold vs StratifiedKFold vs
GroupKFold vs TimeSeriesSplit, why nested CV exists) and the metrics pages for your target type. The
Common Pitfalls page has its own entry above. Use the estimator pages for lookup when you reach each
model.

> **Worth knowing.** Many examples use small bundled datasets with random or stratified folds. Adapt
> them to your time or group split, and read the documentation version that matches your installed
> scikit-learn.

### [Approaching (Almost) Any Machine Learning Problem](https://github.com/abhishekkrthakur/approachingalmost)

_Abhishek Thakur_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 20–30 hours

The missing 'how a practitioner actually does it' book, free from the author himself. It is
code-first and opinionated about what courses skip: how to structure an ML project's folders, how to
build cross-validation schemes correctly for different problem types (stratified, group,
time-based), choosing an evaluation metric, handling categorical variables and text/image features,
feature selection, and hyperparameter tuning. It is the practical partner to ISL's theory and the
closest thing to an apprenticeship in a careful workflow. Read it once your first baseline exists,
in the middle weeks of this chapter.

> **Worth knowing.** Six years old, so the APIs in its code examples have moved on. The linked repo
> holds the book itself, not runnable code. Still strong on cross-validation discipline and problem
> framing.

### [XGBoost official documentation](https://xgboost.readthedocs.io/en/stable/)

_XGBoost contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6–10 hours

Use this to tune one boosted tree, with a written hypothesis for each change. Read the 'Introduction
to Boosted Trees' tutorial (the objective, and why regularisation enters the split criterion), then
the parameter documentation. Predict each change's likely effect, compare on the same validation
protocol, and record whether the results support your prediction.

> **Worth knowing.** Reference documentation for one library. Parameter names and defaults change
> between releases, so read the version in your lock file. It explains how to configure XGBoost, not
> whether a boosted tree beats your baseline.

### [Interpretable Machine Learning: A Guide for Making Black Box Models Explainable](https://christophm.github.io/interpretable-ml-book/)

_Christoph Molnar_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 12–18 hours

The free standard reference for the half of tabular ML that decides whether your model ships:
permutation feature importance and why it misleads under correlated features, partial dependence
and ICE plots, LIME, and SHAP. Molnar covers the methods behind the chapter's argument that
regulated industries need defensible, explainable decisions, and he is candid about each method's
failure modes. Be ready to explain one real error and an interpretation's limits when presenting
your project. Interview expectations vary by role and employer.

### [StatQuest with Josh Starmer (Statistics Fundamentals, Machine Learning, Neural Networks playlists)](https://www.youtube.com/@statquest/playlists)

_Josh Starmer_ &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10–15 hours

Use it as a lookup index for probability versus likelihood, maximum likelihood, distributions,
Bayes' theorem, entropy, bias/variance, cross-validation and classification metrics. Pair a video
with a small calculation or implementation. Hypothesis tests and p-values need careful assumptions
when you run experiments. Chapter 7 covers them in its own branch.

### [FastAPI — Request validation and testing](https://fastapi.tiangolo.com/tutorial/body/)

_FastAPI maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours for the
selected sections

Use the request-body guide and [TestClient tutorial](https://fastapi.tiangolo.com/tutorial/testing/)
for Week 11. Add FastAPI plus HTTPX/pytest to your uv project, define the prediction input schema,
and test both valid and invalid requests. A valid request must reproduce the saved bundle's
prediction, not merely return HTTP 200. Use the chapter's fresh-process check to connect training
with serving.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [Computational Linear Algebra for Coders](https://github.com/fastai/numerical-linear-algebra)

_Rachel Thomas, PhD_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 25–40 hours

The only linear algebra course built entirely on the top-down approach: 'top down, code first,
application centered.' It gets you to real applications (CT scan reconstruction, topic modelling
with NMF/SVD, background removal from video, PageRank) before digging into the detail underneath.
It is the direct methodological counterpoint to MIT 18.06, and worth doing because it teaches the
numerical side that pure-maths courses skip: floating-point error, conditioning, stability, and why
algorithm choice matters at scale. Notebooks are free on GitHub (fastai/numerical-linear-algebra)
and videos on the fast.ai YouTube channel.

> **Worth knowing.** From 2017. The linear-algebra concepts hold, but the code does not run cleanly
> on modern stacks.

### [CS229 Machine Learning — main lecture notes (publicly downloadable PDF)](https://cs229.stanford.edu/main_notes.pdf)

_Tengyu Ma & Andrew Ng_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40–60 hours

The mathematical version of everything Ng teaches gently on Coursera. It derives least squares from
probabilistic assumptions and covers GLMs and the exponential family, generative vs discriminative
learning, kernels and SVMs, learning theory and the formal bias-variance decomposition. Save it for
a few months in, once you want to understand _why_ rather than _how_.

> **Worth knowing.** Rigorous ML-theory notes (SVMs, GLMs, EM) that assume the linear algebra and
> probability covered earlier in this book. Not a beginner on-ramp.

### [Google Machine Learning Crash Course (refreshed edition)](https://developers.google.com/machine-learning/crash-course/)

_Google's ML education team_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 15–20 hours

Best used as a fast, interactive first week or as a refresher, rather than as your main course. The
refreshed version has four sections: ML models (linear/logistic regression, classification), data
(numerical, categorical, overfitting/datasets), advanced models (neural nets, embeddings, LLMs) and
real-world ML (production, AutoML, fairness). The most valuable and current parts are the 'Data' and
'Real-world ML' sections, since very few beginner courses cover production concerns and fairness. A
new LLM module covers tokens, n-grams, transformers, self-attention, distillation, fine-tuning and
prompting. That makes it a reasonable bridge from classical ML into Chapter 5's language-model
material.

> **Worth knowing.** A short survey by design: use it for orientation, not in place of the
> chapter's split, calibration and threshold work. Check each programming exercise's framework
> against this book's scikit-learn and PyTorch route.

### [Hands-On Machine Learning with Scikit-Learn and PyTorch (2025) + official notebooks](https://github.com/ageron/handson-mlp)

_Aurélien Géron_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 60–90 hours

A practical alternative to ISL, with an end-to-end housing project, pipelines, preprocessing,
classification, trees and dimensionality reduction. The
[publisher record](https://www.oreilly.com/library/view/hands-on-machine-learning/9798341607972/)
dates the first PyTorch edition to October 2025. Its framework matches this roadmap's deep-learning
route. The older TensorFlow/Keras edition is still useful for a team using that framework. Choose
one edition and follow its notebook environment rather than buying both.

> **Worth knowing.** A first edition, so fewer errors have been fixed than in the mature
> handson-ml3.

### [Introduction to Probability for Data Science](https://probability4datascience.com/)

_Stanley H. Chan_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 60–100 hours

Probably the best free, rigorous, ML-oriented probability textbook, and probability is the leg of
the tripod beginners most often neglect. Unlike a classical statistics text, it is written for data
science from page one. It balances theory with Matlab and Python code and ships with free lecture
videos, slides and exercises. A second edition with an interactive eBook arrived in 2026, so it is
actively maintained, unlike many free maths texts. Use it after StatQuest gives you the vocabulary,
when you want the real derivations behind maximum likelihood, the Gaussian and estimation, usually a
few months in.

> **Worth knowing.** A long, rigorous course textbook. Pick the random-variable and estimation
> chapters you need. Reading it end to end does not fit inside this chapter's 80 hours.

### [Khan Academy — Linear Algebra, Multivariable Calculus, and Statistics & Probability](https://www.khanacademy.org/math/statistics-probability)

_Sal Khan_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40–60 hours

Khan Academy's best role in 2026 is filling gaps and drilling, rather than main teaching. Go there
when a 3Blue1Brown video assumed something you do not have, or when you realise you can follow a
concept but not yet do it. Its real advantage over video-only resources is graded practice exercises
with hints and mastery tracking. Use single units that match a gap, rather than whole courses:
vectors and matrices, partial derivatives and the gradient, or conditional probability and random
variables.

> **Worth knowing.** Not ML-specific, and practice coverage varies by course. Check that the unit
> you need has exercises as well as videos, then return to the chapter's example.

### [Machine Learning Specialization (3 courses)](https://www.coursera.org/specializations/machine-learning-introduction)

_Andrew Ng with Eddy Shyu, Aarti Bagul & Geoff Ladwig_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free tier
&nbsp;·&nbsp; 60–90 hours

The 2022 ground-up rebuild of the 2012 course, using Python/NumPy/scikit-learn instead of Octave,
which was the loudest complaint about the original. Its great strength for a beginner is that Ng
builds _intuition_ for cost functions, gradient descent, regularisation, bias/variance and the
diagnostic loop ('should I get more data or more features?') better than anyone else teaching. If
you want a guided course track rather than the book-first route the chapter recommends, start here
in your first week and do all three courses.

> **Worth knowing.** Some exercises use TensorFlow/Keras while this roadmap later uses PyTorch.
> Check current preview, assignment and certificate access before planning around a free tier.

### [Mathematics for Machine Learning (the mml-book) + free PDF](https://mml-book.github.io/)

_Marc Peter Deisenroth, A. Aldo Faisal & Cheng Soon Ong_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 40–80 hours

The standard, most-cited free maths-for-ML text. Cambridge University Press published it (April
2020), and the authors have committed to keeping the PDF permanently free
([direct PDF](https://mml-book.github.io/book/mml-book.pdf), continuously updated for typos). Part I
covers linear algebra, analytic geometry, matrix decompositions, vector calculus, probability &
distributions, and continuous optimisation. Part II then _earns_ that maths by deriving linear
regression, PCA, Gaussian mixture models and SVMs. That is the book's real value, since very little
else shows you the payoff. Companion Jupyter notebooks and Overleaf exercise sets with solutions are
on the same site. Use the Part I chapters for lookup when a calculation needs them, and read the
linear regression and PCA chapters once your own model exists.

> **Worth knowing.** Dense and proof-heavy for a first pass. It covers the mathematics only, not
> tree ensembles, deployment-matched validation or practical model evaluation.

### [Mathematics for Machine Learning and Data Science Specialization](https://www.coursera.org/specializations/mathematics-for-machine-learning-and-data-science)

_Luis Serrano, PhD_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 94 hours

The most current well-made paid option, and a better buy than the Imperial specialisation for most
beginners in 2026. It was refreshed in 2024, and its three courses cover the full tripod. Imperial's
third course is PCA rather than probability/statistics, leaving a large statistics gap. This one is
built around ML use cases, with NumPy labs throughout. Serrano is unusually good at visual-first
explanation without giving up correctness. The stated prerequisites are high-school maths plus basic
Python. Treat it as the 'I want one structured paid course that covers everything and holds me
accountable' option, taken alongside coding rather than before it.

> **Worth knowing.** Check current subscription, preview and graded-assignment access. This is an
> optional paid route alongside coding. The author-hosted maths books are free alternatives.

### [Mathematics for Machine Learning Specialization (Imperial College London)](https://www.coursera.org/specializations/mathematics-machine-learning)

_David Dye, Samuel J. Cooper, A. Freddie Page & Marc Deisenroth_ &nbsp;·&nbsp; Course &nbsp;·&nbsp;
Free tier &nbsp;·&nbsp; 58 hours

A structured linear algebra, multivariable calculus and PCA sequence with Python notebook exercises.
Use it when graded mathematical practice helps you follow through. Probability and statistics need a
separate resource. Check the current assignment environment and access policy. Enrolment counts and
ratings do not predict any one learner's outcome.

> **Worth knowing.** The fundamentals can stay useful despite older notebooks. Check API
> compatibility and current graded-assignment access before committing the full time budget.

### [MIT 18.065 — Matrix Methods in Data Analysis, Signal Processing, and Machine Learning](https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/)

_Prof. Gilbert Strang_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 50–80 hours

If you want Strang, **this** is the Strang course to take for machine learning, and beginners are
rarely told so. 18.065 is his ML-facing sequel: column space, matrix factorisation, orthonormal
columns, eigenvalues/eigenvectors, positive definite and semidefinite matrices, SVD, least squares
and gradient descent, reviewed with applications to probability, statistics and optimisation, plus
lectures on deep learning itself. It skips the first-year engineering material that makes 18.06 slow
for an ML learner. Videos of all lectures are free on OCW, except Lectures 28–29, the unrecorded lab
sessions.

> **Worth knowing.** Use it for the linear algebra, not the deep-learning chapters. Strang has
> retired, and there is no updated OCW offering.

### [MIT 18.06SC Linear Algebra (OCW Scholar edition)](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/)

_Prof. Gilbert Strang_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 120–160 hours

Probably the most famous linear algebra course ever recorded. The OCW Scholar (18.06SC) version is
the right one to link: it is built for independent study, with recitation videos by MIT instructors,
problem sets with solutions and full exams, all free under Creative Commons. Strang's
four-fundamental-subspaces framing is genuinely beautiful. Be clear about the fit, though: 18.06 is
a general engineering-mathematics course, not an ML course. It starts with Gaussian elimination,
LU/PA=LU factorisation and null-space computation. The SVD, arguably the most ML-relevant topic,
arrives near the end.

> **Worth knowing.** The "Fall 2011" label is the OCW Scholar packaging date, not the video date.
> The lectures are SD recordings from 1999. The Java demonstrations in the course materials no
> longer run in current browsers.

### [MLU-Explain — visual, interactive explanations of core ML concepts (Amazon Machine Learning University)](https://mlu-explain.github.io/)

_Jared Wilber, Brent Werness and collaborators_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 4–6 hours

Come here when bias-variance, cross-validation, ROC/AUC or precision-recall will not click from
text. Fourteen scroll-driven essays with charts you drag and change: The Bias Variance Tradeoff,
Cross-Validation, Train/Test/Validation Sets, Precision & Recall, ROC & AUC, Decision Trees, Random
Forest, Linear and Logistic Regression, Neural Networks, Equality of Odds, Reinforcement Learning,
and a two-part Double Descent explainer. Double descent links classical bias-variance to why
massively overparameterised modern models work, a useful bridge to the LLM era. No signup, no
install. It teaches more concepts per hour than anything else in this list.

> **Worth knowing.** From roughly 2021. Good for classical ML intuition, but it covers nothing from
> the post-2022 era.

### [Neural Networks (Deep Learning series, chapters 1–7+)](https://www.3blue1brown.com/topics/neural-networks)

_Grant Sanderson_ &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4–6 hours

Visual intuition for gradient descent, backpropagation and the chain rule, with later lessons on
transformers, attention and cross-entropy. The July 16, 2026 cross-entropy lesson is a real
addition, not a reason to drop older calculus explanations. Pick the lesson that answers your
current question, then compute or code a small example. Watching is not the same as mastery. For
this chapter's calculus minimum, chapters 1–4 (the network, gradient descent and both
backpropagation lessons) are enough. The transformer lessons support Chapter 4.

> **Worth knowing.** Visual intuition without exercises. To learn to implement and debug a training
> loop, use Chapter 4's autograd exercise.

### [Seeing Theory — A Visual Introduction to Probability and Statistics](https://seeing-theory.brown.edu/)

_Daniel Kunin, Jingru Guo, Tyler Dae Devlin & Daniel Xiang_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp;
Free &nbsp;·&nbsp; 3–5 hours

A very fast way to build intuition for distributions, sampling and Bayesian updating. You drag
sliders and watch the distributions move instead of reading formulas. Six chapters: basic
probability, compound probability, probability distributions, frequentist inference, Bayesian
inference and regression analysis. Webby Award winner, hosted by Brown. It works well as a 3-hour
weekend session between StatQuest videos, especially for the central limit theorem, likelihood, and
the prior-to-posterior update behind every Bayesian framing in ML.

> **Worth knowing.** Officially archived by its authors and no longer actively maintained, though
> Brown has committed to keep hosting it. If a browser change breaks the D3.js visualisations,
> nobody will fix them.

### [Statistical Learning with Python (StanfordOnline, edX) — free companion course to ISLP](https://www.edx.org/learn/python/stanford-university-statistical-learning-with-python)

_Trevor Hastie & Robert Tibshirani_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 20–30
hours

The authors' own lecture videos, walking through ISL chapter by chapter with Python labs. It is the
cheapest way to have a Stanford statistics professor explain cross-validation and the bootstrap to
you personally. It also removes the main way self-study of ISL fails: bouncing off the notation and
quitting at chapter 3. An R-lab version is on the same platform if you prefer R. Pair it 1:1 with
your ISL reading rather than treating it as a separate course.

> **Worth knowing.** Check current platform access to lectures, labs and graded material. If course
> access is limited, the authors' free book is a dependable reading route.

### [TabPFN-3.5: Technical Report](https://arxiv.org/abs/2609.17895)

_Benjamin Jäger, Nick Erickson, Léo Grinsztajn, Frank Hutter et al._ &nbsp;·&nbsp; Paper
&nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

A developer-authored September 2026 preprint. Read the benchmark protocol and regime breakdown, not
just the overall ranking. Tuned/ensembled MLPs keep the lead on the full grouped, temporal and large
BeyondArena slices, and the group-ID protocol differs from the original benchmark. If its inference
budget fits, compare one fixed checkpoint against your baseline. A supported maximum row count does
not show acceptable memory or serving latency. Headline family rankings mix hosted Thinking and
released-checkpoint variants, so reproduce the variant you plan to use.

> **Worth knowing.** The [official repository](https://github.com/PriorLabs/TabPFN) separates code
> and checkpoint licences and describes the first-use licence/account flow. Check the selected
> weights before deployment. Pretrained inference still uses your labelled training context.

For a counterexample to treating context priors as harmless, read the
[ICML 2026 DistPFN paper](https://proceedings.mlr.press/v306/lee26aw.html) and its
[released sampling routine](https://github.com/seunghan96/DistPFN/blob/main/src/utils.py). The code
resamples training data after a stratified split and duplicates rare test classes to at least ten
examples. The paper's sections describe the split differently. Pin the code and protocol before
reproducing it. The reported gains concern the older models it tested, not TabPFN-3.5 or
unrestricted business drift.

### [Tabular Foundation Models: A short and opinionated guide](https://tabularfoundationmodels.com/)

_Christoph Molnar_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 5–8 hours

A short, author-hosted guide to pretrained tabular models, their Python usage and tradeoffs. Read it
once your boosted-tree baseline exists. In-context inference uses the labelled training rows you
supply, even without task-specific gradient updates. Optional fine-tuning is a different workflow.
For checkpoint-specific results, limits and licences, use papers and official model cards.

> **Worth knowing.** New in 2026, and the author says openly that he is excited about these models.
> Treat it as a guide to how they work, and let your own validation scheme decide whether they help.

### [The Hundred-Page Machine Learning Book](https://www.themlbook.com/)

_Andriy Burkov_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 8–12 hours

The best _map_ of the territory: ~140 pages covering supervised and unsupervised learning, SVMs,
neural networks, ensembles, gradient descent, clustering and dimensionality reduction, autoencoders
and transfer learning, feature engineering and hyperparameter tuning. Use it for orientation and
revision rather than first learning. Read it in a weekend before you start, then again before
interviews. The read-first-buy-later policy lets you judge it for free before deciding. Its 2019
publication date predates the LLM era, so treat the neural-network chapters as historical context.

> **Worth knowing.** 2019 content sold under a 2019–2025 copyright banner, which makes it look
> fresher than it is. A compact classical-ML reference only. The LLM material is in a separate 2025
> companion volume. Paid on an honour system, not free.

### [The Matrix Calculus You Need For Deep Learning](https://explained.ai/matrix-calculus/)

_Terence Parr & Jeremy Howard_ &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4–8 hours

The standard 'just enough' calculus document, and the answer to 'which part of vector calculus
actually matters?' It sets its own scope: 'We assume no math knowledge beyond what you learned in
calculus 1'. It covers exactly the gap between scalar derivatives and the Jacobians/chain rules that
backprop needs, and ends with the gradient of a real neural network loss. Importantly, the authors
tell you **when** to read it: after you are already familiar with training neural networks, not
before. That one sentence from Jeremy Howard is the strongest first-hand support for the top-down
order in this whole field.

> **Worth knowing.** Undated page, with content frozen at 2018.

### [Why do tree-based models still outperform deep learning on typical tabular data? (NeurIPS 2022 Datasets & Benchmarks)](https://openreview.net/forum?id=Fp7__phQszn)

_Léo Grinsztajn, Edouard Oyallon & Gaël Varoquaux_ &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 2–3 hours

A 2022 controlled comparison that also investigates inductive biases: feature orientation,
uninformative features and irregular targets. Read it for hypotheses about why models differ, then
test those hypotheses on your data. Its tested neural architectures and protocols predate today's
tabular foundation models, so it cannot set a universal 2026 ranking.

## Keep for reference

Not for reading end to end. Useful to have when you need to look something up.

### [Appendix: Mathematics for Deep Learning (Dive into Deep Learning)](https://www.d2l.ai/chapter_appendix-mathematics-for-deep-learning/index.html)

_Brent Werness & Rachel Hu, within Dive into Deep Learning by Aston Zhang, Zachary C. Lipton, Mu Li
& Alexander J. Smola_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 15–25 hours

A reference for geometry, linear algebra, calculus, probability, estimation and information theory.
Choose the section that explains your current calculation or model. The full appendix goes beyond
this chapter's starting prerequisites and is not an extra requirement inside the 80-hour budget.
Eigendecompositions, Hessians and integral calculus in particular can wait until the project needs
them. Use its exercises to check your understanding.

> **Worth knowing.** Author affiliations date from the time of writing.

### [LightGBM documentation (Microsoft) and CatBoost documentation (Yandex)](https://lightgbm.readthedocs.io/en/stable/)

_LightGBM and CatBoost contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp;
4–6 hours

Read after XGBoost to compare the mechanisms and their measured tradeoffs. LightGBM's leaf-wise
growth and histogram binning help training run efficiently. Tune `num_leaves` and minimum leaf size
to control overfitting. [CatBoost's categorical handling](https://catboost.ai/docs/en/) is
convenient when customer/product tables contain many categorical fields. Test quality, training
memory and serving latency on the same deployment-matched split. With default parameters, neither
is always the fastest or the strongest.

### [Probabilistic Machine Learning: An Introduction](https://probml.github.io/pml-book/book1.html)

_Kevin Patrick Murphy_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10–20 hours, as a
reference

A graduate reference that unifies probabilistic foundations and modern ML, with an author-hosted
draft and companion code. Use selected sections once you have linear algebra, calculus and
probability foundations. Check the draft's own revision date rather than trusting a date in a
roadmap as its latest version. Code examples need their documented environment.

> **Worth knowing.** A 1000-page graduate-level probabilistic-ML textbook, not a maths primer. Use
> it as a reference or stretch goal rather than prerequisite reading.

---

## Decisions, forecasts and current research

### [scikit-learn — Probability calibration](https://scikit-learn.org/stable/modules/calibration.html)

_scikit-learn contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Build a reliability plot and calibrate on independent data. Keep calibration separate from ranking,
and evaluate the exact model/calibrator pair you serve. The
[CalibratedClassifierCV API](https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibratedClassifierCV.html)
documents default folds and `FrozenEstimator`. Supply deployment-matched calibration data rather
than inheriting entity/time leakage from random or stratified folds. The
[imbalanced-learn pitfalls](https://imbalanced-learn.org/stable/common_pitfalls.html) show why
resampling belongs inside training folds. Keep deployment prevalence for calibration and evaluation,
or document justified sampling weights.

### [scikit-learn — Decision threshold tuning](https://scikit-learn.org/stable/modules/classification_threshold.html)

_scikit-learn contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1
hour

Keep probability estimation separate from the action rule. Tune the rule on validation data and keep
an untouched final test. Read it for the Week 10 exercise, once a calibrated pipeline exists: the
post-tuning section, the notes on internal cross-validation, and fixing a threshold by hand with
`FixedThresholdClassifier`. Its cost-sensitive learning example shows a business-metric scorer.
`TunedThresholdClassifierCV` uses 5-fold stratified cross-validation by default, which ignores a
time or entity split. Supply a deployment-matched splitter, or an already-fitted model with separate
validation data, as the page describes. It optimises one aggregate score, so capacity limits and
case-varying costs still need the chapter's richer decision rule.

### [Forecasting: Principles and Practice — Forecast accuracy](https://otexts.com/fpp3/accuracy.html)

_Rob J. Hyndman & George Athanasopoulos_ &nbsp;·&nbsp; Author-hosted book &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 1–2 hours for this section

Choose errors in meaningful units, and handle zeros and scale differences on purpose. Use the
surrounding book for seasonal baselines and forecasting depth when the project needs it. The
[time-series cross-validation section](https://otexts.com/fpp3/tscv.html) evaluates rolling origins
and error by forecast horizon. Issue forecasts and update features the same way serving will.

### [scikit-learn — Lagged features for time-series forecasting](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html)

_scikit-learn contributors_ &nbsp;·&nbsp; Worked example &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

Compare random splitting with a time backtest, and build lags without importing future
observations. Adapt the horizon and feature windows to demand. A batch of one-step predictions using
updated observations is a different task from issuing the whole future horizon at one origin.

### [Beyond IID: How General Are Tabular Foundation Models, Really?](https://arxiv.org/abs/2606.30410)

_Lennart Purucker and collaborators_ &nbsp;·&nbsp; Benchmark preprint, June 2026 &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 2–3 hours

BeyondArena tests grouped, temporal, large and wide settings, not only small IID tables. Read the
split construction, tuning budgets and model versions in the
[full paper](https://arxiv.org/html/2606.30410v1). Its original comparisons include TabPFN-2.6 and
TabICLv2. Later checkpoints need a new comparison. Borrow its deployment questions, then set a
feasible and consistent compute budget for your project.

### [TabICLv2: A better, faster, scalable, and open tabular foundation model](https://arxiv.org/abs/2602.11139)

_Jingang Qu, David Holzmüller, Gaël Varoquaux & Marine Le Morvan_ &nbsp;·&nbsp; ICML 2026 paper,
revised September 2026 &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

A classification/regression challenger using pretrained in-context learning. The
[official implementation](https://github.com/soda-inria/tabicl) provides Python estimators, and the
[checkpoint model card](https://huggingface.co/jingang/TabICL) lists BSD-3-Clause terms. Pin the
classifier/regressor checkpoint and measure real quality, context size, memory and latency on your
split. A permissive licence and author-reported benchmark results do not guarantee the best model
for a particular dataset.

### [Chronos-2: From Univariate to Universal Forecasting](https://arxiv.org/abs/2510.15821)

_Abdul Fatir Ansari and collaborators_ &nbsp;·&nbsp; Technical report, 2025; implementation updated
in 2026 &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

Pretrained forecasting with related series, past covariates and known-future covariates. Use the
[official repository](https://github.com/amazon-science/chronos-forecasting) and
[Apache-2.0 checkpoint card](https://huggingface.co/amazon/chronos-2) for supported interfaces and
limits. Compare seasonal-naive, statistical and lagged-tree baselines at identical forecast origins.
Measure interval coverage, runtime and business error. Supplying realised future covariates creates
leakage.

### [TimesFM 3: A zero-shot foundation model for multivariate forecasting](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/)

_Google Research_ &nbsp;·&nbsp; Developer research announcement, August 2026 &nbsp;·&nbsp; Free to
read &nbsp;·&nbsp; 1–2 hours

An optional modern forecast challenger with native multivariate and covariate support. Use the
[official repository](https://github.com/google-research/timesfm) to pin the supported release and
check checkpoint terms. Downloadable TimesFM 3 weights have noncommercial/nonproduction
restrictions. Older checkpoint and hosted-service terms differ. Before you choose it for demand
planning, check vendor benchmark results with a matched local backtest.

### [A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification](https://arxiv.org/abs/2107.07511)

_Anastasios N. Angelopoulos & Stephen Bates_ &nbsp;·&nbsp; Tutorial paper &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 2–3 hours for split conformal

Separate calibration scores can turn predictions into sets or intervals. Learn the exchangeability
assumption and the difference between marginal coverage and coverage for each subgroup or person.
An interval with nominal 90% coverage is not automatically valid under temporal drift. Evaluate
coverage and width together. For dependent forecasts, use a time-series-specific design.

### [TargetEncoder: Cross-fitting and custom CV](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.TargetEncoder.html)

_scikit-learn contributors_ &nbsp;·&nbsp; API documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

`fit_transform` cross-fits training encodings. `fit` followed by `transform` on those rows does not.
Version 1.9 permits custom CV and group routing, as long as each sample appears in exactly one
validation fold. Default random folds do not enforce time or entity isolation. An ordinary
forward-only `TimeSeriesSplit` cannot be dropped in directly. Design past-only encodings or choose
another representation.

For treatment effects, constrained policy evaluation and the business cases, use
[Chapter 9's primary sources](../../09-business-machine-learning/resources/README.md).

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
