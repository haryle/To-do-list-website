from backend.model import Task
from tests.helpers import AbstractBaseTestSuite, ResponseValidator


class TestTask(AbstractBaseTestSuite[Task]):
    path = "task"
    fixture = {"first": {"title": "first", "status": True},
               "second": {"title": "second", "status": False},
               "third": {"title": "third", "status": False}}
    update_fixture = {"first": {"title": "first_tag"},
                      "second": {"title": "second_tag"},
                      "third": {"title": "third_tag"}}
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

    async def test_get_item_by_status(self, test_client):
        num_true_tasks = len([value for value in self.fixture.values() if value['status']])
        num_false_tasks = len(self.fixture) - num_true_tasks

        async with test_client as client:
            response = await client.get(self.path, params={"status": True})
            ResponseValidator.validate_return_item_count(num_true_tasks, response)
            response = await client.get(self.path, params={"status": False})
            ResponseValidator.validate_return_item_count(num_false_tasks, response)