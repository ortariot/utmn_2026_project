from uuid import UUID, uuid4
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    Query,
    BackgroundTasks,
)

from celery.result import AsyncResult
from celery import Celery


from services.aiservice import AiService, get_ai_service

from schemas.charschema import (
    CharInDB,
    AiCharCreate,
)
from schemas.taskssheme import TaskAccepted, TaskResult
from taskstore import task_store

REDIS_URL = "redis://localhost:6379/0"

router = APIRouter()
client = Celery("task", broker=REDIS_URL, backend=REDIS_URL)


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
        service.create_char_backround, task_id=task_id, promt=char_data.promt
    )

    return TaskAccepted(task_id=task_id)


@router.get("/background_create_char/{task_id}", response_model=CharInDB)
async def task_by_id(task_id: str):

    task = task_store.get(task_id)

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if task["status"] == "pending":
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, detail="task in processing"
        )
    if task["status"] == "error":
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return task["result"]


# ----------------------- CELERY---------------------


@router.post(
    "/celery_create_char",
    response_model=TaskAccepted,
    status_code=status.HTTP_201_CREATED,
    summary="Create new char in selery",
)
async def create_char_selery(
    char_data: AiCharCreate,
    service: AiService = Depends(get_ai_service),
):

    task = client.send_task("create_ai_char", args=[char_data.promt])

    return TaskAccepted(task_id=task.id, status="pending")


@router.get("/celery_char/{task_id}", response_model=TaskResult)
async def celery_task_by_id(task_id: str):

    task_result = AsyncResult(task_id, app=client)

    if task_result.status.lower() == "pending":
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, detail="task in processing"
        )

    elif task_result.status.lower() == "failed":
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif task_result.status.lower() == "success":

        result = task_result.result.get("result")
        return TaskResult(status="success", data=result)

    return TaskResult(status="success", data="no data")

    #  проблемы была в том что я не учёл что celery передаёт статусы в верхнем регистре испрвлено методом lower()
