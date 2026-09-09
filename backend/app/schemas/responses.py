from pydantic import BaseModel

from balnlp.schemas import AnalysisResult


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail


__all__ = ["AnalysisResult", "ErrorResponse"]
