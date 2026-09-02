# Chapter 2: Data foundations

**Weeks 1-5 &nbsp;·&nbsp; about 50 hours.** &nbsp;·&nbsp; [Index](../README.md) &nbsp;·&nbsp; [Resources for this chapter](resources/README.md)

**The short version.** You already program; this chapter teaches the data dialect — arrays and shapes, dataframes and cleaning judgement, and enough SQL to be trusted with real data. You finish by publishing a small, reproducible analysis of a dataset you found yourself, which becomes the seed of everything you build later.

**This dataset carries forward.** Chapter 3 models it. Chapter 5 can use documents in the same domain. Do not switch datasets mid-book unless you must.

---

## Your five-week plan

About ten hours a week. Each week ends with something on GitHub.

| Week | Focus | Do this | Done when |
|---|---|---|---|
| 1 | Setup + NumPy | uv project; NumPy basics; start 3Blue1Brown Essence of Linear Algebra (1-3 videos) | `arr.shape` and broadcasting exercises work |
| 2 | pandas | McKinney ch 4-7 or pandas Getting Started; write 3 cleaning functions with tests | Functions + tests in `src/` |
| 3 | SQL | SQLBolt 1-13, then ThoughtSpot tutorial; DuckDB on your CSV | Top-N-per-group query runs |
| 4 | Your dataset | Find data **you** sourced (city portal, export, scrape); cleaning decision log | Eight+ tests pass; log has 3+ decisions |
| 5 | Publish | README (question / answer / limitation); five charts; `uv run` reproduces | Stranger can clone and reproduce |

New words in this chapter — array, broadcasting, dataframe, point-in-time — are explained where
they first appear below, and collected in [Terms in plain English](../README.md#glossary).

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

Alongside this, watch 3Blue1Brown's [*Essence of Linear Algebra*](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab). Three hours of video, and it gives
you one idea that pays off immediately: a matrix is a transformation of space, not a grid of numbers
to row-reduce. After that, "a layer is a linear map followed by a nonlinearity" stops being jargon.
It is worth pairing each chapter with code, though. It is quite possible to finish the series
feeling enlightened and still be unable to compute a matrix product.

**Thinking in tables.** pandas, and the judgement that goes with it. The library is the easy half.

The valuable output of this chapter is not a notebook. It is a short document recording **every
cleaning decision you made, what you rejected, and how the choice would change a model downstream**.
Something like this:

```markdown
## delivery_time — 8.2% missing
Pattern: missingness correlates with carrier == "regional" (34% missing) against 0.4%
for national. This is not missing at random; the regional carrier's API does not report it.
Rejected: mean imputation. It would smear the national distribution across regional rows
          and hide the fact that we simply do not observe this segment.
Rejected: dropping the rows. It removes 8% of the data, and non-randomly.
Chose:    keep the nulls, add an explicit delivery_time_observed flag, and let a tree model
          split on it. Recorded as a known limitation.
Impact:   this analysis cannot make claims about regional carrier timing.
```

That paragraph is the thing worth showing people. Anyone can call `dropna()`; the judgement is the
scarce part, and it maps directly onto "data literacy" in a hiring rubric.

**SQL.** The lowest-churn skill in this entire book. The SQL you learn now will still be correct
in fifteen years, which is not true of any Python library here, and it is the thing people moving
into data roles most often under-invest in. Get comfortable with CTEs, window functions
(`ROW_NUMBER`, `RANK`, `LAG`, running totals), join cardinality, and point-in-time correctness.

That last one matters more than it sounds. Most serious data-leakage bugs in machine learning are,
underneath, a query that accidentally used the future.

LLMs write SQL well now, and that changes less than you might expect: you still have to read,
verify and debug the result against a schema you understand, and interviews still test it live.

## Resources

All 27 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [Python for Data Analysis, 3rd Edition](https://wesmckinney.com/book/) — Wes McKinney. A free book, 40-60 hours; chapters 4 to 8 and 10 are the ones that matter.
- [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy documentation contributors. Free documentation, 3-6 hours.
- [Mode / ThoughtSpot SQL Tutorial (Basic, Intermediate, Advanced)](https://www.thoughtspot.com/sql-tutorial) — ThoughtSpot. A free interactive tutorial, 10-15 hours.
- [uv — official documentation](https://docs.astral.sh/uv/) — Charlie Marsh. Free documentation, 2-4 hours; the Getting Started and Projects pages are enough.

If Python is not yet one of your languages, do [CS50P](https://cs50.harvard.edu/python/) first.
Its 90 to 120 hours sit on top of this chapter's 50, not inside them, and the chapter will make
much more sense afterwards.

## What to build

**A published data product.** A public repository containing:

- A README stating the question in one sentence, the answer in one sentence, and the limitation in
  one sentence
- `pyproject.toml` and `uv.lock`, so anyone can reproduce it in one command
- A `src/` package with your cleaning functions, not just a notebook
- At least eight tests over those functions
- Your cleaning decision log
- Five charts, each captioned with what it shows and what it does not

Choose a dataset that **you found yourself**: a city open-data portal, a government export, a niche
marketplace, or your own exported data from a service you use. Prefer one with an outcome you could
later predict — a delay, a price, a category — because [Chapter 3](../03-core-machine-learning/README.md)
will ask you to model it. Your own data works especially well.
You will hit real date parsing, timezone problems and ragged JSON, and you will care enough to
finish.

## Before you move on

- A stranger can clone the repository and reproduce your result with one command.
- You can defend two cleaning decisions against "why not just drop those rows?"
- You can write a top-N-per-group SQL query from memory.
- You can predict the output shape of a broadcast before running it.

## A few things worth knowing

- **The free *Python Data Science Handbook*** at `jakevdp.github.io` is the 2016 first edition,
  written against Python 3.5. It is still widely recommended. The NumPy and matplotlib chapters are
  useful as concepts; the pandas and scikit-learn chapters will teach you idioms that now raise
  errors. Wes McKinney's [*Python for Data Analysis*](https://wesmckinney.com/book/), free on his own site,
  is the better choice.
- **Polars can wait.** It is a good library, but scikit-learn, Hugging Face datasets, seaborn and
  effectively every tutorial speak pandas. Learning Polars first means constant conversion and an
  inability to follow along. If you want a taste, rewrite one cleaning function in it once the pandas version works — optional, and strictly second.
- **Titanic, Iris and MNIST** are fine for a ninety-minute warm-up. As portfolio pieces they are so
  common that they tell a reviewer very little about you, which is a shame given the effort. A
  dataset you sourced yourself does much more work on your behalf.

---

[Previous: Getting oriented](../01-getting-oriented/README.md) &nbsp;·&nbsp; [Next: Core machine learning](../03-core-machine-learning/README.md)
