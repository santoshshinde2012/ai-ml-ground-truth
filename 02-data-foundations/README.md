# Chapter 2: Data foundations

**Weeks 1–5 &nbsp;·&nbsp; about 50 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** You already program. This chapter teaches the data dialect — arrays and
shapes, dataframes and cleaning judgement, and enough SQL to be trusted with real data. You finish
by publishing a small, reproducible analysis of a dataset you found yourself, which becomes the
seed of everything you build later.

**This dataset carries forward.** Chapter 3 models it. Chapter 5 can use documents in the same
domain. Keep the domain where you can. Document a needed change, rather than forcing an unsuitable
dataset to support a claim it cannot answer.

## Choose a dataset you can finish

Before investing in cleaning, check five things:

- **Permission:** you may download, analyse and publish the intended examples.
- **Grain:** you can say what one row represents and spot duplicates or repeated entities.
- **Question:** one useful descriptive question and a feasible binary or numeric prediction target.
- **Clocks:** you know when inputs would be available and when outcomes can be seen. A current
  export with no history supports a limited exercise, not a verified historical backtest.
- **Size and continuity:** a small sample runs on your machine, and related public documents could
  support the later application.

If choosing stalls, use the [reference lab](../labs/README.md) while looking for your own portfolio
dataset. It uses synthetic data, so its results show behaviour under stated assumptions. A city
open-data export, a permitted export of your own data, or a small transaction dataset can work if it
passes these checks. An ordinary, modest dataset is enough.

**Set aside the test set before you explore outcomes.** As soon as you know what you want to
predict, write down the prediction time and time or group split, and set aside the final
holdout. All-row checks of source, schema and integrity are useful. Learned transformations,
charts that use the target, and feature choices belong on training and development data only. If
you have already explored every outcome, label that work exploratory and find fresh data to confirm
it. Splitting afterwards does not undo what you have seen. Chapter 3 reviews this design.

