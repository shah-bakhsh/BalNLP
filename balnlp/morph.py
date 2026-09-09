import importlib

from .config import Settings
from .exceptions import BalNLPError


class BalMorph:
    """Exact inference source is required from the model author."""

    @classmethod
    def from_pretrained(cls, model_id, settings=None, revision=None):
        settings = settings or Settings()
        if not settings.balmorph_adapter:
            raise BalNLPError(
                "MODEL_NOT_AVAILABLE",
                "BalMorph checkpoint exists, but its verified inference implementation is not yet available.",
                503,
            )
        module, separator, name = settings.balmorph_adapter.partition(":")
        if not separator:
            raise BalNLPError(
                "MODEL_LOAD_FAILED", "The morphology adapter configuration is invalid.", 503
            )
        instance = cls()
        instance.adapter = getattr(importlib.import_module(module), name).from_pretrained(
            model_id, settings=settings, revision=revision
        )
        return instance

    def predict(self, tokens):
        return self.adapter.predict(tokens)

    def unload(self):
        self.adapter.unload()
