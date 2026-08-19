# Resources — Chapter 3: Core machine learning

Everything referenced in [the chapter](../README.md), grouped by how central it is, with a short
note on what each one is for.

Prices and free tiers change often, so check a resource's own page before you plan around one.

---

## Start here

The resources on the main path for this chapter. If you only do a few things, do these.

### [An Introduction to Statistical Learning (ISLP — Python edition, 2023; ISLR 2nd ed. — R, 2021, corrected June 2023)](https://www.statlearning.com/)

*Gareth James, Daniela Witten, Trevor Hastie & Robert Tibshirani, with Jonathan Taylor on the Python edition* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 60-90 hours

The single highest-value free text in the whole domain, and the one that makes you *statistically* literate rather than just API-literate. It is where the bias-variance decomposition, resampling/cross-validation, the bootstrap, regularisation (ridge/lasso), and tree ensembles are explained by the people who invented several of them. Take the Python edition (ISLP, 2023, adds the `ISLP` pip package) unless you have a reason to want R. Do NOT confuse it with *The Elements of Statistical Learning* (ESL) by Hastie/Tibshirani/Friedman — same authors, but ESL is the graduate-level maths version and is a classic beginner trap. Read ISL after or alongside Ng, through the middle weeks of this chapter.

### [Approaching (Almost) Any Machine Learning Problem](https://github.com/abhishekkrthakur/approachingalmost)

*Abhishek Thakur* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 20-30 hours

The missing 'how a practitioner actually does it' book, and free from the author himself. It is code-first and opinionated about the things courses skip: how to structure an ML project's folders, how to build cross-validation schemes correctly for different problem types (stratified, group, time-based), evaluation metric selection, approaching categorical variables and text/image features, feature selection, and hyperparameter tuning. This is the practical complement to ISL's theory and the closest thing to an apprenticeship in workflow discipline. Read it after Kaggle Learn's Feature Engineering course.

> **Worth knowing.** A six-year-old book whose code examples' APIs have moved on, and the linked repo hosts the book itself rather than runnable code. Still strong on cross-validation discipline and problem framing.

### [Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)

*Grant Sanderson* &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 8-12 hours

The highest-leverage few hours in this chapter, and the place to start. 16 chapters, ~3 hours of video (8-12 with pauses and notes), and it gives you the one thing most linear algebra courses never do: matrices as geometric transformations of space rather than grids of numbers to row-reduce. After chapter 4 ('Matrix multiplication as composition') the sentence 'a neural network layer is a linear map followed by a nonlinearity' stops being jargon.

### [Hands-On Machine Learning with Scikit-Learn and PyTorch (O'Reilly, published 2 December 2025) + official notebook repo](https://github.com/ageron/handson-mlp)

*Aurélien Géron* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 60-90 hours

This is your *doing* book, the counterweight to ISL's *understanding*. Chapters 1-9 are the best practical treatment anywhere of the end-to-end workflow: the end-to-end housing project, stratified splits, scikit-learn Pipelines and ColumnTransformer, feature scaling and engineering, classification metrics and the precision/recall tradeoff, decision trees, ensembles/boosting, dimensionality reduction and clustering. Note: the previous 3rd edition (*Scikit-Learn, Keras & TensorFlow*, 2022, repo `ageron/handson-ml3`) has been superseded — the new edition swaps TensorFlow/Keras for PyTorch and the Hugging Face ecosystem, ~875 pages, 19 notebooks + 5 appendices. Buy the PyTorch edition.

> **Worth knowing.** A first edition, so it has had far less errata shakeout than the mature handson-ml3.

### [Interpretable Machine Learning: A Guide for Making Black Box Models Explainable](https://christophm.github.io/interpretable-ml-book/)

*Christoph Molnar* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 12-18 hours

The free canonical reference for the half of tabular ML that decides whether your model actually ships: permutation feature importance and why it lies under correlated features, partial dependence and ICE plots, LIME, and SHAP. Molnar covers the methods behind the chapter's argument that regulated industries need defensible, explainable decisions — and he is honest about each method's failure modes. It is also the most common follow-up question after 'which model did you pick?' in interviews.

### [Machine Learning Specialization (3 courses)](https://www.coursera.org/specializations/machine-learning-introduction)

*Andrew Ng with Eddy Shyu, Aarti Bagul & Geoff Ladwig* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 60-90 hours

