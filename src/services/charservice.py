from typing import Any, Optional

from fastapi import Depends

from repositories.charrepo import CharRepository, get_char_repository
from schemas.charschema import CharBase, CharCreate, CharInDB, CharUpdate


class CharService:

    def __init__(self, repo: CharRepository):
        self.repo = repo

    async def get_char_by_id(self, char_id: Any) -> CharInDB:
        char = await self.repo.get_by_id(char_id)

        return char

    async def create_char(self, char_data: CharCreate) -> CharInDB:

        char_dict = char_data.model_dump()
        char = await self.repo.create(char_dict)

        return char

    async def update_char(
        self, char_id: Any, update_data: CharUpdate
    ) -> Optional[CharInDB]:

        update_dict = {
            key: value
            for key, value in update_data.model_dump().items()
            if value is not None
        }

        if not update_dict:
            return None

        char = await self.repo.updare(char_id, update_dict)

        return char

    async def delete_char(self, char_id: Any) -> bool:

        return await self.repo.delete(char_id)

    async def get_all_chars(self, skip: int, limit: int) -> list[CharInDB]:

        return await self.repo.get_all(skip, limit)

    async def get_char_service(
        repo: CharRepository = Depends(get_char_repository),
    ) -> CharService:
        return CharService(repo)
