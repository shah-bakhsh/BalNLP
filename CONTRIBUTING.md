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
The application license must be selected by the owner before an open-source release.
