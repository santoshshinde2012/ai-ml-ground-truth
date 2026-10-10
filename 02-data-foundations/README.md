# Chapter 2: Data foundations

**Weeks 1–5 &nbsp;·&nbsp; about 50 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** You already program; this chapter teaches the data dialect — arrays and
shapes, dataframes and cleaning judgement, and enough SQL to be trusted with real data. You finish
by publishing a small, reproducible analysis of a dataset you found yourself, which becomes the seed
of everything you build later.

**This dataset carries forward.** Chapter 3 models it. Chapter 5 can use documents in the same
domain. Do not switch datasets mid-book unless you must.

**In this chapter:** [Plan](#your-five-week-plan) &nbsp;·&nbsp; [Learn](#what-to-learn)
&nbsp;·&nbsp; [Build](#what-to-build) &nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp;
[Resources](#resources)

---

## Your five-week plan

About ten hours a week. Each week ends with something on GitHub.

| Week | Focus         | Do this                                                                                 | Done when                                            |
| ---- | ------------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| 1    | Setup + NumPy | Reuse uv project; shortlist your dataset; NumPy basics; start Essence of Linear Algebra | `arr.shape` and broadcasting exercises work          |
| 2    | pandas        | McKinney ch 4–7 or pandas Getting Started; write 3 cleaning functions with tests        | Functions in `src/`; tests in `tests/` pass          |
| 3    | SQL           | SQLBolt basics, selected ThoughtSpot window/join lessons; DuckDB on your CSV            | Top-N-per-group query and join-cardinality check run |
| 4    | Your dataset  | Confirm data **you** sourced; schema/source manifest and cleaning decision log          | Eight+ meaningful checks pass; log has 3+ decisions  |
| 5    | Publish       | README (question / answer / limitation); five charts; a locked run from a fresh process | Stranger can clone and reproduce                     |

New words in this chapter — array, broadcasting, dataframe, point-in-time — are explained where they
first appear below, and collected in [Terms in plain English](../README.md#glossary).

Work in the Chapter 1 project. Add the SQL, plotting and test dependencies, then commit the changed
project files:

```bash
uv add duckdb matplotlib
uv add --dev pytest
```

After writing the Week 2 tests in `tests/test_*.py`, run `uv run --locked pytest` from the project
root. Use [pytest's getting-started guide](https://docs.pytest.org/en/stable/getting-started.html)
for discovery and assertions. Keep the initial linear-algebra videos to 1–3; later lessons are
optional within the same 50-hour budget.

---

## What you will be able to do

Take a messy dataset you found yourself and turn it into a published, reproducible analysis that a
stranger can run with one command.

## What to learn

**Thinking in arrays.** You are fluent in loops. Machine learning is written in shapes and batches,
and the second dialect takes a little while. What you need is small but you need it cold: `shape`
and `dtype`, indexing and slicing, views against copies, `reshape` and `transpose`, axis semantics,
vectorising a loop into an array expression, and above all **broadcasting**.

Broadcasting deserves the extra time. It is the set of rules by which NumPy stretches a smaller
array to match a larger one's shape. A large share of the debugging you will do over the next six
months is shape errors, silent broadcasts and transposes in the wrong place.

Alongside this, watch 3Blue1Brown's
[_Essence of Linear Algebra_](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab).
Three hours of video, and it gives you one idea that pays off immediately: a matrix is a
transformation of space, not a grid of numbers to row-reduce. After that, "a layer is a linear map
followed by a nonlinearity" stops being jargon. It is worth pairing each chapter with code, though.
It is quite possible to finish the series feeling enlightened and still be unable to compute a
matrix product.

**Thinking in tables.** pandas, and the judgement that goes with it. The library is the easy half.

Alongside your notebook, record **every cleaning decision you made, what you rejected, and how the
choice would change a model downstream**. Here is an illustrative decision log; the percentages are
an example, not a published dataset:

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

That paragraph is the thing worth showing people. Anyone can call `dropna()`; the judgement is the
scarce part, and it maps directly onto "data literacy" in a hiring rubric.

The author-hosted [missing-data chapter](https://stefvanbuuren.name/fimd/sec-MCAR.html) explains why
dependence on an observed field can be consistent with MAR, and why MNAR needs sensitivity analysis.

Separate missing **features** from missing **targets**. If delivery time is the Chapter 3 target,
its eventual value and observed flag cannot be predictors at dispatch. Do not fill an unfinished
target with zero or a mean. An undelivered package still being tracked has a **right-censored**
duration: you know how long it has remained undelivered, not its eventual delivery time. Restricting
evaluation to completed deliveries can preferentially exclude the slowest ones. The
[scikit-survival introduction](https://scikit-survival.readthedocs.io/en/stable/user_guide/00-introduction.html)
explains event indicators and censoring; a survival model is optional depth, not an extra
prerequisite. For a first project, a fixed-horizon target such as “delivered within seven days” is
often easier to define. After seven days, a tracked non-delivery is negative; a lost tracking record
is still unknown. State which population and follow-up coverage your evaluation actually represents.

For a feature available before prediction, compare an appropriate imputer and missing indicator
fitted inside the training pipeline, or a model that supports that feature's missing values. Keep
the raw missingness information in your analysis either way.

**SQL.** Relational grain, joins and aggregation transfer across tools, though syntax and NULL
semantics vary by engine. Get comfortable with CTEs, window functions (`ROW_NUMBER`, `RANK`, `LAG`,
running totals), join cardinality, and point-in-time correctness.

That last one matters more than it sounds. Most serious data-leakage bugs in machine learning are,
underneath, a query that accidentally used the future.

If an assistant generates SQL, verify it against a schema you understand and a tiny table with
duplicates, NULLs and boundary dates. Plausible SQL can produce the wrong denominator without an
error.

**A schema is more than column names.** Define dtypes, units, allowed categories and missing-value
meaning. Preserve leading zeros in identifiers; choose a timezone policy; represent money with a
documented currency and rounding rule. Distinguish a zero, an unknown value and a value that is not
applicable. Recheck pandas string and nullable dtype behavior after upgrades; pandas 3.0's default
string storage uses PyArrow when installed and falls back otherwise, as the
[string migration guide](https://pandas.pydata.org/docs/user_guide/migration-3-strings.html)
explains.

Write the expected join cardinality before joining. One customer with three orders and four support
events produces twelve rows if both event tables are joined directly; summing the joined orders
inflates revenue fourfold. Aggregate each event table to the intended grain first. In pandas, use
`validate="many_to_one"` for a unique customer lookup and `indicator=True` to check unmatched rows.
Its [merge documentation](https://pandas.pydata.org/docs/reference/api/pandas.merge.html) also warns
that NULL keys on both sides match each other, unlike usual SQL joins. Test this explicitly.

**Write a data contract before training.** Name the unit of a row, its unique key, the prediction
time, the feature lookback, the outcome window, and when that outcome becomes complete. Keep both
`event_time` (when something happened) and `available_at` (when your service could first use it). A
transaction from Monday that arrived on Friday was unavailable to Tuesday's model. Historical
features must pass both clocks, and later corrections need version history.
[Feast's point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)
illustrate historical retrieval; verify availability-time handling in your own query and tool.

Some public exports contain only a current snapshot and no availability history. Record that limit;
do not invent timestamps or claim a verified historical backtest. Use small synthetic late-arrival
cases to test your join logic, and choose the Chapter 3 split whose assumptions the actual data can
support.

For a customer snapshot at time `t`, aggregate features from `[t - lookback, t)`, using records
available by `t`; construct labels from the following outcome window. An unresolved outcome is
**unknown**, not a negative. Record `label_available_at` and `outcome_observed` separately from the
planned maturity date: a window can have elapsed while its source ledger remains incomplete. At a
simulated training cutoff, use only labels whose observation window, reporting delay and actual
availability permit them. Report missing outcomes by cohort and exclusion reason; elapsed time alone
does not establish complete follow-up. Test unique keys, join row counts, timezone conversion,
missingness, late arrivals and duplicate events. Store the extraction cutoff and source version with
the data. Record permission to use the data, keep customer identifiers out of public examples, and
publish only data whose licence and permissions allow it. A reproducible synthetic example is
sufficient when the original data is private.

**Reproduction needs a data manifest.** Record the source URL or export/query version, licence,
retrieval date, extraction cutoff, raw-file checksum, schema version, code commit and environment.
Keep raw inputs immutable where permitted. Document any sampling, seeds and exclusions; use the same
population denominator in your text and charts. Run the cleaning and analysis from a new process
with the locked environment, rather than relying on the notebook's execution history. The questions
in [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) help explain who is represented and
which future uses the dataset cannot support.

If raw data is not in the repository, include its exact download/export steps and expected checksum.
The analysis should fail clearly when the documented input is missing or differs, rather than
silently analyzing a newer export.

## Resources

All 31 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [Python for Data Analysis, 3rd Edition](https://wesmckinney.com/book/) — Wes McKinney. A free
  book, 40–60 hours; chapters 4 to 8 and 10 are the ones that matter.
- [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
  — NumPy documentation contributors. Free documentation, 3–6 hours.
- [Mode / ThoughtSpot SQL Tutorial (Basic, Intermediate, Advanced)](https://www.thoughtspot.com/sql-tutorial)
  — ThoughtSpot. Free lessons; run selected exercises in DuckDB. Budget 10–15 hours for the full
  tutorial, fewer for this chapter's selections.
- [uv — official documentation](https://docs.astral.sh/uv/) — Astral maintainers. Free
  documentation, 2–4 hours; Getting Started and Projects are enough.

These reading estimates are alternatives and full-resource estimates, not hours to add together. Use
selected chapters and lessons inside the 50-hour project budget; finish the analysis before optional
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
- Five charts, each captioned with what it shows and what it does not
- A data contract covering row keys, both timestamps, feature windows, label maturity, actual
  outcome availability/coverage and permitted use
- A source manifest with immutable-input checksums, extraction cutoff and documented exclusions

Give the package an analysis entrypoint and document its exact `uv run --locked ...` command. It
must read the documented inputs and regenerate the cleaned output, summary results and five charts
without notebook state. Test `uv run --locked pytest` separately; passing tests alone does not
reproduce the analysis.

Choose a dataset that **you found yourself**: a city open-data portal, a government export, a niche
marketplace, or your own exported data from a service you use. Before Week 4, identify an outcome
you could later predict — a delay, a price, a category — and inputs available when that prediction
would be made, because [Chapter 3](../03-core-machine-learning/README.md) will ask you to model it.
State the prediction time, row/group key and feasible split in the handoff. If the dataset cannot
support a supervised question, document a necessary dataset change rather than inventing labels or
using the outcome as an input. Your own data can be useful when its export and permissions support
the project.

## Before you move on

- A stranger can install the locked environment, run the tests and regenerate your analysis with the
  documented command.
- You can defend two cleaning decisions against "why not just drop those rows?"
- You can write a top-N-per-group SQL query from memory.
- You can predict the output shape of a broadcast before running it.
- You can show that a late-arriving record and an unfinished label cannot enter a training row.
- You can distinguish a mature observed negative, a censored duration and a missing outcome, and
  explain how each enters your denominator.
- You can show that a join preserves the intended grain and explain the denominator of each chart.
- The Chapter 3 handoff names a target, prediction time, available inputs and defensible split, with
  any historical-data limits stated.

## A few things worth knowing

- **The free _Python Data Science Handbook_** at `jakevdp.github.io` is the 2016 first edition,
  written against Python 3.5. It is still widely recommended. The NumPy and matplotlib chapters are
  useful as concepts; the pandas and scikit-learn chapters teach idioms that may now raise errors or
  behave differently. Check its examples against current documentation. McKinney's book plus the
  pandas migration guides is the main route here.
- **Polars is optional.** pandas keeps this chapter aligned with its selected tutorials. Polars is a
  useful alternative when your team's stack or measured memory/runtime needs justify it;
  [scikit-learn supports Polars transformer output](https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_set_output.html).
  Rewrite one cleaning function only after the analysis works, checking correctness before speed.
- **Titanic, Iris and MNIST** are fine for a ninety-minute warm-up. As portfolio pieces they are so
  common that they tell a reviewer very little about you, which is a shame given the effort. A
  dataset you sourced yourself does much more work on your behalf.

---

[Previous: Getting oriented](../01-getting-oriented/README.md) &nbsp;·&nbsp;
[Next: Core machine learning](../03-core-machine-learning/README.md)
