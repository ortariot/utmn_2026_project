from typing import Any
from sqlalchemy import Column, String


from .base import Base, BaseModelMixin


class Account(Base, BaseModelMixin):
    
    __tablename__ = "account"

    username = Column(String)
    email = Column(String, nullable=False, unique=True)


    def __repr__(self) -> str:
        return f"id - {self.id} username - {self.username} - email - {self.email}"
    
    # TO DO
    def to_dict(self) -> dict[str, Any]:
        pass



class Char(Base, BaseModelMixin):
    pass