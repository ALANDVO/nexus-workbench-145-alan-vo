import json
from pathlib import Path
from typing import List, Optional

from app.models.issue import GitHubIssue, IssueListResponse, IssueStatus, IssuePriority


class IssueCatalogService:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent.parent / "data"
        self.cache_file = self.data_dir / "issues_cache.json"
        self.sync_needed_file = self.data_dir / "sync_needed.flag"
        
    def load_issues_from_cache(self) -> List[GitHubIssue]:
        """Load issues from cache file if it exists."""
        if not self.cache_file.exists():
            return []
            
        try:
            with open(self.cache_file, "r") as f:
                data = json.load(f)
                return [GitHubIssue(**issue) for issue in data]
        except Exception:
            return []
    
    def sync_issues_from_github(self, repository: str = "anthropics/knowledge-work-plugins") -> List[GitHubIssue]:
        """Sync issues from GitHub repository. This is a placeholder for actual GitHub API integration."""
        issues = self.load_issues_from_cache()
        
        if not issues:
            issues = self._fetch_from_github_api(repository)
            self._save_to_cache(issues)
        
        return issues
    
    def _fetch_from_github_api(self, repository: str) -> List[GitHubIssue]:
        """Placeholder for actual GitHub API fetching. In production, this would use requests library."""
        sample_issues = [
            {
                "id": 1,
                "title": "Sarek FASTQ samplesheets fail validation because BAM and BAI are always required",
                "description": "On main at 95bdacc803aa5cfdb10f35e5b9fb2d4b11100133, Sarek samplesheet generation reports missing BAM and BAI columns for FASTQ input.",
                "status": "open",
                "priority": "high",
                "labels": ["bug", "sarek", "validation"],
                "author": "OpenHands",
                "plugin_id": "bio-research",
                "domain": "bio-research",
                "created_at": "2026-01-15T10:00:00",
                "updated_at": "2026-11-15T14:30:00",
                "comments": [
                    "Steps to reproduce: Put two valid FASTQ files in ./fastqs",
                    "Expected behavior: FASTQ rows should not require BAM or BAI columns",
                    "Validator collects required columns then leaves conditional check as pass"
                ],
                "assignees": [],
                "repository": repository,
                "url": f"https://github.com/{repository}/issues/1"
            },
            {
                "id": 2,
                "title": "Add stability lifecycle frontmatter to skills (experimental/stable/deprecated)",
                "description": "Skills in this plugin have no stability indicator. An AI agent cannot distinguish a well-tested default skill from a new/beta one.",
                "status": "closed",
                "priority": "medium",
                "labels": ["enhancement", "stability", "skill-browser"],
                "author": "Alan Vo",
                "plugin_id": "marketing",
                "domain": "marketing",
                "created_at": "2026-02-20T09:15:00",
                "updated_at": "2026-11-10T16:45:00",
                "comments": [
                    "Proposed solution: Add stability: frontmatter field with experimental/stable/deprecated values"
                ],
                "assignees": [],
                "repository": repository,
                "url": f"https://github.com/{repository}/issues/2"
            },
            {
                "id": 3,
                "title": "google-calendar MCP server turned down — productivity plugin broken",
                "description": "The google-calendar MCP connection used by the productivity plugin stopped working.",
                "status": "in_progress",
                "priority": "high",
                "labels": ["bug", "mcp", "productivity", "calendar"],
                "author": "Claude Code",
                "plugin_id": "productivity",
                "domain": "productivity",
                "created_at": "2026-04-17T12:00:00",
                "updated_at": "2026-11-12T18:20:00",
                "comments": [
                    "Original server at gcal.mcp.claude.com has been shut down",
                    "Replacement endpoint doesn't support dynamic client registration"
                ],
                "assignees": ["Alan Vo"],
                "repository": repository,
                "url": f"https://github.com/{repository}/issues/3"
            },
            {
                "id": 4,
                "title": "Built-in create-shortcut skill references non-existent set_scheduled_task tool",
                "description": "The create-shortcut skill references a set_scheduled_task tool that does not exist in the session's available tool set.",
                "status": "open",
                "priority": "low",
                "labels": ["bug", "skill", "create-shortcut"],
                "author": "Alan Vo",
                "plugin_id": "productivity",
                "domain": "productivity",
                "created_at": "2026-02-05T14:30:00",
                "updated_at": "2026-11-13T11:10:00",
                "comments": [
                    "Cowork loads the create-shortcut skill",
                    "Skill instructs Claude to call the set_scheduled_task tool",
                    "Claude cannot find the tool and enters a loop searching for it"
                ],
                "assignees": [],
                "repository": repository,
                "url": f"https://github.com/{repository}/issues/4"
            },
            {
                "id": 5,
                "title": "legal:ms365 plugin/mcp authentication error",
                "description": "When trying to authenticate the ms365 plugin for legal, the following error is thrown: AADSTS9000411: The request is not properly formatted. The parameter 'prompt' is duplicated.",
                "status": "open",
                "priority": "medium",
                "labels": ["bug", "auth", "ms365", "legal"],
                "author": "OpenHands",
                "plugin_id": "legal",
                "domain": "legal",
                "created_at": "2026-03-10T08:45:00",
                "updated_at": "2026-11-14T15:55:00",
                "comments": [
                    "Error occurs when removing first prompt parameter",
                    "Another error: AADSTS900971: No reply address provided"
                ],
                "assignees": [],
                "repository": repository,
                "url": f"https://github.com/{repository}/issues/5"
            }
        ]
        
        return [GitHubIssue(**issue) for issue in sample_issues]
    
    def _save_to_cache(self, issues: List[GitHubIssue]):
        """Save issues to cache file."""
        self.data_dir.mkdir(exist_ok=True)
        data = [issue.dict() for issue in issues]
        
        with open(self.cache_file, "w") as f:
            json.dump(data, f, indent=2)
    
    def _needs_sync(self) -> bool:
        """Check if a sync is needed."""
        if not self.sync_needed_file.exists():
            return True
        
        try:
            with open(self.sync_needed_file, "r") as f:
                return f.read().strip().lower() == "true"
        except Exception:
            return True
    
    def mark_sync_completed(self):
        """Mark that sync has been completed."""
        self.data_dir.mkdir(exist_ok=True)
        with open(self.sync_needed_file, "w") as f:
            f.write("false")
    
    def get_issues(
        self,
        plugin_id: Optional[str] = None,
        domain: Optional[str] = None,
        status: Optional[IssueStatus] = None,
        labels: Optional[List[str]] = None
    ) -> IssueListResponse:
        """Get issues with optional filtering."""
        issues = self.load_issues_from_cache()
        
        if not issues:
            issues = self._fetch_from_github_api("anthropics/knowledge-work-plugins")
            self._save_to_cache(issues)
        
        filtered_issues = issues
        
        if plugin_id:
            filtered_issues = [i for i in filtered_issues if i.plugin_id == plugin_id]
        
        if domain:
            filtered_issues = [i for i in filtered_issues if i.domain == domain]
        
        if status:
            filtered_issues = [i for i in filtered_issues if i.status == status]
        
        if labels:
            filtered_issues = [i for i in filtered_issues if any(label in i.labels for label in labels)]
        
        return IssueListResponse(issues=filtered_issues, total=len(filtered_issues))


# Global instance for use in API
issue_catalog_service = IssueCatalogService()
