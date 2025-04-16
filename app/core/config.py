from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DATABASE_WALLET_URL: PostgresDsn
    DATABASE_PAYMENT_URL: PostgresDsn

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )



settings = Settings()


