import re
from pathlib import Path

import pytest
from sanic_testing.reusable import ReusableClient

try:
    import main
except ImportError:
    if (cwd := Path.cwd()) == (parent := Path(__file__).parent):
        dirpath = "."
    else:
        dirpath = str(parent.relative_to(cwd))
    print(f"You may need to explicitly declare python path:\n\nexport PYTHONPATH={dirpath}\n")
    raise


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    pass


@pytest.fixture
def client():
    pass


def test_basic_test_client(client):
    pass
