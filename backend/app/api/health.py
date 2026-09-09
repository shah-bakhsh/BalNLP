from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from balnlp.memory import memory_diagnostics
from balnlp.schemas import TASKS

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "BalNLP", "version": "0.1.0"}


@router.get("/models")
def models(request: Request):
    settings = request.app.state.settings
    loaded = request.app.state.service.pipeline.manager.loaded_tasks
    memory = memory_diagnostics(settings)
    limited = (
        memory["limit_mb"] is not None and memory["limit_mb"] < settings.balnlp_min_model_memory_mb
    )
    result = {}
    for task in TASKS:
        blocked = task == "morph" and not settings.balmorph_adapter
        enabled = getattr(settings, f"enable_{task}") and bool(settings.model_id(task))
        status = (
            "blocked"
            if blocked
            else "disabled"
            if not enabled
            else "loaded"
            if task in loaded
            else "resource_limited"
            if limited
            else "configured"
        )
        result[task] = {
            "name": {"pos": "BalPOS", "ner": "BalNER", "morph": "BalMorph", "parser": "BalParser"}[
                task
            ],
            "status": status,
            "reason": "Verified original inference implementation is unavailable."
            if blocked
            else "Host memory is below the checkpoint loading budget."
            if status == "resource_limited"
            else None,
            "checkpoint_available": bool(settings.model_id(task)),
            "inference_code_verified": not blocked,
            "loaded": task in loaded,
        }
    return result


@router.get("/capabilities")
def capabilities(request: Request):
    settings = request.app.state.settings
    return {
        "max_text_length": settings.max_text_length,
        "max_tokens": settings.max_tokens,
        "warming": request.app.state.service.warming,
        "tasks": {
            task: {
                "enabled": data["status"] in ("configured", "loaded"),
                "status": data["status"],
                "loaded": data["loaded"],
            }
            for task, data in models(request).items()
        },
    }


@router.get("/ready")
def ready(request: Request):
    registry = models(request)
    runnable = any(data["status"] in ("configured", "loaded") for data in registry.values())
    warming = request.app.state.service.warming
    return JSONResponse(
        status_code=200 if runnable and not warming else 503,
        content={
            "status": "ready_for_lazy_loading" if runnable and not warming else "not_ready",
            "inference_verified_on_host": False,
            "warming": warming,
            "models": registry,
            "memory": memory_diagnostics(request.app.state.settings),
        },
    )


@router.get("/diagnostics")
def diagnostics(request: Request):
    return memory_diagnostics(request.app.state.settings)
