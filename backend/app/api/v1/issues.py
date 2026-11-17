from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List

from app.services.issue_catalog import issue_catalog_service
from app.models.issue import GitHubIssue, IssueListResponse, IssueStatus


router = APIRouter()


@router.get("/issues", response_model=IssueListResponse)
async def list_issues(
    plugin_id: Optional[str] = Query(None, description="Filter by plugin ID"),
    domain: Optional[str] = Query(None, description="Filter by domain"),
    status: Optional[IssueStatus] = Query(None, description="Filter by status"),
    labels: Optional[List[str]] = Query(None, description="Filter by labels (comma-separated)")
) -> IssueListResponse:
    """Get GitHub issues with optional filtering."""
    issues = issue_catalog_service.get_issues(
        plugin_id=plugin_id,
        domain=domain,
        status=status,
        labels=labels
    )
    
    return issues


@router.get("/issues/{issue_id}", response_model=GitHubIssue)
async def get_issue(issue_id: int) -> GitHubIssue:
    """Get a specific issue by ID."""
    issues = issue_catalog_service.get_issues()
    for issue in issues.issues:
        if issue.id == issue_id:
            return issue
    
    raise HTTPException(status_code=404, detail="Issue not found")


@router.get("/issues/sync", summary="Trigger issue sync")
async def trigger_sync():
    """Trigger sync with GitHub repository."""
    issues = issue_catalog_service.sync_issues_from_github()
    return {"message": f"Synced {len(issues)} issues", "total": len(issues)}
