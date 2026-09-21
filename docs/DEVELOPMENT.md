# Development and packaging

Follow the [README installation](../README.md#install-and-run-locally) for Python 3.12
and Node.js 24. For backend unit tests use the same CPU PyTorch pin as CI, then
`python -m pip install -e '.[api,dev]' networkx==3.6.1 numpy==2.5.3`.
Basic tests use synthetic inputs/checkpoints and do not download production weights.
Run the README's Python and frontend checks for affected code.

## Package audit

`pyproject.toml` uses setuptools and already defines `balnlp` 0.1.0, Python
`>=3.12,<3.13`, and separate API, inference, and development extras. The public import
is `from balnlp import BalNLP`. The wheel includes `balnlp` and `backend`, not the web
application, deployment scripts, or model weights. No CLI is currently defined;
`uvicorn backend.app.main:app` is the API entry point. Add a CLI only after defining
its input/output and error contract.

`pip install balnlp` is a future target, not an endorsed current installation command.
PyPI name availability and ownership are not verified. Install this checkout with
`python -m pip install -e .`; select extras for the API or model execution.

## Build before publication

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

Use a clean checkout/environment. Inspect wheel and source archive contents, install
the wheel in a fresh Python 3.12 environment, run `python -m pip check`, import
`balnlp`, and run a known local example with the appropriate extras. CI checks package
construction and core import without downloading checkpoints. A build is not permission
to redistribute code or models. Resolve [licensing](LICENSING.md) before publication.

## Versioning

Use semantic versions and tags `vMAJOR.MINOR.PATCH` when releases are approved.
While below 1.0, describe breaking API/model-contract changes explicitly in each minor
release; use patches for compatible fixes. Keep Python, frontend, API health/version,
and site version strings consistent. Do not create a release date or tag retroactively.
The [release draft](RELEASE_DRAFT.md) is not a published release.

## CI boundaries

Push/PR CI runs Python lint/format/unit checks and frontend lint, TypeScript, tests,
build, and fixture browser checks. Package checks build distribution artifacts.
Real model checks are manual via `Model integration` and can download several GB.
Python type checking is not yet a CI gate; introduce annotations incrementally before
adding a strict checker. Dependency review/secret scanning should be configured and
verified in GitHub settings by the owner; their enablement is not assumed.
