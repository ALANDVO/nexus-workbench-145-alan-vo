import json
from pathlib import Path
from typing import List, Optional

import requests

from app.models.issue import GitHubIssue, IssueListResponse, IssueStatus, IssuePriority


class IssueCatalogService:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent.parent / "data"
        self.cache_file = self.data_dir / "issues_cache.json"
        self.sync_needed_file = self.data_dir / "sync_needed.flag"
        self.default_repository = "anthropics/knowledge-work-plugins"
    
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
        """Sync issues from GitHub repository."""
        issues = self.load_issues_from_cache()
        
        # Always try to fetch from GitHub API to get fresh data
        github_issues = self._fetch_from_github_api(repository)
        if github_issues:
            self._save_to_cache(github_issues)
            return github_issues
        
        # Fall back to cache if API fails
        return issues
    
    def _fetch_from_github_api(self, repository: str) -> List[GitHubIssue]:
        """Fetch issues from GitHub API."""
        try:
            url = f"https://api.github.com/repos/{repository}/issues"
            params = {
                "per_page": 100,
                "state": "all",
                "sort": "created",
                "direction": "desc"
            }
            headers = {
                "Accept": "application/vnd.github.v3+api"
            }
            resp = requests.get(url, params=params, headers=headers, timeout=30)
            
            if resp.status_code != 200:
                print(f"GitHub API returned status {resp.status_code}")
                return []
            
            issues_data = resp.json()
            issues = []
            for issue_data in issues_data:
                # Map GitHub API response to GitHubIssue model
                # Extract labels
                labels = [label["name"] for label in issue_data.get("labels", [])]
                
                # Extract assignees
                assignees = [assignee["login"] for assignee in issue_data.get("assignees", [])]
                
                # Get author/login
                author_data = issue_data.get("user", {})
                author = author_data.get("login") if author_data else None
                
                # Get body/description
                body = issue_data.get("body")
                
                # Get created_at and updated_at
                created_at = issue_data.get("created_at")
                updated_at = issue_data.get("updated_at")
                
                # Build the issue, only include fields that exist in the model
                issue_dict = {
                    "id": issue_data["id"],
                    "title": issue_data["title"],
                    "description": body,
                    "status": IssueStatus(issue_data.get("state", "open")).value 
                        if issue_data.get("state") in ["open", "closed"] 
                        else IssueStatus.OPEN,
                    "priority": IssuePriority.MEDIUM,  # Default, GitHub doesn't have priority directly
                    "labels": labels,
                    "author": author,
                    "plugin_id": None,
                    "domain": None,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "comments": [],  # We'd need separate API call for comments
                    "assignees": assignees,
                    "repository": repository,
                    "url": issue_data.get("html_url", f"https://github.com/{repository}/issues/{issue_data['number']}")
                }
                issues.append(GitHubIssue(**issue_dict))
            
            return issues
            
        except requests.RequestException as e:
            print(f"GitHub API request error: {e}")
            return []
        except Exception as e:
            print(f"Error fetching from GitHub API: {e}")
            return []
    
    def _save_to_cache(self, issues: List[GitHubIssue]):
        """Save issues to cache file."""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            serializable = []
            for issue in issues:
                d = {}
                for field, value in issue.model_dump().items():
                    if value is not None:
                        d[field] = value
                serializable.append(d)
            with open(self.cache_file, "w") as f:
                json.dump(serializable, f, indent=2)
        except Exception as e:
            print(f"Error saving to cache: {e}")
    
    def _needs_sync(self) -> bool:
        """Check if a sync is needed."""
        if not self.cache_file.exists():
            return True
        
        try:
            import os
            cache_mtime = self.cache_file.stat().st_mtime
            flag_content = self.sync_needed_file.read_text().strip() if self.sync_needed_file.exists() else "true"
            return flag_content == "true"
        except Exception:
            return True
    
    def mark_sync_completed(self):
        """Mark that sync has been completed."""
        try:
            self.sync_needed_file.write_text("false")
        except Exception:
            pass
    
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
            issues = self.sync_issues_from_github()
        
        filtered_issues = issues
        
        if plugin_id:
            filtered_issues = [i for i in filtered_issues if i.plugin_id == plugin_id]
        
        if domain:
            filtered_issues = [i for i in filtered_issues if i.domain == domain]
        
        if status:
            filtered_issues = [i for i in filtered_issues if i.status == status]
        
        if labels:
            filtered_issues = [i for i in filtered_issues 
                             if any(label in i.labels for label in labels)]
        
        total = len(filtered_issues)
        return IssueListResponse(issues=filtered_issues, total=total)


# Global instance for use in API
issue_catalog_service = IssueCatalogService()
