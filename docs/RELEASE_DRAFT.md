# Draft v0.1.0 release notes — not published

BalNLP brings Arabic-script Balochi analysis into one Python library, FastAPI service,
and RTL web workspace. The existing package version is 0.1.0; this document does not
create a tag, publish a package, or establish a release date.

## Added

- POS, NER, morphology, and dependency-parser adapters with configurable pinned sources.
- Word alignment, normalized code-point offsets, structured results, and CoNLL-U export.
- Lazy model loading, memory modes, bounded API input, partial results, and error handling.
- RTL web interface and fixture-based Python/frontend/browser checks.
- Contributor forms, security/support policies, citation metadata, and release guidance.

## Changed / Fixed

Repository documentation distinguishes related research from active dependencies,
historical verification from new checks, and smoke tests from quality evaluation.
Package metadata and Docker packaging inputs are aligned for distribution builds.

## Security

Remote Transformers Python is disabled; custom checkpoints use restricted loading.
See the security policy for remaining artifact, dependency, configuration, and hosting risks.
This release draft does not claim a security certification or newly fixed vulnerability.

## Known limitations and release gates

Source licensing is unresolved. PyPI publication/name ownership, fresh full-model
verification, Docker startup, and adequate-memory deployment require maintainer review.
The recorded free host cannot run published checkpoints. Accuracy remains author-reported
unless reproduced under a documented evaluation protocol. See [development](DEVELOPMENT.md),
[licensing](LICENSING.md), and [roadmap](ROADMAP.md) before approving publication.
