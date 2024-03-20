from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar
from litestar.config.cors import CORSConfig

from backend.helpers import create_db_config, provide_transaction
from backend.router import ProjectController, TagController, TaskController

db_config = create_db_config("todo.sqlite")
cors_config = CORSConfig(allow_origins=["*"])


app = Litestar(
    [ProjectController, TaskController, TagController],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
    cors_config=cors_config,
)
