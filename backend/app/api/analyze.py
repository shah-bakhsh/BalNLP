from typing import Annotated

from fastapi import APIRouter, Depends

from ..dependencies import get_service
from ..schemas.requests import AnalyzeRequest
from ..schemas.responses import AnalysisResult

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResult)
async def analyze(body: AnalyzeRequest, service: Annotated[object, Depends(get_service)]):
    return await service.analyze(body.text, body.tasks)
