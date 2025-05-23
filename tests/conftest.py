import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from werkzeug.security import generate_password_hash

from dependencies.database import get_session
from main import app
from models import User
from settings import Base, settings_app

TEST_DB_URL = settings_app.pg_test_dns()

engine_test = create_async_engine(TEST_DB_URL, echo=False)
test_async_session_local = async_sessionmaker(bind=engine_test, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine_test.dispose()


@pytest_asyncio.fixture()
async def session(prepare_database):
    async with test_async_session_local() as session:
        u1 = User(
            email="admin@ex.com",
            password_hash=generate_password_hash("admin"),
        )
        session.add(u1)
        await session.commit()

        yield session


@pytest_asyncio.fixture()
async def client(session):
    async def override_get_db():
        yield session

    app.dependency_overrides[get_session] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
