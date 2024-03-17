import pytest
from litestar.testing import AsyncTestClient

from backend.model import Project

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_add_project(app) -> None:
    project = Project(title="first_project")
    async with AsyncTestClient(app) as client:
        result = await client.post(
            "/project", json=project.to_dict()
        )
        assert result.status_code == 201
        assert result.json()['title'] == project.title
        get_result = await client.get("/project", params={"title": project.title})
        assert get_result.status_code == 200
        assert len(get_result.json()) == 1
        item_id = get_result.json()[0].id
        get_result_by_id = await client.get(f"/project/{item_id}")
        assert get_result_by_id.json().title == project.title
