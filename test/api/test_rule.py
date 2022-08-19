from uuid import uuid4

from .test_event_source_endpoint import _create_event_source
from ..utils import Endpoint

endpoint = Endpoint()


def test_should_return_404_on_get_rule_if_none():
    session_id = str(uuid4())
    response = endpoint.get(f'/rule/{session_id}')
    assert response.status_code == 404
    assert response.json() is None


def test_should_return_404_on_delete_rule_if_none():
    session_id = str(uuid4())
    response = endpoint.delete(f'/rule/{session_id}')
    assert response.status_code == 404
    assert response.json() is None


def test_should_return_error_if_incorrect_source_id():

    data = {
        "id": "rule_id",
        "name": "string",
        "event": {
            "type": "string"
        },
        "flow": {
            "id": "flow_id",
            "name": "string"
        },
        "source": {
            "id": "string",
            "name": "string"
        },
        "enabled": True
    }

    response = endpoint.post('/rule', data=data)
    assert response.status_code == 422

    result = response.json()
    assert result['detail'] == 'Incorrect source id: `string`'


def test_should_create_new_rule():

    flow_id = str(uuid4())
    rule_id = str(uuid4())
    source_id = str(uuid4())

    try:
        # Add source

        assert _create_event_source(source_id, "rest").status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        response = endpoint.get(f'/event-source/{source_id}')
        assert response.status_code == 200

        # Create rule with new source

        data = {
            "id": rule_id,
            "name": "string",
            "event": {
                "type": "string"
            },
            "flow": {
                "id": flow_id,
                "name": "string"
            },
            "source": {
                "id": source_id,
                "name": "javascript"
            },
            "enabled": True
        }

        response = endpoint.post('/rule', data=data)
        result = response.json()

        assert response.status_code == 200
        assert result == {'saved': 1, 'errors': [], 'ids': [rule_id]}

        # Check if flow was created
        assert endpoint.get('/rules/refresh').status_code == 200

        response = endpoint.get(f'/flow/metadata/{flow_id}')
        assert response.status_code == 200
        result = response.json()
        assert result['id'] == flow_id

    finally:
        assert endpoint.get('/rules/refresh').status_code == 200
        assert endpoint.get('/flows/refresh').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]
        assert endpoint.delete(f'/rule/{rule_id}').status_code in [200, 404]
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
