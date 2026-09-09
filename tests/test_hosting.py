import asyncio
import threading

import pytest
from fastapi.testclient import TestClient
from test_api import make_app

from backend.app.config import APISettings
from backend.app.services.balnlp_service import BalNLPService
from balnlp.exceptions import BalNLPError


def test_warmup_occupies_worker_and_skips_unavailable_morphology():
    entered, release = threading.Event(), threading.Event()
    loaded = []

    class Pipeline:
        @property
        def manager(self):
            return self

        def load_model(self, task):
            loaded.append(task)
            entered.set()
            release.wait(2)

        def close(self):
            pass

    service = BalNLPService(
        APISettings(balnlp_warmup=True, balnlp_memory_mode="performance", enable_morph=False),
        Pipeline(),
    )
    try:
        service.start_warmup()
        assert entered.wait(2)
        assert service.warming
        with pytest.raises(BalNLPError, match="another sentence"):
            asyncio.run(service.analyze("text"))
    finally:
        release.set()
        service.close()
    assert loaded == ["pos", "ner", "parser"]
    assert not service.warming


def test_capabilities_reports_missing_morphology_without_loading():
    with TestClient(make_app(balmorph_adapter="")) as client:
        data = client.get("/api/v1/capabilities").json()
        assert data["tasks"]["morph"] == {
            "enabled": False,
            "status": "blocked",
            "loaded": False,
        }
        assert data["tasks"]["pos"]["enabled"] is True
        assert data["warming"] is False


def test_static_website_and_api_share_origin(tmp_path):
    (tmp_path / "index.html").write_text("<h1>BalNLP</h1>")
    page = tmp_path / "analyze"
    page.mkdir()
    (page / "index.html").write_text("<h1>Analyze</h1>")
    assets = tmp_path / "_next" / "static"
    assets.mkdir(parents=True)
    (assets / "test.js").write_text("console.log('test')")
    with TestClient(make_app(balnlp_static_dir=str(tmp_path))) as client:
        assert "BalNLP" in client.get("/").text
        assert "Analyze" in client.get("/analyze/").text
        assert client.get("/api/v1/health").status_code == 200
        assert client.get("/api/docs").status_code == 200
        assert client.get("/missing").status_code == 404
        assert client.get("/api/v1/health").headers["cache-control"] == "no-store"
        assert "immutable" in client.get("/_next/static/test.js").headers["cache-control"]
