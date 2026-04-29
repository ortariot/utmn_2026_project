import pytest
import pytest_asyncio

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text


from main import app
from model.base import Base



TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:55433/chars"


@pytest_asyncio.fixture
async def test_engine():

    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:

    session_factory = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session



@pytest_asyncio.fixture
async def client(test_engine) -> AsyncGenerator[AsyncClient, None]:
  
    from database import get_session

    async def override_get_session():
        session_factory = async_sessionmaker(
            test_engine, class_=AsyncSession, expire_on_commit=False
        )
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()




@pytest.fixture
def sample_char_data() -> dict:
    """Данные для второго тестового персонажа."""
    return {
        "name": "Фродо",
        "gender": "male",
        "is_human": False,
        "power": 10,
        "race": "Хоббит",
        "can_fly": False,
        "specialization": "Носильщик Кольца",
        "biography": "Племянник Бильбо",
    }