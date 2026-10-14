# BalNLP

**Arabic-script Balochi Natural Language Processing** — a Python library, FastAPI service, and
Next.js workspace for exploring Arabic-script Balochi text.

![BalNLP desktop interface](docs/screenshots/home-desktop.png)

[![CI](https://github.com/shah-bakhsh/BalNLP/actions/workflows/ci.yml/badge.svg)](https://github.com/shah-bakhsh/BalNLP/actions/workflows/ci.yml)

**Development status:** Apache-2.0 source license. Version 0.1.0
is package metadata, not a claim of PyPI publication. See [licensing](docs/LICENSING.md).

## Why BalNLP exists

BalNLP brings related Balochi NLP components into a common library, API, and RTL
workspace. Consistent input handling and exports make the models easier to examine
and integrate. Balochi speakers and researchers should be able to inspect predictions
and contribute linguistic feedback. This goal is distinct from proven adoption or
validated accuracy; see [impact evidence](docs/IMPACT.md) and [evaluation](docs/EVALUATION.md).

## Release status

Repository verification records report that all four models ran through the unified API locally. BalMorph uses the recovered author notebook with strict checkpoint loading and exact forward-output verification. Real Balochi inference returns lemmas and morphological features. See [BalMorph verification](docs/balmorph-verification.json) and [source provenance](docs/BALMORPH_SOURCE.md).

The recorded BalParser checks passed strict loading and CPU inference, including
tree validation and CoNLL-U export. See [the release checks](docs/RELEASE_CHECKS.md) for
dated verification evidence for each component. Unit and browser tests use fixtures
only in test files. They do not establish model quality.

**The published checkpoints cannot run within Render Free's 512 MB RAM.** Each is
approximately 1.1 GB of weights. Sequential loading reduces concurrent residency but
does not make one checkpoint fit. No paid GPU is needed; use CPU hardware with enough
RAM, or provide independently validated smaller checkpoints. The free Render config
can boot the API and serve health checks, but is not a working free inference claim.

## Features

- Full or individual POS, NER, morphology interface, and dependency analysis.
- RTL input, word-level tables, POS chips, entity highlighting, SVG dependency trees.
- Copy/download JSON and sentence-aware CoNLL-U; no server-side file storage.
- NFC normalization, preserved Balochi characters, Unicode code-point offsets.
- Lazy loading, low/balanced/performance memory modes, strict custom checkpoint loading.
- One concurrent inference job, bounded bodies, rate limits, timeouts, and partial results.
- No database, accounts, persistent text history, or text logging.

## Architecture

The Next.js browser workspace calls FastAPI, which invokes the Python pipeline and
loads checkpoint files from the Hugging Face cache. Low-memory mode loads and unloads
each task in turn. See [architecture and source map](docs/ARCHITECTURE.md).

The sequence is scheduling order, not a claim that separately trained models share
an encoder or consume each other's predictions. The library has no FastAPI imports.
Adapters can later share representations only if their trained architectures permit it.

## Models

| Component | Repository/model | Current integration status |
|---|---|---|
| BalTokenizer | [shah-bakhsh/BalTokenizer](https://github.com/shah-bakhsh/BalTokenizer) | Related subword-tokenizer project; not integrated into this runtime |
| BalBERT | [shah-bakhsh/BalBERT](https://huggingface.co/shah-bakhsh/BalBERT) | Backbone, not loaded separately |
| BalPOS | [shah-bakhsh/BalPOS](https://huggingface.co/shah-bakhsh/BalPOS) | Token classification |
| BalNER v2 | [shah-bakhsh/BalNER-v2](https://huggingface.co/shah-bakhsh/BalNER-v2) | BIO token classification |
| BalMorph v2 | [shah-bakhsh/BalMorph](https://huggingface.co/shah-bakhsh/BalMorph) | Verified recovered notebook architecture |
| BalParser v2 | [shah-bakhsh/BalParser](https://huggingface.co/shah-bakhsh/BalParser) | Exact author-supplied biaffine architecture |
| BalNLP | [this repository](https://github.com/shah-bakhsh/BalNLP) | Unified Python/API/UI; Apache-2.0 source |

BalNLP uses its own word segmentation and each checkpoint's compatible subword tokenizer;
the separate BalTokenizer must not be substituted without architecture/evaluation checks.
The Hugging Face BalNER-v2 link is configured in source but could not be revalidated
during the 2026-09-21 audit; see [audit](docs/AUDIT.md).

Official revisions are pinned in `balnlp/config.py`. All IDs and revisions can be
overridden through environment variables; local directory paths also work. The empty
`BalNER` repository is deliberately not selected. No remote Python is trusted or run.
See [model integration details](docs/MODELS.md).

## Install and run locally

Requirements: **Python 3.12**, **Node.js 24**, and sufficient disk/RAM for the selected
checkpoints. Dependencies are pinned, with a frontend lockfile. Commands below start
from a checkout of this repository; `pip install balnlp` is not yet a verified distribution route.
In Windows PowerShell, use `Copy-Item` in place of `cp`.

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell instead:
# .\.venv\Scripts\Activate.ps1

python -m pip install torch==2.14.0 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -e '.[api,inference,dev]'
cp .env.example .env
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000 --no-access-log
```

In a second terminal:

```bash
cd frontend
cp .env.example .env.local
npm ci
npm run dev
```

Open http://localhost:3000. The API serves `/docs`, `/redoc`, and `/api/v1/health` on
port 8000. Health checks do not import PyTorch or load weights. Keep the backend
command at repository root so `.env` is found. Alternatively, install the root
package, change into `backend/`, supply environment variables, and run
`uvicorn app.main:app --reload`.

## Python quick start

```python
from balnlp import BalNLP

nlp = BalNLP.from_pretrained()
try:
    result = nlp.analyze("بلوچی متن")
    print(result.model_dump_json(indent=2))
    print(nlp.to_conllu(result))
finally:
    nlp.close()
```

Also supported: `nlp.pos(text)`, `nlp.ner(text)`, `nlp.morph(text)`, `nlp.parse(text)`
and `nlp.analyze(text, tasks=["pos", "ner", "parser"])`. The result is a Pydantic
model with `model_dump()` for a Python dictionary. Missing predictions remain null.

## API

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"بلوچی متن"}'
```

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/health` | Lightweight process liveness |
| GET | `/api/v1/models` | Safe configuration status; does not imply readiness |
| POST | `/api/v1/analyze` | All tasks, or a `tasks` list |
| POST | `/api/v1/pos` | POS only |
| POST | `/api/v1/ner` | NER only |
| POST | `/api/v1/morph` | Morphology only |
| POST | `/api/v1/parse` | Dependency parsing only |

Partial success is HTTP 200 with `meta.completed_tasks` and `meta.failed_tasks`.
If no requested task succeeds, a consistent error object and appropriate HTTP
status are returned. See [API contracts](docs/API.md).

## Tests and production build

```bash
# Root, Python virtual environment active
ruff check balnlp backend tests scripts
ruff format --check balnlp backend tests scripts
pytest -q -m 'not integration'

# Optional real checkpoints (downloads several GB; CPU inference is sequential)
# PowerShell: $env:BALNLP_RUN_INTEGRATION='1'
BALNLP_RUN_INTEGRATION=1 pytest -v -m integration

cd frontend
npm run lint
npm run typecheck
npm test
npm run build
npx playwright install chromium
npm run test:e2e
npm start
```

A model-free segmentation example (not model predictions):

```python
from balnlp.tokenizer import tokenize_balochi

print([token.form for token in tokenize_balochi("بلوچی متن")])
# ["بلوچی", "متن"]
```

The basic CI suite does not download model weights. It installs CPU PyTorch for
small synthetic architecture and decoder tests. Browser tests mock HTTP responses;
real integration tests are separate. GitHub Actions covers unit/fixture suites and the build; real checkpoint checks are
manual. See [development and package builds](docs/DEVELOPMENT.md).

## Docker and deployment

```bash
# Repository root; Docker daemon must be running
cp .env.example .env
docker compose config
docker compose up --build
```

Docker uses an unprivileged user, CPU wheels, one Uvicorn worker, and a shared model
cache volume. The frontend Docker build uses Next.js standalone output. Do not place
the Python backend on Vercel. Follow [Render and Railway deployment steps](docs/DEPLOYMENT.md).

## Memory, privacy, and operational limits

`BALNLP_MEMORY_MODE=low` loads and releases each task immediately. Balanced retains
up to two models with LRU eviction; performance retains up to four. Set those modes
only after measuring the available host memory. Downloads remain in Hugging Face's
cache; unloading weights does not delete the files. RSS release depends on OS and
allocator behavior. Quantization is intentionally not enabled without validation.

The default device is CPU. `BALNLP_DEVICE=auto` uses CUDA if present; `cuda` explicitly
requires it. One inference request runs at once, and busy requests get 503. HTTP
timeouts do not kill PyTorch threads: a timed-out job retains the slot until it ends.
An indefinitely blocked native call requires process restart. There is no unbounded
job queue. Client text is never persisted or logged; hosting-level access logs and
infrastructure behavior remain the operator's responsibility.

## Limitations and roadmap

- Extend author-reviewed linguistic evaluation of the recovered BalMorph adapter.
- Validate smaller or quantized checkpoints before promising 512 MB inference.
- Evaluate tokenization, first-subword POS/NER alignment, dialects, and domain shift.
- Add a broader author-reviewed example set; the shipped input example comes from the brief.
- Review sentence segmentation (punctuation/newlines) against treebank conventions.
- Shared encoder inference is future work, not an assumption about independent checkpoints.
- Dark mode is deferred; functional and accessible light-mode views are implemented.

BalParser's author-reported test results are UAS 54.33%, LAS 45.23%, Macro F1 46.78%,
Weighted F1 71.13%, and Root Accuracy 64.71%. These are not recomputed by the smoke
tests. Other evaluation summaries are not included until reviewed for publication.
See the [evaluation protocol](docs/EVALUATION.md) and [roadmap](docs/ROADMAP.md).

## Screenshots, citation, license, and contributing

[Desktop](docs/screenshots/home-desktop.png) · [Mobile](docs/screenshots/home-mobile.png)

Cite this software using [CITATION.cff](CITATION.cff) and record the exact commit used.
No DOI or paper is claimed.
The application source is licensed under **Apache-2.0**; see [LICENSE](LICENSE) and [NOTICE](NOTICE). Model
licenses are independent. Contributions follow [CONTRIBUTING.md](CONTRIBUTING.md).


## Recorded deployment status (2026-09-09)

These are historical checks, not a fresh availability guarantee. Source is published at https://github.com/shah-bakhsh/BalNLP.

Render API: https://balnlp-api.onrender.com/health — public health and registry checks passed. Analysis returns RESOURCE_LIMITED because the free plan has 512 MB RAM. No paid plan was activated.

Vercel frontend: https://balnlp-shah-bakhshs-projects.vercel.app — public frontend verified on 2026-09-09. Home and analysis pages return HTTP 200 without login; a browser submission reaches the API and displays its resource-limit error. See docs/VERCEL.md for domain setup and docs/deployment-status.json for verification details.

Overall status: DEPLOYMENT_READY_RESOURCE_LIMITED. The four-model pipeline works locally; live public inference is not available on the free API host.

## Contributor and maintainer resources

- [Contributing](CONTRIBUTING.md), [task proposals](docs/CONTRIBUTOR_TASKS.md), and [code of conduct](CODE_OF_CONDUCT.md)
- [Security reporting](SECURITY.md), [privacy](docs/PRIVACY.md), and [support/contact](SUPPORT.md)
- [Changelog](CHANGELOG.md), [release draft](docs/RELEASE_DRAFT.md), and [repository audit](docs/AUDIT.md)
- [Project structure](docs/TREE.md), [impact](docs/IMPACT.md), and [maintainer application drafts](docs/MAINTAINER_APPLICATION.md)

Acknowledgements: the Balochi language community and the maintainers of PyTorch,
Transformers, Hugging Face Hub, FastAPI, Next.js, and the project's other dependencies.
See [model provenance](docs/MODELS.md) for the independently maintained model sources.
