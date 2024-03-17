from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar

from backend.helpers import provide_transaction, create_db_config
from backend.router import ProjectController, TaskController

db_config = create_db_config("todo.sqlite")

app = Litestar(
    [
        ProjectController,
        TaskController
    ],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
)
