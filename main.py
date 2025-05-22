import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import settings
from routes import auth_route, debug_route, nationalize_route
from settings import logger

app = FastAPI(description="Where Are You From", version="0.1", docs_url="/docs")

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_route, prefix="/auth", tags=["auth"])
app.include_router(nationalize_route, prefix="/api", tags=["nationalize"])

if settings.settings_app.DEBUG:
    app.include_router(debug_route, tags=["debug"])

if __name__ == "__main__":
    logger.info("run server")
    uvicorn.run(f"{__name__}:app", reload=True)
