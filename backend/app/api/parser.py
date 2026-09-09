from typing import Annotated

from fastapi import APIRouter, Depends

from ..dependencies import get_service
from ..schemas.requests import TextRequest
from ..schemas.responses import AnalysisResult

router = APIRouter()


@router.post("/parse", response_model=AnalysisResult)
async def parse(body: TextRequest, service: Annotated[object, Depends(get_service)]):
    return await service.analyze(body.text, ["parser"])
