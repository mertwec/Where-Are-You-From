from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash

from crud.user import create_user, get_user
from dependencies.auth import create_access_token, get_current_user
from dependencies.database import get_session
from schemas.user import InputUserData, Token, UserData

route = APIRouter()


@route.post("/registration")
async def registration(
    data_user: InputUserData, session: AsyncSession = Depends(get_session)
) -> UserData:
    user = await get_user(session, str(data_user.email))
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is exists"
        )
    new_user = await create_user(session, data_user)
    return UserData.model_validate(new_user)


@route.post("/token")
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):

    user = await get_user(session, user_email=form_data.username)
    password_hash = str(user.password_hash)
    if not user or not check_password_hash(password_hash, form_data.password):
        raise HTTPException(status_code=400, detail="Username or Password incorrect")
    return Token(
        access_token=create_access_token(data={"sub": user.email}), token_type="bearer"
    )


@route.get("/user_data/")
async def get_current_user(cu=Depends(get_current_user)) -> UserData:
    return UserData.model_validate(cu)
