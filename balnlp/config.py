from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

OFFICIAL_MODELS = {
    "pos": ("shah-bakhsh/BalPOS", "572de08cc59918199ca0eafd47ca6202181f6a2a"),
    "ner": ("shah-bakhsh/BalNER-v2", "d7a879d3e24f53f1d75eced26ab0167c803c9f67"),
    "morph": ("shah-bakhsh/BalMorph", "06815c4e79a755a73890d2857b3d3f5b03d8e118"),
    "parser": ("shah-bakhsh/BalParser", "8937729c3f86c9327a457d9ed8f49238ef7f4b51"),
}


class Settings(BaseSettings):
    enable_pos: bool = True
    enable_ner: bool = True
    enable_morph: bool = True
    enable_parser: bool = True
    balnlp_memory_limit_mb: int | None = Field(default=None, ge=128)
    balnlp_min_model_memory_mb: int = Field(default=2048, ge=1024)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    balpos_model: str = OFFICIAL_MODELS["pos"][0]
    balner_model: str = OFFICIAL_MODELS["ner"][0]
    balmorph_model: str = OFFICIAL_MODELS["morph"][0]
    balparser_model: str = OFFICIAL_MODELS["parser"][0]
    balpos_revision: str | None = None
    balner_revision: str | None = None
    balmorph_revision: str | None = None
    balparser_revision: str | None = None
    hf_token: SecretStr | None = None
    balnlp_memory_mode: Literal["low", "balanced", "performance"] = "low"
    balnlp_device: Literal["cpu", "cuda", "auto"] = "cpu"
    balnlp_cpu_threads: int = Field(default=1, ge=1, le=16)
    max_text_length: int = Field(default=2000, ge=1, le=10000)
    max_tokens: int = Field(default=256, ge=1, le=512)
    max_subwords: int = Field(default=512, ge=8, le=512)
    max_parser_words: int = Field(default=80, ge=1, le=128)
    model_load_attempts: int = Field(default=2, ge=1, le=3)
    balmorph_adapter: str = "balnlp.morph_adapter:NotebookBalMorph"

    @field_validator("hf_token", mode="before")
    @classmethod
    def empty_token_is_anonymous(cls, value):
        return None if isinstance(value, str) and not value.strip() else value

    def model_id(self, task: str) -> str:
        return getattr(self, f"bal{task}_model")

    def revision(self, task: str) -> str | None:
        explicit = getattr(self, f"bal{task}_revision")
        if explicit:
            return explicit
        return OFFICIAL_MODELS[task][1] if self.model_id(task) == OFFICIAL_MODELS[task][0] else None
