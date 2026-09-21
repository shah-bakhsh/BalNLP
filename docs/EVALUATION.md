# Evaluation and evidence

Keep three kinds of evidence separate:

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| Unit/API/browser fixtures | Contracts, failure handling, alignment and UI behavior | Linguistic accuracy |
| Real checkpoint smoke tests | Loading and inference on selected inputs | Benchmark reproduction or dialect coverage |
| Held-out linguistic evaluation | Metrics for the documented corpus/protocol | General performance across unseen domains |

[Historical release checks](RELEASE_CHECKS.md) and [BalMorph verification](balmorph-verification.json)
record earlier local observations. This audit does not independently reproduce them.
Published model-card numbers remain author-reported. No new accuracy, latency,
throughput, or memory benchmark is introduced by repository cleanup.

For a reproducible evaluation, record code commit, checkpoint SHA, licensed corpus
version, split hashes, normalization, sentence/word segmentation, label definitions,
subword alignment, package versions, hardware, seed, and command. Keep the held-out
test data out of tuning. Report POS accuracy, NER entity span precision/recall/F1,
lemma exact match and feature metrics, and parser UAS/LAS with punctuation and root
conventions explicitly stated. Report sample size, exclusions, and uncertainty.

Evaluate punctuation/newlines, joining marks, spelling variants, long words, and
permitted dialect/domain samples with human Balochi reviewers. Compare raw-text results
separately from gold-segmented inputs: the shared tokenizer differs from the parser
card's whitespace convention. BalMorph truncates each word to eight subwords including
special tokens. Record that limitation rather than silently changing the trained path.
