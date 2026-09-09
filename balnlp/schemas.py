from typing import Literal

from pydantic import BaseModel, Field

Task = Literal["pos", "ner", "morph", "parser"]
TASKS: tuple[Task, ...] = ("pos", "ner", "morph", "parser")


class Token(BaseModel):
    id: int
    form: str
    start: int
    end: int
    sentence_id: int = 1
    lemma: str | None = None
    upos: str | None = None
    ner: str | None = None
    feats: dict[str, str] | None = None
    head: int | None = None
    deprel: str | None = None


class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int
    token_ids: list[int]


class TaskFailure(BaseModel):
    task: Task
    code: str
    message: str


class Meta(BaseModel):
    version: str = "0.1.0"
    completed_tasks: list[Task] = Field(default_factory=list)
    failed_tasks: list[TaskFailure] = Field(default_factory=list)
    timings_ms: dict[str, dict[str, float]] = Field(default_factory=dict)
    total_ms: float = 0
    warnings: list[str] = Field(default_factory=list)
    offset_unit: str = "unicode_code_points"
    offset_reference: str = "text (NFC normalized)"


class AnalysisResult(BaseModel):
    text: str
    language: str = "bal"
    tokens: list[Token]
    entities: list[Entity] = Field(default_factory=list)
    dependency_tree: dict = Field(default_factory=dict)
    meta: Meta = Field(default_factory=Meta)
    conllu: str = ""
