import asyncio

from werkzeug.security import generate_password_hash

from models import Country, Name, NameCountryPrediction, User
from settings import Base, async_session, engine


async def create_bd():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data():
    async with async_session() as sess:
        u1 = User(
            email="admin@ex.com",
            password_hash=generate_password_hash("admin"),
        )
        sess.add(u1)
        await sess.commit()


async def main():
    await create_bd()
    print("database created")
    await insert_data()
    print("data added")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
