# Model integration and provenance

Source: the [author's Hugging Face profile](https://huggingface.co/shah-bakhsh), inspected
2026-09-07, and the exact BalParser architecture supplied by the author in this task.

| Task | Revision | Approximate checkpoint bytes |
|---|---|---:|
| BalPOS | `572de08cc59918199ca0eafd47ca6202181f6a2a` | 1,109,885,488 |
| BalNER-v2 | `d7a879d3e24f53f1d75eced26ab0167c803c9f67` | 1,109,863,956 |
| BalMorph | `06815c4e79a755a73890d2857b3d3f5b03d8e118` | 1,112,912,711 |
| BalParser | `8937729c3f86c9327a457d9ed8f49238ef7f4b51` | 1,131,759,483 (`model/parser_head.pt`) |

Official IDs select these commits unless a revision override is provided. Changing
only an ID to a custom repository or local directory disables the official commit
default. Do not commit `HF_TOKEN`; it stays server-side in a masked settings field.

## POS and NER

Both verified configs declare `XLMRobertaForTokenClassification`. The wrapper uses
`AutoModelForTokenClassification`, eval mode, inference mode, and the checkpoint's
id2label. It rejects missing/mismatched weights and generic LABEL_n mappings.
Subword labels are gathered at each word's first subword, following the standard
[Transformers token-classification alignment](https://huggingface.co/docs/transformers/tasks/token_classification).
Training code should be used to confirm this alignment protocol for full evaluation
parity; a successful smoke test is not a reproduction of reported metrics.

## Parser

The network preserves the author-supplied implementation:

- Saved config: 768-dimensional arc MLPs, 256-dimensional relation MLPs, dropout 0.2.
- Linear → ReLU → Dropout MLPs; explicit learned `root_embedding` at index 0.
- Mean word pooling over the supplied word/subword positions.
- Biaffine weights `[labels, head_dim + bias_head, dep_dim + bias_dep]`.
- Arc bias: dependent true, head false. Relation bias: both true.
- Exact einsum `bhd,lde,bne->blhn`; axes remain head then dependent throughout.
- Single-root maximum spanning arborescence enumerates the root child and maximizes
  the same sum of head→dependent scores. It never inserts heuristic dependency edges.
- Relation argmax is taken at the predicted HEAD, never gold HEAD.

The file named `model/parser_head.pt` actually includes the entire fine-tuned encoder.
Load it once with `weights_only=True, mmap=True`; do not load a second encoder weight
copy. Create the architecture on the meta device and use strict `assign=True` loading.
Recreate only XLM-R's nonpersistent position/token-type buffers using the installed
Transformers constructors' deterministic definitions. This does not change learned
parameters. Unexpected or absent trained tensors cause a load failure.

Token IDs are global in JSON, while parser scoring is local to each sentence. Map
predicted local HEADs back to global IDs, and remap on CoNLL-U export. Exactly one
root, valid HEADs, no cycles, no self-loops, and root relation consistency are checked.
Inconsistent predictions are reported as failed inference rather than silently repaired.

## Morphology: verified v2 integration

The author supplied notebook734a3c9640.ipynb. Its model and reconstruction operations are implemented in morph_network.py and morph_adapter.py. Strict full-checkpoint loading succeeds. Raw logits exactly match the notebook class on verification inputs, and real API inference returns lemmas/features. See BALMORPH_SOURCE.md and balmorph-verification.json.

Each word is encoded independently with padding/truncation to 8 subwords, including special tokens, exactly as trained. Masked mean pooling includes special tokens. The lemma head selects a learned strip/append rule; independent feature heads use argmax with NONE omitted. No dictionary or POS fallback is used. The undefined <UNK_RULE> reconstruction returns null. The source notebook reports ambiguity in evaluation; it has no extra inference disambiguation layer.

The trusted adapter interface remains configurable using BALMORPH_ADAPTER. Default: balnlp.morph_adapter:NotebookBalMorph.

## Tokenization limitation

The shared tokenizer separates punctuation, preserves combining marks/joiners, and
uses NFC. The parser card describes whitespace raw-text tokenization. This difference
is intentional to align all task outputs and must be evaluated; published metrics
are treebank results and are not guarantees for this frontend's raw-text workflow.
POS/NER/parser oversized sentences receive a clear error. BalMorph uses the original eight-token word truncation described above.


