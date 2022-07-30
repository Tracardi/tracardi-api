from ..utils import Endpoint
from fastapi import HTTPException

endpoint = Endpoint()


def test_should_post_get_and_delete_validation_schema():
    try:
        data = {
            "event_type": "test-type",
            "name": "test-name",
            "description": "test-description",
            "enabled": True,
            "tags": ["tag1", "tag2", "tag3"],
            "validation": {
                "json_schema": {
                    "event@...": {
                        "type": "object"
                    }
                }
            }
        }

        result = endpoint.post("/event-type/management", data)
        result = result.json()

        assert "added" in result

        result = endpoint.get("/event-type/management/test-type")

        assert result.status_code == 200

        result = result.json()
        assert result["event_type"] == "test-type"

    finally:
        result = endpoint.delete("/event-type/management/test-type")
        result = result.json()

        assert result["deleted"] == 1


def test_get_validation_schemas():
    endpoint.get("/event-type/management")


def test_get_validation_schemas_by_tag():
    endpoint.get("/event-type/management/by_tag")
