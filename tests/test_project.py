import pytest
from httpx import Response

from backend.model import Project


class TestProject:
    title: str = "test_project"

    @pytest.fixture(scope="function")
    async def project_response(self, test_client) -> Response:
        project = Project(title=self.title)
        async with test_client as client:
            response = await client.post(
                "/project", json=project.to_dict()
            )
        yield response
        async with test_client as client:
            await client.delete(f"/project/{project.id}")

    async def test_response_is_successful(self, project_response):
        assert project_response.status_code == 201
        assert project_response.json()["title"] == self.title
        assert project_response.json()["id"] is not None

    async def test_create_another_project_successful(
            self, project_response, test_client
            ):
        project = Project(title=self.title + "_1")
        async with test_client as client:
            response = await client.post(
                "/project", json=project.to_dict()
            )
            assert response.status_code == 201
            assert response.json()["title"] == self.title + "_1"
            project_id = response.json()["id"]
            assert response.json()["id"] is not None
            response = await client.get("/project")
            assert response.status_code == 200
            assert len(response.json()) == 2
            await client.delete(f"/project/{project_id}")
            response = await client.get("/project")
            assert response.status_code == 200
            assert len(response.json()) == 1

    async def test_find_by_id_return_the_same_obj(self, project_response, test_client):
        project_id = project_response.json()["id"]
        async with test_client as client:
            result = await client.get(f"/project/{project_id}")
            assert result.status_code == 200
            assert result.json()["id"] == project_id
            assert result.json()["title"] == self.title

    async def test_find_by_title_return_the_same_obj(
            self, project_response, test_client
    ):
        project_id = project_response.json()["id"]
        async with test_client as client:
            result = await client.get(f"/project/", params={"title": self.title})
            assert result.status_code == 200
            assert len(result.json()) == 1
            assert result.json()[0]["id"] == project_id
            assert result.json()[0]["title"] == self.title

    async def test_find_wrong_title_return_nothing(self, project_response, test_client):
        async with test_client as client:
            result = await client.get(f"/project/", params={"title": self.title + "_"})
            assert result.status_code == 200
            assert len(result.json()) == 0

    async def test_create_same_title_integrity_error(
            self, project_response, test_client
    ):
        project = Project(title=self.title)
        async with test_client as client:
            response = await client.post(
                "/project", json=project.to_dict()
            )
            assert response.status_code == 409

    async def test_delete_object_no_longer_exist(self, project_response, test_client):
        project_id = project_response.json()["id"]
        async with test_client as client:
            response = await client.delete(f"/project/{project_id}")
            assert response.status_code == 204
            result = await client.get(f"/project/{project_id}")
            assert result.status_code == 404
