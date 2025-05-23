import logging
import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")
    DEBUG: bool = True

    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DB_NAME: str = "name_db"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"

    __TEST_DB_NAME: str = "db_base_test"

    SECRET_KEY: str = "secret_key-123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    LOG_NAME: str = "log_nc"
    LOG_DIR: str = "./logs"

    NATIONALIZE_API_KEY: str | None = None
    NATIONALIZE: str = "https://api.nationalize.io"
    COUNTRIES: str = "https://restcountries.com/v3.1/alpha"

    def logger_init(self):
        os.makedirs(self.LOG_DIR, exist_ok=True)

        logging.basicConfig(
            format="[%(asctime)s] /%(filename)s:%(lineno)d/ %(levelname)s - %(message)s",
            filename=f"{self.LOG_DIR}/{self.LOG_NAME}.log",
            filemode="a",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        log = logging.getLogger(name=f"project_log")
        log.setLevel(logging.INFO)

        if self.DEBUG:
            log.setLevel(logging.DEBUG)

        return log

    def pg_dns(self, engine_="asyncpg") -> str:
        return (
            f"postgresql+{engine_}://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    def sqlite_dns(self) -> str:
        return f"sqlite+aiosqlite:///./{self.DB_NAME}.db"

    def pg_test_dns(self, engine_="asyncpg") -> str:
        return (
            f"postgresql+{engine_}://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.__TEST_DB_NAME}"
        )

    def dns(self, type_db="pg"):
        if type_db == "pg":
            return self.pg_dns()
        return self.sqlite_dns()


settings_app = Settings()
logger = settings_app.logger_init()

DATABASE_URL = settings_app.dns()
engine = create_async_engine(DATABASE_URL, echo=settings_app.DEBUG)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass
