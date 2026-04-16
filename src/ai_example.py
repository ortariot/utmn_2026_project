import json
from openai import OpenAI
from langchain_gigachat import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from configs.settings import settings


client = OpenAI(api_key=settings.ai_api_key, base_url="https://api.deepseek.com")


sys_inst = (
    "Ты генератор JSON-данных. Создай персонажа по схеме:"
    "name: str,  gender: Gender, is_human: bool, power: int, race: str, can_fly: bool, specialization: str, biography: str"
    "подробная биография 4 предложения на русском языке"
    "выводи только валидный json без лишнего текста что бы я мог его обработать с помощью python json.loads()"
)

promt = "персонаж для ловли рыбы"

# responce = client.chat.completions.create(
#     model="deepseek-reasoner",
#     messages=[
#         {"role": "system", "content": sys_inst},
#         {"role": "user", "content": promt}
#     ],
#     response_format= {
#         "type": "json_object"
#     }
# )


# content = responce.choices[0].message.content

# print(content)

# char = json.loads(content)  #orjson

# print(char)


model = GigaChat(
    credentials=settings.giga_api_key,
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    verify_ssl_certs=False
)


mes = [
    SystemMessage(content=sys_inst),
    HumanMessage(content=promt)
]


res=model.invoke(mes)

pasrser = StrOutputParser()

content = pasrser.invoke(res)


print(content)


char = json.loads(content.replace("json", "").replace("```", "")) 


print(char)


