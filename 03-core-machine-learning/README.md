# Chapter 3: Core machine learning

**Weeks 6-13 &nbsp;·&nbsp; about 80 hours.** &nbsp;·&nbsp; [Index](../README.md) &nbsp;·&nbsp; [Resources for this chapter](resources/README.md)

**The short version.** This chapter teaches you to train a model honestly: split the data so the score means something, pick a metric that maps to a real cost, beat a simple baseline, and explain the result. The same discipline carries straight into evaluating language models later. You finish with a model served behind an API.

**Use your Chapter 2 dataset.** Same repo or a fork — the story should connect.

---

## Your eight-week plan

About ten hours a week. Follow the rows; do not skip the baseline or the README.

| Week | Focus | Do this | Done when |
|---|---|---|---|
| 6 | Problem + split | Define prediction target; choose split (random / time / group); justify in writing | Split documented in README |
| 7 | Baseline + leakage | Majority-class baseline (`DummyClassifier`); one **deliberate** leakage mistake, then fix with Pipeline | Before/after scores in README |
| 8 | Logistic regression | ISL or scikit-learn MOOC; metric tied to cost | Beats baseline on honest metric |
| 9 | Trees | Random forest + boosted tree (XGBoost); SHAP on one wrong prediction | Model comparison table |
| 10 | Threshold | Cost matrix; pick threshold from curve, not 0.5 | Can explain threshold out loud |
| 11 | API | FastAPI `/predict`; pydantic validation; pytest | Bad input returns 422 |
| 12 | Polish | Confidence intervals; "what failed" section; load-test note | README is the deliverable |
| 13 | Buffer | Re-build one model from empty file; rehearse interview story on leakage | Can rebuild without tutorial |

---

## Is this still worth eight weeks in 2026?

It is a fair question. The hiring and the funding are in language-model work, and you can be
productive with an API and no linear algebra at all.

Two things make me think the answer is yes. First, hiring guides across the current cycle describe
logistic regression, tree models, cross-validation, the metrics and the bias-variance tradeoff as
table stakes: being shaky there tends to be disqualifying, even though being strong there is no
longer distinguishing. Second, and more usefully, **evaluating a generative system is the same
discipline wearing different clothes**. The work you do here on splits, leakage, metrics and cost
is exactly what you will use in [Chapter 5](../05-language-models/README.md) to evaluate an agent. Skipping it here means paying for it
there, with less to hold on to.

Eight weeks, then, rather than six months.

## What you will be able to do

Take an unfamiliar dataset, choose a validation scheme and defend it, choose a metric and tie it to
a real cost, beat a simple baseline, and explain in writing why each model helped or did not.

## What to learn

**The learning problem.** A model is a function with parameters, a loss says how wrong it is, and
gradient descent walks the parameters downhill. Everything from linear regression to a very large
transformer is that sentence. Add regularisation, the bias-variance diagnostic, and learning curves.

Learning curves are the most practically useful idea here and the most often skipped. Plotting
training and validation score against training-set size answers "should I get more data, or a bigger
model?" directly, and almost nobody makes the plot.

**Validation, which is where the real care goes.** Your validation score is an estimate of
performance on data you have never seen. Anything that lets information from outside the training
fold reach the model destroys that estimate quietly, and in your favour. That last part is what
makes leakage dangerous: it never raises an exception, it just makes your numbers better.

Three families to know:

| Kind | What happens | Guard |
|---|---|---|
| **Preprocessing leakage** | You fit a scaler, imputer or target encoder on the whole dataset before splitting, so every fold has seen the test set's statistics | Put all preprocessing inside a `Pipeline`, so cross-validation refits it per fold |
| **Temporal leakage** | You use information that did not exist at prediction time. Random K-fold on time-ordered data trains on Thursday to predict Wednesday | `TimeSeriesSplit`, or rolling-origin backtesting |
| **Group leakage** | The same user, patient or device appears in both train and test, so the model memorises the entity | `GroupKFold` or `StratifiedGroupKFold` |

Two questions, asked before you choose a splitter, prevent most of this: **does a row's identity
repeat, and does time matter?**

**Metrics, which are decisions in disguise.** On a dataset with 1% positives, a model that always
predicts "no" scores 99% accuracy. A metric is a claim about what it costs to be wrong, and choosing
one is a business decision you are making on someone's behalf, usually by leaving it at the default.

Worth knowing well: precision and recall and when each dominates; why ROC-AUC looks optimistic under
heavy imbalance and PR-AUC does not; calibration, and when it matters; and the fact that the
classification threshold is a decision you derive from a cost curve, not the 0.5 that came in the
box.

**A tiny threshold example.** Suppose false negatives cost ten times false positives — you miss a
fraud case ten times worse than you flag an honest transaction. On 1% positives, a model that
always says "no" still scores 99% accuracy. You might choose recall-heavy metrics, plot precision
against recall, and pick a threshold where recall is 0.85 even if precision drops to 0.40 — because
that is what your cost matrix implies. The default 0.5 would never appear in that reasoning.

**Tree models.** For most tabular problems a gradient-boosted tree is the answer, and knowing why
rather than just that is the difference between an engineer and a library caller. Learn what bagging
and boosting each buy you, and what `max_depth`, `min_child_weight`, `subsample`, `colsample_bytree`
and early stopping actually do to bias and variance.

Also learn interpretability: permutation importance and why it misleads under correlated features,
partial dependence, and SHAP, which attributes a single prediction to the features that drove it.
This is precisely what tabular models have and language models largely do not. Where a bank, insurer or hospital needs a defensible reason for a decision, an explainable
tree is the answer.

