import asyncio
from celery_app import celery_app


from database import async_sessiom_maker
from services.aiservice import AiService
from repositories.charrepo import CharRepository
from schemas.charschema import CharInDB


@celery_app.task(bind=True, name="crate_ai_char")
def create_ai_char_task(self, promt: str) -> dict:

    task_id = self.request.id

    async def _run():
        async with async_sessiom_maker() as session:
            repo = CharRepository(session)
            ai_service = AiService(repo)

            orm_result = await ai_service.ai_char_create(promt)

            result = CharInDB.model_validate(orm_result)

            return result.model_dump()
        
    
    try:
        res = asyncio.run(_run())
        return {"status": "SUCCESS", "result": res}
    except Exception as e:
        return {"status": "FALL", "result": str(e)}
        




        

        
    