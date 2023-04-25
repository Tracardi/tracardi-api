from time import sleep
from uuid import uuid4

from test.utils import Endpoint

endpoint = Endpoint()


def _add_event_management_data(event_type, data=None):
    if data is None:
        data = {
            "event_type": event_type,
            "name": event_type,
            "description": "test-description",
            "enabled": True,
            "tags": ["tag1", "tag2", "tag3"]
        }

    response = endpoint.post("/event-type/management", data)
    assert response.status_code == 200
    return response


def test_event_management_refresh():
    assert endpoint.put("/event-type/management/refresh").status_code == 200


def test_should_post_get_and_delete_validation_schema():
    event_type = str(uuid4())
    try:
        response = _add_event_management_data(event_type)
        result = response.json()

        assert "saved" in result
        assert result['saved'] == 1

        result = endpoint.get(f"/event-type/management/{event_type}")

        assert result.status_code == 200

        result = result.json()
        assert result["event_type"] == event_type

    finally:
        result = endpoint.delete(f"/event-type/management/{event_type}")
        result = result.json()

        assert result["deleted"] == 1


def test_get_validation_schemas():
    event_type = str(uuid4())
    try:
        response = _add_event_management_data(event_type)
        result = response.json()
        assert result['ids'][0] == event_type
        sleep(1)
        response = endpoint.get(f"/event-type/management/{event_type}")
        assert response.status_code == 200
        result = response.json()
        assert result['id'] == event_type

        response = endpoint.get(f"/event-type/management")
        assert response.status_code == 200

    finally:
        response = endpoint.delete(f"/event-type/management/{event_type}")
        assert response.status_code == 200
        result = response.json()
        assert result["deleted"] == 1


def test_get_validation_schemas_by_tag():
    event_type = str(uuid4())
    try:
        _add_event_management_data(event_type)
        response = endpoint.get("/event-type/management/search/by_tag?start=0&limit=1000")
        assert response.status_code == 200
        result = response.json()
        assert 'total' in result
        assert 'grouped' in result
        assert 'tag1' in result['grouped']
        assert 'tag2' in result['grouped']
        assert 'tag3' in result['grouped']
    finally:
        response = endpoint.delete(f"/event-type/management/{event_type}")
        assert response.status_code == 200
        result = response.json()
        assert result["deleted"] == 1


