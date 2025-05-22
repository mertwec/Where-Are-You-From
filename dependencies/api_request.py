from typing import Optional

import httpx

from settings import settings_app as s


async def get_nationalize(name: str) -> Optional[dict]:
    params = {"name": name}
    if s.NATIONALIZE_API_KEY:
        params["apikey"] = s.NATIONALIZE_API_KEY

    async with httpx.AsyncClient() as aclient:
        response = await aclient.get(s.NATIONALIZE, params=params)
        if response.status_code == 200:
            return response.json()


async def get_country(code: str) -> Optional[dict]:
    async with httpx.AsyncClient() as aclient:
        response = await aclient.get(s.COUNTRIES + f"/{code}")
        if response.status_code == 200:
            return response.json()[0]
