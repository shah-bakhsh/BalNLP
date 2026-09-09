import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

from balnlp import BalNLP
from balnlp.alignment import entities_from_bio, word_positions
from balnlp.config import Settings
from balnlp.exceptions import BalNLPError
from balnlp.model_manager import ModelManager
from balnlp.tokenizer import normalize_text, tokenize_balochi


class FakeModel:
    def __init__(self, task):
        self.task = task
        self.unloaded = False

    def predict(self, tokens):
        return [{"upos": "NOUN"} if self.task == "pos" else {"ner": "O"} for _ in tokens]

    def unload(self):
        self.unloaded = True


@pytest.mark.parametrize("text", [None, "", "   ", "\n", "...", "\x00word"])
def test_invalid_text(text):
    with pytest.raises(BalNLPError):
        normalize_text(text)


def test_unicode_offsets_and_punctuation():
    text = normalize_text("بلوچی، گوٛازینتگ\nمتن۔")
    tokens = tokenize_balochi(text)
    assert [t.form for t in tokens] == ["بلوچی", "،", "گوٛازینتگ", "متن", "۔"]
    assert all(text[t.start : t.end] == t.form for t in tokens)
    assert tokens[-1].sentence_id == 2


def test_alignment_rejects_missing_word():
    assert word_positions([None, 0, 0, 1, None], 2) == [[1, 2], [3]]
    with pytest.raises(BalNLPError):
        word_positions([None, 0], 2)


def test_pipeline_partial_atomic_merge_and_conllu():
    def factory(task):
        if task == "ner":
            raise RuntimeError("private internal details")
        return FakeModel(task)

    settings = Settings()
    nlp = BalNLP(settings, ModelManager(settings, factory))
    result = nlp.analyze("بلوچی متن", ["pos", "ner"])
    assert result.meta.completed_tasks == ["pos"]
    assert result.meta.failed_tasks[0].code == "MODEL_LOAD_FAILED"
    assert result.tokens[0].ner is None
    assert len(result.conllu.splitlines()[2].split("\t")) == 10
    assert "private" not in result.model_dump_json()


@pytest.mark.parametrize("tasks", [[], ["nope"], ["pos", "pos"], "pos"])
def test_tasks(tasks):
    with pytest.raises(BalNLPError):
        BalNLP().analyze("بلوچی", tasks)


def test_model_cleanup_after_inference_error():
    model = FakeModel("pos")

    def fail(tokens):
        raise RuntimeError("inference failed")

    model.predict = fail
    manager = ModelManager(Settings(), lambda task: model)
    with pytest.raises(RuntimeError):
        manager.predict("pos", [])
    assert model.unloaded
    assert not manager._models


def test_balanced_lru_and_concurrency():
    made = []
    lock = threading.Lock()

    def factory(task):
        with lock:
            made.append(task)
        return FakeModel(task)

    manager = ModelManager(Settings(balnlp_memory_mode="balanced"), factory)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda _: manager.predict("pos", []), range(8)))
    assert made == ["pos"]
    manager.load_model("ner")
    manager.load_model("morph")
    assert list(manager._models) == ["ner", "morph"]
    manager.unload_all()


def test_bio_entity_spans():
    text = "بلوچی متن"
    tokens = tokenize_balochi(text)
    tokens[0].ner, tokens[1].ner = "B-ORG", "I-ORG"
    entity = entities_from_bio(text, tokens)[0]
    assert entity.text == text and entity.token_ids == [1, 2]


def test_missing_morphology_is_explicit():
    from balnlp.morph import BalMorph

    with pytest.raises(BalNLPError, match="verified inference"):
        BalMorph.from_pretrained("shah-bakhsh/BalMorph", settings=Settings(balmorph_adapter=""))


def test_blank_token_from_env_template_is_anonymous():
    assert Settings(hf_token="").hf_token is None
