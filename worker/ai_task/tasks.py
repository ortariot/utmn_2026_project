import asyncio
from celery_app import celery_app


from database import async_sessiom_maker
from services.aiservice import AiService
from repositories.charrepo import CharRepository
from schemas.charschema import CharInDB


# Работло и так как было но не стабильно иногда давало ошибки вроде "Future attached to a different loop"
# чтобы их избежть применен костыль
# собственно, как я и говорил celery c asincio работает не очень хорошо
_loop = None


def _get_loop():
    global _loop
    if _loop is None or _loop.is_closed():
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
    return _loop


@celery_app.task(bind=True, name="create_ai_char")
def create_ai_char_task(self, promt: str) -> dict:

    task_id = self.request.id

    async def _run():
        async with async_sessiom_maker() as session:
            repo = CharRepository(session)
            ai_service = AiService(repo)

            try:
                orm_result = await ai_service.ai_char_create(promt)
                result = CharInDB.model_validate(orm_result)
                return result.model_dump()
            finally:
                # Обязательно закрываем httpx.AsyncClient внутри AsyncOpenAI,
                # чтобы не копились подключения от предыдущих вызовов
                await ai_service.client.close()

    try:
        loop = _get_loop()
        res = loop.run_until_complete(_run())
        return {"status": "success", "result": res}
    except Exception as e:
        return {"status": "failed", "result": str(e)}
        




        

        
    