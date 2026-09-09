from typing import Annotated

from fastapi import APIRouter, Depends

from ..dependencies import get_service
from ..schemas.requests import TextRequest
from ..schemas.responses import AnalysisResult

router = APIRouter()


@router.post("/pos", response_model=AnalysisResult)
async def pos(body: TextRequest, service: Annotated[object, Depends(get_service)]):
    return await service.analyze(body.text, ["pos"])
