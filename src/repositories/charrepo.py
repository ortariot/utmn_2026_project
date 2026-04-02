from typing import Optional, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from model.subjects import Char
from database import get_session


class CharRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, char_data: dict) -> Char:

        char = Char(**char_data)
        self.db.add(char)
        await self.db.commit()
        await self.db.refresh(char)

        return char

    async def get_by_id(self, char_id: Any) -> Optional[Char]:

        result = await self.db.execute(
            select(Char).where(Char.id == char_id)
        )  # SELECT * FROM chars WHERE id = char_id
        return result.scalar_one_or_none()

    async def updare(self, char_id: Any, update_data: dict):

        char = await self.get_by_id(char_id)

        if not char:
            return None

        for key, value in update_data.items():
            setattr(char, key, value)

        await self.db.commit()
        await self.db.refresh(char)

        return char

    async def delete(self, char_id: Any) -> bool:

        char = await self.get_by_id(char_id)

        if char:
            await self.db.delete(char)
            await self.db.commit()
            return True

        return False

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Char]:
        result = await self.db.execute(
            select(Char).offset(skip).limit(limit)
        )  # SELECT * FROM char LIMIT skip limit

        return result.scalars().all()


async def get_char_repository(
    db: AsyncSession = Depends(get_session),
) -> CharRepository:
    return CharRepository(db)
