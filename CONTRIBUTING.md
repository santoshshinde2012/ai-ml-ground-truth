# Contributing to Ground Truth

Corrections are how a book like this stays useful. This page is the short version of
[publishing and contributing](content/publishing.md).

**Report a correction.** Open a
[correction issue](https://github.com/santoshshinde2012/ai-ml-ground-truth/issues/new?template=correction.yml)
with the page, the exact claim, what you saw, and a primary source or reproducible example.
Every page of the web book has a "Suggest a correction" link that fills in the page for you.

**Propose a change.** Keep pull requests small and focused. Chapter prose lives in the numbered
folders, front matter in `content/`, the reference lab in `labs/`, and all website code in
`website/`. See [what to change where](content/publishing.md#what-to-change-where). When you
reorganise or restyle, keep the learning order, the continuing project and the author's voice. Make
content changes separately, and explain why.

**Run the checks** with Node.js 24 and Python 3.10 or newer, from the repository root:

```bash
npm --prefix website ci
npm --prefix website run format:check
npm --prefix website run check
npm --prefix website test
npm --prefix website run build
```

By contributing, you agree that prose, illustrations and reports are released under
[CC BY 4.0](LICENSE) and code under the [MIT licence](LICENSE-CODE).
