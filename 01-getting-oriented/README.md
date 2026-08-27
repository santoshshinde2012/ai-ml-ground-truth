# Chapter 1: Getting oriented

**Week 0 &nbsp;·&nbsp; about 8 hours.** &nbsp;·&nbsp; [Index](../README.md) &nbsp;·&nbsp; [Resources for this chapter](resources/README.md)

**The short version.** Before you learn anything, you make two decisions and one setup: which role you are aiming at, how many hours a week you can honestly give, and a working Python environment with free compute. Eight hours here saves months later, because most people who quit do so over a vague goal or a broken setup, not over hard material.

---

## What you will be able to do

Name the specific role you are working towards, and open a project without fighting your tools.

## What to learn

**Pick one target role.** The five common titles look similar from outside and lead to quite
different curricula. Trying to prepare for all of them at once is one of the more common reasons
people stall, and no popular roadmap asks you to choose — so this book does, here.

| Role | What the day looks like | Degree needed | Fit for a developer |
|---|---|---|---|
| **AI Engineer** | Building products on foundation models: context design, tool use, retrieval, evaluation, cost and latency. The model is a dependency, like a database. | No | Strongest. Your existing skills transfer almost directly. |
| **ML Engineer** | Data pipelines, training, serving, scaling. Also the problems foundation models do not solve: proprietary data, tight latency budgets, statistical guarantees. | Usually not | Good, with more statistics and systems work |
| **Data Scientist** | Experiment design, causal questions, metrics, and persuading people. The output is usually a decision, not a service. | Often preferred | Good, with the most statistics |
| **Applied Scientist** | Research alongside production code, typically with a software-engineering coding bar as well. | Usually | Harder without a graduate degree |
| **Research Engineer** | Frameworks, distributed training, new methods. Publications expected. | Effectively yes | Hardest route |

**Data Engineer** is worth mentioning as well. It is the most credential-agnostic track in this
whole field, it hires steadily at junior level, and people moving into AI often skip past it without
realising how much of it they already have.

If you genuinely cannot decide, **AI Engineer** is a reasonable default. It has the most open doors
for someone who already ships software, and the shared part of this book takes you most of the
way towards the other two.

**Know what the interviews assess.** Eugene Yan — who led ML teams earlier in his career, spent years as a Principal Applied Scientist
at Amazon, and is now at Anthropic — has published [his own hiring rubric](https://eugeneyan.com/writing/how-to-interview/). He assesses software engineering
fundamentals, **data literacy**, comfort with uncertainty, **evaluation frameworks**, and breadth of
knowledge. The two in bold are the ones almost no course teaches and almost no portfolio
demonstrates, so the projects in this book are built to produce evidence of them.

**Set up your tools.** Three things changed recently enough that a lot of tutorials are now wrong.

- **Environments: use [uv](https://docs.astral.sh/uv/).** One binary replaces pip, venv, pyenv,
  pipx and poetry, and it installs Python itself. Four commands get you a working project. It is
  still pre-1.0, and it does not replace conda for CUDA or heavy compiled scientific stacks.
- **pandas 3.0 changed some defaults.** Copy-on-Write is now the only mode, so chained assignment
  raises an error rather than a warning, and text columns get a real string dtype instead of
  `object`. This makes a useful test of any tutorial: if it teaches `inplace=True`, works around
  `SettingWithCopyWarning`, or checks for `object` dtype on text, it predates pandas 3.0. NumPy 2.0
  also removed `np.float`, `np.int`, `np.bool` and `np.object`.
- **Editor.** VS Code with the Python and Jupyter extensions is the common default. Its own data
  science tutorial is still worth reading for the mechanics, though it will tell you to use conda
  and install TensorFlow, both of which are dated advice now.

**A note on Anaconda.** Its licence terms require payment for organisations above a certain size,
including some non-profits and government bodies. If you learn an Anaconda-first workflow you may
not be able to use it at work. Miniforge with conda-forge is the free alternative if you need conda.

**Where your compute comes from.**

Nothing on the main path of this book needs a GPU you have to buy. "I cannot learn deep learning without a
GPU" is a common worry and, happily, not true.

| Option | Cost | Good for | Worth knowing |
|---|---|---|---|
| Google Colab | Free tier | Weeks 1-5, and anything you want running in a minute | GPU access is best effort, quotas move, sessions time out |
| Kaggle Notebooks | Free, no card | Anything that matters; datasets are already mounted | A published weekly GPU quota and a session cap. Check the current numbers. |
| Lightning AI | Free tier | When session limits start to hurt, since your work persists | Check the pricing page for the current allowance |
| Modal | Free monthly credits | Real GPU work and deployed demos; it scales to zero so idle costs nothing | Currently the most generous realistic option for a student |

A good working pattern is to prototype in Colab because it starts quickly, run anything that matters
on Kaggle because the quota is predictable, and move to Modal when you need a real GPU for a few
hours.

## Resources

All 9 resources for this chapter, with notes on each, are in **[resources/](resources/README.md)**.

The ones to begin with:

- [2025 Stack Overflow Developer Survey — AI section](https://survey.stackoverflow.co/2025/ai) — Stack Overflow research team. A free dataset, 1 hour.
- [AI and Job Postings: From Destruction to Creation?](https://hiringlab.indeed.com/2026/07/08/ai-and-job-postings-from-destruction-to-creation/) — Guillermo Gallacher. A free article, under an hour.
- [Deliberate Practice and Performance in Music, Games, Sports, Education, and Professions: A Meta-Analysis](https://gwern.net/doc/psychology/2014-macnamara.pdf) — Brooke N. Macnamara, David Z. Hambrick & Frederick L. Oswald. A free paper, 2 hours.
- [How to Interview and Hire ML/AI Engineers](https://eugeneyan.com/writing/how-to-interview/) — Eugene Yan. A free article, 1 hour.

## What to build

Create your learning repository, add a `LOG.md`, make your first commit, and push it. Public is
better, even this early. Then set up one project with `uv` and confirm you can get a GPU session
in Colab.

## Before you move on

- You can state the role you are training for, and one reason for it that is not salary.
- You can create a project with `uv` and hand someone the two files they need to reproduce it.
- You can look at an unfamiliar pandas tutorial and tell whether it predates pandas 3.0.
- You know where your GPU hours will come from.

## A few things worth knowing

- **Course collecting.** CS50P, Python for Everybody and Automate the Boring Stuff overlap heavily.
  Doing all three is a lot of hours to learn one thing once. Pick whichever suits you and finish it.
- **Certificates.** Completion rates on open online courses are very low, around 3% in the largest
  study I could find, so a list of certificates mostly signals enrolment. Everything in this book
  produces a public artefact instead, which tends to be more convincing.
- **Perfecting the plan.** It is possible to spend a happy weekend on a study schedule. The
  schedule is not the work.

---

[Back to the index](../README.md) &nbsp;·&nbsp; [Next: Data foundations](../02-data-foundations/README.md)
