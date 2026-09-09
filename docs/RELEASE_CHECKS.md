# Current update: BalMorph recovered and verified

46 Python tests and five frontend tests pass. Strict checkpoint loading and exact logits against the author notebook class pass. The real unified API returns all four tasks, lemmas, features and valid CoNLL-U with no failed tasks. See balmorph-verification.json. Hosting remains resource-limited and not publicly deployed.

The following is the earlier release audit retained for history; its missing-BalMorph entries are superseded by this update.

# BalNLP 0.1.0 — verified release checks

Validation dates: 2026-09-07–08. Environment: Windows, Python 3.12.14, CPU PyTorch
2.14.0, Transformers 5.16.1, Node.js 24.17.0, Next.js 16.3.4, Microsoft Edge.

**Release status: application implemented; morphology and live deployment remain
blocked/unverified. It is not a fully complete four-model production release.**

| Area | Check | Status and evidence |
|---|---|---|
| Repository | Requested monorepo structure | PASS — source, docs, scripts, CI, deployment files present |
| Core | Python syntax/imports | PASS — compileall and FastAPI import/startup |
| Core | Tokenization and offsets | PASS — Unicode marks, NFC, punctuation, spans, invalid text tests |
| Core | POS wrapper | PASS — actual pinned BalPOS checkpoint CPU inference |
| Core | NER wrapper | PASS — actual pinned BalNER-v2 checkpoint CPU inference |
| Core | Morph wrapper interface | PASS — explicit safe missing-architecture response |
| Core | Real morphology integration | BLOCKED — author requires original source; no guessed predictions |
| Core | Parser wrapper | PASS — actual pinned checkpoint, strict loading, author-supplied operations |
| Core | Parser graph validity | PASS — one ROOT, valid HEADs, no self-loops/cycles, relation decoding |
| Core | Parser MST objective | PASS — random small graphs match exhaustive single-root optimum |
| Core | Biaffine score axes | PASS — direct bilinear calculation agrees with trained convention |
| Core | Unified analysis/merging | PASS — real browser request returns POS, NER, parser and morphology failure |
| Core | CoNLL-U | PASS — 10-column exports checked in unit and real inference tests |
| Core | Model manager | PASS — low-mode cleanup, failure cleanup, concurrent load prevention, LRU tests |
| Backend | FastAPI startup/health | PASS — real Uvicorn starts; liveness endpoint and docs tested |
| Backend | Analyze/POS/NER/parse API | PASS — endpoint unit tests and real unified HTTP inference |
| Backend | Morph API | PASS for contract/error handling; real inference BLOCKED |
| Backend | Errors/limits/CORS | PASS — input validation, body-size/rate controls, origin tests |
| Backend | Timeout/concurrency | PASS — timed-out job keeps the busy slot until completion |
| Frontend | Installation | PASS — npm install; lockfile generated; audit reported zero vulnerabilities |
| Frontend | ESLint | PASS — no errors or warnings in application lint |
| Frontend | TypeScript | PASS — tsc --noEmit |
| Frontend | Production build | PASS — requested routes prerender successfully |
| Frontend | Responsive UI | PASS — desktop 1280×720 and mobile 390×664 browser checks; no document overflow |
| Frontend | RTL rendering | PASS — RTL input attribute and visually inspected rendered screenshots |
| Frontend | API integration | PASS — real browser → FastAPI → three model checkpoints → result tabs |
| Frontend | Dependency SVG/exports | PASS — tree renders, JSON download succeeds; CoNLL-U generated |
| Security | Source secret-pattern scan | NONE FOUND — application source contains no credential-pattern matches |
| Security | Sensitive public variables | NONE FOUND — frontend only receives public URL/length/link values |
| Security | Critical TODO/FIXME/fake production predictions | NONE FOUND — morphology fails explicitly |
| Testing | Backend unit suite | PASS — 40 tests; real checkpoint tests separately deselected |
| Testing | Real checkpoint suite | PASS — 3 tests, one each POS/NER/parser, sequential CPU inference |
| Testing | Frontend component/client tests | PASS — 5 tests |
| Testing | Browser smoke suite | PASS — 4 fixture-based desktop/mobile tests |
| Testing | Real browser smoke | PASS — 2 desktop/mobile tests before the structured-registry update, 200 response, correct partial-result tasks |
| Dependencies | Python consistency | PASS — pip check found no broken requirements |
| Deployment | Docker Compose schema | PASS — docker compose config --quiet with example environment |
| Deployment | Docker image build/start | NOT RUN — Docker daemon unavailable on this machine |
| Deployment | Render configuration | PASS for YAML parsing/inspection; live deployment NOT RUN |
| Deployment | Render Free inference | BLOCKED — ~1.1 GB checkpoints exceed 512 MB RAM |
| Deployment | Vercel configuration | PASS for JSON/framework and production build; live deployment NOT RUN |
| Deployment | Environment templates | PASS — separate server/public settings; blank HF_TOKEN is anonymous |
| Release | Application license | BLOCKED — owner has not selected a license |

