"""Inference recovered from the author-supplied BalMorph v2 notebook."""

import re
import unicodedata

from .exceptions import BalNLPError
from .model_base import BaseWrapper, ModelSource


def decode_rule(word, encoded):
    if encoded == "<UNK_RULE>":
        return None
    count, separator, suffix = encoded.partition("::")
    if not separator or not count.isdecimal():
        raise BalNLPError("MODEL_LOAD_FAILED", "Invalid BalMorph lemma rule encoding.", 503)
    strip = min(int(count), len(word))
    return (word[: len(word) - strip] if strip > 0 else word) + suffix


class NotebookBalMorph(BaseWrapper):
    @classmethod
    def from_pretrained(cls, model_id, settings, revision=None):
        import torch
        from transformers import AutoConfig, AutoModel, AutoTokenizer

        from .morph_network import BalMorphModel

        source = ModelSource(model_id, settings, revision)
        training = source.json("training_config.json")
        labels = source.json("label_mappings.json")
        if (
            training.get("pooling") != "mean"
            or training.get("attrs_present") != labels["ATTRS_PRESENT"]
        ):
            raise BalNLPError(
                "MODEL_LOAD_FAILED",
                "BalMorph configuration differs from the verified notebook.",
                503,
            )
        rules = {v: k for k, v in labels["RULE2ID"].items()}
        attrs = {
            a: {v: k for k, v in labels["ATTR2ID"][a].items()} for a in labels["ATTRS_PRESENT"]
        }
        for mapping in [rules, *attrs.values()]:
            if set(mapping) != set(range(len(mapping))):
                raise BalNLPError(
                    "MODEL_LOAD_FAILED", "BalMorph label IDs must be contiguous.", 503
                )
        for rule in rules.values():
            decode_rule("", rule)
        config = AutoConfig.from_pretrained(source.file("config.json"), trust_remote_code=False)
        with torch.device("meta"):
            model = BalMorphModel(
                AutoModel.from_config(config, trust_remote_code=False),
                config.hidden_size,
                len(rules),
                {a: len(m) for a, m in attrs.items()},
                dropout=training["dropout"],
            )
        state = torch.load(
            source.file("pytorch_model.bin"), map_location="cpu", weights_only=True, mmap=True
        )
        model.load_state_dict(state, strict=True, assign=True)
        del state
        embeddings = model.encoder.embeddings
        embeddings.position_ids = torch.arange(config.max_position_embeddings).expand((1, -1))
        embeddings.token_type_ids = torch.zeros(embeddings.position_ids.size(), dtype=torch.long)
        tokenizer = AutoTokenizer.from_pretrained(model_id, **source.kwargs())
        instance = cls(source, model, tokenizer)
        instance.rules, instance.attrs = rules, attrs
        return instance

    def predict(self, tokens):
        import torch

        predictions = []
        with torch.inference_mode():
            for start in range(0, len(tokens), 32):
                words = [
                    re.sub(
                        r"\s+", " ", unicodedata.normalize("NFC", t.form.replace("\ufeff", ""))
                    ).strip()
                    for t in tokens[start : start + 32]
                ]
                encoded = self.tokenizer(
                    words, truncation=True, max_length=8, padding="max_length", return_tensors="pt"
                ).to(self.device)
                rule_logits, attr_logits = self.model(
                    encoded["input_ids"], encoded["attention_mask"], pooling="mean"
                )
                rules = rule_logits.argmax(-1).tolist()
                features = {a: logits.argmax(-1).tolist() for a, logits in attr_logits.items()}
                for i, word in enumerate(words):
                    feats = {
                        a: self.attrs[a][ids[i]]
                        for a, ids in features.items()
                        if self.attrs[a][ids[i]] != "NONE"
                    }
                    predictions.append(
                        {"lemma": decode_rule(word, self.rules[rules[i]]), "feats": feats}
                    )
        return predictions
