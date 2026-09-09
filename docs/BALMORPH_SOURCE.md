# BalMorph v2 source provenance

Author-supplied notebook: notebook734a3c9640.ipynb

SHA-256: 6a3673e684c95cd843fa88063b60772bead7ddb0f60a0819b41aaa094a997d7e

Inference uses cells 16 (normalization), 36 (edit rules), 38 (labels), 42 (network), 44 (word inputs, max length 8), 54 (argmax decoding), and 70 (serialization). No training, installation, secret access or publishing cells were executed.

Mean pooling includes every attention-masked position, including special tokens. Each input is one word, padded/truncated to 8 subwords including special tokens. Learned edit rules strip a suffix and append the model-selected suffix. NONE feature labels are omitted. No dictionary or POS fallback is used.

The notebook has no valid reconstruction for the <UNK_RULE> class: apply_rule would attempt to unpack its string. This adapter reports lemma=null for that class and retains actual predicted features, instead of inventing a lemma or crashing. Valid learned rules use the exact notebook operation.
