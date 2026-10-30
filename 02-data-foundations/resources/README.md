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

Use Getting Started and Projects to create an environment, choose Python, add dependencies and run
code. Follow the Chapter 1 commands and commit the project files. uv manages Python dependencies and
interpreters. OS libraries, GPU drivers and some compiled scientific stacks still need
platform-specific setup. Learn what the commands do, rather than copying a speed claim or installing
every package manager.

> **Worth knowing.** Pin a supported Python version and dependency lock on purpose, and keep
> upgrades apart from reproduction runs. The [locking and syncing](#uv-locking-and-syncing) entry
> under Keep for reference explains the `--locked` check used throughout this chapter.

For Week 2 tests, pair this workflow with
[pytest's getting-started guide](https://docs.pytest.org/en/stable/getting-started.html). Install it
with `uv add --dev pytest`, keep test files in `tests/`, and run `uv run --locked pytest` from the
project root. Test small cases with known outputs before checking the full dataset.

### [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)

_NumPy documentation contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3–6
hours

Official exercises for dimensions, shape, dtype, slicing, reshaping, broadcasting and views versus
copies. Pair each concept with a small calculation, and predict its shape first. Old `np.int`,
`np.float` and `np.object` aliases expired in
[NumPy 1.24](https://numpy.org/doc/2.3/release/1.24.0-notes.html).
[NumPy 2.0](https://numpy.org/doc/stable/release/2.0.0-notes.html) brought back `np.bool` with NumPy
boolean dtype semantics, so seeing it does not by itself date a tutorial.

### [Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)

_Grant Sanderson_ &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 8–12 hours

The most valuable few hours in this chapter, and the place to start. It has 16 chapters and ~3 hours
of video (8–12 with pauses and notes). It gives you what most linear algebra courses leave out:
matrices as geometric transformations of space rather than grids of numbers to row-reduce. After
chapter 4 ('Matrix multiplication as composition') the sentence 'a neural network layer is a linear
map followed by a nonlinearity' stops being jargon. For Week 1, watch chapters 1–4. Determinants,
change of basis and eigenvectors can wait until a later chapter needs them.

> **Worth knowing.** Intuition without graded exercises. Pair each video with a small NumPy
> calculation. It is possible to finish the series and still be unable to compute a matrix product.

### [Python for Data Analysis, 3rd Edition (Open Access edition)](https://wesmckinney.com/book/)

_Wes McKinney_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40–60 hours

The pandas creator's open-access book. Read chapters 4–8 and 10 for arrays, loading, cleaning, joins
and aggregation, and use it for judgement as well as API examples. The third edition predates pandas
3.0, so read current migration guides alongside it. Its chained assignments need fixing, but an
operation using `inplace=True` is not necessarily broken or obsolete.

> **Worth knowing.** Some patterns it teaches now raise errors or behave differently in pandas 3.0.
> Read it alongside the pandas 3.0 migration guide.

### [pandas official Getting Started tutorials + "10 minutes to pandas"](https://pandas.pydata.org/docs/getting_started/index.html)

_pandas core development team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 8–15
hours

Task-based tutorials for selecting, combining, reshaping and summarising tables, with bridges from
SQL, Excel and R. Check the documentation version against your installed pandas. For the 3.0
migration, read the Copy-on-Write and string guides below. Default string storage uses PyArrow if
available and falls back otherwise, so you can use pandas 3.0 without PyArrow.

> **Worth knowing.** These docs track pandas 3.x. Any pre-3.0 tutorial found elsewhere, including
> the Python Data Science Handbook later in this list, teaches idioms 3.0 has changed or removed.

### [SQLBolt — interactive SQL lessons](https://sqlbolt.com/)

_Anonymous maintainer_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4–6 hours

In-browser exercises for SELECT, filtering, joins and aggregation. Use selected lessons as a first
pass, then write the same queries against your dataset in DuckDB. Showing you understand duplicates,
NULLs and aggregation grain matters more than lesson numbers.

> **Worth knowing.** Follow with window functions, CTEs and realistic joins. The basics alone do not
> complete this chapter's SQL work.

### [Mode / ThoughtSpot SQL Tutorial (Basic, Intermediate, Advanced)](https://www.thoughtspot.com/sql-tutorial)

_ThoughtSpot_ &nbsp;·&nbsp; Tutorial &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10–15 hours for the full
sequence

Use selected intermediate and advanced lessons for window functions, self-joins, analytical
questions and debugging wrong results. Run the exercises locally in DuckDB and check dialect
differences. Pick lessons that fit Week 3's budget, rather than treating the whole sequence as
required reading.

> **Worth knowing.** Now republished under ThoughtSpot branding, without the original interactive
> Mode query editor, so the hands-on exercises may not run as described.

### [DuckDB documentation](https://duckdb.org/docs/current/)

_Hannes Mühleisen & Mark Raasveldt; DuckDB Foundation_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp;
Free &nbsp;·&nbsp; 4–8 hours

An embedded analytical SQL engine. After `uv add duckdb`, you can query CSV, Parquet and DataFrames
without running a database server. Start with the Python client and CSV/Parquet pages. It can help
with analytical workloads that exceed a pandas workflow's memory. Measure the actual query and allow
for its memory and temporary-disk needs. SQLite is still useful for transactional SQL exercises.
Choose an engine for the question, not from a universal ranking.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [Automate the Boring Stuff with Python, 3rd edition](https://automatetheboringstuff.com/3e/)

_Al Sweigart_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 30–45 hours

The 3rd edition, published in May 2025, targets Python 3.13 and adds chapters on databases and sound
files. Excellent, but not an ML foundation: it teaches file, Excel, PDF, email and web-scraping
automation, which is a different career. If CS50P feels too dry, read chapters 1–9 (the language
fundamentals), then switch to the data stack. Sweigart says in the intro that the book targets
'office workers, administrators, academics' rather than aspiring developers. Treat the back half as
a fun optional side quest, not curriculum.

> **Worth knowing.** The landing page puts purchase links first. The chapter pages themselves are
> readable at /3e/chapterN.html.

### [CS50's Introduction to Programming with Python (CS50P)](https://cs50.harvard.edu/python/)

_David J. Malan_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 90–120 hours

A structured Python introduction with exceptions, unit tests, regular expressions and classes,
backed by graded problem sets. Choose it when Python itself is new and you want plenty of practice.
Budget its hours before this chapter's 50. Experienced Python programmers can skip it. Python for
Everybody and Think Python are alternative routes, not extra prerequisites.

### [DataLemur — SQL & data science interview practice](https://datalemur.com/)

_Nick Singh_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 15–30 hours

Optional interview practice once you can write SQL. The site offers a free tutorial and interactive
questions tagged with company names. A tag does not show how that employer interviews today. Try
timed attempts, then check your query against duplicates, NULLs and the question's assumptions. It
supports the Chapter 2 analysis without replacing its data sourcing and reproducibility work.

> **Worth knowing.** Some questions and solutions are free and others require Premium. Check the
> exercises you need before paying. Its SQL/analytics practice is the relevant part here.

### [Effective Pandas 2: Opinionated Patterns for Data Manipulation](https://store.metasnake.com/effective-pandas-book)

_Matt Harrison_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 15–25 hours

Opinionated method chaining, dtypes and replacing row-by-row loops. Read it once you have a working
analysis and can compare styles on your own functions. Copy-on-Write stops chained updates from
changing the parent frame. Other mutation and supported `inplace` operations still work. When an
older example differs, follow the official migration guide.

> **Worth knowing.** Paid, so check current book and bundle prices. Read older examples alongside
> the pandas 3.0 migration documentation.

### [GitHub Learn / GitHub Skills](https://learn.github.com/skills)

_GitHub education team_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Short hands-on modules that run inside real GitHub repos, with an automated bot giving feedback:
'Introduction to GitHub', a first pull request, GitHub Pages and Actions. The point is the
collaboration surface: forks, PRs, issues, reviews and CI. Get Git theory from Learn Git Branching.
Beginners who learn Git alone and never open a PR can reach their first job unready to work with
others. The URL moved from skills.github.com to learn.github.com/skills, and older bookmarks
redirect. Start with 'Introduction to GitHub' and the pull-request module. The Pages and Actions
modules can wait until you publish or automate something.

> **Worth knowing.** The bot checks that each step happened, not the quality of your commits or
> review comments. The module catalogue also changes. Ask a person to review one real pull request.

### [Kaggle Learn micro-courses (Python, Pandas, Data Cleaning, Data Visualization, Intro to ML)](https://www.kaggle.com/learn)

_Kaggle education team_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4–7 hours

Nothing to install: everything runs in Kaggle's hosted notebooks, with graded exercises on real
datasets, so a beginner gets practice without touching an environment. The Data Cleaning course
(missing values, scaling/normalisation, date parsing, character encodings, inconsistent text entry)
is a useful set of short drills for this chapter. These narrow exercises practise method calls. Use
McKinney and your decision log to think through why a transformation fits. Do the drills that fill a
gap in your own analysis.

> **Worth knowing.** Check the hosted notebook's pandas version before carrying an example into your
> locked local environment.

### [Learn Git Branching](https://learngitbranching.js.org/)

_Peter Cottle_ &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3–5 hours

An interactive way to practise branching, merging, rebasing and remotes. It animates the commit
graph as you type commands. It runs entirely in the browser, with no signup or install, and is
translated into many languages. The visual graph can make relationships clearer than a terminal log.
Do the Main and Remote levels. The 'Git golf' challenges are optional. Pair it with Missing
Semester's Git lecture for the underlying model, then practise on a throwaway real repo.

> **Worth knowing.** It simulates the commit graph only. There are no files, so staging, merge
> conflicts and authenticating to a real remote never come up. Practise those on the real repo.

### [marimo — reactive Python notebooks](https://marimo.io/)

_marimo team_ &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2–3 hours

An optional notebook tool that stores code as Python files and tracks cell dependencies. That helps
review and reruns dependent calculations. External files, network requests and side effects still
need their own care to be reproducible. Whichever notebook you choose, keep this chapter's source
manifest and fresh-process run. If notebook diffs or execution order cause problems, try it once the
analysis works.

> **Worth knowing.** A tool rather than a learning resource. It teaches nothing by itself and sits
> oddly in a beginner-foundations reading list.

### [Modern Polars](https://kevinheavey.github.io/modern-polars/)

_Kevin Heavey_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6–10 hours

A free side-by-side book showing the same task in idiomatic Polars and idiomatic pandas, with
commentary on API design and performance. If you already know pandas, it is one of the quickest ways
to pick up Polars, because it teaches by difference rather than from scratch. The method-chaining
and indexing chapters also make a strong free case for writing cleaner pandas, whether or not you
adopt Polars. Read it once pandas feels comfortable. Learning both APIs from cold is confusing.

> **Worth knowing.** The code is current, but the commentary dates to 2023 and some pandas-vs-Polars
> framing predates pandas 3.0. It assumes you already know pandas well, so it is not for complete
> beginners.

### [Polars User Guide](https://docs.pola.rs/user-guide/getting-started/)

_Polars documentation contributors_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp;
6–10 hours

Expressions, contexts and lazy queries for an alternative dataframe workflow. This chapter uses
pandas to match its main tutorials. Polars can be a reasonable first choice on a team already using
it. Interoperability depends on the operation, and
[scikit-learn supports Polars output](https://scikit-learn.org/stable/auto_examples/miscellaneous/plot_set_output.html),
so you may not need constant conversion. Choose after measuring correctness, memory and runtime on a
representative task.

> **Worth knowing.** Take it after pandas, not alongside.

### [Python for Everybody (PY4E)](https://www.py4e.com/)

_Charles R. Severance_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 50–70 hours

A gentle route for someone new to programming, with lessons, exercises and an author-hosted
[Python 3 book](https://www.py4e.com/book.php). Choose this or CS50P as your main introduction,
since their Python fundamentals overlap a lot. Its data examples focus on files, web data, XML/JSON
and databases, so continue with this chapter's NumPy/pandas material afterwards. Check the book
edition and examples against your installed Python. A platform's current copyright year does not
prove the text was revised.

> **Worth knowing.** Stops at basic Python plus web scraping and databases, with no NumPy, pandas or
> ML. It is a prerequisite rather than a data-foundations course, so pair it with something else.

### [The Missing Semester of Your CS Education (IAP 2026 edition)](https://missing.csail.mit.edu/)

_Anish Athalye, Jon Gjengset & Jose Javier Gonzalez Ortiz_ &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free
&nbsp;·&nbsp; 10–15 hours

Fills a gap that sinks many self-taught ML beginners: shell fluency, editors, version control,
debugging and profiling. MIT taught the course again in January 2026 and updated it substantially.
New lectures cover packaging/shipping code, code quality and agentic coding, and AI tooling now runs
through every lecture instead of sitting in one. That 2026 refresh makes it one of the few truly
current free CS courses. The older lecture on data wrangling with command-line tools is not in the
2026 syllabus, but it is still on the site under topics from previous years. At minimum, do the
Shell, Command-line Environment, Version Control (Git) and Debugging lectures. Each is ~1 hour of
video plus exercises.

> **Worth knowing.** The exercises assume a Unix-like shell. On Windows, plan to use WSL or a Linux
> virtual machine. The remaining lectures are optional for this book's path.

### [Think Python, 3rd edition (2024)](https://allendowney.github.io/ThinkPython/)

_Allen B. Downey_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 35–50 hours

A free introductory book presented as Jupyter notebooks with Colab links. Every chapter suggests
ways to use AI assistants to learn more and get help with exercises. Run and explain your own
solution before treating an assistant's feedback as proof of understanding. Use selected pages
alongside CS50P when you want a written explanation, or make it your main self-paced route if video
lectures do not suit you. For the Chapter 1 entry check, the chapters on functions, conditionals,
iteration, strings, lists, dictionaries and files matter most. The object-oriented chapters can
wait.

> **Worth knowing.** A general programming introduction that stops before NumPy and pandas, so
> continue with this chapter's data material afterwards.

## Keep for reference

Not for reading end to end. Useful to have when you need to look something up.

### [Google Colab](https://colab.research.google.com/)

_Google Research_ &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 1 hour

A quick hosted notebook with shareable links. The
[official FAQ](https://research.google.com/colaboratory/faq.html) says accelerator availability,
types and limits vary, so no particular free GPU is guaranteed. A shared notebook does not
automatically include runtime files or installed libraries. Save outputs and resumable checkpoints
elsewhere, and keep a documented local CPU route for this chapter.

> **Worth knowing.** A hosted tool, not an environment lock. Record the actual package versions and
> test the project outside the current runtime.

### [pandas 3.0 Copy-on-Write migration](https://pandas.pydata.org/docs/user_guide/copy_on_write.html)

_pandas core development team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

Copy-on-Write is the only mode in pandas 3.0. A chained update cannot change the original frame, so
use a single `.loc[...] = ...` assignment. Supported `inplace` operations still exist, but an
in-place update to a selected temporary column cannot update its parent. Read the examples and test
the result you intend. Many mutations remain valid, and not every message is a raised exception.

### [pandas 3.0 string migration guide](https://pandas.pydata.org/docs/user_guide/migration-3-strings.html)

_pandas core development team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

Default string inference, missing-value semantics and dtype checks changed. Tell inferred `str`
apart from an explicitly requested nullable `string`, and test missing values through conversion and
export. PyArrow-backed storage is used when PyArrow is installed, with a fallback otherwise. Useful
when a cleaning test changes after an environment upgrade.

### [pandas merge: NULL keys, indicators and cardinality validation](https://pandas.pydata.org/docs/reference/api/pandas.merge.html)

_pandas core development team_ &nbsp;·&nbsp; API documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1
hour

Practise `validate` and `indicator` on tiny duplicate-key examples before a real join. In pandas,
NULL keys can match each other, unlike typical SQL behaviour. Check unique lookup keys, unmatched
coverage and row counts. A many-to-many join can quietly inflate totals.

### [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)

_Timnit Gebru, Jamie Morgenstern, Briana Vecchione, Jennifer Wortman Vaughan, Hanna Wallach, Hal
Daumé III & Kate Crawford_ &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1–2 hours

Questions for documenting motivation, composition, collection, preprocessing, intended uses and
maintenance. Apply selected questions to your source manifest: who is represented, which records are
excluded, what permission exists and what claims the dataset cannot support. This established
framework is still useful alongside current tooling.

### [Pro Git, 2nd edition](https://git-scm.com/book/en/v2)

_Scott Chacon & Ben Straub_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6 hours

The official Git book, free on git-scm.com and maintained with community corrections. Use it as a
reference. Chapters 1–3 cover basics and branching. Sections 7.1–7.3 cover revision selection,
interactive staging and stashing/cleaning, and 7.7 explains reset. Chapter 6 covers GitHub, but
check its hosting instructions against today's interface. The second edition dates to 2014. Its
commit and branch concepts still hold, though Git commands and hosted workflows keep changing.
Chapter 10's internals are optional depth.

> **Worth knowing.** A 2014 book. Still one of the best free explanations of Git fundamentals
> (branching, merging, internals). The GitHub/hosting chapter is a decade behind the current
> platform UI.

### [Python Data Science Handbook (free online edition)](https://jakevdp.github.io/PythonDataScienceHandbook/)

_Jake VanderPlas_ &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 30–40 hours

Included here as a warning. It is widely recommended, and few people check the date. The free
jakevdp.github.io version is the **first** edition. Its preface carries a 2016 copyright, and the
repo README says it was written and tested against Python 3.5, with notes about Python 2.7
compatibility. That is pre-pandas-1.0, pre-CoW and pre-NumPy-2, and its scikit-learn and matplotlib
APIs have drifted. The 2nd edition (2022) is real and good but is not free at that URL. Use the free
version only as a conceptual reference for the NumPy and matplotlib chapters. For pandas, use
McKinney's open-access 3rd edition instead.

> **Worth knowing.** The linked first edition predates current string defaults and Copy-on-Write.
> Fix chained updates using current docs. `inplace` itself was not removed everywhere.

### [uv: Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)

_Astral maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The reference companion to the [uv documentation](#uv--official-documentation) entry above. Use
`uv sync --locked` and `uv run --locked ...` for a fresh-process check against the committed lock.
`--locked` checks that the lock matches project metadata and fails rather than relocking. `--frozen`
skips that check. Upgrade on purpose, then review and commit the changed lock.

> **Worth knowing.** Dependencies are one part of reproduction. Also version data, code and
> Python/platform details.

### [VS Code Data Science tutorial (Python + Jupyter extensions)](https://code.visualstudio.com/docs/datascience/data-science-tutorial)

_Microsoft VS Code documentation team_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp;
2–4 hours

Use for the Python and Jupyter extensions, notebook kernels, variables and dataframe inspection.
Select your project's `.venv` interpreter and confirm the kernel uses it. Its conda and TensorFlow
workflow is a valid alternative. Stay on this book's uv/PyTorch route rather than mixing
environments by accident. Learn modelling in Chapter 3.

> **Worth knowing.** An editor workflow, not a data contract or validation curriculum.

---

## Added for the business ML track

### [Feast — Point-in-time joins](https://docs.feast.dev/getting-started/concepts/point-in-time-joins)

_Feast maintainers_ &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; about 1 hour

Read alongside the data contract in the chapter. Build a historical feature join and test a
late-arriving event. Keep event time separate from first availability, and version later
corrections. Verify how your implementation behaves rather than assuming a feature store infers the
missing timestamps.

The [business ML delivery plan](../../09-business-machine-learning/delivery-plan.md) adds snapshot
keys, outcome maturity, exposure/assignment logging and reproducible contracts.

Pair the timestamp exercise with the
[scikit-survival introduction](https://scikit-survival.readthedocs.io/en/stable/user_guide/00-introduction.html)
when the target is a duration. Record event status and follow-up time. An unfinished delivery is not
a zero-duration example. This is optional reading on censoring. You do not need to fit a survival
model inside the chapter's 50 hours.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
