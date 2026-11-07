from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from pathlib import Path

from app.services.skill_catalog import get_skills, PLUGINS_DIR
from app.models.skill import SkillListResponse, SkillStability

router = APIRouter()


@router.get("/skills", response_model=SkillListResponse)
async def list_skills(
    plugin_id: Optional[str] = Query(None, description="Filter by plugin ID"),
    stability: Optional[SkillStability] = Query(None, description="Filter by stability level"),
) -> SkillListResponse:
    return get_skills(plugin_id=plugin_id, stability=stability)


@router.get("/skills/{plugin_id}/{skill_id}/content")
async def get_skill_content(plugin_id: str, skill_id: str):
    skill_file = PLUGINS_DIR / plugin_id / "skills" / skill_id / "SKILL.md"
    if not skill_file.exists():
        raise HTTPException(status_code=404, detail="Skill not found")
    try:
        content = skill_file.read_text()
        return content
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to read skill content")
