from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class IssueStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"


class IssuePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class GitHubIssue(BaseModel):
    id: int = Field(..., description="GitHub issue number")
    title: str = Field(..., description="Issue title")
    description: Optional[str] = Field(None, description="Issue body/content")
    status: IssueStatus = Field(default=IssueStatus.OPEN)
    priority: IssuePriority = Field(default=IssuePriority.MEDIUM)
    labels: List[str] = Field(default=[], description="List of label names")
    author: Optional[str] = Field(None, description="Issue author")
    plugin_id: Optional[str] = Field(None, description="Plugin associated with issue")
    domain: Optional[str] = Field(None, description="Domain (bio-research, marketing, productivity)")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    updated_at: Optional[str] = Field(None, description="Last update timestamp")
    comments: List[str] = Field(default=[], description="List of comment contents")
    assignees: List[str] = Field(default=[], description="List of assignees")
    repository: str = Field(..., description="Source repository (e.g., anthropics/knowledge-work-plugins)")
    url: str = Field(..., description="Direct URL to the issue")


class IssueListResponse(BaseModel):
    issues: List[GitHubIssue]
    total: int
