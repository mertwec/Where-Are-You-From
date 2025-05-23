import types
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient


# --- helpers ---------------------------------------------------------------
def _fake_country(code: str, name: str = "United States"):
    """Простейший объект, имитирующий запись Country из БД."""
    o = types.SimpleNamespace()
    o.code = code
    o.name = name
    return o


# ---------------------------------------------------------------------------
@pytest.mark.asyncio
@patch("crud.get_country", new_callable=AsyncMock)          # путь корректируй под себя
@patch("crud.get_top_names_by_country", new_callable=AsyncMock)
async def test_popular_names_success(mock_get_top, mock_get_country, client: AsyncClient):
    """Успешный сценарий: страна найдена, топ-имена получены."""
    mock_get_country.return_value = _fake_country("US", "United States")
    mock_get_top.return_value = [("Garcia", 0.12), ("johnson", 0.10), ("smith", 0.08)]

    resp = await client.get("/api/popular-names/?country=US")
    assert resp.status_code == 200

    data = resp.json()
    assert data["country"] == "United States"
    assert data["top_names"][0] == {"name": "Garcia", "probability": 0.12}
    assert len(data["top_names"]) == 3


@pytest.mark.asyncio
async def test_popular_names_missing_param(client: AsyncClient):
    """Параметр country не передан → 400."""
    resp = await client.get("/api/popular-names/")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Query parameter 'country' is required"


@pytest.mark.asyncio
@patch("crud.get_country", new_callable=AsyncMock)
async def test_popular_names_country_not_found(mock_get_country, client: AsyncClient):
    """Страна отсутствует в БД → 404."""
    mock_get_country.return_value = None

    resp = await client.get("/api/popular-names/?country=XX")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Country not found"


@pytest.mark.asyncio
@patch("crud.get_country", new_callable=AsyncMock)
@patch("crud.get_top_names_by_country", new_callable=AsyncMock)
async def test_popular_names_no_names(mock_get_top, mock_get_country, client: AsyncClient):
    """Для страны нет статистики имён → 404."""
    mock_get_country.return_value = _fake_country("US", "United States")
    mock_get_top.return_value = []          # пустой список → 404

    resp = await client.get("/api/popular-names/?country=US")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "No name data found for this country"
