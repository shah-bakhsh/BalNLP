import json
from itertools import groupby
from pathlib import Path
from time import sleep

from .alignment import word_positions
from .config import Settings
from .exceptions import BalNLPError


class ModelSource:
    def __init__(self, model_id, settings, revision=None):
        if not model_id:
            raise BalNLPError("MODEL_NOT_AVAILABLE", "This model is not configured.", 503)
        self.model_id, self.settings, self.revision = model_id, settings, revision

    def file(self, filename):
        if Path(self.model_id).is_dir():
            path = Path(self.model_id) / filename
            if not path.is_file():
                raise BalNLPError("MODEL_LOAD_FAILED", "A required model file is missing.", 503)
            return str(path)
        import httpx
        from huggingface_hub import hf_hub_download
        from huggingface_hub.errors import HfHubHTTPError

        for attempt in range(self.settings.model_load_attempts):
            try:
                return hf_hub_download(
                    self.model_id,
                    filename,
                    revision=self.revision,
                    token=self.settings.hf_token.get_secret_value()
                    if self.settings.hf_token
                    else None,
                )
            except (httpx.TransportError, HfHubHTTPError) as error:
                status = getattr(getattr(error, "response", None), "status_code", 500)
                if (
                    status < 500
                    and status != 429
                    or attempt + 1 == self.settings.model_load_attempts
                ):
                    raise BalNLPError(
                        "MODEL_LOAD_FAILED",
                        "The model download failed. Please try again later.",
                        503,
                    ) from None
                sleep(attempt + 1)

    def json(self, filename):
        return json.loads(Path(self.file(filename)).read_text(encoding="utf-8"))

    def kwargs(self):
        return {
            "revision": self.revision,
            "trust_remote_code": False,
            "token": self.settings.hf_token.get_secret_value() if self.settings.hf_token else None,
        }


class BaseWrapper:
    def __init__(self, source, model, tokenizer):
        import torch

        self.source, self.model, self.tokenizer = source, model, tokenizer
        torch.set_num_threads(source.settings.balnlp_cpu_threads)
        requested = source.settings.balnlp_device
        device = "cuda" if requested == "auto" and torch.cuda.is_available() else requested
        self.device = "cpu" if device == "auto" else device
        if self.device == "cuda" and not torch.cuda.is_available():
            raise BalNLPError("MODEL_LOAD_FAILED", "CUDA was selected but is unavailable.", 503)
        self.model.to(self.device).eval()

    def batches(self, tokens, limit=None):
        for _, sentence in groupby(tokens, key=lambda t: t.sentence_id):
            words = list(sentence)
            encoded = self.tokenizer(
                [t.form for t in words],
                is_split_into_words=True,
                return_tensors="pt",
                truncation=False,
            )
            maximum = min(
                limit or self.source.settings.max_subwords,
                self.source.settings.max_subwords,
                getattr(self.tokenizer, "model_max_length", 512),
                512,
            )
            if encoded["input_ids"].shape[1] > maximum:
                raise BalNLPError(
                    "TEXT_TOO_LONG",
                    f"A sentence exceeds the model's {maximum}-subword limit. Split it into shorter sentences.",
                )
            positions = word_positions(encoded.word_ids(), len(words))
            yield words, encoded.to(self.device), positions

    def unload(self):
        self.model = None
        self.tokenizer = None


class TokenClassificationWrapper(BaseWrapper):
    field = "upos"

    @classmethod
    def from_pretrained(cls, model_id, settings=None, revision=None):
        from transformers import AutoModelForTokenClassification, AutoTokenizer

        source = ModelSource(model_id, settings or Settings(), revision)
        # Explicit safetensors only; reject accidental masked-LM/random classification heads.
        config = source.json("config.json")
        if not any("ForTokenClassification" in x for x in config.get("architectures", [])):
            raise BalNLPError(
                "MODEL_LOAD_FAILED", "This checkpoint is not a token classifier.", 503
            )
        tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True, **source.kwargs())
        if not tokenizer.is_fast:
            raise BalNLPError(
                "MODEL_LOAD_FAILED", "A fast tokenizer is required for word alignment.", 503
            )
        model, info = AutoModelForTokenClassification.from_pretrained(
            model_id, use_safetensors=True, output_loading_info=True, **source.kwargs()
        )
        if info.get("missing_keys") or info.get("mismatched_keys"):
            raise BalNLPError(
                "MODEL_LOAD_FAILED", "The checkpoint has missing or incompatible weights.", 503
            )
        return cls(source, model, tokenizer)

    def predict(self, tokens):
        import torch

        result = []
        with torch.inference_mode():
            for _, encoded, positions in self.batches(tokens):
                logits = self.model(**encoded).logits[0]
                # Standard training alignment: classify the first subword of each word.
                for indices in positions:
                    label = self.model.config.id2label[int(logits[indices[0]].argmax())]
                    if label.startswith("LABEL_"):
                        raise BalNLPError(
                            "INFERENCE_FAILED", "The model needs a descriptive label mapping.", 500
                        )
                    result.append({self.field: label})
        return result
