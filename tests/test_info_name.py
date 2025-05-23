import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
import json

@pytest.mark.asyncio
@patch("dependencies.api_request.get_nationalize", new_callable=AsyncMock)
@patch("dependencies.api_request.get_country", new_callable=AsyncMock)
async def test_get_name_info_success(mock_get_country, mock_get_nationalize, client):
    # Настраиваем моки
    mock_get_nationalize.return_value = {
        "name": "johnson",
        "country": [
            {"country_id": "US", "probability": 0.7},
            {"country_id": "GB", "probability": 0.2}
        ]
    }

    mock_get_country.side_effect = lambda code: {
        "US": json.loads(r'{"name":{"common":"United States"}}'),
        "GB": json.loads(r'{"name":{"common":"United Kingdom"}}')
    }[code]

    # Делаем запрос
    response = await client.get("/api/names/?name=johnson")
    assert response.status_code == 200
    data = response.json()

    # Проверяем результат
    assert data["name"] == "johnson"
    assert len(data["results"]) == 2

    assert data["results"][0]["country_code"] == "US"
    assert data["results"][0]["country"] == "United States"
    assert data["results"][0]["probability"] == 0.7


@pytest.mark.asyncio
async def test_missing_query_param(client):
    response = await client.get("/api/names/")
    assert response.status_code == 422


@patch("dependencies.api_request.get_nationalize", new_callable=AsyncMock)
async def test_empty_nationalize_data(mock_get_nationalize, client):
    mock_get_nationalize.return_value = {"country": []}
    response = await client.get("/api/names/?name=UnknownName")
    assert response.status_code == 404
    assert response.json()["detail"] == "No country prediction found for this name"


@patch("dependencies.api_request.get_nationalize", new_callable=AsyncMock)
async def test_nationalize_failure(mock_get_nationalize, client):
    mock_get_nationalize.return_value = None
    response = await client.get("/api/names/?name=FailName")
    assert response.status_code == 502
    assert response.json()["detail"] == "Failed to fetch from Nationalize.io"
