from pytest import mark
from httpx import ASGITransport, AsyncClient
from python_container_demo.server import app


@mark.asyncio
async def test_root() -> None:
    """Test the server's root path."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.content.decode() == '"Hello, World!"'
    assert response.status_code == 200


@mark.asyncio
@mark.parametrize("phrase", ["amiao", "yahaha"])
async def test_echo(phrase: str) -> None:
    """Test if the server responds with status_code 404 for non-root path."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(f"/echo/{phrase}")
    assert response.content.decode() == f'"{phrase}"'
    assert response.status_code == 200


@mark.asyncio
@mark.parametrize("path", ["/random", "/random/path"])
async def test_fallback(path: str) -> None:
    """Test if the server responds with status_code 404 for non-root path."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(path)
    assert response.status_code == 404
