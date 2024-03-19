from pathlib import Path

from backend.model.project import Project
from tests.helpers import AbstractBaseTestSuite, ResponseValidator


class TestProject(AbstractBaseTestSuite[Project]):
    path = "project"
    fixture = {"first": {"title": "first"},
               "second": {"title": "second"},
               "third": {"title": "third"}}
    update_fixture = {"first": {"title": "first_project"},
                      "second": {"title": "second_project"},
                      "third": {"title": "third_project"}}
    invalid_create_fixture = {"first": {"title": "first"},
                              "second": {"title": "second"},
                              "third": {"title": "third"}}

    async def test_get_item_by_title(self, test_client):
        for key, value in self.fixture.items():
            title = value['title']
            async with test_client as client:
                response = await client.get(self.path, params={"title": title})
                ResponseValidator.validate_return_item_count(1, response)
                ResponseValidator.validate_response_body(response.json()[0], title=title)