from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class SkillStability(str, Enum):
    EXPERIMENTAL = "experimental"
    STABLE = "stable"
    DEPRECATED = "deprecated"


class Skill(BaseModel):
    id: str
    name: str
    description: str
    plugin_id: str
    stability: SkillStability = SkillStability.EXPERIMENTAL
    tags: List[str] = []
    file_path: str


class SkillListResponse(BaseModel):
    skills: List[Skill]
    total: int
