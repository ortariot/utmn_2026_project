from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict

from model.subjects import Gender


class CharBase(BaseModel):

    name: str
    gender: Gender
    is_human: bool 
    power: int
    race: str
    can_fly: bool
    specialization: str
    biography: str


class CharCreate(CharBase):
    pass


class CharUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    is_human: Optional[bool] = None
    power: Optional[int] = None
    race: Optional[str] = None
    can_fly: Optional[bool] = None
    specialization: Optional[str] = None
    biography: Optional[str] = None

class CharInDB(CharBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True) 


class AiCharCreate(BaseModel):
    promt: Optional[str] = None
