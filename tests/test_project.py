import random

import pytest
from litestar.testing import AsyncTestClient

from backend.model import Project
from tests.helpers import ResponseValidator


class TestProject:
    titles = ["first", "second", "third"]
    ids = {}

    @pytest.fixture(scope="class", autouse=True)
    async def create_item(self, test_client: AsyncTestClient):
        async def _create_item(title):
            project = Project(title=title)
            async with test_client as client:
                response = await client.post("/project", json=project.to_dict())
                ResponseValidator.validate_item_created(response, title=title)
                project_id = response.json()["id"]
            return project_id

        titles = random.sample(self.titles, len(self.titles))
        for title in titles:
            self.ids[title] = await _create_item(title)

        yield

        async def _destroy_item(project_id):
            async with test_client as client:
                response = await client.delete(f"/project/{project_id}")
                ResponseValidator.validate_item_deleted(response)
                response = await client.get(f"/project/{project_id}")
                ResponseValidator.validate_item_not_found(response)

        for title, id in self.ids.items():
            await _destroy_item(id)

    async def test_items_successfully_created(self, test_client):
        async with test_client as client:
            for title, project_id in self.ids.items():
                response = await client.get(f"/project/{project_id}")
                ResponseValidator.validate_item_exist(response, title=title)
                response = await client.get("/project", params={"title": title})
                assert len(response.json()) == 1
                ResponseValidator.validate_response_body(
                    response.json()[0], title=title
                )
                response = await client.get("/project")
                assert len(response.json()) == len(self.titles)

    async def test_create_project_same_title_throws_error(self, test_client):
        async with test_client as client:
            project = Project(title=self.titles[0])
            response = await client.post("/project", json=project.to_dict())
            ResponseValidator.validate_item_conflict(response)