This is the 2022 ground-up rebuild of the 2012 course — Python/NumPy/scikit-learn instead of Octave, which was the single loudest complaint about the original. It beats every other on-ramp on one axis that matters enormously for a beginner: Ng builds *intuition* for cost functions, gradient descent, regularisation, bias/variance and the diagnostic loop ('should I get more data or more features?') better than anyone else teaching. Start here in your first week of this chapter and do all three courses.

> **Worth knowing.** Teaches TensorFlow/Keras while the rest of the deep-learning path is PyTorch, the dominant research and industry framework — a real friction cost. Paid, with limited audit access.

### [Neural Networks (Deep Learning series, chapters 1-7+)](https://www.3blue1brown.com/topics/neural-networks)

*Grant Sanderson* &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-6 hours

The best free explanation on the internet of the two ideas that ARE the math of deep learning: gradient descent (ch. 2-3) and backpropagation calculus (ch. 5, which walks the chain rule through ∂C/∂w explicitly). Crucially, this series is actively maintained and now current for the LLM era — it extends through 'Transformers, the tech behind LLMs' (ch. 5-6 in the newer numbering), 'Attention in transformers, step-by-step', 'How might LLMs store facts', and a July 2026 lesson on cross-entropy ('Compression is Intelligence Part 2'). That matters: most 'math for ML' curricula stop at 2018-era content, and the attention/softmax/QK^T math is now table stakes.

### [scikit-learn MOOC — Machine learning in Python with scikit-learn (Inria)](https://inria.github.io/scikit-learn-mooc/)

*scikit-learn community with Inria Learning Lab, Inria Academy and probabl* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 35-50 hours

The most underrated resource in this list, and arguably the best free structured course for the *workflow* half of classical ML. Eight modules: ML concepts, predictive modelling pipelines, model selection, hyperparameter tuning, linear models, decision trees, ensembles, evaluation — plus extras on dimensionality reduction, feature selection, interpretation and clustering. What makes it better than the alternatives is that it is written by the people who maintain the library, so the idioms you learn are the correct ones (proper Pipeline construction, cross_validate, nested tuning), and it is continuously updated to run against the current scikit-learn rather than frozen in 2019.

> **Worth knowing.** The hosted cohort run is on fun-mooc.fr; the GitHub Pages version is the always-open self-study copy.

### [scikit-learn User Guide (v1.9 stable) — especially §3 Model Selection and Evaluation and §12 Common Pitfalls](https://scikit-learn.org/stable/user_guide.html)

*scikit-learn core developers* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-15 hours

Almost every beginner treats sklearn docs as API lookup and never reads the prose. That is a mistake: the User Guide is a genuine textbook with the math and the failure modes written by the people who implemented them. Two pages are non-negotiable — the model-selection/cross-validation chapter (why KFold vs StratifiedKFold vs GroupKFold vs TimeSeriesSplit, why nested CV exists) and 'Common Pitfalls and Recommended Practices', which is the clearest free write-up of data leakage, inconsistent preprocessing, and controlling randomness.

### [scikit-learn: Common Pitfalls and Recommended Practices](https://scikit-learn.org/stable/common_pitfalls.html)

*scikit-learn core developer team* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2-3 hours

Called out separately from the User Guide because it is the highest-leverage page for a beginner and almost nobody reads it. It covers inconsistent preprocessing, the two flavours of data leakage (fitting a transformer on the full dataset before splitting; leaking during cross-validation) with correct-vs-incorrect code side by side, and how to control randomness so your results are actually reproducible. Data leakage is the #1 reason beginner models show 0.97 AUC in a notebook and fail in production; this page is the vaccine. Read it in your first week or two of this chapter, not months later.

### [Statistical Learning with Python (StanfordOnline, edX) — free companion course to ISLP](https://www.edx.org/learn/python/stanford-university-statistical-learning-with-python)

*Trevor Hastie & Robert Tibshirani* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 20-30 hours

The authors' own lecture videos walking through ISL chapter by chapter, with Python labs. This is the cheapest possible way to get a Stanford statistics professor to explain cross-validation and the bootstrap to you personally, and it removes the main failure mode of self-studying ISL (bouncing off the notation and quitting at chapter 3). An R-lab version exists at the same platform if you prefer R. Pair it 1:1 with your ISL reading rather than treating it as a separate course.

> **Worth knowing.** Lectures are a decade old and were filmed for the R edition — only the labs are Python. "Free" means audit-only; the certificate and some graded material are paid.