One nuance worth carrying: the familiar line that tree ensembles always beat deep learning on
tabular data was well supported through about 2024, and is now more qualified. Tabular foundation
models now lead on small and medium datasets where rows are independent of one another. A June 2026
benchmark, [BeyondArena](https://arxiv.org/abs/2606.30410), found trees and other models trained on each dataset
still ahead on temporal, grouped, large and wide data. Newer vendor releases claim to narrow that gap; test
the claim with this chapter's split design rather than taking it on trust. Tree ensembles remain
the safe production default at scale and wherever interpretability, latency or licensing matter. Describing
the regime rather than the slogan is the better answer in an interview, and this area is moving
quickly enough that it is worth checking before you quote it.

**The maths, paid for as you go.** This is the most argued-about part of any AI roadmap, so here is
my reading of it, plainly.

The people who teach the hands-on courses are unusually consistent: fast.ai's own prerequisites page
says high-school maths is sufficient, Karpathy's course asks for "intro-level math (e.g. derivative,
gaussian)", and Parr and Howard tell readers to come to their matrix-calculus paper only **after**
they are already training networks. The failure I see most often is not under-preparing but
over-preparing: committing to a long linear algebra course before writing any model, and stalling
around month three with nothing built.

The minimum is small enough to name:

- **Linear algebra:** vectors, matrices and tensors; shapes and axes; matrix multiplication and why
  shapes must line up; transpose; dot product as similarity; broadcasting; a matrix as a
  transformation, and matrix products as composition. Eigenvectors, SVD, rank, norms and
  orthogonality can wait a few weeks.
- **Calculus:** the derivative as sensitivity; partial derivatives; the gradient; **the chain rule**,
  which carries more weight than anything else here; recognising a Jacobian; and gradient descent.
  Integrals, Hessians and hand-derived matrix calculus can wait, or may never come up.
- **Probability and statistics:** random variables, expectation and variance, independence,
  conditional probability, Bayes' rule, the Gaussian, Bernoulli and categorical distributions,
  likelihood and maximum likelihood, log-probabilities, and cross-entropy as a loss.

That is perhaps twenty to forty hours of honest study rather than a semester. Classical hypothesis
testing is deliberately down-weighted here; it matters a great deal for experimentation work, which
is covered in the [Data Scientist branch of Chapter 7](../07-specialisation/README.md).

The counter-argument deserves respect too. People who take the code-first route and never come back
to the maths tend to plateau at the point where they need to read a paper, debug an unusual loss, or
design an architecture. The bill arrives either way. Paying it here, once you have something
concrete to attach it to, tends to go better.

## Resources

All 32 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [An Introduction to Statistical Learning (ISLP — Python edition)](https://www.statlearning.com/) — Gareth James, Daniela Witten, Trevor Hastie & Robert Tibshirani, with Jonathan Taylor. A free book, 60-90 hours across the chapter.
- [scikit-learn: Common Pitfalls and Recommended Practices](https://scikit-learn.org/stable/common_pitfalls.html) — scikit-learn core developers. Free documentation, 2-3 hours. Read it in week 7, before the leakage exercise.
- [Approaching (Almost) Any Machine Learning Problem](https://github.com/abhishekkrthakur/approachingalmost) — Abhishek Thakur. A free book, 20-30 hours.
- [Interpretable Machine Learning](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar. A free book, 12-18 hours; the SHAP and permutation-importance chapters first.

## What to build

**A model behind an API.** Take your [Chapter 2](../02-data-foundations/README.md) dataset and complete the loop:

1. A split you chose deliberately and justified in writing
2. All preprocessing inside a `Pipeline`
3. A simple baseline, then logistic regression, then a random forest, then a boosted tree
4. A metric tied to a stated cost, reported with confidence intervals
5. An operating threshold taken from the cost curve
6. SHAP explanations, including one prediction the model got wrong
7. A FastAPI endpoint with schema validation, and tests for both code and data

The README is the deliverable. Include a table of every model and what it bought you, a section on
what did not work, and a section on known failures. Those last two are unusual in a junior portfolio
and they do a lot of quiet good.

**Worth considering as well:** build a model with leakage on purpose, record the inflated score, fix
it properly inside a `Pipeline`, record the honest score, and write up the gap. It shows you
understand the mechanism rather than the name, and it makes a good story.

## Before you move on

- Given a dataset description, you can choose a split and a metric and defend both in a minute.
- You can explain your cost matrix and derive your threshold out loud.
- You can explain what SHAP computes, and one thing it does not tell you.
- You can call your own endpoint and show it rejecting a malformed request.

## A few things worth knowing

- **Start with ISL rather than ESL.** They share authors and the titles are similar, but *Elements
  of Statistical Learning* is a graduate statistics text. People often start there, stop at chapter
  three, and conclude they are not a maths person. They usually are; it was the wrong book.
- **If you want Strang's linear algebra**, MIT 18.065 is the machine-learning-facing course. 18.06
  is excellent and spends its first month on material you will not use here.
- **Kaggle is a good gym and a weak portfolio.** Competitions give fast, honest feedback on
  validation design, which is genuinely valuable. They also remove problem framing, data sourcing
  and metric choice, which are three of the harder parts of the job.

---

[Previous: Data foundations](../02-data-foundations/README.md) &nbsp;·&nbsp; [Next: Deep learning](../04-deep-learning/README.md)
