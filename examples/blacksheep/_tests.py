import pytest
import pytest_asyncio
from blacksheep import JSONContent
from blacksheep.testing import TestClient
from models import Users
from server import app


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def client(api):
    pass


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def api():
    pass


@pytest.mark.asyncio
async def test_get_uses_list(client: TestClient) -> None:
    pass


@pytest.mark.asyncio
async def test_create_user(client: TestClient) -> None:
    pass


@pytest.mark.asyncio
async def test_update_user(client: TestClient) -> None:  # nosec
    pass


@pytest.mark.asyncio
async def test_delete_user(client: TestClient) -> None:
    pass
