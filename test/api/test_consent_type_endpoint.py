from ..utils import Endpoint

endpoint = Endpoint()


def _add_consent_type(name='test-name', data=None):
    if data is None:
        data = {
            "name": name,
            "description": "test-description",
            "revokable": True,
            "default_value": "grant",
            "enabled": True,
            "tags": ["tag1", "tag2", "tag3"],
            "required": True,
            "auto_revoke": "15m"
        }
    response = endpoint.post("/consent/type", data)
    assert response.status_code == 200

    return response


def test_should_add_consent_type():
    try:
        response = _add_consent_type()
        result = response.json()

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
    finally:
        endpoint.delete("/consent/type/test-name")


def test_should_get_consent_type_id():
    try:
        _add_consent_type()

        result = endpoint.get("/consent/type/test-name")
        result = result.json()

        assert "id" in result and result["id"] == "test-name"
    finally:
        endpoint.delete("/consent/type/test-name")


def test_should_delete_consent_type_id():
    try:

        _add_consent_type()

        result = endpoint.delete("/consent/type/test-name")
        result = result.json()

        assert result == {"deleted": 1}

        result = endpoint.delete("/consent/type/test-name")
        result = result.json()

        assert result == {"deleted": 0}

    finally:
        endpoint.delete("/consent/type/test-name")


def test_should_get_consents_type():
    try:
        _add_consent_type()

        response = endpoint.get("/consents/type")

        assert response.status_code == 200

        result = response.json()
        assert result['result'][0]['id'] == 'test-name'
    finally:
        endpoint.delete("/consent/type/test-name")


def test_should_get_consents_type_enabled():
    try:
        _add_consent_type()

        result = endpoint.get("/consents/type/enabled")
        result = result.json()

        assert {consent["enabled"] for consent in result["result"]} == {True}

    finally:
        endpoint.delete("/consent/type/test-name")


def test_should_put_consents_type_refresh():
    response = endpoint.put("/consents/type/refresh")
    assert response.status_code == 200


def test_should_get_consents_type_by_tag():
    try:
        data = {
            "name": 'test-name',
            "description": "test-description",
            "revokable": True,
            "default_value": "grant",
            "enabled": True,
            "tags": ["tag1", "tag2", "tag3"],
            "required": True,
            "auto_revoke": "15m"
        }

        _add_consent_type(data=data)

        response = endpoint.get("/consents/type/by_tag")
        assert response.status_code == 200

        result = response.json()

        assert response.status_code == 200
        assert result['total'] == 1
        assert 'tag1' in result['grouped']
        assert 'tag2' in result['grouped']
        assert 'tag3' in result['grouped']

        data["id"] = 'test-name'

        assert result['grouped']['tag1'][0] == data
        assert result['grouped']['tag2'][0] == data
        assert result['grouped']['tag3'][0] == data
    finally:
        endpoint.delete("/consent/type/test-name")


def test_should_get_consents_type_ids():
    try:
        _add_consent_type()
        response = endpoint.get("/consents/type/ids")
        result = response.json()
        assert response.status_code == 200
        assert result['result'] == ['test-name']
    finally:
        endpoint.delete("/consent/type/test-name")