from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    ieee_api_key: str = ""
    llm_provider: str = "kimi"
    openai_api_key: str = ""
    gemini_api_key: str = ""
    kimi_api_key: str = ""
    library_path: str = "/app/library"
    db_path: str = "/app/data/app.db"
    default_publication: str = "TIFS"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = DATA_DIR / "settings.json"


def load_runtime_settings() -> dict:
    if CONFIG_FILE.exists():
        return __import__("json").loads(CONFIG_FILE.read_text())
    return {}


def save_runtime_settings(payload: dict) -> None:
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(__import__("json").dumps(payload, indent=2))


def get_settings() -> AppSettings:
    base = AppSettings()
    runtime = load_runtime_settings()
    merged = {**base.model_dump(), **runtime}
    return AppSettings(**merged)
