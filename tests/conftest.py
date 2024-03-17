from pathlib import Path

import pytest
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar
from litestar.testing import AsyncTestClient

from backend.helpers import create_db_config, provide_transaction
from backend.router import ProjectController, TagController, TaskController


@pytest.fixture(scope="function")
def test_client() -> AsyncTestClient:
    p = Path("test.sqlite")
    db_config = create_db_config("test.sqlite")
    app = Litestar(
        [ProjectController, TaskController, TagController],
        dependencies={"transaction": provide_transaction},
        plugins=[SQLAlchemyPlugin(db_config)]
    )
    yield AsyncTestClient(app=app)
    p.unlink(missing_ok=True)
