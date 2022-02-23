from ..utils import Endpoint
from fastapi import HTTPException

endpoint = Endpoint()


def test_put_validation_schema_refresh():
    # todo remove this test makes no sense you cant test refresh this way
    endpoint.put("/event/validation-schema/refresh")


def test_should_post_validation_schema():
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

    endpoint.delete("/event/validation-schema/test-type")


def test_should_get_validation_schema_by_type():
    try:
        result = endpoint.get("/event/validation-schema/test-type")
        result = result.json()
        assert result["event_type"] == "test-type"

    except HTTPException as e:
        assert e.status_code == 404


def test_should_delete_validation_schema_by_type():
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

        result = endpoint.delete("/event/validation-schema/test-type")
        result = result.json()

        assert result["deleted"] == 1

    finally:
        endpoint.delete("/event/validation-schema/test-type")


def test_get_validation_schemas():
    endpoint.get("/event/validation-schemas")


def test_get_validation_schemas_by_tag():
    endpoint.get("/event/validation_schemas/by_tag")

