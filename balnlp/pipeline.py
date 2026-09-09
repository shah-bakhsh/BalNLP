import logging
from time import perf_counter

from .alignment import entities_from_bio, merge_predictions
from .config import Settings
from .conllu import to_conllu
from .exceptions import BalNLPError
from .model_manager import ModelManager
from .schemas import TASKS, AnalysisResult, TaskFailure
from .tokenizer import normalize_text, tokenize_balochi

logger = logging.getLogger("balnlp.pipeline")


class BalNLP:
    def __init__(self, settings=None, manager=None):
        self.settings = settings or Settings()
        self.manager = manager or ModelManager(self.settings)

    @classmethod
    def from_pretrained(cls, **configuration):
        return cls(Settings(**configuration))

    def analyze(self, text, tasks=None):
        start = perf_counter()
        selected = (
            [task for task in TASKS if getattr(self.settings, f"enable_{task}")]
            if tasks is None
            else tasks
        )
        if (
            not isinstance(selected, list)
            or not selected
            or any(task not in TASKS for task in selected)
            or len(set(selected)) != len(selected)
        ):
            raise BalNLPError("INVALID_TASKS", "Choose one or more distinct supported tasks.")
        normalized = normalize_text(text, self.settings.max_text_length)
        tokens = tokenize_balochi(normalized)
        if len(tokens) > self.settings.max_tokens:
            raise BalNLPError(
                "TEXT_TOO_LONG", f"Please use at most {self.settings.max_tokens} tokens."
            )
        result = AnalysisResult(text=normalized, tokens=tokens)
        failures = []
        for task in TASKS:
            if task not in selected:
                continue
            try:
                if not getattr(self.settings, f"enable_{task}"):
                    raise BalNLPError(
                        "MODEL_NOT_AVAILABLE",
                        "Morphology is disabled in the service configuration."
                        if task == "morph"
                        else f"The {task} model is disabled.",
                        503,
                    )
                predictions, timing = self.manager.predict(task, result.tokens)
                merged = merge_predictions(result.tokens, predictions, task)
                if task == "parser":
                    from .parser import validate_heads

                    validate_heads(merged)
                result.tokens = merged
                result.meta.timings_ms[task] = timing
                result.meta.completed_tasks.append(task)
            except Exception as error:
                safe = (
                    error
                    if isinstance(error, BalNLPError)
                    else BalNLPError(
                        "INFERENCE_FAILED", f"The {task} analysis could not be completed.", 500
                    )
                )
                logger.warning("task_failed task=%s code=%s", task, safe.code)
                failures.append(safe)
                result.meta.failed_tasks.append(
                    TaskFailure(task=task, code=safe.code, message=safe.message)
                )
        if not result.meta.completed_tasks:
            raise failures[0]
        if "ner" in result.meta.completed_tasks:
            result.entities = entities_from_bio(result.text, result.tokens)
        if "parser" in result.meta.completed_tasks:
            result.dependency_tree = {
                "edges": [
                    {
                        "head": t.head,
                        "dependent": t.id,
                        "relation": t.deprel,
                        "sentence_id": t.sentence_id,
                    }
                    for t in result.tokens
                ]
            }
        result.meta.total_ms = round((perf_counter() - start) * 1000, 2)
        result.conllu = to_conllu(result)
        return result

    def pos(self, text):
        return self.analyze(text, ["pos"])

    def ner(self, text):
        return self.analyze(text, ["ner"])

    def morph(self, text):
        return self.analyze(text, ["morph"])

    def parse(self, text):
        return self.analyze(text, ["parser"])

    def to_conllu(self, result):
        return to_conllu(result)

    def close(self):
        self.manager.unload_all()
