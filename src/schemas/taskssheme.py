from typing import Optional, Any

from pydantic import BaseModel



class TaskAccepted(BaseModel):
    task_id: str
    status: str = "pending"
    mesage: str = "task started"


class TaskResult(BaseModel):
    status: str
    data: Optional[Any]