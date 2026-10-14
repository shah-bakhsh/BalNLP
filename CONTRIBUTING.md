# Contributing to BalNLP

Use Python 3.12 and Node.js 24. Follow README.md for the isolated Python environment
and frontend installation. Work on a feature branch and open a pull request with the
problem, resulting behavior, and relevant verification.

Before a PR: run `ruff check balnlp backend tests scripts`, `ruff format --check balnlp
backend tests scripts`, and `pytest -m 'not integration'` from the root. In frontend/
run `npm run lint`, `npm run typecheck`, `npm test`, and `npm run build`.

Keep the core independent of FastAPI. Preserve model architecture, label conventions,
and null values; never substitute heuristic or mock predictions in production. Use
mock models only in tests. Adding a model requires an architecture source, strict
checkpoint loading, alignment tests, and separate real-checkpoint verification.

Do not commit credentials, submitted user text, weights, dependency folders, or local
environment files. Report vulnerabilities privately to the repository maintainer
rather than including credentials or an exploit against a live service in an issue.

Changes to tokenization must describe their effect on the models' evaluation protocol.
Attach viewport screenshots for UI changes and keep all controls keyboard accessible.
The application source is licensed under Apache-2.0; see LICENSE and NOTICE.

## Getting started

Read [development](docs/DEVELOPMENT.md), [support](SUPPORT.md), and the
[code of conduct](CODE_OF_CONDUCT.md). Choose a focused [task proposal](docs/CONTRIBUTOR_TASKS.md),
check for an existing issue, and discuss scope before substantial work. These proposals
are not automatically opened issues or assigned work. Documentation, accessibility,
linguistic feedback, and reproducible bug reports are useful contributions.

Use the issue forms and PR template. Explain what evidence is synthetic, real-model,
or author-reported; attach only text/data you have permission to share. Document any
checks you could not run. Submit only material you have the right to contribute. Contributions intentionally
submitted for inclusion follow Apache-2.0 Section 5 unless explicitly stated otherwise.
Discuss third-party material and any different terms with the maintainer before submission.
