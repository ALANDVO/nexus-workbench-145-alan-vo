import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_list_issues():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/issues")
        assert response.status_code == 200
        data = response.json()
        assert "issues" in data
        assert "total" in data
        assert isinstance(data["issues"], list)
        assert data["total"] == len(data["issues"])
        # Should have at least the sample issues we created
        assert data["total"] >= 3


@pytest.mark.asyncio
async def test_list_issues_filter_by_plugin():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/issues?plugin_id=marketing")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        for issue in data["issues"]:
            assert issue["plugin_id"] == "marketing"


@pytest.mark.asyncio
async def test_list_issues_filter_by_status():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/issues?status=open")
        assert response.status_code == 200
        data = response.json()
        for issue in data["issues"]:
            assert issue["status"] == "open"


@pytest.mark.asyncio
async def test_get_issue():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First get all issues to find one to test
        response = await client.get("/api/v1/issues")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        issue_id = data["issues"][0]["id"]
        
        # Now fetch the specific issue
        response = await client.get(f"/api/v1/issues/{issue_id}")
        assert response.status_code == 200
        issue = response.json()
        assert issue["id"] == issue_id
        assert len(issue["title"]) > 0


@pytest.mark.asyncio
async def test_sync_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/github-sync")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "total" in data
        assert data["total"] >= 1
