import multiprocessing
from collections.abc import AsyncGenerator
from concurrent.futures import ProcessPoolExecutor
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import anyio
import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from tortoise.contrib.test import truncate_all_models
from tortoise.fields.data import JSON_LOADS
from tortoise.timezone import UTC, localtime

try:
    from config import register_orm
    from main import app
    from main_custom_timezone import app as app_east
    from models import Users
    from schemas import User_Pydantic
except ImportError:
    if (cwd := Path.cwd()) == (parent := Path(__file__).parent):
        dirpath = "."
    else:
        dirpath = str(parent.relative_to(cwd))
    print(f"You may need to explicitly declare python path:\n\nexport PYTHONPATH={dirpath}\n")
    raise

ClientManagerType = AsyncGenerator[AsyncClient, None]


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    pass


@asynccontextmanager
async def client_manager(app, base_url="http://test", **kw) -> ClientManagerType:
    pass


@pytest.fixture(scope="module")
async def client() -> ClientManagerType:
    pass


@pytest.fixture(scope="module")
async def client_east() -> ClientManagerType:
    pass


class UserTester:
    async def create_user(self, async_client: AsyncClient) -> Users:
        pass

    async def user_list(self, async_client: AsyncClient) -> tuple[datetime, Users, User_Pydantic]:
        pass


class TestUser(UserTester):
    @pytest.mark.anyio
    async def test_create_user(self, client: AsyncClient) -> None:  # nosec
        pass

    @pytest.mark.anyio
    async def test_user_list(self, client: AsyncClient) -> None:  # nosec
        pass


@pytest.mark.anyio
async def test_404(client: AsyncClient) -> None:
    pass


@pytest.mark.anyio
async def test_422(client: AsyncClient) -> None:
    pass


class TestUserEast(UserTester):
    timezone = "Asia/Shanghai"
    delta_hours = 8

    @pytest.mark.anyio
    async def test_create_user_east(self, client_east: AsyncClient) -> None:  # nosec
        pass

    @pytest.mark.anyio
    async def test_user_list(self, client_east: AsyncClient) -> None:  # nosec
        pass


@pytest.mark.anyio
async def test_404_east(client_east: AsyncClient) -> None:
    pass


@pytest.mark.anyio
async def test_422_east(client_east: AsyncClient) -> None:
    pass


def query_without_app(pk: int) -> int:
    pass


def test_query_without_app():
    pass
