import asyncio
from tortoise import Tortoise
from app.shared.config import settings


TORTOISE_ORM = {
    "connections": {
        "default": settings.db_url,
    },
    "apps": {
        "models": {
            "models": [
                "app.domain.models",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}


async def init_tortoise():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


# ================================================================================

# from pydantic_settings import BaseSettings, SettingsConfigDict
#
#
# class PostgresSettings(BaseSettings):
#     POSTGRES_HOST: str
#     POSTGRES_PORT: int
#     POSTGRES_USER: str
#     POSTGRES_PASSWORD: str
#     POSTGRES_DB: str
#
#     @property
#     def async_url(self) -> str:
#         return (
#             f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
#             f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
#         )
#
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_ignore_empty=True,
#         extra="ignore",
#     )
#
#
# settings = PostgresSettings()
