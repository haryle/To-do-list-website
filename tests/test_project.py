import pytest
from litestar.testing import AsyncTestClient

from backend.model import Project

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_add_project_to_db(test_client) -> None:
    async with test_client as client:
        first_project = Project(title="first_project")
        await client.post("/project", json=first_project.to_dict())

        fetch_result = await client.get(
            "/project", params={"title": first_project.title}
        )
        assert fetch_result.status_code == 200
        assert len(fetch_result.json()) == 1
        item_id = fetch_result.json()[0]["id"]
        get_result_by_id = await client.get(f"/project/{item_id}")
        assert get_result_by_id.json()["title"] == first_project.title
        delete_result = await client.delete(f"/project/{item_id}")
        assert delete_result.status_code == 204
        get_result_by_id = await client.get(f"/project/{item_id}")
        assert get_result_by_id.status_code == 404
