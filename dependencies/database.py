from sqlalchemy.ext.asyncio import AsyncSession

from settings import async_session


async def get_session() -> AsyncSession:
    async with async_session() as sess:
        yield sess