The real browser smoke used the brief's example `بلوچی متن`. Its full request took
approximately 39 seconds on this machine. This is a single smoke observation, not a
benchmark or latency promise. The desktop real-model screenshot records actual
predictions; the other analysis screenshots use explicitly test-only fixture results.

The suite does not re-estimate linguistic accuracy or establish parity with the
original evaluation corpus. BalParser's published metrics remain attributed to the
author's locked test run. Broader text/dialect evaluation is still needed.

Nonblocking dependency warnings: Starlette's current TestClient warns about httpx
and an AnyIO alias; tests pass. Some build/browser tools emit terminal-color warnings.
Those warnings do not change the outcomes above.

## Reproduce

See README.md for setup. Run the unit, lint, typecheck, build, and browser commands
there. For real browser verification, start the backend on port 8000 with
`FRONTEND_URL=http://127.0.0.1:3000`, cache/configure the real models, then run in frontend:

```bash
BALNLP_LIVE_E2E=1 npm run test:e2e -- --project=desktop
```

On Windows PowerShell: `$env:BALNLP_LIVE_E2E='1'`. If using installed Microsoft Edge,
set `$env:PLAYWRIGHT_CHANNEL='msedge'`; otherwise install Playwright Chromium.

## Remaining release work

1. Obtain and integrate exact BalMorph source, then add real morphology tests.
2. Select the application source license.
3. Build/start both Docker images on a host with Docker running.
4. Deploy to sufficient-memory CPU hosting and Vercel, then verify the live CORS/API flow.
5. Validate smaller models before describing Render Free inference as supported.


## Latest resource-aware release checks

40 Python tests pass, including disabled morphology, null morphology fields, memory guard and health/readiness distinction. Five frontend tests, ESLint, TypeScript compilation and Next static export pass after the structured registry change. Three actual checkpoint tests passed earlier in this session; BalPOS was additionally measured with real inference at 964 MiB RSS. Six desktop/mobile browser checks passed before the registry contract update. The final browser rerun was blocked by automatic approval review's usage-limit rejection; it is not claimed as rerun.

The release uses Render first and Railway as fallback. `render.yaml`, `railway.json` and portable `backend/Dockerfile` are present. Docker daemon validation and public deployment are outstanding. GitHub upload received HTTP 403: Resource not accessible by integration. Status: DEPLOYMENT_READY_RESOURCE_LIMITED. No paid resources have been activated.

Final local FastAPI TestClient lifecycle and real unified inference passed after the registry changes: POS/NER/parser completed, morphology fields null, one root, valid CoNLL-U. Request 37.54 seconds; process peak RSS 968.92 MiB. Website docs and API docs routes both returned 200. This was a local ASGI check, not a deployed public endpoint test.
