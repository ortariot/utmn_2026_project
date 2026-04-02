import asyncio
from typing import Any

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


from repositories.charrepo import CharRepository
from configs.settings import settings
from model.subjects import Gender


async def create(item: dict):
    engine = create_async_engine(settings.db_dsl, echo=True)

    async_sessiom_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


    async with async_sessiom_maker() as db:
        repo = CharRepository(db)

        await repo.create(item)



async def getbyid(id: Any):
    engine = create_async_engine(settings.db_dsl, echo=True)

    async_sessiom_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


    async with async_sessiom_maker() as db:
        repo = CharRepository(db)

    
        result = await repo.get_by_id(id)

    
    return result


async def update(id: Any, data: dict):
    engine = create_async_engine(settings.db_dsl, echo=True)

    async_sessiom_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


    async with async_sessiom_maker() as db:
        repo = CharRepository(db)

        result = await repo.updare(id, data)

    
    return result



if __name__ == "__main__":

    char_1 = {
        "name": "Buration",
        "gender": Gender.MALE,
        "is_human": False,
        "power": 50,
        "race": "wooden doll",
        "can_fly": False,
        "specialization": "theater"
    }


    # asyncio.run(create(char_1))

    res = asyncio.run(getbyid("9ff0074f-af0f-4b15-b8ee-16191545f35a"))

    print(res)


    res = asyncio.run(update("9ff0074f-af0f-4b15-b8ee-16191545f35a", {"name": "Pinokio"}))



    res = asyncio.run(getbyid("9ff0074f-af0f-4b15-b8ee-16191545f35a"))

    print(res)





