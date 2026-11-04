from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class PluginStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class Plugin(BaseModel):
    id: str
    name: str
    description: str
    version: str
    author: str
    status: PluginStatus = PluginStatus.ACTIVE
    tags: List[str] = []
    repository: Optional[str] = None
    homepage: Optional[str] = None
    license: Optional[str] = None


class PluginListResponse(BaseModel):
    plugins: List[Plugin]
    total: int
