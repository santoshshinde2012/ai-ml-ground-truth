# Resources — Chapter 1: Getting oriented

Everything referenced in [the chapter](../README.md), grouped by how central it is, with a short
note on what each one is for.

Prices and free tiers change often, so check a resource's own page before you plan around one.

---

## Start here

The resources on the main path for this chapter, in the order the chapter uses them. If you only do a few things, do these.

### [How to Interview and Hire ML/AI Engineers](https://eugeneyan.com/writing/how-to-interview/)

*Eugene Yan* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

Read the hiring manager's own rubric rather than an interview-prep vendor's guess. The structure: five one-hour interviews plus 30-minute pre-brief and debrief (~10 hours of company time per candidate). Assessed dimensions: SWE fundamentals (30–60 min coding), data literacy, comfort with model opacity/uncertainty, evaluation frameworks, and science breadth/depth — plus his AICE framework for the non-technical rounds (Ambiguity, Influence, Complexity, Execution). This book's capstone projects are shaped around that list; 'evaluation frameworks' and 'data literacy' are the two most under-practised and most-tested skills.

### [The Rise of the AI Engineer](https://www.latent.space/p/ai-engineer)

*Shawn "swyx" Wang* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The essay that named the role you are most likely to be hired into, published 30 June 2023 and endorsed by Karpathy. Foundation models 'shifted right' so that work needing a research team now needs 'API docs and a spare afternoon'; AI Engineers will outnumber ML Engineers within five years because there are ~50M software engineers versus ~5K LLM researchers; 'when it comes to shipping AI products, you want engineers, not researchers'. It is the strategic argument for why someone entering the field does not need a PhD-shaped curriculum. Read it critically — it is a movement-building manifesto, and swyx has commercial interest in the term.

> **Worth knowing.** Read it as the origin document for the term, not as current market analysis — its 2023 supply/demand reasoning predates both the agent era and the junior-market contraction.

### [AI and Job Postings: From Destruction to Creation?](https://hiringlab.indeed.com/2026/07/08/ai-and-job-postings-from-destruction-to-creation/)

*Guillermo Gallacher* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

The single best primary dataset on the 2026 junior question, and it contradicts both the doom narrative and the hype. Software development postings rose ~15% since Claude Code's launch (late Feb 2025) while overall postings fell 7%; 71% of the May-2025-to-May-2026 increase is senior roles and 37% is AI-titled roles; postings still sit 27.5% below Feb 2020. Gallacher names the mechanism 'seniority-biased technological change'. Read it early to set honest expectations — the door is open but narrower than it was, and your job is to look less like a junior.

> **Worth knowing.** The headline finding is correlational: the roughly 15% rebound is anchored to a coding-assistant release date, which invites a causal reading the data does not support.

### [Teach Yourself Programming in Ten Years](https://www.norvig.com/21-days.html)

*Peter Norvig* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

The best possible antidote to '30 days to AI engineer' marketing, and 25 years old precisely because it is about the invariant. It cites Bloom, Bryan & Harter, Hayes, and Simon & Chase for the ~10-year figure; notes Gladwell popularised 10,000 hours while experts stress the time varies by person and domain; even Mozart needed 13 years past prodigy status. His recipe — get interested and keep it fun, program actively, talk with and read the code of other programmers, work on projects with others, learn several languages across paradigms, understand what the hardware costs.

## Optional depth

Worth your time if the chapter left you wanting more, or if this is where you want to specialise.

### [2025 Stack Overflow Developer Survey — AI section](https://survey.stackoverflow.co/2025/ai)

*Stack Overflow research team* &nbsp;·&nbsp; Dataset &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The full breakdowns behind the numbers quoted in the introduction — trust, debugging time, confidence — plus the cuts that matter for a learner: 39.5% of people learning to code use AI daily, and 33% use it mainly to learn new concepts. These numbers, together with the 2026 trial described there, are the basis for the two-mode assistant rule in the introduction.

> **Worth knowing.** 2025 data — check whether a 2026 edition has landed before relying on it as current. Respondent counts vary by question rather than matching the headline survey total.

### [Deliberate Practice and Performance in Music, Games, Sports, Education, and Professions: A Meta-Analysis](https://gwern.net/doc/psychology/2014-macnamara.pdf)

*Brooke N. Macnamara, David Z. Hambrick & Frederick L. Oswald* &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2 hours

