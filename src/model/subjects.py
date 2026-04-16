from typing import Any
from enum import Enum

from sqlalchemy import ForeignKey, Column, String, Boolean, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID

from .base import Base, BaseModelMixin


class Account(Base, BaseModelMixin):
    
    __tablename__ = "account"

    username = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # status = Column(Boolean, nullable=False, default=True


    def __repr__(self) -> str:
        return f"id - {self.id} username - {self.username} - email - {self.email}"
    
    # TO DO
    def to_dict(self) -> dict[str, Any]:
        pass


class Gender(Enum):
    MALE = "male"
    FEMALE = "female" 


class Char(Base, BaseModelMixin):
    
    __tablename__ = "chars"

    name = Column(String, nullable=False)
    gender = Column(SQLEnum(Gender), nullable=False)
    is_human = Column(Boolean, default=True)
    power = Column(Integer)
    race = Column(String, nullable=False)
    can_fly = Column(Boolean, default=False)
    specialization = Column(String, nullable=True)
    biography = Column(String, nullable=True)


    account_id = Column(
        UUID(as_uuid=True),
        ForeignKey("account.id", ondelete="SET NULL"),
        nullable=True
    )


    def __repr__(self) -> str:
        return f"id: {self.id} name: {self.name} race: {self.race}"


    # TO DO
    def to_dict(self) -> dict[str, Any]:
        pass
