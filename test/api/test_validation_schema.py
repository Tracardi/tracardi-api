from ..utils import Endpoint
from fastapi import HTTPException

endpoint = Endpoint()


def test_should_post__get_and_delete_validation_schema():
    try:
        data = {
            "event_type": "test-type",
            "name": "test-name",
            "description": "test-description",
            "enabled": True,
            "tags": ["tag1", "tag2", "tag3"],
            "validation": {
                "event@...": {
                    "type": "object"
                }
            }
        }

        result = endpoint.post("/event/validation-schema", data)
        result = result.json()

        assert "added" in result

        result = endpoint.get("/event/validation-schema/test-type")

        assert result.status_code == 200

        result = result.json()
        assert result["event_type"] == "test-type"

    finally:
        result = endpoint.delete("/event/validation-schema/test-type")
        result = result.json()

        assert result["deleted"] == 1


def test_get_validation_schemas():
    endpoint.get("/event/validation-schemas")


def test_get_validation_schemas_by_tag():
    endpoint.get("/event/validation_schemas/by_tag")

