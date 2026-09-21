# Repository audit — 2026-09-21

Base commit: `8308d84062333d25a5cef5dab9c85a6a705351a1`.
The GitHub tree contains 123 text files and five PNG screenshots. Source was fetched
at this commit; no history was rewritten. Screenshots were inventoried, not freshly
rendered or visually revalidated. This is an engineering review, not a legal opinion,
penetration test, or independent reproduction of linguistic metrics.

## Findings and treatment

| Area | Existing evidence | Treatment / remaining gap |
|---|---|---|
| Core/package | Installable setuptools project; public BalNLP class; four adapters | Preserve inference; add README/author/URL metadata and package build checks |
| API | FastAPI routes, safe errors, resource guard, rate limits, single worker | Preserve controls; document unauthenticated boundary and transient IP state |
| Frontend | Next.js RTL workspace, exports, TypeScript and fixture tests | Preserve UI; propose status-message/accessibility improvements |
| Models | Official SHA pins; no remote Transformers code; strict custom loading | Preserve architectures; model quality remains independently unverified |
| Tokenization | Internal word segmentation plus checkpoint tokenizers | Explicitly distinguish separate BalTokenizer research project |
| CI | Unit lint/format checks, frontend typecheck/test/build/browser checks | Add distribution build/import checks and manual model workflow |
| Security | Ignored local env files, blank example token, safe log fields | Add disclosure/support policy; history and dependency vulnerability scans pending |
| Licensing | LICENSE explicitly grants no open-source rights | Preserve notice; owner must select license and verify provenance |
| Docs | Useful API/model/deployment details and dated verification artifacts | Add focused missing guides; mark superseded release entries as historical |
| Governance | CONTRIBUTING exists; other policies/forms absent | Add policies, citation, issue forms, PR checklist, ten task proposals |
| Releases | Package version 0.1.0; no GitHub releases listed | Prepare changelog/release draft; no tag or package published |
| Impact | 0 stars, 0 forks at audit time | Record honestly; omit unverified adoption/download/citation counts |
| Metadata | Empty GitHub description/topics | Prepared below; connector has no repository-metadata update action |

## Preserve

Existing tests, trained checkpoint semantics, revision pins, memory guard, API error
contracts, frontend behavior, historical JSON artifacts, and screenshots are preserved.
No models/datasets are relicensed. No fake outputs or model-quality scores are added.

## Links and evidence

Hugging Face pages for BalBERT, BalPOS, BalMorph, and BalParser opened during this audit.
BalTokenizer's GitHub repository and README were retrieved. BalNER-v2 is configured
in source but its live Hugging Face page could not be fetched; availability and license
need revalidation. No newly invented component URL was added. Existing links retained
in older documents are not all independently availability-checked.

The existing base-commit CI run was successful:
https://github.com/shah-bakhsh/BalNLP/actions/runs/34348038897
This historical success does not certify this change set. Fresh checks and limitations
are reported with the review branch/PR. Recorded real-model tests and deployment
observations have not been rerun by this audit.

## Owner actions and publication gates

1. Review the proposed changes and resulting CI; merge when satisfied.
2. Confirm authorship/provenance and choose the source license; review model/data terms.
3. Confirm the private reporting contact and enable private vulnerability reporting if desired.
4. Set repository metadata below; create the suggested labels when useful.
5. Revalidate BalNER-v2 and model licenses at their pinned revisions.
6. Run real checkpoint tests, Docker startup, and live API/UI checks on adequate hardware.
7. Establish licensed held-out evaluation and human linguistic review.
8. Verify PyPI name ownership, distribution contents, and version consistency before
   explicitly approving any upload or release.
9. Recheck program terms and evidence before submitting the application draft.

## Prepared repository metadata

Description until source licensing is resolved:
“Arabic-script Balochi NLP toolkit integrating POS tagging, NER, morphology and dependency parsing through Python, FastAPI and a web UI.”

After the source license is approved, the owner can accurately add “Open-source”.
Suggested topics: `balochi`, `nlp`, `natural-language-processing`,
`low-resource-languages`, `computational-linguistics`, `huggingface`, `transformers`,
`pos-tagging`, `named-entity-recognition`, `dependency-parsing`, `python`, `fastapi`,
`machine-learning`.

Suggested labels: `good first issue`, `help wanted`, `bug`, `enhancement`,
`documentation`, `research`, `model`, `frontend`, `backend`, `accessibility`,
`balochi`, `testing`. No issues or labels were manufactured as activity.

## Readiness

The repository has substantial implemented functionality and an existing passing CI
baseline. Open-source release readiness remains blocked by source licensing; package
publication and production inference require the checks above. Claude OSS eligibility
is not established. See [application drafts](MAINTAINER_APPLICATION.md),
[release draft](RELEASE_DRAFT.md), and [30-day plan](ROADMAP.md).

## Local verification in this audit

All fetched Python source parsed with Python 3.12; JSON, YAML, CFF, and TOML parsed.
Relative Markdown file links resolved against the repository inventory, including
existing screenshot paths. A limited credential-pattern scan found no matches in
the fetched text snapshot; this is not a full-history or comprehensive secret scan.
Package-index access failed locally, so dependency installation and the full application
test/build suites could not run here. GitHub CI is the fresh verification route for
the proposed branch. No new model-quality or live-deployment result is claimed.

Local setuptools 84.0.0 successfully built the source archive and wheel without
installing dependencies. Archive inspection confirmed package name/version, Python
constraint, README metadata, core/backend modules, the unchanged license notice, and
no model weights or .env file. This is not a fresh-environment installation/import test.
