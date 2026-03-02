from __future__ import annotations

from typing import Literal
from pydantic import BaseModel


class SettingsPayload(BaseModel):
    ieee_api_key: str = ""
    llm_provider: Literal["openai", "gemini"] = "openai"
    openai_api_key: str = ""
    gemini_api_key: str = ""
    library_path: str = "./library"
    default_publication: str = "TIFS"


class SearchRequest(BaseModel):
    publication: str = "TIFS"
    query: str = "federated learning"
    year_from: int
    year_to: int
    limit: int = 50


class SwipeRequest(BaseModel):
    paper_id: str
    decision: Literal["LIKED", "SKIPPED"]
    tags: list[str] = []
    notes: str | None = None
