from typing import Any, Literal

from httpx import Response

HTTP_CODE = Literal[200, 201, 204, 404, 500, 409]


class ResponseValidator:
    @staticmethod
    def validate_status(expected_code: HTTP_CODE, response: Response) -> None:
        assert response.status_code == expected_code

    @staticmethod
    def validate_body_empty(response: Response) -> None:
        ResponseValidator.validate_return_item_count(0, response)

    @staticmethod
    def validate_return_item_count(expected_count: int, response: Response) -> None:
        assert len(response.json()) == expected_count

    @staticmethod
    def validate_response_body(response_body: dict[str, Any], **kwargs) -> None:
        for key, value in kwargs.items():
            assert response_body.get(key, None) == value

    @staticmethod
    def validate_item_created(response: Response, **kwargs) -> None:
        ResponseValidator.validate_status(201, response)
        ResponseValidator.validate_response_body(response.json(), **kwargs)

    @staticmethod
    def validate_item_exist(response: Response, **kwargs) -> None:
        ResponseValidator.validate_status(200, response)
        ResponseValidator.validate_response_body(response.json(), **kwargs)

    @staticmethod
    def validate_item_deleted(response: Response) -> None:
        ResponseValidator.validate_status(204, response)

    @staticmethod
    def validate_item_not_found(response: Response) -> None:
        ResponseValidator.validate_status(404, response)

    @staticmethod
    def validate_item_conflict(response)->None:
        ResponseValidator.validate_status(409, response)
