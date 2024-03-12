from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from backend.model.project import Project


class ProjectReadDTO(SQLAlchemyDTO[Project]):
    config = SQLAlchemyDTOConfig(exclude={"tasks"})


class ProjectWriteDTO(SQLAlchemyDTO[Project]):
    config = SQLAlchemyDTOConfig(exclude={"tasks", "id"})


class ProjectUpdateDTO(SQLAlchemyDTO[Project]):
    config = SQLAlchemyDTOConfig(exclude={"tasks", "id", "created_at"})