import pytest
from fastapi.testclient import TestClient
from test_api import Model, make_app

from balnlp import BalNLP
from balnlp.config import Settings
from balnlp.exceptions import BalNLPError
from balnlp.model_manager import ModelManager


def test_disabled_morphology_stays_null():
    settings = Settings(enable_pos=True, enable_ner=True, enable_morph=False, enable_parser=True)
    nlp = BalNLP(settings, ModelManager(settings, Model))
    result = nlp.analyze("بلوچی متن")
    assert result.meta.completed_tasks == ["pos", "ner", "parser"]
    assert all(token.lemma is None and token.feats is None for token in result.tokens)
    with pytest.raises(BalNLPError, match="disabled"):
        nlp.morph("بلوچی متن")


def test_resource_limit_blocks_before_transformer_load():
    nlp = BalNLP.from_pretrained(balnlp_memory_limit_mb=512)
    with pytest.raises(BalNLPError) as error:
        nlp.pos("بلوچی متن")
    assert error.value.code == "RESOURCE_LIMITED"
    assert not nlp.manager.loaded_tasks


def test_liveness_distinct_from_resource_readiness():
    with TestClient(make_app(balnlp_memory_limit_mb=512)) as client:
        assert client.get("/health").status_code == 200
        response = client.get("/ready")
        assert response.status_code == 503
        assert response.json()["models"]["pos"]["status"] == "resource_limited"
        morph = client.get("/api/v1/models").json()["morph"]
        assert morph["checkpoint_available"] is True
        assert morph["inference_code_verified"] is True
        assert morph["status"] == "resource_limited"
