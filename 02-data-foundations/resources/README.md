# Resources — Chapter 2: Data foundations

Everything referenced in [the chapter](../README.md), grouped by how central it is, with a short
note on what each one is for.

Prices and free tiers change often, so check a resource's own page before you plan around one.

---

## Start here

The resources on the main path for this chapter, in the order the chapter uses them. If you only do a few things, do these.

### [uv — official documentation](https://docs.astral.sh/uv/)

*Charlie Marsh* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2-4 hours

The clear answer to the 2026 environment question. One Rust binary that replaces pip, pip-tools, pipx, poetry, pyenv, twine and virtualenv, installs Python interpreters itself, and resolves 10-100x faster than pip. For a beginner this collapses the single biggest early-quitting hazard — 'I spent a weekend and still can't install pandas' — into four commands: `uv python install 3.14`, `uv init`, `uv add pandas numpy jupyterlab`, `uv run`. Read Getting Started + the Projects guide only; skip workspaces. Two honest caveats: uv has not hit 1.0 (0.12.x as of September 2026), and it does not replace conda for CUDA/GDAL/compiled scientific stacks.

> **Worth knowing.** The docs still brand uv as backed by Astral with no mention of the OpenAI agreement, so post-deal governance and stewardship are not yet reflected there.

### [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)

*NumPy documentation contributors* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3-6 hours

Current for NumPy 2.5. Short, official, and covers exactly the things that later bite you in PyTorch: ndim/shape/dtype, slicing, reshape/transpose, broadcasting, and copies-vs-views. Broadcasting in particular is the concept that makes tensor code readable — spend disproportionate time there. Note: any tutorial using `np.float`, `np.int`, `np.object` or `np.bool` aliases is pre-NumPy-2.0 (removed) and should be treated as stale. You need far less NumPy than people think — one focused afternoon plus this page is enough before starting scikit-learn.

### [Essence of Linear Algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)

*Grant Sanderson* &nbsp;·&nbsp; Video &nbsp;·&nbsp; Free &nbsp;·&nbsp; 8-12 hours

The highest-leverage few hours in this chapter, and the place to start. 16 chapters, ~3 hours of video (8-12 with pauses and notes), and it gives you the one thing most linear algebra courses never do: matrices as geometric transformations of space rather than grids of numbers to row-reduce. After chapter 4 ('Matrix multiplication as composition') the sentence 'a neural network layer is a linear map followed by a nonlinearity' stops being jargon.

### [Python for Data Analysis, 3rd Edition (Open Access edition)](https://wesmckinney.com/book/)

*Wes McKinney* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 40-60 hours

Written by the person who created pandas, free in full on his own site, and the canonical text for the pandas + NumPy layer. This is the single highest-value book in the entire foundations track. Do chapters 4 (NumPy basics), 5 (pandas intro), 6 (data loading), 7 (data cleaning), 8 (join/combine/reshape), 10 (groupby) — that is ~80% of everything you will actually do in an ML job. Note: published Aug 2022 against pandas 1.x/2.x, so its `inplace=` and chained-assignment examples predate pandas 3.0 Copy-on-Write; read the pandas 3.0 release notes alongside it. Errata are fixed periodically on the site.

> **Worth knowing.** Predates pandas 3.0 — some patterns it teaches now raise errors or behave differently, so read it alongside the pandas 3.0 migration guide.

### [pandas official Getting Started tutorials + "10 minutes to pandas"](https://pandas.pydata.org/docs/getting_started/index.html)

*pandas core development team* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 8-15 hours

Currently documents pandas 3.0.6 — the **only** beginner-facing pandas material guaranteed to be correct for Copy-on-Write and PyArrow-backed string dtype. Ten task-shaped tutorials ('How do I select a subset of a DataFrame?', 'How to combine data from multiple tables'), plus comparison guides from SQL, Excel and R that are the fastest bridge if you already think in spreadsheets. Use this as the version-of-record to sanity-check anything you read in an older book or blog post. Read it after McKinney's chapters, not instead of them — the docs teach the API, McKinney teaches the judgment.

> **Worth knowing.** These docs track pandas 3.x, so any pre-3.0 pandas tutorial found elsewhere — including the Python Data Science Handbook later in this list — teaches idioms 3.0 has changed or removed.

### [SQLBolt — interactive SQL lessons](https://sqlbolt.com/)

