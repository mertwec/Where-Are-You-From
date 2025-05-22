from fastapi import APIRouter
from fastapi.responses import RedirectResponse

route = APIRouter()


@route.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")
