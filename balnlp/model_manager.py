import logging
import threading
from collections import OrderedDict
from time import perf_counter

from .config import Settings
from .exceptions import BalNLPError
from .utils import release_memory

logger = logging.getLogger("balnlp.models")


class ModelManager:
    """Lock spans loading AND inference, preventing eviction of an in-use model."""

    def __init__(self, settings: Settings, factory=None):
        self.settings = settings
        self.factory = factory or self._factory
        self._models = OrderedDict()
        self._loaded_tasks = ()
        self._lock = threading.RLock()
        self.capacity = {"low": 1, "balanced": 2, "performance": 4}[settings.balnlp_memory_mode]

    def _factory(self, task):
        from .memory import memory_diagnostics

        limit = memory_diagnostics(self.settings)["limit_mb"]
        if limit is not None and limit < self.settings.balnlp_min_model_memory_mb:
            raise BalNLPError(
                "RESOURCE_LIMITED",
                "This host has insufficient memory for the published checkpoint. Inference requires a larger host; no prediction was generated.",
                503,
            )
        from .morph import BalMorph
        from .ner import BalNER
        from .parser import BalParser
        from .pos import BalPOS

        cls = {"pos": BalPOS, "ner": BalNER, "morph": BalMorph, "parser": BalParser}[task]
        return cls.from_pretrained(
            self.settings.model_id(task),
            settings=self.settings,
            revision=self.settings.revision(task),
        )

    def load_model(self, task):
        with self._lock:
            if task not in self._models:
                if not self.settings.model_id(task):
                    raise BalNLPError(
                        "MODEL_NOT_AVAILABLE", f"The {task} model is not configured.", 503
                    )
                while len(self._models) >= self.capacity:
                    self.unload_model(next(iter(self._models)))
                start = perf_counter()
                try:
                    self._models[task] = self.factory(task)
                except BalNLPError:
                    raise
                except Exception:
                    release_memory()
                    raise BalNLPError(
                        "MODEL_LOAD_FAILED",
                        f"The {task} model could not be loaded. Please try again later.",
                        503,
                    ) from None
                logger.info(
                    "model_loaded task=%s duration_ms=%.1f", task, (perf_counter() - start) * 1000
                )
            self._models.move_to_end(task)
            self._loaded_tasks = tuple(self._models)
            return self._models[task]

    @property
    def loaded_tasks(self):
        """Immutable status snapshot; never waits on a heavy inference lock."""
        return self._loaded_tasks

    get_model = load_model

    def predict(self, task, tokens):
        with self._lock:
            start = perf_counter()
            try:
                model = self.load_model(task)
                loaded = perf_counter()
                predictions = model.predict(tokens)
                end = perf_counter()
                return predictions, {
                    "load": round((loaded - start) * 1000, 2),
                    "inference": round((end - loaded) * 1000, 2),
                }
            finally:
                if self.settings.balnlp_memory_mode == "low":
                    self.unload_model(task)

    def unload_model(self, task):
        with self._lock:
            model = self._models.pop(task, None)
            self._loaded_tasks = tuple(self._models)
            if model is not None:
                model.unload()
                del model
                release_memory()

    def unload_all(self):
        with self._lock:
            for task in list(self._models):
                self.unload_model(task)
