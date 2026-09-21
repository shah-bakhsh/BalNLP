# Architecture

BalNLP unifies independently trained model adapters behind one result schema. It does
not merge the component repositories or assume a shared encoder at inference time.

| Layer | Source | Responsibility |
|---|---|---|
| Web workspace | `frontend/components/AnalysisWorkspace.tsx` | RTL input, task selection, request state |
| HTTP client | `frontend/lib/api.ts` | API calls, timeout/error handling |
| API | `backend/app/main.py`, `backend/app/api/` | Routes, lifecycle, CORS, structured errors |
| Resource controls | `backend/app/middleware.py`, `backend/app/services/` | Bounded requests, rate limits, one inference slot |
| Pipeline | `balnlp/pipeline.py` | Normalization, tokenization, task order, atomic result merging |
| Model management | `balnlp/model_manager.py` | Lazy loading, locking, LRU retention, unload |
| Adapters | `balnlp/model_base.py`, `morph_adapter.py`, `parser.py` | Checkpoint-compatible inference |
| Export | `balnlp/conllu.py` | Sentence-local CoNLL-U IDs and heads |

Word segmentation is implemented in `balnlp/tokenizer.py`; checkpoint tokenizers handle
subwords. The separate BalTokenizer project is related research, not a runtime dependency.
The core imports no FastAPI. API concurrency controls wrap synchronous CPU inference;
a timed-out HTTP request does not cancel its worker thread. Pipeline tasks run in
POS, NER, morphology, parser order, but do not consume each other's predictions.

JSON uses document-wide IDs and Unicode code-point offsets into NFC-normalized text.
CoNLL-U remaps IDs and heads per sentence. Unavailable predictions stay null. See
[API](API.md), [models](MODELS.md), and [privacy](PRIVACY.md).
