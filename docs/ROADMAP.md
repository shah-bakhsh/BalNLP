# Roadmap

This is a plan, not a delivery guarantee. Existing implemented components include the
Python pipeline, four model adapters, FastAPI routes, RTL workspace, exports, and
fixture-based CI. Their presence does not imply complete linguistic validation.

## Next 30 days

| Period | Work | Completion evidence |
|---|---|---|
| Days 1–7 | Confirm third-party licensing provenance, private reporting contact, review this audit, verify package build | Approved license/provenance record; green checks |
| Days 8–14 | Add permitted Balochi examples, tokenizer edge cases, RTL accessibility review | Reviewed examples and focused tests/PRs |
| Days 15–21 | Define held-out evaluation protocol; run real models on adequate CPU hardware | Reproducible command, revision/hardware record, human feedback |
| Days 22–30 | Test Docker, verify deployment, review package name and release draft | Image startup/API checks and explicit release decision |

## Medium term

- Publish to PyPI only after licensing, package ownership, and distribution checks.
- Evaluate dialect/domain coverage and quantify raw-text segmentation effects.
- Measure memory and latency; validate optimized or smaller models before advertising them.
- Improve Python typing, frontend error messages, and contributor onboarding from real feedback.

## Long term

- Support independently verified research/developer use and community-maintained resources.
- Share datasets only where licenses and consent permit.
- Add downstream tasks when data and reproducible evaluation support them.
- Explore shared representations only where trained architectures are compatible.

See [contributor tasks](CONTRIBUTOR_TASKS.md). No adoption target should be pursued
through fake stars, reciprocal PRs, or meaningless activity.
