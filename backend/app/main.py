import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles

from .api import analyze, health, morph, ner, parser, pos
from .config import APISettings
from .exceptions import register_handlers
from .middleware import SafetyMiddleware
from .schemas.responses import ErrorResponse
from .services.balnlp_service import BalNLPService


def create_app(settings=None, pipeline=None):
    settings = settings or APISettings()

    @asynccontextmanager
    async def lifespan(app):
        app.state.service = BalNLPService(settings, pipeline)
        app.state.service.start_warmup()
        yield
        await asyncio.to_thread(app.state.service.close)

    app = FastAPI(
        title="BalNLP API",
        version="0.1.0",
        docs_url="/api/docs" if settings.balnlp_static_dir else "/docs",
        redoc_url="/api/redoc" if settings.balnlp_static_dir else "/redoc",
        lifespan=lifespan,
        description="Balochi language analysis. Text is not persistently stored.",
    )
    app.add_api_route("/health", health.health, methods=["GET"])
    app.add_api_route("/ready", health.ready, methods=["GET"])
    app.state.settings = settings
    register_handlers(app)
    for router in [
        health.router,
        analyze.router,
        pos.router,
        ner.router,
        morph.router,
        parser.router,
    ]:
        app.include_router(
            router,
            prefix="/api/v1",
            responses={
                status: {"model": ErrorResponse} for status in [413, 422, 429, 500, 503, 504]
            },
        )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(SafetyMiddleware, settings=settings)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
        expose_headers=["X-Request-ID"],
    )
    if settings.balnlp_static_dir:
        app.mount("/", StaticFiles(directory=settings.balnlp_static_dir, html=True), name="website")
    return app


logging.basicConfig(level=logging.INFO, format="%(message)s")
app = create_app()
