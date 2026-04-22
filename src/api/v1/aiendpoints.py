from uuid import UUID, uuid4
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    Query,
    BackgroundTasks,
)


from services.aiservice import AiService, get_ai_service

from schemas.charschema import (
    CharInDB,
    AiCharCreate,
)
from schemas.taskssheme import TaskAccepted
from taskstore import task_store

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


# -------------------------------------


@router.post(
    "/background_create_char",
    response_model=TaskAccepted,
    status_code=status.HTTP_201_CREATED,
    summary="Create new char  background",
)
async def create_char_background(
    char_data: AiCharCreate,
    background_task: BackgroundTasks,
    service: AiService = Depends(get_ai_service),
):
    task_id = str(uuid4())
    task_store[task_id] = {"status": "pending"}

    background_task.add_task(
        service.create_char_backround,
        task_id=task_id,
        promt=char_data.promt
    )

    return TaskAccepted(task_id=task_id)



@router.get(
    "/background_create_char/{task_id}",
    response_model=CharInDB
    )
async def task_by_id(task_id: str):

    task = task_store.get(task_id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if task["status"] == "pending":
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="task in processing")
    if task["status"] == "error":
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return task["result"]