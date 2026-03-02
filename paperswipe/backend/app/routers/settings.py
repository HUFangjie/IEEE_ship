from fastapi import APIRouter

from ..schemas import SettingsPayload
from ..settings import get_settings, save_runtime_settings

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("")
def get_app_settings():
    s = get_settings()
    return {
        "ieee_api_key_set": bool(s.ieee_api_key),
        "llm_provider": s.llm_provider,
        "openai_api_key_set": bool(s.openai_api_key),
        "gemini_api_key_set": bool(s.gemini_api_key),
        "library_path": s.library_path,
        "default_publication": s.default_publication,
    }


@router.post("")
def save_settings(payload: SettingsPayload):
    save_runtime_settings(payload.model_dump())
    return {"ok": True}