*Anonymous maintainer* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-6 hours

18 lessons plus intermediate topics, all in-browser with a live query engine and no signup, no email wall, no upsell. It is the fastest way to go from zero SQL to writing joins and aggregates in one afternoon, which is why it survives despite being the only resource here without an identifiable expert author (last copyright refresh 2024). Do lessons 1-13 (SELECT through joins and aggregates, then a first INSERT) in one sitting, then move to a real engine.

> **Worth knowing.** Stale (2024 copyright, no visible maintenance) and anonymous. Window functions, CTEs and analytic SQL are thin to absent — a 60-minute on-ramp, not sufficient SQL preparation for an AI/ML data role.

### [Mode / ThoughtSpot SQL Tutorial (Basic, Intermediate, Advanced)](https://www.thoughtspot.com/sql-tutorial)

*ThoughtSpot* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-15 hours

The best free SQL curriculum written by working analysts rather than by a course company — it teaches SQL the way an analyst actually uses it (exploring an unfamiliar table, debugging a wrong number, performance tuning) and includes the window functions, CTEs and self-joins SQLBolt skips. ThoughtSpot acquired Mode for $200M and has kept the tutorial live and free at mode.com/sql-tutorial (now redirecting to thoughtspot.com/sql-tutorial), copyright refreshed to 2026. Do this immediately after SQLBolt; together they are a complete beginner SQL education.

> **Worth knowing.** Now republished under ThoughtSpot branding; the original interactive Mode query editor is not part of it, so the hands-on exercises may not run as described.

### [DuckDB documentation](https://duckdb.org/docs/current/)

*Hannes Mühleisen & Mark Raasveldt; DuckDB Foundation* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-8 hours

