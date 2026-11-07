import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_list_skills():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/skills")
        assert response.status_code == 200
        data = response.json()
        assert "skills" in data
        assert "total" in data
        assert isinstance(data["skills"], list)
        assert data["total"] == len(data["skills"])
        # Should have at least the sample skills we created
        assert data["total"] >= 5


@pytest.mark.asyncio
async def test_list_skills_filter_by_plugin():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/skills?plugin_id=bio-research")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 2
        for skill in data["skills"]:
            assert skill["plugin_id"] == "bio-research"


@pytest.mark.asyncio
async def test_list_skills_filter_by_stability():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/skills?stability=stable")
        assert response.status_code == 200
        data = response.json()
        for skill in data["skills"]:
            assert skill["stability"] == "stable"


@pytest.mark.asyncio
async def test_get_skill_content():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First get a skill to test
        response = await client.get("/api/v1/skills?plugin_id=bio-research")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        skill = data["skills"][0]
        
        # Now fetch its content
        content_response = await client.get(f"/api/v1/skills/{skill['plugin_id']}/{skill['id']}/content")
        assert content_response.status_code == 200
        content = content_response.text
        assert len(content) > 0
        assert "---" in content  # Frontmatter delimiter
