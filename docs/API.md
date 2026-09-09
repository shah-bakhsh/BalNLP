# API contract

Base path `/api/v1`. Input is `{ "text": "بلوچی متن" }`. The analyze endpoint also
accepts a distinct nonempty `tasks` array drawn from `pos`, `ner`, `morph`, `parser`.
An omitted/null tasks field means all enabled tasks (all four models by default). Unknown input properties are rejected.

Successful responses contain `text`, `language`, `tokens`, `entities`,
`dependency_tree`, `meta`, and `conllu`. Text is NFC-normalized. Offsets use Unicode
code points, not UTF-16 indices; the frontend uses `Array.from(text)` for highlighting.
Token IDs are document-wide, with `sentence_id` and HEAD 0 for ROOT. Unavailable
fields are null; an empty feature dictionary means an available model predicted no
features. Metadata reports completed/failed tasks, per-task load/inference times,
and total elapsed time. No paths or credentials are returned.

| Code | HTTP | Meaning |
|---|---:|---|
| INVALID_TEXT / INVALID_TASKS | 422 | Invalid JSON contract or unusable input |
| TEXT_TOO_LONG | 422 | Character, word, or model subword limit |
| REQUEST_TOO_LARGE | 413 | Body exceeds configured byte limit |
| REQUEST_TIMEOUT | 408 | Body did not arrive within the configured deadline |
| MODEL_NOT_AVAILABLE | 503 | Missing model or blocked adapter |
| MODEL_LOAD_FAILED | 503 | Download/config/checkpoint failure |
| SERVICE_BUSY | 503 | A job is already running |
| RATE_LIMITED | 429 | In-process request limit |
| INFERENCE_TIMEOUT | 504 | Request deadline elapsed |
| INFERENCE_FAILED | 500 | Model execution, alignment, or tree validation failed |
| INTERNAL_ERROR | 500 | Unexpected application error |

```json
{"error":{"code":"INVALID_TEXT","message":"Please enter Balochi text."}}
```

Partial success is HTTP 200, with each failed task listed in `meta.failed_tasks`.
All requested tasks failing yields an error response using the first failure. The
UI only shows result tabs for completed tasks.

`/health` (also `/api/v1/health`) is liveness. `/ready` reports whether this host can accept lazy inference; it returns 503 under the free-host memory limit. `/api/v1/models` returns an object for each task with name, status, reason, checkpoint_available, inference_code_verified and loaded. Status is configured, loaded, disabled, resource_limited or blocked. Configured means loadable configuration, not verified successful inference. The verified notebook morphology adapter is enabled by default. `/api/v1/diagnostics` exposes memory numbers only. No checkpoint loading occurs on these requests.

`RESOURCE_LIMITED` is HTTP 503 and means the declared/container RAM is below the model budget. No guessed or downgraded prediction is generated. Interactive API docs are `/docs` and `/redoc` for the separate API, or `/api/docs` and `/api/redoc` when serving the combined website.

Only the exact configured FRONTEND_URL origin is allowed. Requests do not need cookies.
Rate limiting stores only bounded transient IP/timestamp records and is suitable for
one instance/worker. Forwarded headers are not trusted by default, so proxied users
may share a limit. Configure trusted proxy addresses at the server layer only after
verifying the hosting topology; never blindly use X-Forwarded-For.

Timeouts cannot kill native threads. The heavy job stays in its single execution slot
after an HTTP timeout. Wait for it to finish or restart the process if a native call
is permanently blocked. Do not run multiple workers on a constrained host.