The 2026 answer to 'how do I practice real SQL without installing a database?' — `pip install duckdb` (or `uv add duckdb`) and you can immediately run full analytical SQL, including window functions and CTEs, directly against CSV and Parquet files and against pandas/Polars DataFrames, in-process, no server, no Docker. This is a strictly better beginner SQL sandbox than SQLite and it doubles as the escape hatch when a dataset stops fitting in pandas. Read the Python client API and the CSV/Parquet import pages. Do not learn it before SQL itself — it is the practice environment, not the curriculum.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [Automate the Boring Stuff with Python, 3rd edition](https://automatetheboringstuff.com/3e/)

*Al Sweigart* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 30-45 hours

3rd edition published May 2025, targets Python 3.13, adds new chapters on databases and sound files. Genuinely excellent and genuinely not an ML foundation — it teaches file/Excel/PDF/email/web-scraping automation, which is a different career. Read chapters 1-9 (the language fundamentals) if CS50P feels too dry, then stop and switch to the data stack. Sweigart himself says in the intro the book targets 'office workers, administrators, academics' rather than aspiring developers. Treat the back half as a fun optional side quest, not curriculum.

> **Worth knowing.** The landing page foregrounds purchase links; the chapter pages themselves are readable at /3e/chapterN.html.

### [CS50's Introduction to Programming with Python (CS50P)](https://cs50.harvard.edu/python/)

*David J. Malan* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 90-120 hours

The single best rigor-per-hour intro to Python that exists, and the only free beginner course that makes you write unit tests (pytest), handle exceptions properly, and use regex and OOP. Its problem sets are auto-graded with real edge cases, which forces you to practise debugging in a way gentler courses do not. Choose this over Python for Everybody if you have the discipline for a course that will actually fail your submissions. Weeks 0-8 are the mandatory part; the final project is optional for an ML path. If Python is not yet one of your languages, do this first, before touching NumPy or pandas — and budget its hours on top of the chapter's 50. If Python is already yours, skip it entirely.

### [DataLemur — SQL & data science interview practice](https://datalemur.com/)

*Nick Singh* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 15-30 hours

Where you go once you can write SQL and need to get fast at it. Free tier includes a full SQL tutorial and a substantial bank of real questions sourced from Meta/Amazon/Google/Netflix loops, with in-browser execution against realistic schemas. Value here is calibration — you find out whether your SQL is job-grade or tutorial-grade. Not a beginner's first stop and not necessary for ML per se; it is necessary if the goal is a data/ML job in the next 12 months. Skip the paid tier until you have an interview scheduled.

> **Worth knowing.** Freemium, not free: many questions and all solutions sit behind DataLemur Premium. It is a SQL/analytics interview trainer with only marginal ML content.

### [Effective Pandas 2: Opinionated Patterns for Data Manipulation](https://store.metasnake.com/effective-pandas-book)

*Matt Harrison* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 15-25 hours

The one paid book worth naming here. Where McKinney teaches you what pandas can do, Harrison teaches you which 20% to actually use and how to chain it — method chaining, avoiding `inplace`, correct dtypes, and killing the loop-over-rows habit. Its central thesis (chain, never mutate) happens to be exactly the style pandas 3.0's Copy-on-Write now enforces, which makes it more relevant in 2026 than when it was written, not less. Buy it only after you have written pandas for a few weeks and can feel your own code getting ugly; buying it first wastes it.

> **Worth knowing.** Paid: $49 for the book, $99 and $249 for bundles. Targets pandas 2, not pandas 3.

### [GitHub Learn / GitHub Skills](https://learn.github.com/skills)

*GitHub education team* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1-2 hours

Short hands-on modules that run inside real GitHub repos with an automated bot giving feedback — 'Introduction to GitHub', first pull request, GitHub Pages, Actions. The point is not Git theory (get that from Learn Git Branching) but the collaboration surface: forks, PRs, issues, reviews, CI. Beginners who learn Git in isolation and never open a PR arrive at their first job unable to work with anyone. Note the URL moved from skills.github.com to learn.github.com/skills, so older bookmarks redirect.

### [Kaggle Learn micro-courses (Python, Pandas, Data Cleaning, Data Visualization, Intro to ML)](https://www.kaggle.com/learn)

*Kaggle education team* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 4-7 hours

Zero-install: everything runs in Kaggle's hosted notebooks with graded exercises against real datasets, so a beginner gets reps without touching an environment. The Data Cleaning course (missing values, scaling/normalisation, date parsing, character encodings, inconsistent text entry) is the best free treatment of that specific topic anywhere and is the one not to skip. That said, these are deliberately shallow API tours — they teach which method to call, not why. They are excellent reps and a poor primary curriculum. Use them as drills between chapters of McKinney.

> **Worth knowing.** Short and free, but stale — the material will not reflect pandas 3.0 behaviour.

### [Learn Git Branching](https://learngitbranching.js.org/)

*Peter Cottle* &nbsp;·&nbsp; Interactive &nbsp;·&nbsp; Free &nbsp;·&nbsp; 3-5 hours

The only Git resource that makes branching, merging, rebasing and remotes click, because it animates the commit graph as you type real commands. Entirely client-side, no signup, no install, translated into many languages. Git's mental model is a directed graph and every text tutorial fails to convey that; this one shows it. Do the Main levels and the Remote levels; the 'Git golf' challenges are optional fun. Pair it with Missing Semester's Git lecture (theory) — this one supplies the muscle memory.

### [marimo — reactive Python notebooks](https://marimo.io/)

*marimo team* &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2-3 hours

The most interesting change in the notebook layer since Jupyter. Notebooks are stored as plain `.py` files (so `git diff` works and there is no JSON merge hell), execution is reactive (change a cell and every dependent cell reruns, eliminating the hidden-state bug that produces the classic 'it worked yesterday' notebook), and a notebook can be run as a script or deployed as a web app. Crossed 20k+ GitHub stars in 2026 and shipped an agent-native pair mode. Recommendation: learn Jupyter first because every course, every Kaggle kernel and every Colab link assumes it — then adopt marimo for your own projects.

> **Worth knowing.** A tool rather than a learning resource — it teaches nothing by itself and sits oddly in a beginner-foundations reading list.

### [Modern Polars](https://kevinheavey.github.io/modern-polars/)

*Kevin Heavey* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6-10 hours

A free side-by-side book showing the same task in idiomatic Polars and idiomatic pandas, with commentary on API design and performance. This is the most efficient possible way for someone who already knows pandas to pick up Polars, because it teaches by diff rather than from scratch. The method-chaining and indexing chapters are also the best free argument for writing cleaner pandas, regardless of whether you ever adopt Polars. Read it only once pandas feels comfortable — reading both APIs cold will just confuse you.

> **Worth knowing.** Code is current, but the commentary dates to 2023 and some pandas-vs-Polars framing predates pandas 3.0. It assumes prior pandas fluency, so it is not an absolute-beginner resource.

### [Polars User Guide](https://docs.pola.rs/user-guide/getting-started/)

*Polars documentation contributors* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6-10 hours

Polars is now a mainstream production dataframe library and worth knowing — but it is your **second** dataframe library, not your first. scikit-learn, statsmodels, Hugging Face datasets, seaborn and every ML tutorial on earth speak pandas/NumPy, so learning Polars first means constant `.to_pandas()` friction and inability to follow any course. Come here after you are fluent in pandas, when a dataset gets slow or when a job description names it. The expressions-and-contexts model (select / with_columns / filter / group_by) is genuinely cleaner than pandas and will retroactively improve your pandas.

> **Worth knowing.** Take it after pandas, not alongside.

### [Python for Everybody (PY4E)](https://www.py4e.com/)

*Charles R. Severance* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 50-70 hours

The gentlest on-ramp for someone who has never programmed and is intimidated. Free autograder, gradebook, and discussion forums directly on py4e.com with no Coursera paywall — that free autograder is the reason to use py4e.com rather than the Coursera mirror. Book last updated Jan 2024 to Python 3.12, Twitter API chapters removed, databases chapter rewritten. Pick this or CS50P, never both — they overlap ~80%. Caveat: its 'data' framing is web scraping, XML/JSON and raw SQLite, not NumPy/pandas, so it does not actually shorten your path to ML; it is a confidence-builder.

> **Worth knowing.** Stops at basic Python plus web scraping and databases, with no numpy, pandas or ML — a prerequisite rather than a data-foundations course. Pair it with something else.

### [The Missing Semester of Your CS Education (IAP 2026 edition)](https://missing.csail.mit.edu/)

*Anish Athalye, Jon Gjengset & Jose Javier Gonzalez Ortiz* &nbsp;·&nbsp; Course &nbsp;·&nbsp; Free &nbsp;·&nbsp; 10-15 hours

Fills the exact gap that sinks self-taught ML beginners: shell fluency, editors, version control, debugging and profiling. The older lecture on data wrangling with command-line tools is not in the 2026 syllabus, but it is still on the site under topics from previous years. MIT re-taught the course in January 2026 and materially updated it — new lectures on packaging/shipping code, code quality, and agentic coding, with AI tooling folded into every lecture rather than quarantined into one. That 2026 refresh makes it one of the few genuinely current free CS courses. Do the Shell, Command-line Environment, Version Control (Git) and Debugging lectures at minimum; each is ~1 hour of video plus exercises.

### [Think Python, 3rd edition (2024)](https://allendowney.github.io/ThinkPython/)

*Allen B. Downey* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 35-50 hours

The most underrated item on this list and the best-updated free Python book. The entire 3rd edition is written as Jupyter notebooks that run one-click in Colab, so a beginner never fights an install on day one, and every chapter ends with explicit guidance on using LLMs to get unstuck — the only mainstream Python book that treats AI assistance as a first-class study skill rather than pretending it doesn't exist. Use as the reading companion alongside CS50P's problem sets, or as a full self-paced substitute if video lectures aren't your format.

## Keep for reference

Not for reading end to end. Useful to have when you need to look something up.

### [Google Colab](https://colab.research.google.com/)

*Google Research* &nbsp;·&nbsp; Tool &nbsp;·&nbsp; Free tier &nbsp;·&nbsp; 1 hour

Still the correct day-one surface: zero install, pandas/NumPy/scikit-learn/PyTorch preinstalled, shareable links, and free NVIDIA T4 access when you later need a GPU. Use it for your first 2-4 weeks so that environment problems cannot make you quit, then deliberately move to a local uv + VS Code setup, because building and debugging your own environment is itself a required job skill. 2026 free-tier reality check: GPU is never guaranteed, and Google does not publish the usage limits, which change over time. Sessions run for at most 12 hours and idle timeouts are aggressive — fine for learning, unusable for anything long-running.

> **Worth knowing.** A tool, not a learning resource. Free-tier GPU access is best-effort and heavily throttled — expect disconnects and "no GPU available" on any nontrivial training run.

### [Pandas 3.0 release announcement (Copy-on-Write, PyArrow strings)](https://pandas.pydata.org/community/blog/pandas-3.0.html)

*pandas core development team* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

Read this early and treat it as a staleness detector. pandas 3.0 makes Copy-on-Write the only mode (chained assignment like `df[df.A>0]['B'] = 1` now errors instead of warning) and infers a real `str` dtype instead of numpy `object` for text columns. Once you know these two facts you can instantly date any tutorial: if it teaches `inplace=True`, works around `SettingWithCopyWarning`, or checks for `object` dtype on strings, it was written for pandas 2.x or earlier. That one skill will save a beginner dozens of hours of confusing errors across every other resource on this list.

### [Pro Git, 2nd edition](https://git-scm.com/book/en/v2)

*Scott Chacon & Ben Straub* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 6 hours

The official Git book, free on git-scm.com in HTML/PDF/EPUB, maintained on GitHub by hundreds of contributors. Use as reference, not as a read-through — a beginner should read chapters 1-3 (basics and branching) and dip into chapter 6 (GitHub) and 7.1-7.3 (revision selection, stashing, reset). Note: the 2nd edition dates to 2014 with community patches since, so it predates GitHub's modern PR review UI and says nothing about GitHub Actions; that is fine because Git the tool has barely changed. Do not attempt chapter 10 (Git internals) as a beginner.

> **Worth knowing.** A 2014 book. Still the best free explanation of git fundamentals — branching, merging, internals — but the GitHub/hosting chapter is a decade behind current platform UI.

### [Python Data Science Handbook (free online edition)](https://jakevdp.github.io/PythonDataScienceHandbook/)

*Jake VanderPlas* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Free &nbsp;·&nbsp; 30-40 hours

Included here as a warning. Everyone recommends this and almost nobody checks the date: the free jakevdp.github.io version is the **first** edition — its preface carries a 2016 copyright and the repo README states it was written and tested against Python 3.5, with notes about Python 2.7 compatibility. That is pre-pandas-1.0, pre-CoW, pre-NumPy-2, and its scikit-learn and matplotlib APIs have drifted. The 2nd edition (2022) is real and good but is not free at that URL. Use the free version only as a conceptual reference for the NumPy and matplotlib chapters, and use McKinney's open-access 3rd edition as your actual pandas text instead.

> **Worth knowing.** This is the 2016 first edition. Its pandas chapters contradict current pandas (Copy-on-Write, PyArrow strings, removed inplace/chained-assignment idioms) and its scikit-learn chapter predates the modern estimator API. Prefer the 2nd-edition notebooks.

### [Thoughts on OpenAI acquiring Astral (uv / Ruff / ty)](https://simonwillison.net/2026/mar/19/openai-acquiring-astral/)

*Simon Willison* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

Context you should have before betting your whole toolchain on uv. OpenAI announced its acquisition of Astral on 19 March 2026, absorbing uv, Ruff and the ty type checker into the Codex ecosystem, with a stated commitment to keep supporting the open-source products. Willison is the most credible independent voice on Python tooling politics and lays out the concentration-risk argument fairly. Practical takeaway for a beginner: still use uv (the tools remain MIT-licensed and are a genuine leap forward), but keep knowing how plain `python -m venv` and `pip install -r requirements.txt` work as a fallback.

> **Worth knowing.** Ecosystem news commentary, not a learning resource — useful as context for tooling choices, not as something to study. Short shelf life: the acquisition's consequences are still unresolved.

### [VS Code Data Science tutorial (Python + Jupyter extensions)](https://code.visualstudio.com/docs/datascience/data-science-tutorial)

*Microsoft VS Code documentation team* &nbsp;·&nbsp; Documentation &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2-4 hours

Useful for the mechanics only: installing the Python and Jupyter extensions, running .ipynb natively inside the editor, the Variables Explorer and Data Viewer, and the Data Wrangler extension (a genuinely good free GUI for profiling and cleaning a DataFrame that emits the equivalent pandas code — an underrated learning aid). Parts of it are dated: it still instructs you to create a conda environment and to install TensorFlow/Keras, both 2019-era defaults. Follow it for the editor setup, then substitute `uv` for conda and ignore the Keras section entirely.

> **Worth knowing.** Three and a half years stale and teaches deprecated tooling (Keras/TF on Titanic). Use it for the mechanical half — installing the Python and Jupyter extensions and running notebooks — and learn the modelling elsewhere.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
