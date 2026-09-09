import asyncio
import json
import logging
from collections import OrderedDict, deque
from time import monotonic
from uuid import uuid4

from .exceptions import error_response

logger = logging.getLogger("balnlp.requests")


class SafetyMiddleware:
    """Bound bodies before parsing, rate-limit clients, and log no submitted content."""

    def __init__(self, app, settings):
        self.app, self.settings = app, settings
        self.clients = OrderedDict()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        start, request_id, status = monotonic(), uuid4().hex, 500

        async def safe_send(message):
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
                message["headers"] += [
                    (b"x-request-id", request_id.encode()),
                    (b"x-content-type-options", b"nosniff"),
                    (b"referrer-policy", b"no-referrer"),
                    (
                        b"cache-control",
                        b"public, max-age=31536000, immutable"
                        if scope["path"].startswith("/_next/static/")
                        else b"no-store",
                    ),
                ]
            await send(message)

        async def reject(code, message, status):
            await error_response(code, message, status)(scope, receive, safe_send)

        try:
            if scope["method"] == "POST":
                now = monotonic()
                # Use ASGI client only. Trust proxy headers only through a configured server.
                client = (scope.get("client") or ("unknown",))[0]
                if self.settings.rate_limit_enabled:
                    while self.clients and next(iter(self.clients.values()))[-1] <= now - 60:
                        self.clients.popitem(last=False)
                    queue = self.clients.get(client)
                    if queue is None:
                        if len(self.clients) >= self.settings.rate_limit_max_clients:
                            return await reject(
                                "RATE_LIMITED",
                                "The service is busy. Please try again in a minute.",
                                429,
                            )
                        queue = self.clients[client] = deque()
                    while queue and queue[0] <= now - 60:
                        queue.popleft()
                    if len(queue) >= self.settings.rate_limit_per_minute:
                        return await reject(
                            "RATE_LIMITED", "Too many requests. Please wait a minute.", 429
                        )
                    queue.append(now)
                    self.clients.move_to_end(client)
                body = bytearray()
                deadline = monotonic() + self.settings.body_timeout_seconds
                while True:
                    try:
                        part = await asyncio.wait_for(receive(), max(0.001, deadline - monotonic()))
                    except TimeoutError:
                        return await reject(
                            "REQUEST_TIMEOUT",
                            "The request arrived too slowly. Please try again.",
                            408,
                        )
                    if part["type"] == "http.disconnect":
                        return
                    body.extend(part.get("body", b""))
                    if len(body) > self.settings.max_request_bytes:
                        return await reject(
                            "REQUEST_TOO_LARGE",
                            "The request is too large. Please shorten the text.",
                            413,
                        )
                    if not part.get("more_body", False):
                        break
                delivered = False

                async def replay():
                    nonlocal delivered
                    if not delivered:
                        delivered = True
                        return {"type": "http.request", "body": bytes(body), "more_body": False}
                    return await receive()

                await self.app(scope, replay, safe_send)
            else:
                await self.app(scope, receive, safe_send)
        finally:
            # Only fixed known paths are logged; never query strings, arbitrary URLs or text.
            path = scope["path"]
            endpoint = (
                path
                if path
                in {
                    f"/api/v1/{x}"
                    for x in ["health", "models", "analyze", "pos", "ner", "morph", "parse"]
                }
                else "other"
            )
            logger.info(
                json.dumps(
                    {
                        "request_id": request_id,
                        "endpoint": endpoint,
                        "duration_ms": round((monotonic() - start) * 1000, 2),
                        "status": status,
                        "success": status < 400,
                    }
                )
            )
