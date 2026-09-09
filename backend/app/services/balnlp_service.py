import asyncio
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

from balnlp import BalNLP
from balnlp.exceptions import BalNLPError


class BalNLPService:
    """One running job, no unbounded queue. Timeout retains occupancy until exit."""

    def __init__(self, settings, pipeline=None):
        self.settings = settings
        self.pipeline = pipeline or BalNLP(settings)
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="balnlp")
        self.gate = threading.Lock()
        self.warming = False

    def start_warmup(self):
        if not self.settings.balnlp_warmup or not self.gate.acquire(blocking=False):
            return
        self.warming = True

        def warm():
            try:
                for task in ("pos", "ner", "morph", "parser"):
                    if not getattr(self.settings, f"enable_{task}"):
                        continue
                    if not self.settings.model_id(task) or (
                        task == "morph" and not self.settings.balmorph_adapter
                    ):
                        continue
                    try:
                        self.pipeline.manager.load_model(task)
                    except Exception:
                        logging.getLogger("balnlp.models").warning("warmup_failed task=%s", task)
            finally:
                if self.settings.balnlp_memory_mode == "low":
                    self.pipeline.manager.unload_all()
                self.warming = False

        try:
            future = self.executor.submit(warm)
        except Exception:
            self.warming = False
            self.gate.release()
            raise
        future.add_done_callback(lambda _: self.gate.release())

    async def analyze(self, text, tasks=None):
        if not self.gate.acquire(blocking=False):
            raise BalNLPError(
                "SERVICE_BUSY",
                "The service is analyzing another sentence. Please try again shortly.",
                503,
            )
        try:
            future = self.executor.submit(self.pipeline.analyze, text, tasks)
        except Exception:
            self.gate.release()
            raise
        future.add_done_callback(lambda _: self.gate.release())
        wrapped = asyncio.wrap_future(future)
        # Consume errors even when the HTTP caller has timed out or disconnected.
        wrapped.add_done_callback(lambda done: done.exception() if not done.cancelled() else None)
        try:
            return await asyncio.wait_for(
                asyncio.shield(wrapped), self.settings.request_timeout_seconds
            )
        except TimeoutError:
            raise BalNLPError(
                "INFERENCE_TIMEOUT",
                "Analysis took too long. The service may still be starting; please retry shortly.",
                504,
            ) from None

    def close(self):
        self.executor.shutdown(wait=True, cancel_futures=True)
        self.pipeline.close()
