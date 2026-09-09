from pydantic import BaseModel, ConfigDict, Field

from balnlp.schemas import Task


class TextRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    text: str


class AnalyzeRequest(TextRequest):
    tasks: list[Task] | None = Field(default=None, min_length=1, max_length=4)
