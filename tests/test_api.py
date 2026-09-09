import asyncio
import threading

import pytest
from fastapi.testclient import TestClient

from backend.app.config import APISettings
from backend.app.main import create_app
from backend.app.services.balnlp_service import BalNLPService
from balnlp import BalNLP
from balnlp.exceptions import BalNLPError
from balnlp.model_manager import ModelManager


class Model:
    def __init__(self, task):
        self.task = task

    def predict(self, tokens):
        return [
            {"upos": "NOUN"}
            if self.task == "pos"
            else {"ner": "O"}
            if self.task == "ner"
            else {"lemma": None, "feats": {}}
            if self.task == "morph"
            else {"head": 0 if i == 0 else 1, "deprel": "root" if i == 0 else "dep"}
            for i, _ in enumerate(tokens)
        ]

    def unload(self):
        self.task = None


def make_app(**kwargs):
    settings = APISettings(**kwargs)
    pipeline = BalNLP(settings, ModelManager(settings, Model))
    return create_app(settings, pipeline)


def test_health_no_loading_and_models_safe():
    with TestClient(make_app()) as client:
        assert client.get("/api/v1/health").json() == {
            "status": "ok",
            "service": "BalNLP",
            "version": "0.1.0",
        }
        assert client.get("/api/v1/models").json()["morph"]["status"] == "configured"
        assert client.get("/docs").status_code == 200
        assert client.get("/redoc").status_code == 200
        assert client.get("/openapi.json").status_code == 200


@pytest.mark.parametrize("endpoint", ["analyze", "pos", "ner", "morph", "parse"])
def test_endpoints(endpoint):
    with TestClient(make_app()) as client:
        response = client.post(f"/api/v1/{endpoint}", json={"text": "بلوچی متن"})
        assert response.status_code == 200
        assert len(response.json()["tokens"]) == 2
        assert response.headers["x-request-id"]


@pytest.mark.parametrize(
    "body", [{}, {"text": None}, {"text": 12}, {"text": " "}, {"text": "بلوچی", "tasks": []}]
)
def test_validation(body):
    with TestClient(make_app()) as client:
        response = client.post("/api/v1/analyze", json=body)
        assert response.status_code == 422
        assert set(response.json()) == {"error"}


def test_limits_and_cors():
    with TestClient(
        make_app(max_text_length=5, rate_limit_per_minute=2, max_request_bytes=256)
    ) as client:
        assert (
            client.post("/api/v1/pos", json={"text": "abcdef"}).json()["error"]["code"]
            == "TEXT_TOO_LONG"
        )
        response = client.post(
            "/api/v1/pos", content="x" * 300, headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 413
        assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
        assert client.post("/api/v1/pos", json={"text": "word"}).status_code == 429
        assert (
            "access-control-allow-origin"
            not in client.get("/api/v1/health", headers={"Origin": "https://evil.example"}).headers
        )


def test_timeout_keeps_worker_busy():
    finished = threading.Event()

    class SlowPipeline:
        def analyze(self, text, tasks):
            finished.wait(2)
            return None

        def close(self):
            finished.set()

    service = BalNLPService(APISettings(request_timeout_seconds=0.01), SlowPipeline())

    async def run():
        with pytest.raises(BalNLPError, match="too long"):
            await service.analyze("word")
        with pytest.raises(BalNLPError, match="another sentence"):
            await service.analyze("word")
        finished.set()

    asyncio.run(run())
    service.close()
