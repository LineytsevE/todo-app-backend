import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv("app/.env")


@dataclass
class Settings:
    DATABASE_URL: str
    CORS_ORIGINS: list[str]


def get_settings() -> Settings:
    cors_raw = os.getenv("CORS_ORIGINS", "")
    return Settings(
        DATABASE_URL=os.getenv("DATABASE_URL", ""),
        CORS_ORIGINS=[
            origin.strip() for origin in cors_raw.split(",") if origin.strip()
        ],
    )
