import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import create_user
from schemas.user import InputUserData


@pytest.mark.asyncio
async def test_successful_registration(session, client: AsyncClient):
    payload = {
        "email": "testuser@example.com",
        "password": "strongpassword",
        "password_repeat": "strongpassword",
    }

    response = await client.post("/auth/registration", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_registration_user_exists(client: AsyncClient, session: AsyncSession):
    # Создаём пользователя заранее
    await create_user(
        session,
        InputUserData(email="existing@example.com", password="pass123", password_repeat="pass123"),
    )

    payload = {
        "email": "existing@example.com",
        "password": "pass123",
        "password_repeat": "pass123",
    }

    response = await client.post("/auth/registration", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "User is exists"
