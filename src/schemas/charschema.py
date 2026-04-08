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


class CharCreate(CharBase):
    pass

# было:
# class CharUpdate(BaseModel):
#     name: Optional[str]
#     gender: Optional[Gender]
#     is_human: Optional[bool]
#     power: Optional[int]
#     race: Optional[str]
#     can_fly: Optional[bool]
#     specialization: Optional[str]


# стало:
class CharUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    is_human: Optional[bool] = None
    power: Optional[int] = None
    race: Optional[str] = None
    can_fly: Optional[bool] = None
    specialization: Optional[str] = None
# чтобы была возможность не передавать некоторые атрибуты,
# нужно задать им значения по умолчанию
# что я благополучно и забыл)))

class CharInDB(CharBase):
    id: UUID


    model_config = ConfigDict(from_attributes=True)


    