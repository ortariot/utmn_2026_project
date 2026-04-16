from typing import Any, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from model.subjects import Account
from database import get_session


class AccRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_date: dict) -> Account:
        user = Account(**user_date)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, id: Any) -> Optional[Account]:
        result = await self.db.execute(select(Account).where(Account.id == id))

        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Account]:
        result = await self.db.execute(
            select(Account).where(Account.username == name)
        )

        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[Account]:
        result = await self.db.execute(
            select(Account).where(Account.email == email)
        )

        return result.scalar_one_or_none()

async def get_acc_reposetory(
    db: AsyncSession = Depends(get_session),
) -> AccRepository:
    return AccRepository(db)
