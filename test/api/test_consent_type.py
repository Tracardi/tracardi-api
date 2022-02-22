from ..utils import Endpoint
from fastapi import HTTPException

endpoint = Endpoint()


def test_post_consent_type():
    data = {
        "name": "test-name",
        "description": "test-description",
        "revokable": True,
        "default_value": "grant",
        "enabled": True,
        "tags": ["tag1", "tag2", "tag3"],
        "required": True,
        "auto_revoke": "15m"
    }
    result = endpoint.post("/consent/type", data)
    result = result.json()

    assert not result["errors"]
    assert result["saved"] == 1
    assert result["ids"] == ["test-name"]

    data = {
        "name": "test-name",
        "description": "test-description",
        "revokable": False,
        "default_value": "deny",
        "enabled": False,
        "tags": ["tag1", "tag2", "tag3"],
        "required": False,
        "auto_revoke": "15m"
    }
    result = endpoint.post("/consent/type", data)
    result = result.json()

    assert not result["errors"]
    assert result["saved"] == 1
    assert result["ids"] == ["test-name"]

    data = {
        "name": "test-name",
        "description": "test-description",
        "revokable": False,
        "default_value": "incorrect_data",
        "enabled": False,
        "tags": ["tag1", "tag2", "tag3"],
        "required": False,
        "auto_revoke": "incorrect_data"
    }
    result = endpoint.post("/consent/type", data)
    result = result.json()

    assert "detail" in result
    assert result["detail"][0]["loc"][1] == "default_value"
    assert result["detail"][1]["loc"][1] == "auto_revoke"

    endpoint.delete("/consent/type/test-name")


def test_get_consent_type_id():
    data = {
        "name": "test-name",
        "description": "test-description",
        "revokable": True,
        "default_value": "grant",
        "enabled": True,
        "tags": ["tag1", "tag2", "tag3"],
        "required": True,
        "auto_revoke": "15m"
    }
    result = endpoint.post("/consent/type", data)
    result = result.json()

    assert not result["errors"]
    assert result["saved"] == 1
    assert result["ids"] == ["test-name"]

    result = endpoint.get("/consent/type/test-name")
    result = result.json()

    assert "id" in result and result["id"] == "test-name"

    endpoint.delete("/consent/type/test-name")


def test_delete_consent_type_id():
    data = {
        "name": "test-name",
        "description": "test-description",
        "revokable": True,
        "default_value": "grant",
        "enabled": True,
        "tags": ["tag1", "tag2", "tag3"],
        "required": True,
        "auto_revoke": "15m"
    }
    result = endpoint.post("/consent/type", data)
    result = result.json()

    assert not result["errors"]
    assert result["saved"] == 1
    assert result["ids"] == ["test-name"]

    result = endpoint.delete("/consent/type/test-name")
    result = result.json()

    assert result == {"deleted": 1}

    result = endpoint.delete("/consent/type/test-name")
    result = result.json()

    assert result == {"deleted": 0}


def test_get_consents_type():
    result = endpoint.get("/consents/type")


def test_get_consents_type_enabled():
    result = endpoint.get("/consents/type/enabled")
    result = result.json()

    assert {consent["enabled"] for consent in result["result"]} == {True}


def test_put_consents_type_refresh():
    result = endpoint.put("/consents/type/refresh")


def test_get_consents_type_by_tag():
    result = endpoint.get("/consents/type/by_tag")









