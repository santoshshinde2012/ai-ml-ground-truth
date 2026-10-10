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

The single highest-value free text in the whole domain, and the one that makes you _statistically_
literate rather than just API-literate. It is where the bias-variance decomposition,
resampling/cross-validation, the bootstrap, regularisation (ridge/lasso), and tree ensembles are
explained by the people who invented several of them. Take the Python edition (ISLP, 2023, adds the
`ISLP` pip package) unless you have a reason to want R. Do not confuse it with _The Elements of
Statistical Learning_ (ESL) by Hastie/Tibshirani/Friedman — same authors, but ESL is the
graduate-level maths version and is a classic beginner trap. Start ISL in your first week and read
it through the middle weeks of this chapter — alongside Ng's courses, if you take that track.

### [scikit-learn MOOC — Machine learning in Python with scikit-learn (Inria)](https://inria.github.io/scikit-learn-mooc/)

_scikit-learn community with Inria Learning Lab, Inria Academy and probabl_ &nbsp;·&nbsp; Course
&nbsp;·&nbsp; Free &nbsp;·&nbsp; 35–50 hours

A free structured route through pipelines, model selection, tuning, linear and tree models, and
evaluation. Use it as an alternative to the book-first route, following its specified environment
and adapting examples to your deployment split. Maintainer authorship is useful, but does not
guarantee every notebook matches whichever scikit-learn version you install.

> **Worth knowing.** The hosted cohort run is on fun-mooc.fr; the GitHub Pages version is the
> always-open self-study copy.

### [scikit-learn: Common Pitfalls and Recommended Practices](https://scikit-learn.org/stable/common_pitfalls.html)

_scikit-learn core developer team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3
hours

Read in Week 7 for side-by-side examples of inconsistent preprocessing, leakage and randomness. Fit
preprocessing within training folds, and understand how seeds and estimator state behave in repeated
fits. Combine this with the chapter's availability-time and label-maturity checks: a pipeline cannot
repair a feature that was already extracted from the future.

### [scikit-learn User Guide — Model Selection, Evaluation and Common Pitfalls](https://scikit-learn.org/stable/user_guide.html)

_scikit-learn core developers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10–15
hours

Almost every beginner treats sklearn docs as API lookup and never reads the prose. That is a
mistake: the User Guide is a genuine textbook with the math and the failure modes written by the
people who implemented them. Two pages are non-negotiable — the model-selection/cross-validation
chapter (why KFold vs StratifiedKFold vs GroupKFold vs TimeSeriesSplit, why nested CV exists) and
'Common Pitfalls and Recommended Practices', which is the clearest free write-up of data leakage,
inconsistent preprocessing, and controlling randomness.

### [Approaching (Almost) Any Machine Learning Problem](https://github.com/abhishekkrthakur/approachingalmost)

_Abhishek Thakur_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 20–30 hours

The missing 'how a practitioner actually does it' book, and free from the author himself. It is
code-first and opinionated about the things courses skip: how to structure an ML project's folders,
how to build cross-validation schemes correctly for different problem types (stratified, group,
time-based), evaluation metric selection, approaching categorical variables and text/image features,
feature selection, and hyperparameter tuning. This is the practical complement to ISL's theory and
the closest thing to an apprenticeship in workflow discipline. Read it once your first baseline
exists, in the middle weeks of this chapter.

> **Worth knowing.** A six-year-old book whose code examples' APIs have moved on, and the linked
> repo hosts the book itself rather than runnable code. Still strong on cross-validation discipline
> and problem framing.

### [XGBoost official documentation](https://xgboost.readthedocs.io/en/stable/)

_XGBoost contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6–10 hours

You cannot claim tabular ML competence without being able to tune a boosted tree deliberately rather
than by superstition. Read the 'Introduction to Boosted Trees' tutorial (Chen's own derivation of
the objective and why regularisation is baked into the split criterion) and then the parameter
documentation until you can predict each parameter's effect on bias and variance before you change
it.

### [Interpretable Machine Learning: A Guide for Making Black Box Models Explainable](https://christophm.github.io/interpretable-ml-book/)

_Christoph Molnar_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 12–18 hours

The free canonical reference for the half of tabular ML that decides whether your model actually
ships: permutation feature importance and why it misleads under correlated features, partial
dependence and ICE plots, LIME, and SHAP. Molnar covers the methods behind the chapter's argument
that regulated industries need defensible, explainable decisions — and he is honest about each
method's failure modes. It is also the most common follow-up question after 'which model did you
pick?' in interviews.

