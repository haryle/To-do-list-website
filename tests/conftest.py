import pytest
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar
from litestar.testing import AsyncTestClient

from backend.helpers import create_db_config, provide_transaction
from backend.router import ProjectController, TagController, TaskController

db_config = create_db_config("test.sqlite")

@pytest.fixture(scope="function")
def app() -> Litestar:
    return Litestar(
        [ProjectController, TaskController, TagController],
        dependencies={"transaction": provide_transaction},
        plugins=[SQLAlchemyPlugin(db_config)]
    )


@pytest.fixture(scope="function")
async def test_client() -> AsyncTestClient:
    return AsyncTestClient(app=app)
