# Chapter 1: Getting oriented

**Week 0 &nbsp;·&nbsp; about 8 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** Choose a target role, a weekly time budget and a working Python environment.
Start on your own CPU or a free notebook service. You finish with a repository another person can
run, and no hardware to buy.

**In this chapter:** [Plan](#your-week-0-plan) &nbsp;·&nbsp; [Learn](#what-to-learn) &nbsp;·&nbsp;
[Build](#what-to-build) &nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp;
[Resources](#resources)

---

## Your week 0 plan

About eight hours. Do the days in order, and finish every step that ends in a commit or log line.

| Day | Hours | Do this                                                                                                                                                                          | Done when                                                                           |
| --- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 1   | 2     | Read "Pick one target role" below. Write your choice, one non-salary reason and a weekly study budget in README.                                                                 | Role, weekly hours and study sessions are written down                              |
| 2   | 2     | Run the uv commands below. Commit the project and push to a repo.                                                                                                                | Fresh clone passes the locked install and import check below                        |
| 3   | 1     | Create `LOG.md`. Add today's line (see What to build).                                                                                                                           | First log entry exists                                                              |
| 4   | 1     | Open Google Colab. Run `import pandas as pd; print(pd.__version__)`. Try switching to a GPU runtime.                                                                             | Notebook runs; CPU is fine today                                                    |
| 5   | 2     | Read Eugene Yan's interview article (linked in Resources) and note the two skills in bold. Check five current job descriptions in your target market and skim the compute table. | Role choice matches real requirements. You have a CPU plan and an optional GPU plan |

---

## What you will be able to do

Name the specific role you are working towards, and open a project without fighting your tools.

## A quick entry check

Try these with documentation but without a tutorial. They show what to prepare, and are not a timed
admission test.

1. Read a small CSV, check that an amount is numeric, and return a useful error for a bad row.
2. Write a function and a test, run them from a terminal, and explain the stack trace of a
   deliberate failure.
3. In a throwaway repo, make a Git commit, look at its diff, and undo one accidental change.
4. Explain why 12 events among 80 eligible cases is 15%, then say what would make that denominator
   wrong.

If the first three feel unfamiliar, use the programming resources in
[Chapter 2's resource list](../02-data-foundations/resources/README.md#optional-depth) before
counting the chapter budgets. Take one Python course, such as
[CS50P](../02-data-foundations/resources/README.md#cs50s-introduction-to-programming-with-python-cs50p)
or [Python for Everybody](../02-data-foundations/resources/README.md#python-for-everybody-py4e),
then [Learn Git Branching](../02-data-foundations/resources/README.md#learn-git-branching) and
[The Missing Semester](../02-data-foundations/resources/README.md#the-missing-semester-of-your-cs-education-iap-2026-edition)
for Git and the shell. If fractions or function notation feel rusty, list the maths topics to
revisit and work through the examples alongside Chapters 2 and 3. You can start without a full
mathematics course. The [reference lab](../labs/README.md) is a small project with no API calls for
checking your local workflow.

## What to learn

**Pick one target role.** The five common titles look similar from outside and lead to quite
different curricula. Trying to prepare for all of them at once is one of the more common reasons
people stall. Treat the table as a guide to the work. Employers use these titles inconsistently.

| Role                  | What the day looks like                                                                   | Qualifications to check in actual vacancies                                                   | Fit for a developer                                               |
| --------------------- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **AI Engineer**       | Products using foundation models: context, tools, retrieval, evaluation, cost and latency | Software experience and product judgement. Degree filters vary                                | Application skills transfer directly                              |
| **ML Engineer**       | Data pipelines, training, serving and scaling. Model performance under deployment limits  | Proven software and statistics skills. Degree filters vary                                    | Good, with more statistics and systems work                       |
| **Data Scientist**    | Experiment design, causal questions, metrics and communicating decisions                  | Statistics, domain knowledge and sometimes a quantitative degree                              | Good, with the most statistics                                    |
| **Applied Scientist** | Research alongside production code                                                        | Some employers require a graduate degree or equivalent research experience                    | Needs a stronger record of experiments and research               |
| **Research Engineer** | Frameworks, distributed training and implementing new methods                             | Systems ability and research experience. Publications and graduate degrees depend on the role | A demanding route for developers with relevant systems experience |

**Data Engineer** is worth considering as well: ingestion, data quality, modelling, orchestration
and reliable analytical systems. Your SQL, backend and infrastructure experience can transfer.

If you cannot decide, **AI Engineer** is a reasonable first choice for someone who already ships
applications. Revisit it after checking local vacancies and after your first project. A
title alone does not show hiring demand or an employer's degree requirements.

**Know what interviews can assess.** Eugene Yan has published
[his own hiring rubric](https://eugeneyan.com/writing/how-to-interview/). He assesses software
engineering fundamentals, **data literacy**, comfort with uncertainty, **evaluation frameworks**,
and breadth of knowledge. It is one practitioner's rubric, so expect other interviews to differ.
The projects in this book are built to show the two skills in bold.

**Set up your tools.** Use one documented workflow, and check version-sensitive examples against
current documentation.

- **Environments: use [uv](https://docs.astral.sh/uv/).** It manages dependencies, virtual
  environments and Python installations. First follow its
  [installation instructions for your operating system](https://docs.astral.sh/uv/getting-started/installation/),
  reopen your terminal if needed, and check `uv --version`. Then create the project:

  ```bash
  uv python install 3.14
  uv init --python 3.14 my-learning-repo
  cd my-learning-repo
  uv add pandas numpy jupyterlab
  ```

  Check that the installed packages import:

  ```bash
  uv run --locked python -c "import numpy as np; import pandas as pd; print(np.__version__, pd.__version__)"
  ```

  Both version numbers should print without an error. Open notebooks with
  `uv run jupyter lab`. Commit `pyproject.toml`, `uv.lock`, `.python-version` and the generated
  `src/` package. Note the Python patch version, uv version and operating system. Use
  `uv sync --locked` and `uv run --locked ...` for a reproduction check. The flag fails if the lock
  disagrees with project metadata, rather than quietly changing it. See
  [locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/). A lock does not pin your
  data, GPU driver or every hardware-dependent result.

  Two details trip people up. Since uv 0.12, `uv init` creates a small package under `src/`, which
  suits the tested cleaning functions you write in Chapter 2. Add `--no-package` if you want the
  older single-file layout. For the Python version, pick the newest one that PyTorch, the
  deep-learning library you meet in Chapter 4, has ready-built packages for. In September 2026 that
  is 3.14, as the official
  [PyTorch installation guide](https://pytorch.org/get-started/locally/) shows. If a needed library
  lacks a compatible wheel, choose a supported Python version and regenerate the lock on purpose.

- **pandas 3.0 changed some defaults.** Copy-on-Write is now the only mode, so chained assignment
  cannot update the original dataframe. Use a single `.loc[...] = ...` assignment. Text columns also
  default to a string dtype. Some operations still support `inplace=True`, so seeing it does not
  date a tutorial. Check the
  [pandas migration guide](https://pandas.pydata.org/docs/user_guide/copy_on_write.html). NumPy's
  old aliases such as `np.int`, `np.float` and `np.object` expired in
  [1.24](https://numpy.org/doc/2.3/release/1.24.0-notes.html). NumPy
  [2.0 reintroduced `np.bool`](https://numpy.org/doc/stable/release/2.0.0-notes.html) with boolean
  dtype semantics. Use explicit dtypes when precision matters.

- **Editor.** VS Code with the Python and Jupyter extensions is a practical default. Select the
  project's `.venv` interpreter and notebook kernel. Its
  [data science tutorial](../02-data-foundations/resources/README.md#vs-code-data-science-tutorial-python--jupyter-extensions)
  also covers conda and TensorFlow. Those are valid, but use one documented environment here.

**A note on package sources.** At work, follow your organisation's package and licensing policy.
Anaconda's commercial terms depend on the service and organisation, so read its current terms if you
use it. Miniforge with conda-forge is another option if you need conda.

**Where your compute comes from.**

Nothing on the main path of this book needs a GPU you have to buy. "I cannot learn deep learning
without a GPU" is a common worry and, happily, not true.

| Option           | Cost                                | Good for                                 | Worth knowing                                                                                       |
| ---------------- | ----------------------------------- | ---------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Your computer    | No additional service cost          | Chapters 1–3 and small CPU experiments   | Keep the dataset small and note memory use and runtime                                              |
| Google Colab     | Free tier                           | Quick interactive notebooks              | GPU type, availability and limits change. Save work and checkpoints outside the runtime             |
| Kaggle Notebooks | Free tier                           | Public datasets and notebook experiments | Check account eligibility, the current accelerator allowance and session limits                     |
| Lightning AI     | Free tier or credits where offered  | Persistent development projects          | Check which machines use credits and how saved work is billed                                       |
| Modal            | Starter credits, then usage charges | Scripted CPU/GPU jobs and services       | Credits and endpoint billing follow different rules. Set a spending limit and check current pricing |

Start locally or in a free notebook. Choose a GPU service later, to fit the exercise's memory,
runtime and storage needs. A provider's allowance can change, so keep a CPU fallback and checkpoint training
so it can resume. Official compute links are in this chapter's resources.

## Resources

All 13 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [How to Interview and Hire ML/AI Engineers](https://eugeneyan.com/writing/how-to-interview/) —
  Eugene Yan. A free article, 1 hour. The hiring rubric this book is built around.
- [The Rise of the AI Engineer](https://www.latent.space/p/ai-engineer) — Shawn "swyx" Wang. A free
  article, 1 hour. The essay that first framed the role. Compare it with current vacancies.
- [AI and Job Postings: From Destruction to Creation?](https://hiringlab.indeed.com/2026/07/08/ai-and-job-postings-from-destruction-to-creation/)
  — Guillermo Gallacher. A free article, under an hour. Realistic expectations about the junior
  market.
- [Teach Yourself Programming in Ten Years](https://www.norvig.com/21-days.html) — Peter Norvig. A
  free article, under an hour. The antidote to "AI engineer in 30 days".

## What to build

Create your learning repository, add a `LOG.md`, make your first commit, and push it. Public is
better, even this early. One line per session is enough:

```markdown
2026-10-09 · 2h · Created repo with uv; CPU notebook runs · Broke: selected wrong kernel
```

From a fresh clone, run `uv sync --locked`, then repeat the import check above. Write those exact
commands in the project README, with your role and weekly study sessions. Keep credentials and
private datasets out of the repository. A public project helps when its data and code can be shared.

## Before you move on

- You can state the role you are training for, and one reason for it that is not salary.
- Your weekly hours and study sessions are written down. If ten hours a week is unrealistic, stretch
  the schedule.
- A fresh clone installs from the committed lock and passes the documented import check.
- You can correct a pandas chained-assignment example using the migration guide.
- You have a working CPU environment and know how to check an optional GPU service's current limits.

## A few things worth knowing

- **Course collecting.**
  [CS50P](../02-data-foundations/resources/README.md#cs50s-introduction-to-programming-with-python-cs50p),
  [Python for Everybody](../02-data-foundations/resources/README.md#python-for-everybody-py4e) and
  [Automate the Boring Stuff](../02-data-foundations/resources/README.md#automate-the-boring-stuff-with-python-3rd-edition)
  overlap heavily. Doing all three is a lot of hours to learn one thing once. Pick whichever suits
  you and finish it.
- **Certificates.** A certificate shows you finished a course, not that you can build or evaluate
  things on your own. Historical MOOC completion rates count everyone who registered, including
  people who never meant to finish, so they are a poor guide to your own success. Alongside any
  certificate, build something a reviewer can inspect.
- **Perfecting the plan.** It is possible to spend a happy weekend on a study schedule. The schedule
  is not the work.

---

[Back to the index](../README.md) &nbsp;·&nbsp;
[Next: Data foundations](../02-data-foundations/README.md)