**In this chapter:** [Plan](#your-five-week-plan) &nbsp;·&nbsp; [Learn](#what-to-learn)
&nbsp;·&nbsp; [Build](#what-to-build) &nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp;
[Resources](#resources)

---

## Your five-week plan

About ten hours a week. Each week ends with something on GitHub.

| Week | Focus         | Do this                                                                                               | Done when                                            |
| ---- | ------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| 1    | Setup + NumPy | Reuse the uv project, shortlist your dataset, learn NumPy basics, start Essence of Linear Algebra     | `arr.shape` and broadcasting exercises work          |
| 2    | pandas        | McKinney ch 4–8, 10 or pandas Getting Started. Write 3 cleaning functions with tests                  | Functions in `src/` and tests in `tests/` pass       |
| 3    | SQL           | SQLBolt basics, selected ThoughtSpot window and join lessons, then DuckDB on your CSV                 | Top-N-per-group query and join-cardinality check run |
| 4    | Your dataset  | Confirm data **you** sourced. Write a schema/source manifest and cleaning decision log                | Eight+ meaningful checks pass. Log has 3+ decisions  |
| 5    | Publish       | README with question, answer and limitation. Charts that answer questions. A locked fresh-process run | A stranger can clone and reproduce it                |

New words in this chapter, such as array, broadcasting, dataframe and point-in-time, are explained
where they first appear below and collected in
[Terms in plain English](../content/reader-guide.md#glossary).

Work in the Chapter 1 project. Add the SQL, plotting and test dependencies, then commit the changed
project files:

```bash
uv add duckdb matplotlib
uv add --dev pytest
```

After writing the Week 2 tests in `tests/test_*.py`, run `uv run --locked pytest` from the project
root. Use [pytest's getting-started guide](https://docs.pytest.org/en/stable/getting-started.html)
for discovery and assertions. Start the linear-algebra videos with chapters 1–4, ending with
"Matrix multiplication as composition". Later lessons are optional, inside the same 50-hour budget.

---

## What you will be able to do

Take a messy dataset you found yourself and turn it into a published, reproducible analysis that a
stranger can run with one command.

## What to learn

### Worked lesson: the event happened, but you did not know it

Suppose you predict at the start of 3 January, using the previous seven days. These invented
transactions separate when an event happened from when the service received it:

| Amount | Event time | Available at | Available for this prediction? |
| --- | --- | --- | --- |
| 10 | 1 January | 1 January | Yes |
| 20 | 2 January | 4 January | No: it arrived later |
| 30 | 4 January | 4 January | No: the event is in the future |

The historical total is **10**. Filtering on event time alone gives 30 and leaks a late arrival.
Using today's complete customer total gives 60 and also includes a future event. Values correct
today can be wrong inputs for a past decision.

```python
from datetime import datetime, timedelta, timezone

def day(number):
    return datetime(2026, 1, number, tzinfo=timezone.utc)

events = [(10, day(1), day(1)), (20, day(2), day(4)), (30, day(4), day(4))]
as_of = day(3)
total = sum(amount for amount, event_at, available_at in events
            if as_of - timedelta(days=7) <= event_at < as_of
            and available_at <= as_of)
assert total == 10
```

**Try it yourself.** Move the decision to 5 January. Which records now qualify, and what is the
total? Then add an event exactly at the prediction time. Decide whether it belongs before running.

<details>
<summary>Hint and explained answer</summary>

Both clocks must pass. At 5 January all three original records qualify, so the total is 60.
An event at exactly `as_of` falls outside the half-open event window `[as_of - lookback, as_of)`.
That boundary stops the current decision's own activity from becoming its historical input. The
availability rule here does include records arriving exactly at `as_of`. Test and document whether
your real extraction order can actually use them.

</details>

Use this tiny fixture to test a larger SQL or pandas implementation. The
[reference lab](../labs/README.md) builds the same habit on a reproducible synthetic project.

### Core concepts

**Thinking in arrays.** You are fluent in loops. Machine learning is written in shapes and batches,
and the second dialect takes a little while. What you need is small but you need it cold: `shape`
and `dtype`, indexing and slicing, views against copies, `reshape` and `transpose`, axis semantics,
vectorising a loop into an array expression, and above all **broadcasting**.

Broadcasting deserves the extra time. It is the set of rules by which NumPy stretches a smaller
array to match a larger one's shape. A large share of the debugging you will do over the next six
months is shape errors, silent broadcasts and transposes in the wrong place.

```python
import numpy as np

predictions = np.arange(100.0).reshape(100, 1)  # one column, shape (100, 1)
targets = np.arange(100.0)                      # shape (100,)
errors = predictions - targets
```

**Try it yourself.** Predict `errors.shape` before running it. Every prediction equals its target,
so the mean squared error should be zero. What does `(errors ** 2).mean()` return, and why?

<details>
<summary>Hint and explained answer</summary>

Align the shapes from the right. `(100,)` is treated as `(1, 100)`, and each size-1 dimension
stretches to match. So `errors` has shape `(100, 100)`: every prediction minus every target. The
mean is 1666.5, the average squared difference over all 10,000 pairs, and nothing raises an error.
Compare matching rows with `predictions[:, 0] - targets`, then assert `errors.shape == (100,)`
before reducing. That one line catches the same bug in a metric, a loss or a pandas-to-NumPy
conversion.

</details>

Alongside this, watch 3Blue1Brown's
[_Essence of Linear Algebra_](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab).
Three hours of video, and it gives you one idea that pays off immediately: a matrix is a
transformation of space, not a grid of numbers to row-reduce. After that, "a layer is a linear map
followed by a nonlinearity" stops being jargon. It helps to pair each chapter with code, though.
It is quite possible to finish the series feeling enlightened and still be unable to compute a
matrix product.

**Thinking in tables.** pandas, and the judgement that goes with it. The library is the easy half.

Alongside your notebook, record **every cleaning decision you made, what you rejected, and how the
choice would change a model downstream**. Here is an example decision log, with invented
percentages:

```markdown
## delivery_time — 8.2% missing
Pattern: missingness correlates with carrier == "regional" (34% missing) against 0.4%
for national. This is not missing completely at random: it depends on observed carrier.
This pattern alone cannot establish MAR versus MNAR; missing delivery times are unobserved.
Rejected: mean imputation. It would smear the national distribution across regional rows
          and hide the fact that we simply do not observe this segment.
Rejected: dropping the rows. It removes 8% of the data, and non-randomly.
Chose:    keep the nulls and a delivery_time_observed flag for descriptive coverage checks.
          Report observed timing by carrier, alongside missingness and sample counts.
Impact:   observed rows alone cannot establish timing for all regional-carrier deliveries.
```

That paragraph is the thing worth showing people. Anyone can call `dropna()`. The judgement is the
scarce part, and it maps directly onto "data literacy" in a hiring rubric.

The author-hosted [missing-data chapter](https://stefvanbuuren.name/fimd/sec-MCAR.html) explains why
dependence on an observed field can fit MAR (missing at random), and why MNAR (missing not at
random) needs sensitivity analysis.

Separate missing **features** from missing **targets**. If delivery time is the Chapter 3
target, its eventual value and observed flag cannot be predictors at dispatch. Avoid filling an
unfinished target with zero or a mean. A package still being tracked has a **right-censored**
duration: you know how long it has gone undelivered, not when it will arrive. Evaluating only
completed deliveries can leave out the slowest ones. The
[scikit-survival introduction](https://scikit-survival.readthedocs.io/en/stable/user_guide/00-introduction.html)
explains event indicators and censoring. A survival model is optional depth, not an extra
prerequisite. For a first project, a fixed-horizon target such as “delivered within seven days” is
often easier to define. After seven days, a tracked non-delivery is negative. A lost tracking
record is still unknown. State which population and follow-up your evaluation covers.

For a feature available before prediction, compare an imputer and missing indicator fitted inside
the training pipeline with a model that handles that feature's missing values. Either way, keep the
raw missingness information in your analysis.

**SQL.** Grain, joins and aggregation carry across tools, though syntax and NULL behaviour vary by
engine. Get comfortable with CTEs, window functions (`ROW_NUMBER`, `RANK`, `LAG`, running totals),
join cardinality, and point-in-time correctness.

That last one matters more than it sounds. Most serious data-leakage bugs in machine learning are,
underneath, a query that accidentally used the future.

If an assistant writes SQL, check it against a schema you understand and a tiny table with
duplicates, NULLs and boundary dates. Plausible SQL can give the wrong denominator with no error.

**A schema is more than column names.** Define dtypes, units, allowed categories and what a missing
value means. Keep leading zeros in identifiers. Choose a timezone policy. Store money with a
documented currency and rounding rule. Tell apart a zero, an unknown value and a value that does not
apply. Recheck pandas string and nullable dtype behaviour after upgrades. In pandas 3.0, default
string storage uses PyArrow when installed and falls back otherwise, as the
[string migration guide](https://pandas.pydata.org/docs/user_guide/migration-3-strings.html)
explains.

Write the expected join cardinality before joining. One customer with three orders and four
support events produces twelve rows if both event tables are joined directly. Summing the joined
orders inflates revenue fourfold. Aggregate each event table to the intended grain first. In
pandas, use `validate="many_to_one"` for a unique customer lookup and `indicator=True` to check
unmatched rows. Its
[merge documentation](https://pandas.pydata.org/docs/reference/api/pandas.merge.html) also warns
that NULL keys on both sides match each other, unlike usual SQL joins. Test this explicitly.

**Write a data contract before training.** Name the unit of a row, its unique key, the prediction
time, the feature lookback, the outcome window, and when that outcome becomes complete. Keep both
`event_time` (when something happened) and `available_at` (when your service could first use it). A
transaction from Monday that arrived on Friday was unavailable to Tuesday's model. Historical
features must pass both clocks, and later corrections need version history.
[Feast's point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)
show historical retrieval. Check how your own query and tool handle availability time.

Some public exports hold only a current snapshot, with no availability history. Record that limit,
and avoid inventing timestamps or claiming a verified backtest. Test your join logic with small
synthetic late-arrival cases, and choose a Chapter 3 split your data can support.

For a customer snapshot at time `t`, build features from `[t - lookback, t)`, using records
available by `t`. Build labels from the outcome window that follows. An unresolved outcome is
**unknown**, not a negative. Record `label_available_at` and `outcome_observed` separately from the
planned maturity date, because a window can pass while its source ledger is still incomplete. At a
simulated training cutoff, use only labels that the observation window, reporting delay and actual
availability allow. Report missing outcomes by cohort and exclusion reason. Elapsed time alone does
not prove follow-up is complete.

Test unique keys, join row counts, timezone conversion, missingness, late arrivals and duplicate
events. Store the extraction cutoff and source version with the data. Record permission to use
the data, keep customer identifiers out of public examples, and publish only data whose licence and
permissions allow it. When the original data is private, a reproducible synthetic example is enough.

**Reproduction needs a data manifest.** Record the source URL or export/query version, licence,
retrieval date, extraction cutoff, raw-file checksum, schema version, code commit and environment.
Where permitted, keep raw inputs unchanged. Document any sampling, seeds and exclusions, and use the
same population denominator in your text and charts. Run the cleaning and analysis in a fresh
process with the locked environment, not from the notebook's execution history. The questions
in [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) help explain who is represented and
which future uses the dataset cannot support.

If raw data is not in the repository, include its exact download or export steps and expected
checksum. If the documented input is missing or differs, the analysis should fail clearly, not
quietly analyse a newer export.

## Resources

All 31 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [Python for Data Analysis, 3rd Edition](https://wesmckinney.com/book/) — Wes McKinney. A free
  book, 40–60 hours. Chapters 4 to 8 and 10 are the ones that matter.
- [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
  — NumPy documentation contributors. Free documentation, 3–6 hours.
- [Mode / ThoughtSpot SQL Tutorial (Basic, Intermediate, Advanced)](https://www.thoughtspot.com/sql-tutorial)
  — ThoughtSpot. Free lessons. Run selected exercises in DuckDB. Budget 10–15 hours for the full
  tutorial, fewer for this chapter's selections.
- [uv — official documentation](https://docs.astral.sh/uv/) — Astral maintainers. Free
  documentation, 2–4 hours. Getting Started and Projects are enough.

These are whole-resource estimates, and some are alternatives, so do not add them up. Fit selected
chapters and lessons inside the 50-hour project budget, and finish the analysis before optional
depth.

If Python is not yet one of your languages, do [CS50P](https://cs50.harvard.edu/python/) first. Its
90 to 120 hours sit on top of this chapter's 50, not inside them, and the chapter will make much
more sense afterwards.

## What to build

**A published data product.** A public repository containing:

- A README stating the question in one sentence, the answer in one sentence, and the limitation in
  one sentence
- `pyproject.toml`, `uv.lock`, Python/platform details and a command tested after `uv sync --locked`
- A `src/` package with your cleaning functions, not just a notebook
- At least eight meaningful checks spanning cleaning functions, unique keys, joins, timestamps and
  missingness
- Your cleaning decision log
- Only charts that answer named questions, each with a denominator, units, source and limitation.
  Cover the relevant distributions, missingness/coverage and time or group variation. Show
  uncertainty when making an estimate. Use readable labels and a palette that works without colour.
- A data contract covering row keys, both timestamps, feature windows, label maturity, actual
  outcome availability/coverage and permitted use
- A source manifest with raw-input checksums, extraction cutoff and documented exclusions

Give the package an analysis entry point and document its exact `uv run --locked ...` command. It
must read the documented inputs and rebuild the cleaned output, summary results and chosen charts
without notebook state. Run `uv run --locked pytest` separately. Passing tests alone do not
reproduce the analysis.

Choose a dataset that **you found yourself**: a city open-data portal, a government export, a niche
marketplace, or your own data exported from a service you use. Before Week 4, pick an outcome you
could later predict, such as a delay, a price or a category, and the inputs available at
prediction time. [Chapter 3](../03-core-machine-learning/README.md) will ask you to model
it. In the handoff, state the prediction time, row/group key, reserved holdout and a workable split.
If the dataset cannot support a supervised question, change the dataset and write down why. Avoid
inventing labels or using the outcome as an input.

## Before you move on

- A stranger can install the locked environment, run the tests and regenerate your analysis with the
  documented command.
- You can defend two cleaning decisions against "why not just drop those rows?"
- You can write and explain a top-N-per-group query, checking ties and duplicate keys on a fixture.
  Documentation is allowed.
- You can predict the output shape of a broadcast before running it.
- You can show that a late-arriving record and an unfinished label cannot enter a training row.
- You can tell apart a mature observed negative, a censored duration and a missing outcome, and
  explain how each enters your denominator.
- You can show that a join preserves the intended grain and explain the denominator of each chart.
- The Chapter 3 handoff names a target, prediction time, available inputs and defensible split, and
  states any historical-data limits.

## A few things worth knowing

- **The free _Python Data Science Handbook_** at `jakevdp.github.io` is the 2016 first edition,
  written against Python 3.5, though still widely recommended. The NumPy and matplotlib chapters are
  useful for the concepts. The pandas and scikit-learn chapters teach idioms that may now raise
  errors or behave differently, so check its examples against current documentation. McKinney's
  book plus the pandas migration guides is the main route here.
- **Polars is optional.** This chapter uses pandas to match its selected tutorials. Polars is a
  useful alternative when your team's stack or measured memory and runtime needs call for it.
  [scikit-learn supports Polars transformer output](https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_set_output.html).
  Rewrite one cleaning function only after the analysis works, and check correctness before speed.
- **Titanic, Iris and MNIST** are fine for a ninety-minute warm-up. As portfolio pieces they are so
  common that they tell a reviewer very little about you, which is a shame given the effort. A
  dataset you sourced yourself does much more work on your behalf.

---

[Previous: Getting oriented](../01-getting-oriented/README.md) &nbsp;·&nbsp;
[Next: Core machine learning](../03-core-machine-learning/README.md)
