# Chapter 1: Getting oriented

**Week 0 &nbsp;·&nbsp; about 8 hours.**

[Book index](../README.md) &nbsp;·&nbsp; [Chapter resources](resources/README.md)

**The short version.** Choose a target role, a weekly time budget, and a working Python environment.
Start on your own CPU or a free notebook service. This chapter produces a repository that another
person can run; it does not require buying hardware.

**In this chapter:** [Plan](#your-week-0-plan) &nbsp;·&nbsp; [Learn](#what-to-learn) &nbsp;·&nbsp;
[Build](#what-to-build) &nbsp;·&nbsp; [Completion](#before-you-move-on) &nbsp;·&nbsp;
[Resources](#resources)

---

## Your week 0 plan

About eight hours total. Do the days in order; skip nothing that ends in a commit or a log line.

| Day | Hours | Do this                                                                                                                                                                       | Done when                                                                              |
| --- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 1   | 2     | Read "Pick one target role" below. Write your choice, one non-salary reason and a weekly study budget in README.                                                              | Role, weekly hours and study sessions are written down                                 |
| 2   | 2     | Run the uv commands below. Commit the project and push to a repo.                                                                                                             | Fresh clone passes the locked install and import check below                           |
| 3   | 1     | Create `LOG.md`. Add today's line (see What to build).                                                                                                                        | First log entry exists                                                                 |
| 4   | 1     | Open Google Colab. Run `import pandas as pd; print(pd.__version__)`. Try switching to a GPU runtime.                                                                          | Notebook runs; CPU is fine today                                                       |
| 5   | 2     | Read Eugene Yan's interview article (linked in Resources); note the two skills in bold. Check five current job descriptions in your target market and skim the compute table. | Role choice reflects actual requirements; you have a CPU plan and an optional GPU plan |

---

## What you will be able to do

Name the specific role you are working towards, and open a project without fighting your tools.

## What to learn

**Pick one target role.** The five common titles look similar from outside and lead to quite
different curricula. Trying to prepare for all of them at once is one of the more common reasons
people stall. Treat the following as a guide to the work; employers use these titles inconsistently.

| Role                  | What the day looks like                                                                       | Qualifications to check in actual vacancies                                                   | Fit for a developer                                               |
| --------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| **AI Engineer**       | Products using foundation models: context, tools, retrieval, evaluation, cost and latency     | Software experience, product judgement; degree filters vary                                   | Direct transfer from application development                      |
| **ML Engineer**       | Data pipelines, training, serving and scaling; model performance under deployment constraints | Software and statistics evidence; degree filters vary                                         | Good, with more statistics and systems work                       |
| **Data Scientist**    | Experiment design, causal questions, metrics and communicating decisions                      | Statistics, domain knowledge and sometimes a quantitative degree                              | Good, with the most statistics                                    |
| **Applied Scientist** | Research alongside production code                                                            | Some employers require a graduate degree or equivalent research experience                    | Requires stronger experimental and research evidence              |
| **Research Engineer** | Frameworks, distributed training and implementing new methods                                 | Systems ability and research experience; publications and graduate degrees are role-dependent | A demanding route for developers with relevant systems experience |

**Data Engineer** is worth considering as well: ingestion, data quality, modelling, orchestration
and reliable analytical systems. Existing SQL, backend and infrastructure experience can transfer.

If you cannot decide, **AI Engineer** is a reasonable starting assumption for someone who already
ships applications. Revisit it after checking vacancies in your geography and after the first
project. A title alone does not establish hiring demand or an employer's degree requirements.

**Know what interviews can assess.** Eugene Yan has published
[his own hiring rubric](https://eugeneyan.com/writing/how-to-interview/). He assesses software
engineering fundamentals, **data literacy**, comfort with uncertainty, **evaluation frameworks**,
and breadth of knowledge. This is one practitioner's rubric, rather than a universal interview
format. The projects in this book deliberately produce evidence of the two skills in bold.

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

  Check that the installed packages import successfully:

  ```bash
  uv run --locked python -c "import numpy as np; import pandas as pd; print(np.__version__, pd.__version__)"
  ```

  Both version numbers should print without an import error. Open notebooks with
  `uv run jupyter lab`. Commit `pyproject.toml`, `uv.lock`, `.python-version` and the generated
  `src/` package. Record the Python patch version, uv version and operating system; use
  `uv sync --locked` and `uv run --locked ...` for a reproduction check. The flag fails if the lock
  disagrees with project metadata instead of silently changing it; see
  [locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/). A dependency lock does
  not pin your data, GPU driver or every hardware-dependent result.

  Two details trip people up. Since uv 0.12, `uv init` creates a small package under `src/`, which
  suits the tested cleaning functions you write in Chapter 2; add `--no-package` if you want the
  older single-file layout. And for the Python version, pick the newest one that PyTorch, the
  deep-learning library you meet in Chapter 4, has ready-built packages for. In September 2026 that
  is 3.14, supported by the official
  [PyTorch installation guide](https://pytorch.org/get-started/locally/). If a needed library lacks
  a compatible wheel, choose a supported Python version and regenerate the lock deliberately.

- **pandas 3.0 changed some defaults.** Copy-on-Write is now the only mode; chained assignment
  cannot update the original dataframe. Use a single `.loc[...] = ...` assignment. Text columns also
  default to a string dtype. `inplace=True` remains supported for some operations, so its presence
  alone does not date a tutorial. Check the
  [pandas migration guide](https://pandas.pydata.org/docs/user_guide/copy_on_write.html). NumPy's
  old aliases such as `np.int`, `np.float` and `np.object` expired in
  [1.24](https://numpy.org/doc/2.3/release/1.24.0-notes.html);
  [2.0 reintroduced `np.bool`](https://numpy.org/doc/stable/release/2.0.0-notes.html) with NumPy
  boolean dtype semantics. Use explicit dtypes when precision matters.

- **Editor.** VS Code with the Python and Jupyter extensions is a practical default. Select the
  project's `.venv` interpreter and notebook kernel. Its data science tutorial also covers conda and
  TensorFlow; these are valid alternatives, but use one documented environment for this project.

**A note on package sources.** At work, follow your organisation's package and licensing policy.
Anaconda's commercial terms depend on the service and organisation; consult its current terms if you
use it. Miniforge with conda-forge is another option when a conda environment is needed.

**Where your compute comes from.**

Nothing on the main path of this book needs a GPU you have to buy. "I cannot learn deep learning
without a GPU" is a common worry and, happily, not true.

| Option           | Cost                                | Good for                                 | Worth knowing                                                                                     |
| ---------------- | ----------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Your computer    | No additional service cost          | Chapters 1–3 and small CPU experiments   | Use a bounded dataset and record memory/runtime                                                   |
| Google Colab     | Free tier                           | Quick interactive notebooks              | GPU type, availability and limits are dynamic; save work and checkpoints outside the runtime      |
| Kaggle Notebooks | Free tier                           | Public datasets and notebook experiments | Verify account eligibility, current accelerator allowance and session limits                      |
| Lightning AI     | Free tier or credits where offered  | Persistent development projects          | Check which machines consume credits and how persistence is billed                                |
| Modal            | Starter credits, then usage charges | Scripted CPU/GPU jobs and services       | Credits and endpoint billing have different rules; set a spending limit and check current pricing |

Start locally or in a free notebook. Choose a GPU service later using the exercise's memory, runtime
and persistence needs. Provider allowances are not reproducibility guarantees; keep a CPU fallback
and checkpoint resumable training. Official compute links are in this chapter's resources.

## Resources

All 13 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [How to Interview and Hire ML/AI Engineers](https://eugeneyan.com/writing/how-to-interview/) —
  Eugene Yan. A free article, 1 hour. The hiring rubric this book is built around.
- [The Rise of the AI Engineer](https://www.latent.space/p/ai-engineer) — Shawn "swyx" Wang. A free
  article, 1 hour. The role's original framing; compare it with current vacancies.
- [AI and Job Postings: From Destruction to Creation?](https://hiringlab.indeed.com/2026/07/08/ai-and-job-postings-from-destruction-to-creation/)
  — Guillermo Gallacher. A free article, under an hour. Honest expectations about the junior market.
- [Teach Yourself Programming in Ten Years](https://www.norvig.com/21-days.html) — Peter Norvig. A
  free article, under an hour. The antidote to "AI engineer in 30 days".

## What to build

Create your learning repository, add a `LOG.md`, make your first commit, and push it. Public is
better, even this early. One line per session is enough:

```markdown
2026-10-09 · 2h · Created repo with uv; CPU notebook runs · Broke: selected wrong kernel
```

From a fresh clone, run `uv sync --locked`, then repeat the import check above. Record those exact
commands in the project README, alongside your role and weekly study sessions. Keep credentials and
private datasets out of the repository. A public project is useful where its data and code may be
shared.

## Before you move on

- You can state the role you are training for, and one reason for it that is not salary.
- Your weekly hours and study sessions are written down; stretch the schedule if ten hours a week is
  unrealistic.
- A fresh clone installs from the committed lock and passes the documented import check.
- You can correct a pandas chained-assignment example using the migration guide.
- You have a working CPU environment and know how to check an optional GPU service's current limits.

## A few things worth knowing

- **Course collecting.** CS50P, Python for Everybody and Automate the Boring Stuff overlap heavily.
  Doing all three is a lot of hours to learn one thing once. Pick whichever suits you and finish it.
- **Certificates.** A certificate can document completion; it does not by itself demonstrate
  independent engineering or evaluation ability. Historical MOOC completion rates use registrations
  as the denominator, including people who never intended to finish. Build an inspectable artefact
  alongside any certificate rather than treating those rates as a prediction of your own success.
- **Perfecting the plan.** It is possible to spend a happy weekend on a study schedule. The schedule
  is not the work.

---

[Back to the index](../README.md) &nbsp;·&nbsp;
[Next: Data foundations](../02-data-foundations/README.md)