### [StatQuest with Josh Starmer (Statistics Fundamentals, Machine Learning, Neural Networks playlists)](https://www.youtube.com/@statquest/playlists)

_Josh Starmer_ &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10–15 hours

Use as a lookup index for probability versus likelihood, maximum likelihood, distributions, Bayes'
theorem, entropy, bias/variance, cross-validation and classification metrics. Pair a video with a
small calculation or implementation. Hypothesis tests and p-values need careful assumptions when you
run experiments; Chapter 7 covers that branch rather than asking you to ignore them.

### [FastAPI — Request validation and testing](https://fastapi.tiangolo.com/tutorial/body/)

_FastAPI maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours for the
selected sections

Use the request-body guide and [TestClient tutorial](https://fastapi.tiangolo.com/tutorial/testing/)
for Week 11. Add FastAPI plus HTTPX/pytest to your uv project, define the prediction input schema
and test both valid and invalid requests. A valid request must reproduce the saved bundle's
prediction, not merely return HTTP 200. Use the chapter's fresh-process check to connect training
with serving.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [Computational Linear Algebra for Coders](https://github.com/fastai/numerical-linear-algebra)

_Rachel Thomas, PhD_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 25–40 hours

The only linear algebra course built entirely on the top-down philosophy — 'top down, code first,
application centered,' getting you to real applications (CT scan reconstruction, topic modelling
with NMF/SVD, background removal from video, PageRank) before digging into underlying detail. It is
the direct methodological counterpoint to MIT 18.06 and is worth doing precisely because it teaches
the numerical side that pure-math courses skip: floating-point error, conditioning, stability, why
algorithm choice matters at scale. Notebooks are free on GitHub (fastai/numerical-linear-algebra)
and videos on the fast.ai YouTube channel.

> **Worth knowing.** 2017 vintage: the linear-algebra concepts hold, but the code does not run
> cleanly on modern stacks.

### [CS229 Machine Learning — main lecture notes (publicly downloadable PDF)](https://cs229.stanford.edu/main_notes.pdf)

_Tengyu Ma & Andrew Ng_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40–60 hours

This is the mathematical version of everything Ng teaches gently on Coursera — the derivations of
least squares from probabilistic assumptions, GLMs and the exponential family, generative vs
discriminative learning, kernels and SVMs, learning theory and the formal bias-variance
decomposition. It is not a first course; it is the course you come back to a few months in, once you
want to understand _why_ rather than _how_.

> **Worth knowing.** Rigorous ML-theory notes (SVMs, GLMs, EM), not a beginner on-ramp — they assume
> the linear algebra and probability covered earlier in this book.

### [Google Machine Learning Crash Course (refreshed edition)](https://developers.google.com/machine-learning/crash-course/)

_Google's ML education team_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 15–20 hours

Best used as a fast, interactive first week or as a refresher — not as your main course. The
refreshed version restructured into four sections: ML models (linear/logistic regression,
classification), data (numerical, categorical, overfitting/datasets), advanced models (neural nets,
embeddings, LLMs), and real-world ML (production, AutoML, fairness). The genuinely valuable and
modern parts are the 'Data' section and the 'Real-world ML' section — production concerns and
fairness are things almost no beginner course covers — plus a new LLM module covering tokens,
n-grams, transformers, self-attention, distillation, fine-tuning and prompting, which is why this is
now a reasonable bridge from classical ML into Chapter 5's language-model material.

### [Hands-On Machine Learning with Scikit-Learn and PyTorch (2025) + official notebooks](https://github.com/ageron/handson-mlp)

_Aurélien Géron_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 60–90 hours

A practical alternative to ISL with an end-to-end housing project, pipelines, preprocessing,
classification, trees and dimensionality reduction. The
[publisher record](https://www.oreilly.com/library/view/hands-on-machine-learning/9798341607972/)
dates the first PyTorch edition to October 2025. Its framework matches this roadmap's deep-learning
route. The older TensorFlow/Keras edition remains useful for a team using that framework; choose one
edition and follow its notebook environment rather than buying both.

> **Worth knowing.** A first edition, so it has had far less errata shakeout than the mature
> handson-ml3.

### [Introduction to Probability for Data Science](https://probability4datascience.com/)

_Stanley H. Chan_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 60–100 hours

The best free, rigorous, genuinely ML-oriented probability textbook — and probability is the leg of
the tripod beginners most reliably under-serve. Unlike a classical stats text it is written for data
science from page one, balances theory with Matlab AND Python code, and ships with free lecture
videos, slides, and exercises; a second edition with an interactive eBook landed in 2026, so it is
actively maintained (many free math texts are not). Correct placement: after StatQuest gives you the
vocabulary, use this when you want the actual derivations behind maximum likelihood, the Gaussian,
and estimation — typically a few months in.

### [Khan Academy — Linear Algebra, Multivariable Calculus, and Statistics & Probability](https://www.khanacademy.org/math/statistics-probability)

_Sal Khan_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40–60 hours

The right role for Khan Academy in 2026 is remediation and drill, not primary instruction — it is
where you go when a 3Blue1Brown video assumed something you don't have, or when you realise you can
watch a concept but not execute it. Its genuine advantage over every video-only resource is graded
practice exercises with hints and mastery tracking, which is exactly what visual-intuition resources
lack.

### [Machine Learning Specialization (3 courses)](https://www.coursera.org/specializations/machine-learning-introduction)

_Andrew Ng with Eddy Shyu, Aarti Bagul & Geoff Ladwig_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free tier
&nbsp;·&nbsp; 60–90 hours

This is the 2022 ground-up rebuild of the 2012 course — Python/NumPy/scikit-learn instead of Octave,
which was the single loudest complaint about the original. It beats every other on-ramp on one axis
that matters enormously for a beginner: Ng builds _intuition_ for cost functions, gradient descent,
regularisation, bias/variance and the diagnostic loop ('should I get more data or more features?')
better than anyone else teaching. If you want a guided course track rather than the book-first route
the chapter recommends, start here in your first week and do all three courses.

> **Worth knowing.** Some exercises use TensorFlow/Keras while this roadmap later uses PyTorch.
> Check current preview, assignment and certificate access before planning around a free tier.

### [Mathematics for Machine Learning (the mml-book) + free PDF](https://mml-book.github.io/)

_Marc Peter Deisenroth, A. Aldo Faisal & Cheng Soon Ong_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 40–80 hours

The canonical, most-cited free maths-for-ML text, published by Cambridge University Press
(April 2020) with the authors committing to keep the PDF permanently free
([direct PDF](https://mml-book.github.io/book/mml-book.pdf), continuously updated for typos). Part I
covers linear algebra, analytic geometry, matrix decompositions, vector calculus, probability &
distributions, and continuous optimisation; Part II then _earns_ that math by deriving linear
regression, PCA, Gaussian mixture models and SVMs — which is the book's real value, since almost
nothing else shows you the payoff. Companion Jupyter notebooks and Overleaf exercise sets with
solutions are on the same site.

### [Mathematics for Machine Learning and Data Science Specialization](https://www.coursera.org/specializations/mathematics-for-machine-learning-and-data-science)

_Luis Serrano, PhD_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 94 hours

The most current well-produced paid alternative, and the better buy than the Imperial specialisation
for most 2026 beginners: it was refreshed in 2024, its three courses cover the full tripod
(Imperial's third course is PCA rather than probability/statistics, leaving a gaping stats hole),
and it is explicitly built around ML use cases with NumPy labs throughout. Serrano is unusually good
at the visual-first explanation style without sacrificing correctness. Prereqs are stated as
high-school math plus basic Python. Place it as the 'I want one structured paid course that covers
everything and holds me accountable' option, taken alongside coding — not before it.

> **Worth knowing.** Check current subscription, preview and graded-assignment access. This is an
> optional paid route alongside coding; the author-hosted maths books provide free alternatives.

### [Mathematics for Machine Learning Specialization (Imperial College London)](https://www.coursera.org/specializations/mathematics-machine-learning)

_David Dye, Samuel J. Cooper, A. Freddie Page & Marc Deisenroth_ &nbsp;·&nbsp; Course &nbsp;·&nbsp;
Free tier &nbsp;·&nbsp; 58 hours

A structured linear algebra, multivariable calculus and PCA sequence with Python notebook exercises.
Use it when graded mathematical practice helps you follow through. Probability and statistics need a
separate resource. Check the current assignment environment and access policy; enrolment counts and
ratings are not evidence of a particular learner's outcome.

> **Worth knowing.** The fundamentals can remain useful despite older notebooks; check API
> compatibility and current graded-assignment access before committing the full time budget.

### [MIT 18.065 — Matrix Methods in Data Analysis, Signal Processing, and Machine Learning](https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/)

_Prof. Gilbert Strang_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 50–80 hours

If you want Strang, **this** is the Strang course to take for machine learning, and almost nobody
tells beginners that. 18.065 is his ML-facing sequel: column space, matrix factorisation,
orthonormal columns, eigenvalues/eigenvectors, positive definite and semidefinite matrices, SVD,
least squares, and gradient descent — reviewed with applications to probability, statistics and
optimisation, plus lectures on deep learning itself. It skips the freshman-engineering material that
makes 18.06 slow for an ML learner. Videos of all lectures are free on OCW (except Lectures 28–29,
unrecorded lab sessions).

> **Worth knowing.** Use it for the linear algebra, not the deep-learning chapters. Strang has
> retired and there is no updated OCW offering.

### [MIT 18.06SC Linear Algebra (OCW Scholar edition)](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/)

_Prof. Gilbert Strang_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 120–160 hours

The most famous linear algebra course ever recorded, and the OCW Scholar (18.06SC) version is the
right one to link — it is built for independent study with recitation videos by MIT instructors,
problem sets with solutions, and full exams, all free under Creative Commons. Strang's
four-fundamental-subspaces framing is genuinely beautiful. But be clear-eyed about the fit: 18.06 is
a general engineering-mathematics course, not an ML course. It front-loads Gaussian elimination,
LU/PA=LU factorisation, and null-space computation, and the SVD — arguably the single most
ML-relevant topic — arrives near the end.

> **Worth knowing.** The "Fall 2011" label is the OCW Scholar packaging date, not the video date —
> the lectures are 1999-vintage SD. The Java demonstrations in the course materials no longer run in
> current browsers.

### [MLU-Explain — visual, interactive explanations of core ML concepts (Amazon Machine Learning University)](https://mlu-explain.github.io/)

_Jared Wilber, Brent Werness and collaborators_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 4–6 hours

When bias-variance, cross-validation, ROC/AUC or precision-recall refuse to click from text, come
here. Fourteen scroll-driven essays with charts you drag and manipulate: The Bias Variance Tradeoff,
Cross-Validation, Train/Test/Validation Sets, Precision & Recall, ROC & AUC, Decision Trees, Random
Forest, Linear and Logistic Regression, Neural Networks, Equality of Odds, Reinforcement Learning,
and a two-part Double Descent explainer (which is the concept that connects classical bias-variance
to why massively overparameterised modern models work — a genuinely useful bridge to the LLM era).
No signup, no install. Highest concept-per-hour ratio of anything in this list.

> **Worth knowing.** Roughly 2021 vintage: good for classical ML intuition, but it covers nothing
> from the post-2022 era.

### [Neural Networks (Deep Learning series, chapters 1–7+)](https://www.3blue1brown.com/topics/neural-networks)

_Grant Sanderson_ &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4–6 hours

Visual intuition for gradient descent, backpropagation and the chain rule, with later lessons on
transformers, attention and cross-entropy. The July 16, 2026 cross-entropy lesson is a real
addition, rather than a reason to discard older calculus explanations. Pick the lesson answering
your current question, then compute or code a small example; passive familiarity is not a mastery
check.

### [Seeing Theory — A Visual Introduction to Probability and Statistics](https://seeing-theory.brown.edu/)

_Daniel Kunin, Jingru Guo, Tyler Dae Devlin & Daniel Xiang_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp;
Free &nbsp;·&nbsp; 3–5 hours

The fastest possible way to get intuition for distributions, sampling, and Bayesian updating,
because you drag sliders and watch the distributions move rather than reading formulas. Six
chapters: basic probability, compound probability, probability distributions, frequentist inference,
Bayesian inference, and regression analysis. Webby Award winner, hosted by Brown. Perfect as a
3-hour weekend session slotted between StatQuest videos, especially for grasping the central limit
theorem, likelihood, and the prior-to-posterior update that underpins every Bayesian framing in ML.
Note: the site is no longer actively maintained, though Brown has committed to continue hosting it.

> **Worth knowing.** Officially archived by its authors — if a browser change breaks the D3.js
> visualisations, nobody will fix them.

### [Statistical Learning with Python (StanfordOnline, edX) — free companion course to ISLP](https://www.edx.org/learn/python/stanford-university-statistical-learning-with-python)

_Trevor Hastie & Robert Tibshirani_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 20–30
hours

The authors' own lecture videos walking through ISL chapter by chapter, with Python labs. This is
the cheapest possible way to get a Stanford statistics professor to explain cross-validation and the
bootstrap to you personally, and it removes the main failure mode of self-studying ISL (bouncing off
the notation and quitting at chapter 3). An R-lab version exists at the same platform if you prefer
R. Pair it 1:1 with your ISL reading rather than treating it as a separate course.

> **Worth knowing.** Check current platform access to lectures, labs and graded material. Use the
> author's free book as a dependable reading route if course access is limited.

### [TabPFN-3.5: Technical Report](https://arxiv.org/abs/2609.17895)

_Benjamin Jäger, Nick Erickson, Léo Grinsztajn, Frank Hutter et al._ &nbsp;·&nbsp; Paper
&nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

September 2026 developer-authored preprint. Read the benchmark protocol and regime breakdown, not
just its overall ranking: tuned/ensembled MLPs retain the lead on full grouped, temporal and large
BeyondArena slices, and the group-ID protocol differs from the original benchmark. Compare one fixed
checkpoint against your baseline if its inference budget fits. A supported maximum row count does
not establish acceptable memory or serving latency. Headline family rankings mix hosted Thinking and
released-checkpoint variants; reproduce the variant you intend to use.

> **Worth knowing.** The [official repository](https://github.com/PriorLabs/TabPFN) separates code
> and checkpoint licences and describes the first-use licence/account flow. Check the selected
> weights before deployment; pretrained inference still uses your labelled training context.

For a counterexample to treating context priors as harmless, read the
[ICML 2026 DistPFN paper](https://proceedings.mlr.press/v306/lee26aw.html) and its
[released sampling routine](https://github.com/seunghan96/DistPFN/blob/main/src/utils.py). The
implementation resamples training after a stratified split and duplicates rare test classes to at
least ten examples; the paper's sections differ in their split wording. Pin the code/protocol before
reproducing it. Reported gains concern older tested models, not TabPFN-3.5 or unrestricted business
drift.

### [Tabular Foundation Models: A short and opinionated guide](https://tabularfoundationmodels.com/)

_Christoph Molnar_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 5–8 hours

A short author-hosted guide to pretrained tabular models, Python usage and tradeoffs. Read after
your boosted-tree baseline exists. In-context inference uses supplied labelled training rows, even
when there are no task-specific gradient updates; optional fine-tuning is a different workflow. Use
papers and official model cards for checkpoint-specific results, limits and licences.

> **Worth knowing.** New in 2026, and the author says openly that he is excited about these models.
> Treat it as a guide to how they work, and let your own validation scheme decide whether they help.

### [The Hundred-Page Machine Learning Book](https://www.themlbook.com/)

_Andriy Burkov_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 8–12 hours

The best _map_ of the territory: ~140 pages covering supervised and unsupervised learning, SVMs,
neural networks, ensembles, gradient descent, clustering and dimensionality reduction, autoencoders
and transfer learning, feature engineering and hyperparameter tuning. Its job is orientation and
revision, not first learning — read it in a weekend before you start, then again before interviews.
The read-first-buy-later policy means you can evaluate it for free before deciding. Note the 2019
publication date: it predates the LLM era, so treat the neural-network chapters as historical
context.

> **Worth knowing.** 2019 content sold under a 2019–2025 copyright banner, which reads fresher than
> it is. A compact classical-ML reference only — the LLM material lives in a separate 2025 companion
> volume. Honour-system paid, not free.

### [The Matrix Calculus You Need For Deep Learning](https://explained.ai/matrix-calculus/)

_Terence Parr & Jeremy Howard_ &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4–8 hours

The definitive 'just enough' calculus document, and the answer to 'what part of vector calculus is
actually load-bearing.' It explicitly scopes itself — 'We assume no math knowledge beyond what you
learned in calculus 1' — and covers exactly the gap between scalar derivatives and the
Jacobians/chain rules that backprop needs, ending with the gradient of an actual neural network
loss. Critically, the authors themselves tell you **when** to read it: after you're already familiar
with training neural networks, not before. That single sentence from Jeremy Howard is the strongest
primary-source evidence for the top-down ordering in this whole domain.

> **Worth knowing.** Undated page with content frozen at 2018.

### [Why do tree-based models still outperform deep learning on typical tabular data? (NeurIPS 2022 Datasets & Benchmarks)](https://openreview.net/forum?id=Fp7__phQszn)

_Léo Grinsztajn, Edouard Oyallon & Gaël Varoquaux_ &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 2–3 hours

A 2022 controlled comparison and investigation of inductive biases: feature orientation,
uninformative features and irregular targets. Read for hypotheses about why models differ, then test
those hypotheses on your data. Its tested neural architectures and protocols predate today's tabular
foundation models; it cannot establish a universal 2026 ranking.

## Keep for reference

Not for reading end to end. Useful to have when you need to look something up.

### [Appendix: Mathematics for Deep Learning (Dive into Deep Learning)](https://www.d2l.ai/chapter_appendix-mathematics-for-deep-learning/index.html)

_Brent Werness & Rachel Hu, within Dive into Deep Learning by Aston Zhang, Zachary C. Lipton, Mu Li
& Alexander J. Smola_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 15–25 hours

A reference for geometry, linear algebra, calculus, probability, estimation and information theory.
Choose the section that explains your current calculation or model; the full appendix goes beyond
this chapter's starting prerequisites. In particular, eigendecompositions, Hessians and integral
calculus can wait until the project needs them. Use its exercises to check understanding, without
turning the complete appendix into an additional requirement inside the 80-hour budget.

> **Worth knowing.** Author affiliations are as of writing rather than current.

### [LightGBM documentation (Microsoft) and CatBoost documentation (Yandex)](https://lightgbm.readthedocs.io/en/stable/)

_LightGBM and CatBoost contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp;
4–6 hours

Read after XGBoost to compare the mechanisms and their measured tradeoffs. LightGBM's leaf-wise
growth and histogram binning are useful for efficient training; tune `num_leaves` and minimum leaf
size to control overfitting. [CatBoost's categorical handling](https://catboost.ai/docs/en/) is
convenient when customer/product tables contain many categorical fields. Test quality, training
memory and serving latency on the same deployment-matched split. Neither is always fastest or
strongest with default parameters.

### [Probabilistic Machine Learning: An Introduction](https://probml.github.io/pml-book/book1.html)

_Kevin Patrick Murphy_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10–20 hours, as a
reference

A graduate reference unifying probabilistic foundations and modern ML, with an author-hosted draft
and companion code. Use selected sections after you have linear algebra, calculus and probability
foundations. Check the draft's own revision date instead of treating a date in a roadmap as its
latest version; code examples need their documented environment.

> **Worth knowing.** A 1000-page graduate-level probabilistic-ML textbook, not a maths primer — use
> it as a reference or stretch goal rather than prerequisite reading.

---

## Decisions, forecasts and current research

### [scikit-learn — Probability calibration](https://scikit-learn.org/stable/modules/calibration.html)

_scikit-learn contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Build a reliability plot and calibrate on independent data. Keep calibration separate from ranking
and evaluate the exact model/calibrator pair you serve. The
[CalibratedClassifierCV API](https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibratedClassifierCV.html)
documents default folds and `FrozenEstimator`; supply deployment-matched calibration data rather
than inheriting random or stratified entity/time leakage. The
[imbalanced-learn pitfalls](https://imbalanced-learn.org/stable/common_pitfalls.html) demonstrate
why resampling belongs inside training folds. Preserve deployment prevalence for calibration and
evaluation, or document justified sampling weights.

### [scikit-learn — Decision threshold tuning](https://scikit-learn.org/stable/modules/classification_threshold.html)

_scikit-learn contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1
hour

Separate probability estimation from an action rule, tune the rule on validation data and preserve
an untouched final test.

### [Forecasting: Principles and Practice — Forecast accuracy](https://otexts.com/fpp3/accuracy.html)

_Rob J. Hyndman & George Athanasopoulos_ &nbsp;·&nbsp; Author-hosted book &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 1–2 hours for this section

Choose errors in meaningful units and handle zeros and scale differences deliberately. Use the
surrounding book for seasonal baselines and forecasting depth when the project needs it. The
[time-series cross-validation section](https://otexts.com/fpp3/tscv.html) evaluates rolling origins
and error by forecast horizon; use the same forecast issuance and feature-update policy as serving.

### [scikit-learn — Lagged features for time-series forecasting](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html)

_scikit-learn contributors_ &nbsp;·&nbsp; Worked example &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

Compare random splitting with a time backtest and build lags without importing future observations.
Adapt the horizon and feature windows to demand. A batch of one-step predictions using updated
observations is a different task from issuing the whole future horizon at one origin.

### [Beyond IID: How General Are Tabular Foundation Models, Really?](https://arxiv.org/abs/2606.30410)

_Lennart Purucker and collaborators_ &nbsp;·&nbsp; Benchmark preprint, June 2026 &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 2–3 hours

BeyondArena tests grouped, temporal, large and wide settings rather than only small IID tables. Read
split construction, tuning budgets and model versions in the
[full paper](https://arxiv.org/html/2606.30410v1). Its original comparisons include TabPFN-2.6 and
TabICLv2; later checkpoints need a new comparison. Borrow its deployment questions, then specify a
feasible and consistent compute budget for your project.

### [TabICLv2: A better, faster, scalable, and open tabular foundation model](https://arxiv.org/abs/2602.11139)

_Jingang Qu, David Holzmüller, Gaël Varoquaux & Marine Le Morvan_ &nbsp;·&nbsp; ICML 2026 paper,
revised September 2026 &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

A classification/regression challenger using pretrained in-context learning. The
[official implementation](https://github.com/soda-inria/tabicl) provides Python estimators; the
[checkpoint model card](https://huggingface.co/jingang/TabICL) lists BSD-3-Clause terms. Pin the
classifier/regressor checkpoint and evaluate actual quality, context size, memory and latency on
your split. Permissive availability and author-reported benchmark performance do not guarantee the
best operating model for a particular dataset.

### [Chronos-2: From Univariate to Universal Forecasting](https://arxiv.org/abs/2510.15821)

_Abdul Fatir Ansari and collaborators_ &nbsp;·&nbsp; Technical report, 2025; implementation updated
in 2026 &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

Pretrained forecasting with related series, past covariates and known-future covariates. Use the
[official repository](https://github.com/amazon-science/chronos-forecasting) and
[Apache-2.0 checkpoint card](https://huggingface.co/amazon/chronos-2) for supported interfaces and
limits. Compare seasonal-naive, statistical and lagged-tree baselines at identical forecast origins.
Measure interval coverage, runtime and business error; supplying realised future covariates creates
leakage.

### [TimesFM 3: A zero-shot foundation model for multivariate forecasting](https://research.google/blog/timesfm-3-a-zero-shot-foundation-model-for-multivariate-forecasting/)

_Google Research_ &nbsp;·&nbsp; Developer research announcement, August 2026 &nbsp;·&nbsp; Free to
read &nbsp;·&nbsp; 1–2 hours

An optional modern forecast challenger with native multivariate and covariate support. Use the
[official repository](https://github.com/google-research/timesfm) to pin the supported release and
check checkpoint terms. Downloadable TimesFM 3 weights have noncommercial/nonproduction
restrictions; older checkpoint and hosted-service terms differ. Vendor benchmark results need a
matched local backtest before choosing it for demand planning.

### [A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification](https://arxiv.org/abs/2107.07511)

_Anastasios N. Angelopoulos & Stephen Bates_ &nbsp;·&nbsp; Tutorial paper &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 2–3 hours for split conformal

Separate calibration scores can turn predictions into sets or intervals. Learn the exchangeability
assumption and the distinction between marginal coverage and coverage for each subgroup or person.
An interval with nominal 90% coverage is not automatically valid under temporal drift. Evaluate
coverage and width together; use a time-series-specific design for dependent forecasts.

### [TargetEncoder: Cross-fitting and custom CV](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.TargetEncoder.html)

_scikit-learn contributors_ &nbsp;·&nbsp; API documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

`fit_transform` cross-fits training encodings; `fit` followed by `transform` on those rows does not.
Version 1.9 permits custom CV and group routing, with each sample required to appear in exactly one
validation fold. Default random folds do not enforce time or entity isolation. Ordinary forward-only
`TimeSeriesSplit` cannot be substituted directly; design past-only encodings or choose another
representation.

For treatment effects, constrained policy evaluation and the business cases, use
[Chapter 9's primary sources](../../09-business-machine-learning/resources/README.md).

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
