from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar

from backend.helpers import create_db_config, provide_transaction
from backend.router import ProjectController, TagController, TaskController

db_config = create_db_config("todo.sqlite")

app = Litestar(
    [
        ProjectController,
        TaskController,
        TagController
    ],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
)
