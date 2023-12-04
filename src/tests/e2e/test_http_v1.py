import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_http_health(app_test):
    async with AsyncClient(app=app_test, base_url="http://test") as client:
        response = await client.get("/health", follow_redirects=True)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
