from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import generate_password_hash

from models.user import User
from schemas.user import InputUserData


async def get_user(session: AsyncSession, user_email: str | None):
    if user_email:
        return await session.scalar(select(User).where(User.email == user_email))


async def create_user(session: AsyncSession, data_user: InputUserData):
    user_dict = data_user.model_dump()
    user_dict["password_hash"] = generate_password_hash(user_dict["password"])
    del user_dict["password_repeat"]
    del user_dict["password"]

    new_user = User(**user_dict)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