### [StatQuest with Josh Starmer (Statistics Fundamentals, Machine Learning, Neural Networks playlists)](https://www.youtube.com/@statquest/playlists)

*Josh Starmer* &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-15 hours

The probability-and-statistics leg of the tripod, and the correct antidote to sitting through a semester of intro stats. Starmer is a real statistician (not a content farm), and his videos are the fastest path to genuine understanding of the handful of stats concepts that matter for ML: probability vs likelihood, maximum likelihood estimation, expected value, the normal/binomial distributions, Bayes' theorem, entropy and cross-entropy, R², bias-variance, cross-validation, ROC/AUC, confusion matrices, and p-values-explained-well-enough-to-then-ignore. Use it as a *lookup index*, not a linear course: the moment a term confuses you, search 'StatQuest <term>' and watch one 12-minute video. If you want the same material as a book, his *StatQuest Illustrated Guide to Machine Learning* is the paid version.

### [The Matrix Calculus You Need For Deep Learning](https://explained.ai/matrix-calculus/)

*Terence Parr & Jeremy Howard* &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-8 hours

The definitive 'just enough' calculus document, and the answer to 'what part of vector calculus is actually load-bearing.' It explicitly scopes itself — 'We assume no math knowledge beyond what you learned in calculus 1' — and covers exactly the gap between scalar derivatives and the Jacobians/chain rules that backprop needs, ending with the gradient of an actual neural network loss. Critically, the authors themselves tell you **when** to read it: after you're already familiar with training neural networks, not before. That single sentence from Jeremy Howard is the strongest primary-source evidence for the top-down ordering in this whole domain.

> **Worth knowing.** Undated page with content frozen at 2018.

### [XGBoost official documentation (v3.x)](https://xgboost.readthedocs.io/en/stable/)

*Tianqi Chen* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6-10 hours

