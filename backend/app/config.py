from pydantic import Field, field_validator

from balnlp.config import Settings


class APISettings(Settings):
    balnlp_static_dir: str = ""
    balnlp_warmup: bool = False
    frontend_url: str = "http://localhost:3000"
    request_timeout_seconds: float = Field(default=180, ge=0.01, le=600)
    max_request_bytes: int = Field(default=32768, ge=256, le=131072)
    body_timeout_seconds: float = Field(default=15, ge=1, le=60)
    rate_limit_per_minute: int = Field(default=10, ge=1, le=1000)
    rate_limit_enabled: bool = True
    rate_limit_max_clients: int = Field(default=4096, ge=1, le=100000)

    @field_validator("frontend_url")
    @classmethod
    def validate_origin(cls, value):
        from urllib.parse import urlparse

        parsed = urlparse(value)
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.netloc
            or parsed.path not in {"", "/"}
            or parsed.query
            or parsed.fragment
            or parsed.username
            or parsed.password
        ):
            raise ValueError("FRONTEND_URL must be an explicit HTTP(S) origin")
        return value.rstrip("/")
