import orjson
from openai import (
    AsyncOpenAI,
)  # обратите внимание что OpenAI теперь асинхронный

from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

from fastapi import Depends, HTTPException, status

from repositories.charrepo import CharRepository, get_char_repository
from configs.settings import settings
from schemas.charschema import CharCreate, CharInDB
from taskstore import task_store


class AiService:

    system_instr = (
        "Ты генератор JSON-данных. Создай персонажа по схеме:"
        "name: str,  gender: Gender ('male' или 'female'), is_human: bool, power: int, "
        "race: str, can_fly: bool, specialization: str, biography: str"
        "подробная биография 4 предложения на русском языке"
        "выводи только валидный json без лишнего текста что бы я мог "
        "его обработать с помощью python json.loads()"
    )

    def __init__(self, repo: CharRepository):
        self.repo = repo
        self.client = AsyncOpenAI(
            api_key=settings.ai_api_key, base_url="https://api.deepseek.com"
        )

        self.giga = GigaChat(
            credentials=settings.giga_api_key,
            scope="GIGACHAT_API_PERS",
            model="GigaChat",
            verify_ssl_certs=False,
        )

    async def ai_char_create(self, promt: str) -> CharInDB:

        try:

            print(
                "отправляю запрос"
            )  # по идее надо логер но его мы не проходили

            response = await self.client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[
                    {"role": "system", "content": self.system_instr},
                    {
                        "role": "user",
                        "content": f"Персонаж {promt}",
                    },
                ],
                response_format={"type": "json_object"},
            )

        except Exception as e:  # можно использовать базовый Exception

            print(f"Ошибка API {e}")
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        raw_content = response.choices[0].message.content

        try:
            data = orjson.loads(raw_content)
        except orjson.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")
        
        data = CharCreate(**data)

        char = await self.repo.create(data.model_dump())

        return char

    async def gigaai_char_create(self, promt: str) -> CharInDB:

        messages = [
            SystemMessage(content=self.system_instr),
            HumanMessage(content=promt),
        ]

        try:
            res = self.giga.invoke(messages)

        except Exception as e: 

            print(f"Ошибка API {e}")
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        parser = StrOutputParser()

        pars = parser.invoke(res)

        content = (
            pars.replace("json", "").replace("```", "").replace("```", "")
        )

        try:
            data = orjson.loads(str(content))
        except orjson.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")
    

        data = CharCreate(**data)

        char = await self.repo.create(data.model_dump())

        return char
    
    async def create_char_backround(self, task_id: str,  promt: str):
        try:
            res = await self.ai_char_create(promt)
            task_store[task_id] = {"status": "comleted", "result": res}
        except Exception as e:
            task_store[task_id] = {"status": "error", "error": e}





async def get_ai_service(
    repo: CharRepository = Depends(get_char_repository),
) -> AiService:
    return AiService(repo)