The evidence that undercuts the '10,000 hours' framing many learning guides still repeat. Deliberate practice explained 26% of performance variance in games, 21% music, 18% sports, 4% education, and less than 1% in professions — and only ~5% when restricted to studies using practice logs rather than retrospective recall. Ericsson's rebuttal (that the included studies did not use his 1993 definition — coach-designed, individualised, immediate-feedback practice) is legitimate, so read the two together rather than taking the meta-analysis as the last word.

> **Worth knowing.** The linked copy is a third-party mirror on gwern.net, not the publisher of record.

### [Make It Stick: The Science of Successful Learning](https://www.makeitstick.com/)

*Peter C. Brown with Henry L. Roediger III & Mark A. McDaniel* &nbsp;·&nbsp; Book &nbsp;·&nbsp; Paid &nbsp;·&nbsp; 8-10 hours

The readable trade version of the Dunlosky/Roediger literature, produced out of a ten-year collaboration among 11 cognitive scientists at six universities. It practises what it preaches: it demonstrates each principle on you before explaining it. Its core prescription — retrieval practice, spacing, interleaving, and deliberately waiting until a little forgetting has occurred before restudying — is directly implementable as a chapter schedule. Skip it if budget-constrained; the Dunlosky paper is free and more precise.

### [Study offers data to show MOOCs didn't achieve their goals (coverage of Reich & Ruipérez-Valiente, 'The MOOC pivot', Science, 2019)](https://www.insidehighered.com/digital-learning/article/2019/01/16/study-offers-data-show-moocs-didnt-achieve-their-goals)

*Doug Lederman* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; 1 hour

The definitive dropout dataset and the reason this book is designed around completion rather than content. 565 MITx/HarvardX courses on edX over 6.5 years, 12.67 million registrations; completion fell to 3.13% in 2017–18 from ~4% the two prior years and nearly 6% in 2014–15; 52% of registrants never start the course. Two design implications: (1) the drop-off is front-loaded, so the first session must produce a working artefact, and (2) any roadmap that is a list of MOOCs is statistically a list of things you will not finish. If you can, read the Science paper itself (doi 10.1126/science.aav7958) rather than this coverage.

> **Worth knowing.** Trade-press coverage of a study you can read directly, and Inside Higher Ed is partly metered. The 2012–2018 completion data is weak evidence about how people learn online in 2026.

### [The 2026 AI Index Report — Economy chapter](https://hai.stanford.edu/ai-index/2026-ai-index-report/economy)

*Stanford Institute for Human-Centered AI* &nbsp;·&nbsp; Paper &nbsp;·&nbsp; Free &nbsp;·&nbsp; 2 hours

The most citable, methodologically serious source for labour-market claims — academic, annual, open access, and it does not sell anything (unlike bootcamp/vendor 'reports'). Employment for software developers aged 22–25 fell nearly 20% from 2024; one-third of organisations expect AI to reduce headcount within a year; measured productivity gains of 26% in software development; yet large-scale job losses have not shown up in aggregate employment data. Full chapter list: R&D, Technical Performance, Responsible AI, Economy, Science, Medicine, Education, Policy, Public Opinion. When you want a labour-market claim you can check, start here rather than with social-media commentary.

### [The Labor Market Is Tilting Toward Seniority](https://hiringlab.indeed.com/2026/07/23/the-labor-market-is-tilting-toward-seniority/)

*Felix Aidala & Sneha Puri, Indeed Hiring Lab* &nbsp;·&nbsp; Article &nbsp;·&nbsp; Free &nbsp;·&nbsp; under an hour

A second Indeed Hiring Lab piece that pairs well with the Gallacher article. In Q1 2026, senior roles made up 69.3% of US software development postings on Indeed, and entry-level roles just 4.5%. Across all US postings, senior-level postings rose 14.7% in the year to May 2026, while entry-level postings fell 7.5%. Senior roles are still only about 14% of all postings. Read it to see why this book asks you to build evidence that makes you look less like a junior.

> **Worth knowing.** It counts US postings on one job site, not hires, so it shows demand rather than who actually gets the jobs. The authors also weigh causes other than AI, such as remote work and interest rates.

---

[Back to the chapter](../README.md) &nbsp;·&nbsp; [Back to the book](../../README.md)
