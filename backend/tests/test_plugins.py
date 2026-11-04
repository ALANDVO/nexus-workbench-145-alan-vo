import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_list_plugins():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/plugins")
        assert response.status_code == 200
        data = response.json()
        assert "plugins" in data
        assert "total" in data
        assert isinstance(data["plugins"], list)
        assert data["total"] == len(data["plugins"])
        # Should have at least the three sample plugins
        assert data["total"] >= 3
