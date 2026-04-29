import pytest
import sys
import os
from uuid import UUID


from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from model.subjects import Char
from schemas.charschema import CharCreate




class TestChar:

    @pytest.mark.asyncio
    async def test_create_char_success(self, client: AsyncClient, db_session, sample_char_data: dict
    ):

        response = await client.post("/api/v1/char/", json=sample_char_data)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data

        result = await db_session.execute(
            select(Char).where(Char.id == UUID(data["id"]))
        )
        char = result.scalar_one_or_none()
        assert char is not None
        assert char.name == sample_char_data["name"]
        assert char.race == sample_char_data["race"]
        assert char.gender == sample_char_data["gender"]
        assert char.power == sample_char_data["power"]
        assert char.is_human == sample_char_data["is_human"]
        assert char.can_fly == sample_char_data["can_fly"]
        assert char.specialization == sample_char_data["specialization"]
        assert char.biography == sample_char_data["biography"]




    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "in_data, out_data",
        [
            (
                {
                    "name": "Гендальф",
                    "gender": "male",
                    "is_human": False,
                    "power": 100,
                    "race": "Майар",
                    "can_fly": False,
                    "specialization": "Магия",
                    "biography": "Серый маг",
                },
                {
                    "status": status.HTTP_201_CREATED
                }
            ),
            (
                {
                    "name": "Фродо",
                    "gender": "муж",
                    "is_human": False,
                    "power": 10,
                    "race": "Хоббит",
                    "can_fly": False,
                    "specialization": "Носильщик Кольца",
                    "biography": "Племянник Бильбо",
                },
                {
                    "status": status.HTTP_422_UNPROCESSABLE_CONTENT 
                }
                # gender не верный
            ),
            (
                {
                    "gender": "male",
                    "is_human": False,
                    "power": 10,
                    "race": "Хоббит",
                    "can_fly": False,
                    "specialization": "Носильщик Кольца",
                    "biography": "Племянник Бильбо",
                },
                {
                    "status": status.HTTP_422_UNPROCESSABLE_CONTENT
                }
            ),
        ],
    )
    async def test_create_chars_success(
        self,
        in_data, out_data, 
        client: AsyncClient, db_session
    ):
        """Успешное создание персонажа — проверяем и ответ, и запись в БД."""
        response = await client.post("/api/v1/char/", json=in_data)
        assert response.status_code == out_data["status"]
