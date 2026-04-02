from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException, Query

from services.charservice import CharService, get_char_service
from schemas.charschema import CharCreate, CharUpdate, CharInDB

router = APIRouter()


@router.post(
    "/",
    response_model=CharInDB,
    status_code=status.HTTP_201_CREATED,
    summary="create new char",
)
async def create_char(
    char_data: CharCreate, service: CharService = Depends(get_char_service)
):
    res = await service.create_char(char_data)

    return res


@router.get(
    "/",
    response_model=list[CharInDB],
    status_code=status.HTTP_200_OK,
    summary="get all chars",
)
async def get_all_chars(
    skip: int = Query(0, ge=0, description="offset"),
    limit: int = Query(100, ge=1, le=1000, description="limit"),
    service: CharService = Depends(get_char_service),
):
    chars = await service.get_all_chars(skip, limit)

    if chars is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="chars table is empty",
        )

    return chars


@router.get(
    "/{char_id}",
    response_model=CharInDB,
    status_code=status.HTTP_200_OK,
    summary="get char by id",
)
async def get_char(
    char_id: UUID, service: CharService = Depends(get_char_service)
) -> CharInDB:
    char = await service.get_char_by_id(char_id)

    if char is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"char with {char_id} not found",
        )

    return char


@router.patch(
    "/{char_id}",
    response_model=CharInDB,
    status_code=status.HTTP_202_ACCEPTED,
    summary="update char",
)
async def update_char(
    char_id: UUID,
    char_data: CharUpdate,
    service: CharService = Depends(get_char_service),
):
    char = await service.get_char_by_id(char_id)

    if char is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"char with {char_id} not found",
        )

    print("!!!")
    res = await service.update_char(char_id, char_data)

    return res


@router.delete(
    "/{char_id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="delete char",
)
async def delete_char(
    char_id: UUID, service: CharService = Depends(get_char_service)
):
    await service.delete_char(char_id)
