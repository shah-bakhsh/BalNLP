# Contributor task proposals

These are scoped ideas, not opened issues or claimed contributions. Confirm scope and
licensing with the maintainer before starting. Suggested labels below are a taxonomy;
they have not been created in GitHub.

## 1. Add permitted Balochi examples

- **Background:** Only one brief example is shipped.
- **Task:** Collect 5–10 short examples with permission/provenance and have a Balochi speaker review spelling.
- **Expected outcome:** Examples include provenance and task purpose; no fabricated gold annotations or private text.
- **Suggested files:** frontend/lib/examples.ts; docs/EVALUATION.md
- **Difficulty:** Easy
- **Labels:** good first issue, documentation, balochi
- **Acceptance criteria:** Examples include provenance and task purpose; no fabricated gold annotations or private text.

## 2. Expand Unicode tokenizer edge cases

- **Background:** Offsets are into NFC-normalized text; joiners and combining marks matter.
- **Task:** Add focused fixtures for ZWJ/ZWNJ, combining marks, CRLF, mixed punctuation, and emoji boundaries.
- **Expected outcome:** Each fixture checks token spans and sentence IDs; expected linguistic decisions are explained.
- **Suggested files:** tests/test_core.py; balnlp/tokenizer.py
- **Difficulty:** Easy
- **Labels:** good first issue, testing, balochi
- **Acceptance criteria:** Each fixture checks token spans and sentence IDs; expected linguistic decisions are explained.

## 3. Review sentence segmentation conventions

- **Background:** Shared punctuation segmentation differs from parser-card whitespace input.
- **Task:** Document difficult abbreviation and repeated-punctuation examples and propose an explicit convention.
- **Expected outcome:** Human-reviewed examples distinguish current behavior from proposed changes; compatibility impact documented.
- **Suggested files:** balnlp/tokenizer.py; docs/MODELS.md
- **Difficulty:** Medium
- **Labels:** research, balochi, testing
- **Acceptance criteria:** Human-reviewed examples distinguish current behavior from proposed changes; compatibility impact documented.

## 4. Audit RTL keyboard accessibility

- **Background:** The workspace supports RTL input but broader accessibility coverage is useful.
- **Task:** Check keyboard focus order, task radios, error announcements, and result tabs; fix a reproducible issue.
- **Expected outcome:** Document browser/viewport and keyboard steps; add a focused test for an actual defect.
- **Suggested files:** frontend/components/AnalysisWorkspace.tsx; frontend/components/Results.tsx; frontend/e2e/analysis.spec.ts
- **Difficulty:** Medium
- **Labels:** frontend, accessibility, help wanted
- **Acceptance criteria:** Document browser/viewport and keyboard steps; add a focused test for an actual defect.

## 5. Document partial-result API handling

- **Background:** HTTP 200 can still contain failed tasks.
- **Task:** Add a Python HTTP client example that inspects meta.failed_tasks and handles 429/503 safely.
- **Expected outcome:** Example matches actual response shapes and does not retry indefinitely or log private text.
- **Suggested files:** docs/API.md; backend/app/schemas/responses.py
- **Difficulty:** Easy
- **Labels:** good first issue, documentation, backend
- **Acceptance criteria:** Example matches actual response shapes and does not retry indefinitely or log private text.

## 6. Describe dialect/domain evaluation coverage

- **Background:** Smoke tests do not measure coverage of Balochi varieties.
- **Task:** Propose a consented evaluation matrix with reviewers and annotation conventions.
- **Expected outcome:** Mark unmeasured cells explicitly; list permitted sources and avoid claiming results.
- **Suggested files:** docs/EVALUATION.md; docs/MODELS.md
- **Difficulty:** Medium
- **Labels:** research, model, balochi
- **Acceptance criteria:** Mark unmeasured cells explicitly; list permitted sources and avoid claiming results.

## 7. Build a reproducible benchmark harness

- **Background:** Historical timings are single observations, not benchmarks.
- **Task:** Design an opt-in script recording model/code revisions, warm/cold state, hardware, memory, and repeated timings.
- **Expected outcome:** No default weight download in basic CI; output schema and sample synthetic run clearly labeled.
- **Suggested files:** scripts/; docs/EVALUATION.md
- **Difficulty:** Medium
- **Labels:** research, testing, help wanted
- **Acceptance criteria:** No default weight download in basic CI; output schema and sample synthetic run clearly labeled.

## 8. Improve unavailable-task explanations

- **Background:** The UI currently says a task is not connected even when memory is insufficient.
- **Task:** Map disabled, blocked, and resource_limited status to accurate user messages.
- **Expected outcome:** Tests cover each status and preserve text after errors; no promise that retrying fixes insufficient RAM.
- **Suggested files:** frontend/components/AnalysisWorkspace.tsx; frontend/lib/api.ts; frontend/tests/workspace.test.tsx
- **Difficulty:** Easy
- **Labels:** good first issue, frontend
- **Acceptance criteria:** Tests cover each status and preserve text after errors; no promise that retrying fixes insufficient RAM.

## 9. Add focused Python type annotations

- **Background:** Python has some annotations but no static-type CI gate.
- **Task:** Choose a small pure utility module, annotate its public contract, and propose a scoped checker configuration.
- **Expected outcome:** Runtime behavior unchanged; checker command and excluded scope documented; no blanket ignore rules.
- **Suggested files:** balnlp/conllu.py; balnlp/alignment.py; pyproject.toml
- **Difficulty:** Medium
- **Labels:** backend, help wanted
- **Acceptance criteria:** Runtime behavior unchanged; checker command and excluded scope documented; no blanket ignore rules.

## 10. Validate dependency-tree rendering on longer sentences

- **Background:** The SVG tree needs broader mixed-direction/long-input review.
- **Task:** Use fixture results to reproduce overlapping labels or overflow and improve rendering where necessary.
- **Expected outcome:** Before/after screenshots at desktop/mobile widths; fixtures clearly not accuracy evidence.
- **Suggested files:** frontend/components/DependencyTree.tsx; frontend/e2e/analysis.spec.ts
- **Difficulty:** Medium
- **Labels:** frontend, accessibility
- **Acceptance criteria:** Before/after screenshots at desktop/mobile widths; fixtures clearly not accuracy evidence.