You cannot claim tabular ML competence without being able to tune a boosted tree deliberately rather than by superstition. Read the 'Introduction to Boosted Trees' tutorial (Chen's own derivation of the objective and why regularisation is baked into the split criterion) and then the parameter documentation until you can predict each parameter's effect on bias and variance before you change it.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [Computational Linear Algebra for Coders](https://github.com/fastai/numerical-linear-algebra)

*Rachel Thomas, PhD* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 25-40 hours

The only linear algebra course built entirely on the top-down philosophy — 'top down, code first, application centered,' getting you to real applications (CT scan reconstruction, topic modelling with NMF/SVD, background removal from video, PageRank) before digging into underlying detail. It is the direct methodological counterpoint to MIT 18.06 and is worth doing precisely because it teaches the numerical side that pure-math courses skip: floating-point error, conditioning, stability, why algorithm choice matters at scale. Notebooks are free on GitHub (fastai/numerical-linear-algebra) and videos on the fast.ai YouTube channel.

> **Worth knowing.** 2017 vintage: the linear-algebra concepts hold, but the code does not run cleanly on modern stacks.

### [CS229 Machine Learning — main lecture notes (publicly downloadable PDF)](https://cs229.stanford.edu/main_notes.pdf)

*Tengyu Ma & Andrew Ng* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40-60 hours

This is the mathematical version of everything Ng teaches gently on Coursera — the derivations of least squares from probabilistic assumptions, GLMs and the exponential family, generative vs discriminative learning, kernels and SVMs, learning theory and the formal bias-variance decomposition. It is NOT a first course; it is the course you come back to a few months in, once you want to understand *why* rather than *how*.

> **Worth knowing.** Rigorous ML-theory notes (SVMs, GLMs, EM), not a beginner on-ramp — they assume the linear algebra and probability covered earlier in this book.

### [Google Machine Learning Crash Course (refreshed edition)](https://developers.google.com/machine-learning/crash-course/)

*Google's ML education team* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 15-20 hours

Best used as a fast, interactive first week or as a refresher — not as your main course. The refreshed version restructured into four sections: ML models (linear/logistic regression, classification), data (numerical, categorical, overfitting/datasets), advanced models (neural nets, embeddings, LLMs), and real-world ML (production, AutoML, fairness). The genuinely valuable and modern parts are the 'Data' section and the 'Real-world ML' section — production concerns and fairness are things almost no beginner course covers — plus a new LLM module covering tokens, n-grams, transformers, self-attention, distillation, fine-tuning and prompting, which is why this is now a reasonable bridge from classical ML into Chapter 5's language-model material.

### [Introduction to Probability for Data Science](https://probability4datascience.com/)

*Stanley H. Chan* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 60-100 hours

The best free, rigorous, genuinely ML-oriented probability textbook — and probability is the leg of the tripod beginners most reliably under-serve. Unlike a classical stats text it is written for data science from page one, balances theory with Matlab AND Python code, and ships with free lecture videos, slides, and exercises; a second edition with an interactive eBook landed in 2026, so it is actively maintained (many free math texts are not). Correct placement: after StatQuest gives you the vocabulary, use this when you want the actual derivations behind maximum likelihood, the Gaussian, and estimation — typically a few months in.

### [Khan Academy — Linear Algebra, Multivariable Calculus, and Statistics & Probability](https://www.khanacademy.org/math/statistics-probability)

*Sal Khan* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40-60 hours

The right role for Khan Academy in 2026 is remediation and drill, not primary instruction — it is where you go when a 3Blue1Brown video assumed something you don't have, or when you realise you can watch a concept but not execute it. Its genuine advantage over every video-only resource is graded practice exercises with hints and mastery tracking, which is exactly what visual-intuition resources lack.

### [Mathematics for Machine Learning (the mml-book) + free PDF](https://mml-book.github.io/)

*Marc Peter Deisenroth, A. Aldo Faisal & Cheng Soon Ong* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40-80 hours

The canonical, most-cited free maths-for-ML text, published by Cambridge University Press (April 2020) with the authors committing to keep the PDF permanently free (direct PDF: https://mml-book.github.io/book/mml-book.pdf, continuously updated for typos). Part I covers linear algebra, analytic geometry, matrix decompositions, vector calculus, probability & distributions, and continuous optimisation; Part II then *earns* that math by deriving linear regression, PCA, Gaussian mixture models and SVMs — which is the book's real value, since almost nothing else shows you the payoff. Companion Jupyter notebooks and Overleaf exercise sets with solutions are on the same site.

### [Mathematics for Machine Learning and Data Science Specialization](https://www.coursera.org/specializations/mathematics-for-machine-learning-and-data-science)

*Luis Serrano, PhD* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 94 hours

The most current well-produced paid alternative, and the better buy than the Imperial specialization for most 2026 beginners: it was refreshed in 2024, its three courses cover the full tripod (Imperial's third course is PCA rather than probability/statistics, leaving a gaping stats hole), and it is explicitly built around ML use cases with NumPy labs throughout. Serrano is unusually good at the visual-first explanation style without sacrificing correctness. Prereqs are stated as high-school math plus basic Python. Place it as the 'I want one structured paid course that covers everything and holds me accountable' option, taken alongside coding — not before it.

> **Worth knowing.** Coursera paid subscription required; the free audit has no graded assignments. This is the only paywalled item among otherwise free maths resources.

### [Mathematics for Machine Learning Specialization (Imperial College London)](https://www.coursera.org/specializations/mathematics-machine-learning)

*David Dye, Samuel J. Cooper, A. Freddie Page & Marc Deisenroth* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 58 hours

The best-known structured, graded, Python-notebook-based maths-for-ML sequence — 277,000+ enrolments, 4.6/5 from 15,000+ reviews — and its distinctive value over passive video is that you write NumPy code implementing Gram-Schmidt, gradient descent, Newton-Raphson and PCA, which forces the concepts to become operational. Deisenroth (co-author of the mml-book) taught the calculus course, so the notation is consistent with that book. Its flaw: the courses date from roughly 2016-2018 and have not been meaningfully refreshed.

> **Worth knowing.** About seven years old, and paywalled beyond the audit track — assignments require a subscription. Courses 1–2 are the strongest; course 3 (PCA) is a notably harder slog.

### [MIT 18.065 — Matrix Methods in Data Analysis, Signal Processing, and Machine Learning](https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/)

*Prof. Gilbert Strang* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 50-80 hours

If you want Strang, **this** is the Strang course to take for machine learning, and almost nobody tells beginners that. 18.065 is his ML-facing sequel: column space, matrix factorization, orthonormal columns, eigenvalues/eigenvectors, positive definite and semidefinite matrices, SVD, least squares, and gradient descent — reviewed with applications to probability, statistics and optimisation, plus lectures on deep learning itself. It skips the freshman-engineering material that makes 18.06 slow for an ML learner. Videos of all lectures are free on OCW (except Lectures 28-29, unrecorded lab sessions).

> **Worth knowing.** Use it for the linear algebra, not the deep-learning chapters. Strang has retired and there is no updated OCW offering.

### [MIT 18.06SC Linear Algebra (OCW Scholar edition)](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/)

*Prof. Gilbert Strang* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 120-160 hours

The most famous linear algebra course ever recorded, and the OCW Scholar (18.06SC) version is the right one to link — it is built for independent study with recitation videos by MIT instructors, problem sets with solutions, and full exams, all free under Creative Commons. Strang's four-fundamental-subspaces framing is genuinely beautiful. But be clear-eyed about the fit: 18.06 is a general engineering-mathematics course, not an ML course. It front-loads Gaussian elimination, LU/PA=LU factorization, and null-space computation, and the SVD — arguably the single most ML-relevant topic — arrives near the end.

> **Worth knowing.** The "Fall 2011" label is the OCW Scholar packaging date, not the video date — the lectures are 1999-vintage SD. The Java demonstrations in the course materials no longer run in current browsers.

### [MLU-Explain — visual, interactive explanations of core ML concepts (Amazon Machine Learning University)](https://mlu-explain.github.io/)

*Jared Wilber, Brent Werness and collaborators* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-6 hours

When bias-variance, cross-validation, ROC/AUC or precision-recall refuse to click from text, come here. Fourteen scroll-driven essays with charts you drag and manipulate: The Bias Variance Tradeoff, Cross-Validation, Train/Test/Validation Sets, Precision & Recall, ROC & AUC, Decision Trees, Random Forest, Linear and Logistic Regression, Neural Networks, Equality of Odds, Reinforcement Learning, and a two-part Double Descent explainer (which is the concept that connects classical bias-variance to why massively overparameterized modern models work — a genuinely useful bridge to the LLM era). No signup, no install. Highest concept-per-hour ratio of anything in this list.

> **Worth knowing.** Roughly 2021 vintage: good for classical ML intuition, but it covers nothing from the post-2022 era.

### [Seeing Theory — A Visual Introduction to Probability and Statistics](https://seeing-theory.brown.edu/)

*Daniel Kunin, Jingru Guo, Tyler Dae Devlin & Daniel Xiang* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3-5 hours

The fastest possible way to get intuition for distributions, sampling, and Bayesian updating, because you drag sliders and watch the distributions move rather than reading formulas. Six chapters: basic probability, compound probability, probability distributions, frequentist inference, Bayesian inference, and regression analysis. Webby Award winner, hosted by Brown. Perfect as a 3-hour weekend session slotted between StatQuest videos, especially for grasping the central limit theorem, likelihood, and the prior-to-posterior update that underpins every Bayesian framing in ML. Note: the site is no longer actively maintained, though Brown has committed to continue hosting it.

> **Worth knowing.** Officially archived by its authors — if a browser change breaks the D3.js visualisations, nobody will fix them.

### [TabPFN-2.5: Advancing the State of the Art in Tabular Foundation Models](https://arxiv.org/abs/2511.08667)

*Léo Grinsztajn, Noah Hollmann, Frank Hutter et al.* &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2-3 hours

Read this so you are not two years out of date on the one question everyone thinks they know the answer to. TabPFN is a transformer pretrained on millions of synthetic supervised tasks that does in-context learning on tabular data with no task-specific training. TabPFN-2.5 reports a 100% win rate against default XGBoost on classification datasets up to ~10k rows / 500 features and ~87% on datasets up to 100k rows / 2k features, and leads TabArena, substantially outperforming *tuned* tree-based models.

> **Worth knowing.** A frontier research paper, not beginner reading — useful as a pointer that the tabular baseline is moving.

### [The Hundred-Page Machine Learning Book](https://www.themlbook.com/)

*Andriy Burkov* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 8-12 hours

The best *map* of the territory: ~140 pages covering supervised and unsupervised learning, SVMs, neural networks, ensembles, gradient descent, clustering and dimensionality reduction, autoencoders and transfer learning, feature engineering and hyperparameter tuning. Its job is orientation and revision, not first learning — read it in a weekend before you start, then again before interviews. The read-first-buy-later policy means you can evaluate it for free with no piracy. Note the 2019 publication date: it predates the LLM era, so treat the neural-network chapters as historical context.

> **Worth knowing.** 2019 content sold under a 2019–2025 copyright banner, which reads fresher than it is. A compact classical-ML reference only — the LLM material lives in a separate 2025 companion volume. Honour-system paid, not free.

### [The state of Tabular Foundation Models (2026) — Mindful Modeler](https://mindfulmodeler.substack.com/p/the-state-of-tabular-foundation-models)

*Christoph Molnar* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The clearest plain-English field survey of where tabular ML actually stands right now, from someone with no vendor stake. Molnar's timeline: 2021-22 prior-data fitted networks as proof of concept; 2024-25 the acceleration (TabICL, TabPFN v2, TabDPT); 2026 maturity where 'SOTA changes every couple of months or weeks.' His current personal pick is TabICL v2 for speed, performance and being fully open-source, and he flags a real risk that the field drifts closed-source via commercial licensing (e.g. RealTabPFN). Read this plus the TabArena leaderboard (tabarena.ai, which now redirects to a Hugging Face Space) rather than trusting any static blog ranking.

> **Worth knowing.** Opinion/newsletter writing, not peer-reviewed or benchmarked, and its named-model pick (TabICL v2) is a snapshot of a fast-moving area that will date quickly.

### [Why do tree-based models still outperform deep learning on typical tabular data? (NeurIPS 2022 Datasets & Benchmarks)](https://openreview.net/forum?id=Fp7__phQszn)

*Léo Grinsztajn, Edouard Oyallon & Gaël Varoquaux* &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2-3 hours

The paper that everyone cites for 'use XGBoost on tabular data', and worth reading yourself rather than quoting secondhand — its actual contribution is the *mechanism*: tree ensembles win because they are rotation-non-invariant (they respect individual feature meanings), robust to uninformative features, and biased toward the irregular, non-smooth target functions typical of real tabular data. Understanding those three reasons is what lets you predict when the result will and won't hold, which is exactly what a good interviewer probes.

## Keep for reference

Not for reading end to end. Useful to have when you need to look something up.

### [Appendix: Mathematics for Deep Learning (Dive into Deep Learning)](https://www.d2l.ai/chapter_appendix-mathematics-for-deep-learning/index.html)

*Brent Werness & Rachel Hu, within Dive into Deep Learning by Aston Zhang, Zachary C. Lipton, Mu Li & Alexander J. Smola* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 15-25 hours

The most precisely scoped free answer to 'exactly which math does deep learning use, and nothing more.' Eleven sections: geometry & linear-algebraic operations, eigendecompositions, single-variable calculus, multivariable calculus (gradients, chain rule, backpropagation, Hessians), integral calculus, random variables, maximum likelihood, distributions, naive Bayes, statistics, and information theory (entropy, KL, cross-entropy). That list IS the minimum viable curriculum — you can use it directly as a syllabus checklist against any other resource.

> **Worth knowing.** Author affiliations are as of writing rather than current.

### [LightGBM documentation (Microsoft) and CatBoost documentation (Yandex)](https://lightgbm.readthedocs.io/en/stable/)

*LightGBM: Guolin Ke and the Microsoft Research/DMTK team · CatBoost: Yandex research team* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-6 hours

Read after XGBoost, and mainly to learn *when each wins* rather than to memorise APIs. LightGBM's leaf-wise growth and histogram binning make it the speed choice on wide/large data (and the thing most likely to overfit if you don't cap `num_leaves`); CatBoost's ordered target statistics and ordered boosting make it the default when you have many high-cardinality categorical features and don't want to hand-build target encoding (and it's usually the strongest out-of-the-box with untuned defaults). Knowing this three-way tradeoff concretely is a common practical interview question and a real production decision.

### [Probabilistic Machine Learning: An Introduction](https://probml.github.io/pml-book/book1.html)

*Kevin Patrick Murphy* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-20 hours, as a reference

The definitive modern graduate reference for probabilistic ML — MIT Press, March 2022, with the free draft PDF still being updated (latest revision 2025-04-18) and every figure reproducible via Python/JAX/TensorFlow colabs in the probml/pyprobml repo. It unifies classical statistical foundations with deep learning in one consistent notation, and a companion volume ('Advanced Topics') goes further. On placement: this is roughly a thousand pages and it is NOT a book that teaches you math — it is a book that assumes linear algebra, multivariable calculus and probability and then uses them at speed. Endorsements calling it suitable for 'people new to the field' mean new to ML, not new to math.

> **Worth knowing.** A 1000-page graduate-level probabilistic-ML textbook, not a maths primer — use it as a reference or stretch goal rather than prerequisite reading.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
