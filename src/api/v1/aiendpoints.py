from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException, Query


from services.aiservice import AiService, get_ai_service

from schemas.charschema import (
    CharInDB,
    AiCharCreate,
)

router = APIRouter()


@router.post(
    "/",
    response_model=CharInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Create new char",
)
async def create_char(
    char_data: AiCharCreate, service: AiService = Depends(get_ai_service)
):
    res = await service.ai_char_create(char_data.promt)
    return res


@router.post(
    "/giga",
    response_model=CharInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Create new char",
)
async def create_char(
    char_data: AiCharCreate, service: AiService = Depends(get_ai_service)
):
    res = await service.gigaai_char_create(char_data.promt)
    return res
