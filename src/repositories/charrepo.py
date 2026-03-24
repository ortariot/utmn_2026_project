from typing import Optional, Any

from model.subjects import Char


class CharRepository:
    # TO DO TYPING
    def __init__(self, db):
        self.db = db


    async def create(self, char_data: dict) -> Char:
        
        char = Char(**char_data)
        self.db.add(char)
        await self.db.commit()
        await self.db.refresh(char)

        return char




    async def get_by_id(self, char_id: Any) -> Optional[Char]:

        pass



    async def updare(self, char_id: Any, update_data: dict):

        pass


    async def delete(self, char_id: Any):
        pass


    async def get_all(self):
        pass