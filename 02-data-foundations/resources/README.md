# Resources — Chapter 2: Data foundations

Everything referenced in [the chapter](../README.md), grouped by how central it is, with a short
note on what each one is for.

Prices and free tiers change often, so check a resource's own page before you plan around one.

**Browse:** [Start here](#start-here) &nbsp;·&nbsp; [Optional depth](#optional-depth) &nbsp;·&nbsp;
[Keep for reference](#keep-for-reference) &nbsp;·&nbsp;
[Added for the business ML track](#added-for-the-business-ml-track)

---

## Start here

The resources on the main path for this chapter, in the order the chapter uses them. If you only do
a few things, do these.

### [uv — official documentation](https://docs.astral.sh/uv/)

_Astral maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–4 hours

Use Getting Started and Projects to create an environment, select Python, add dependencies and run
code. Follow the Chapter 1 commands and commit the project files. uv manages Python dependencies and
interpreters; OS libraries, GPU drivers and some compiled scientific stacks still need
platform-specific setup. Learn what the commands do rather than copying a speed claim or installing
every package manager.

> **Worth knowing.** Deliberately pin a supported Python version and dependency lock. Upgrade
> separately from a reproduction run.

For Week 2 tests, pair this workflow with
[pytest's getting-started guide](https://docs.pytest.org/en/stable/getting-started.html): install it
with `uv add --dev pytest`, keep test files in `tests/`, and run `uv run --locked pytest` from the
project root. Test small cases with known outputs before checking the full dataset.

### [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)

_NumPy documentation contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3–6
hours

Official exercises for dimensions, shape, dtype, slicing, reshaping, broadcasting and views versus
copies. Pair each concept with a small calculation whose shape you predict first. Old `np.int`,
`np.float` and `np.object` aliases expired in
[NumPy 1.24](https://numpy.org/doc/2.3/release/1.24.0-notes.html);
[NumPy 2.0](https://numpy.org/doc/stable/release/2.0.0-notes.html) reintroduced `np.bool` with NumPy
boolean dtype semantics. Its presence alone does not identify an obsolete tutorial.

### [Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)

_Grant Sanderson_ &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 8–12 hours

The highest-leverage few hours in this chapter, and the place to start. 16 chapters, ~3 hours of
video (8–12 with pauses and notes), and it gives you the one thing most linear algebra courses never
do: matrices as geometric transformations of space rather than grids of numbers to row-reduce. After
chapter 4 ('Matrix multiplication as composition') the sentence 'a neural network layer is a linear
map followed by a nonlinearity' stops being jargon.

### [Python for Data Analysis, 3rd Edition (Open Access edition)](https://wesmckinney.com/book/)

_Wes McKinney_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40–60 hours

The pandas creator's open-access book. Select chapters 4–8 and 10 for arrays, loading, cleaning,
joins and aggregation; use it for judgement as well as API examples. The third edition predates
pandas 3.0, so read current migration guides alongside it. Chained assignment needs correction; an
operation using `inplace=True` is not necessarily broken or obsolete.

> **Worth knowing.** Predates pandas 3.0 — some patterns it teaches now raise errors or behave
> differently, so read it alongside the pandas 3.0 migration guide.

### [pandas official Getting Started tutorials + "10 minutes to pandas"](https://pandas.pydata.org/docs/getting_started/index.html)

_pandas core development team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 8–15
hours

Task-shaped tutorials for selecting, combining, reshaping and summarising tables, with bridges from
SQL, Excel and R. Check the documentation version against your installed pandas. For 3.0 migration,
read the Copy-on-Write and string guides below; default string storage uses PyArrow if available and
has a fallback, so PyArrow is not required merely to use pandas 3.0.

> **Worth knowing.** These docs track pandas 3.x, so any pre-3.0 pandas tutorial found elsewhere —
> including the Python Data Science Handbook later in this list — teaches idioms 3.0 has changed or
> removed.

### [SQLBolt — interactive SQL lessons](https://sqlbolt.com/)

_Anonymous maintainer_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4–6 hours

In-browser exercises for SELECT, filtering, joins and aggregation. Use selected lessons as a first
pass, then write the same queries against your dataset in DuckDB. Lesson numbering is less useful
than proving that you understand duplicates, NULLs and aggregation grain.

> **Worth knowing.** Follow with window functions, CTEs and realistic joins; these basics alone do
> not complete this chapter's SQL work.

### [Mode / ThoughtSpot SQL Tutorial (Basic, Intermediate, Advanced)](https://www.thoughtspot.com/sql-tutorial)

_ThoughtSpot_ &nbsp;·&nbsp; Tutorial &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10–15 hours for the full
sequence

Use selected intermediate and advanced lessons for window functions, self-joins, analytical
questions and debugging incorrect results. The republished tutorial does not supply the original
Mode query editor; run exercises locally in DuckDB and check dialect differences. Fit selections to
Week 3's budget instead of treating the whole sequence as required reading.

> **Worth knowing.** Now republished under ThoughtSpot branding; the original interactive Mode query
> editor is not part of it, so the hands-on exercises may not run as described.

### [DuckDB documentation](https://duckdb.org/docs/current/)

_Hannes Mühleisen & Mark Raasveldt; DuckDB Foundation_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp;
Free &nbsp;·&nbsp; 4–8 hours

An embedded analytical SQL engine: `uv add duckdb`, then query CSV, Parquet and DataFrames without
running a database server. Start with the Python client and CSV/Parquet pages. It can help with
analytical workloads that exceed a pandas workflow's memory, but measure the particular query and
account for its memory and temporary-disk needs. SQLite remains useful for transactional SQL
exercises; choose an engine for the question rather than a universal ranking.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [Automate the Boring Stuff with Python, 3rd edition](https://automatetheboringstuff.com/3e/)

_Al Sweigart_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 30–45 hours

3rd edition published May 2025, targets Python 3.13, adds new chapters on databases and sound files.
Genuinely excellent and genuinely not an ML foundation — it teaches
file/Excel/PDF/email/web-scraping automation, which is a different career. Read chapters 1–9 (the
language fundamentals) if CS50P feels too dry, then stop and switch to the data stack. Sweigart
himself says in the intro the book targets 'office workers, administrators, academics' rather than
aspiring developers. Treat the back half as a fun optional side quest, not curriculum.

> **Worth knowing.** The landing page foregrounds purchase links; the chapter pages themselves are
> readable at /3e/chapterN.html.

### [CS50's Introduction to Programming with Python (CS50P)](https://cs50.harvard.edu/python/)

_David J. Malan_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 90–120 hours

A structured Python introduction with exceptions, unit tests, regular expressions and classes,
supported by graded problem sets. Choose it when Python itself is new and you want substantial
practice. Budget its hours before this chapter's 50; experienced Python programmers can skip it.
Python for Everybody and Think Python are alternative routes, rather than additional prerequisites.

### [DataLemur — SQL & data science interview practice](https://datalemur.com/)

_Nick Singh_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 15–30 hours

Optional interview practice once you can write SQL. The site offers a free tutorial and interactive
questions with company attributions; those attributions do not establish any employer's current
interview format. Use timed attempts, then check your query against duplicates, NULLs and the
question's assumptions. This complements the Chapter 2 analysis rather than replacing its data
sourcing and reproducibility work.

> **Worth knowing.** Some questions and solutions are publicly accessible; others require Premium.
> Check the exercises you need before paying. Its SQL/analytics practice is the relevant part here.

### [Effective Pandas 2: Opinionated Patterns for Data Manipulation](https://store.metasnake.com/effective-pandas-book)

_Matt Harrison_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 15–25 hours

Opinionated method chaining, dtypes and replacing row-by-row loops. Read after you have a working
analysis and can compare styles on your own functions. Copy-on-Write prevents chained updates from
mutating the parent frame; it does not prohibit mutation or supported `inplace` operations. The
official migration guide takes precedence when an older example differs.

> **Worth knowing.** Paid; check current book and bundle prices. Read older examples alongside
> pandas 3.0 migration documentation.

### [GitHub Learn / GitHub Skills](https://learn.github.com/skills)

_GitHub education team_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Short hands-on modules that run inside real GitHub repos with an automated bot giving feedback —
'Introduction to GitHub', first pull request, GitHub Pages, Actions. The point is not Git theory
(get that from Learn Git Branching) but the collaboration surface: forks, PRs, issues, reviews, CI.
Beginners who learn Git in isolation and never open a PR arrive at their first job unable to work
with anyone. Note the URL moved from skills.github.com to learn.github.com/skills, so older
bookmarks redirect.

### [Kaggle Learn micro-courses (Python, Pandas, Data Cleaning, Data Visualization, Intro to ML)](https://www.kaggle.com/learn)

_Kaggle education team_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4–7 hours

Zero-install: everything runs in Kaggle's hosted notebooks with graded exercises against real
datasets, so a beginner gets reps without touching an environment. The Data Cleaning course (missing
values, scaling/normalisation, date parsing, character encodings, inconsistent text entry) is the
best free treatment of that specific topic anywhere and is the one not to skip. That said, these are
deliberately shallow API tours — they teach which method to call, not why. They are excellent reps
and a poor primary curriculum. Use them as drills between chapters of McKinney.

> **Worth knowing.** Check the hosted notebook's pandas version before carrying an example into your
> locked local environment.

### [Learn Git Branching](https://learngitbranching.js.org/)

_Peter Cottle_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3–5 hours

The only Git resource that makes branching, merging, rebasing and remotes click, because it animates
the commit graph as you type real commands. Entirely client-side, no signup, no install, translated
into many languages. Git's mental model is a directed graph and every text tutorial fails to convey
that; this one shows it. Do the Main levels and the Remote levels; the 'Git golf' challenges are
optional fun. Pair it with Missing Semester's Git lecture (theory) — this one supplies the muscle
memory.

### [marimo — reactive Python notebooks](https://marimo.io/)

_marimo team_ &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

An optional notebook tool storing code as Python files and tracking reactive cell dependencies. That
helps review and rerunning dependent calculations; it does not make external files, network requests
or side effects reproducible automatically. Keep this chapter's source manifest and fresh-process
run whichever notebook interface you choose. Try it after the analysis works if notebook diffs or
execution order are causing problems.

> **Worth knowing.** A tool rather than a learning resource — it teaches nothing by itself and sits
> oddly in a beginner-foundations reading list.

### [Modern Polars](https://kevinheavey.github.io/modern-polars/)

_Kevin Heavey_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6–10 hours

A free side-by-side book showing the same task in idiomatic Polars and idiomatic pandas, with
commentary on API design and performance. This is the most efficient possible way for someone who
already knows pandas to pick up Polars, because it teaches by diff rather than from scratch. The
method-chaining and indexing chapters are also the best free argument for writing cleaner pandas,
regardless of whether you ever adopt Polars. Read it only once pandas feels comfortable — reading
both APIs cold will just confuse you.

> **Worth knowing.** Code is current, but the commentary dates to 2023 and some pandas-vs-Polars
> framing predates pandas 3.0. It assumes prior pandas fluency, so it is not an absolute-beginner
> resource.

### [Polars User Guide](https://docs.pola.rs/user-guide/getting-started/)

_Polars documentation contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp;
6–10 hours

Expressions, contexts and lazy queries for an alternative dataframe workflow. This chapter chooses
pandas to match its main tutorials; Polars can be a reasonable first choice on a team already using
it. Interoperability varies by downstream operation, and
[scikit-learn supports Polars output](https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_set_output.html),
so constant conversion is not inevitable. Choose after measuring correctness, memory and runtime on
a representative task.

> **Worth knowing.** Take it after pandas, not alongside.

### [Python for Everybody (PY4E)](https://www.py4e.com/)

_Charles R. Severance_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 50–70 hours

A gentle route for someone new to programming, with lessons, exercises and an author-hosted
[Python 3 book](https://www.py4e.com/book.php). Choose this or CS50P as your main introductory
route; their Python fundamentals overlap substantially. Its data examples emphasize files, web data,
XML/JSON and databases, so continue with the NumPy/pandas material in this chapter afterwards. Check
the particular book edition and examples against your installed Python rather than assuming a
platform's current copyright year identifies a revised text.

> **Worth knowing.** Stops at basic Python plus web scraping and databases, with no numpy, pandas or
> ML — a prerequisite rather than a data-foundations course. Pair it with something else.

### [The Missing Semester of Your CS Education (IAP 2026 edition)](https://missing.csail.mit.edu/)

_Anish Athalye, Jon Gjengset & Jose Javier Gonzalez Ortiz_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 10–15 hours

Fills the exact gap that sinks self-taught ML beginners: shell fluency, editors, version control,
debugging and profiling. The older lecture on data wrangling with command-line tools is not in the
2026 syllabus, but it is still on the site under topics from previous years. MIT re-taught the
course in January 2026 and materially updated it — new lectures on packaging/shipping code, code
quality, and agentic coding, with AI tooling folded into every lecture rather than quarantined into
one. That 2026 refresh makes it one of the few genuinely current free CS courses. Do the Shell,
Command-line Environment, Version Control (Git) and Debugging lectures at minimum; each is ~1 hour
of video plus exercises.

### [Think Python, 3rd edition (2024)](https://allendowney.github.io/ThinkPython/)

_Allen B. Downey_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 35–50 hours

A free introductory book presented as Jupyter notebooks with Colab links. Every chapter includes
suggestions for using assistants to learn more and get help with exercises. Run and explain your own
solution before treating assistant feedback as evidence of understanding. Use selected pages
alongside CS50P when you need a written explanation, or choose it as the main self-paced route if
video lectures do not suit you.

## Keep for reference

Not for reading end to end. Useful to have when you need to look something up.

### [Google Colab](https://colab.research.google.com/)

_Google Research_ &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 1 hour

A quick hosted notebook with shareable links. The
[official FAQ](https://research.google.com/colaboratory/faq.html) says accelerator availability,
types and limits vary; a particular free GPU is not guaranteed. Runtime files and installed
libraries are not automatically included in a shared notebook. Save outputs and resumable
checkpoints externally, and keep a documented local CPU route for this chapter.

> **Worth knowing.** A hosted tool, not an environment lock. Record the actual package versions and
> test the project outside the current runtime.

### [pandas 3.0 Copy-on-Write migration](https://pandas.pydata.org/docs/user_guide/copy_on_write.html)

_pandas core development team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

Copy-on-Write is the only mode in pandas 3.0. A chained update cannot modify the original frame; use
a single `.loc[...] = ...` assignment. Supported `inplace` operations still exist, while an in-place
update to a selected temporary column cannot update its parent. Read the examples and test the
intended result instead of treating every mutation as invalid or every message as a raised
exception.

### [pandas 3.0 string migration guide](https://pandas.pydata.org/docs/user_guide/migration-3-strings.html)

_pandas core development team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

Default string inference, missing-value semantics and dtype checks changed. Distinguish inferred
`str` from explicitly requested nullable `string`, and test missing values through conversion and
export. PyArrow-backed storage is used when PyArrow is installed; there is a fallback. Useful when a
cleaning test changes after an environment upgrade.

### [pandas merge: NULL keys, indicators and cardinality validation](https://pandas.pydata.org/docs/reference/api/pandas.merge.html)

_pandas core development team_ &nbsp;·&nbsp; API documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1
hour

Practise `validate` and `indicator` on tiny duplicate-key examples before a real join. NULL keys can
match each other in pandas, unlike typical SQL behavior. Check unique lookup keys, unmatched
coverage and row counts; a many-to-many join can silently inflate totals.

### [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)

_Timnit Gebru, Jamie Morgenstern, Briana Vecchione, Jennifer Wortman Vaughan, Hanna Wallach, Hal
Daumé III & Kate Crawford_ &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Questions for documenting motivation, composition, collection, preprocessing, intended uses and
maintenance. Apply selected questions to your source manifest: who is represented, which records are
excluded, what permission exists and what claims the dataset cannot support. This established
framework remains useful alongside current tooling.

### [Pro Git, 2nd edition](https://git-scm.com/book/en/v2)

_Scott Chacon & Ben Straub_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6 hours

The official Git book, free on git-scm.com and maintained with community corrections. Use as a
reference: chapters 1–3 cover basics and branching; 7.1–7.3 cover revision selection, interactive
staging, and stashing/cleaning; 7.7 explains reset. Chapter 6 covers GitHub, but check its hosting
instructions against today's interface. The second edition dates to 2014; its commit and branch
concepts remain useful without implying that Git commands or hosted workflows have stopped changing.
Chapter 10's internals are optional depth.

> **Worth knowing.** A 2014 book. Still the best free explanation of git fundamentals — branching,
> merging, internals — but the GitHub/hosting chapter is a decade behind current platform UI.

### [Python Data Science Handbook (free online edition)](https://jakevdp.github.io/PythonDataScienceHandbook/)

_Jake VanderPlas_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 30–40 hours

Included here as a warning. Everyone recommends this and almost nobody checks the date: the free
jakevdp.github.io version is the **first** edition — its preface carries a 2016 copyright and the
repo README states it was written and tested against Python 3.5, with notes about Python 2.7
compatibility. That is pre-pandas-1.0, pre-CoW, pre-NumPy-2, and its scikit-learn and matplotlib
APIs have drifted. The 2nd edition (2022) is real and good but is not free at that URL. Use the free
version only as a conceptual reference for the NumPy and matplotlib chapters, and use McKinney's
open-access 3rd edition as your actual pandas text instead.

> **Worth knowing.** The linked first edition predates current string defaults and Copy-on-Write.
> Correct chained updates using current docs; `inplace` itself was not universally removed.

### [uv: Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)

_Astral maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

Use `uv sync --locked` and `uv run --locked ...` for a fresh-process check against the committed
lock. `--locked` verifies consistency with project metadata and fails rather than relocking;
`--frozen` skips that check. Upgrade deliberately, then review and commit the changed lock.

> **Worth knowing.** Dependencies are one part of reproduction; also version data, code and the
> Python/platform details.

### [VS Code Data Science tutorial (Python + Jupyter extensions)](https://code.visualstudio.com/docs/datascience/data-science-tutorial)

_Microsoft VS Code documentation team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp;
2–4 hours

Use for the Python and Jupyter extensions, notebook kernels, variables and dataframe inspection.
Select your project's `.venv` interpreter and verify the kernel uses it. Its conda and TensorFlow
workflow is a valid alternative; keep this book's uv/PyTorch route consistent rather than mixing
environments accidentally. Learn modelling in Chapter 3.

> **Worth knowing.** An editor workflow, not a data contract or validation curriculum.

---

## Added for the business ML track

### [Feast — Point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)

_Feast maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

Read alongside the data contract in the chapter. Build a historical feature join and test a
late-arriving event. Distinguish event time from first availability and version later corrections;
verify your implementation's semantics rather than assuming a feature store infers the missing
timestamps.

The [business ML delivery plan](../../09-business-machine-learning/delivery-plan.md) adds snapshot
keys, outcome maturity, exposure/assignment logging and reproducible contracts.

Pair the timestamp exercise with the
[scikit-survival introduction](https://scikit-survival.readthedocs.io/en/stable/user_guide/00-introduction.html)
when the target is a duration. Record event status and follow-up time; an unfinished delivery is not
a zero-duration example. This is an optional explanation of censoring, not a requirement to fit a
survival model inside the chapter's 50 hours.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
