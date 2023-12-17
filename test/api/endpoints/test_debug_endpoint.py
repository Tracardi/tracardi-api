from uuid import uuid4

from datetime import datetime

from test.api.endpoints.test_event_source_endpoint import _create_event_source
from tracardi.context import ServerContext, Context

from test.utils import Endpoint, get_test_tenant
from tracardi.service.storage.index import Resource

endpoint = Endpoint()


def test_should_return_indices():
    with ServerContext(Context(production=False, tenant=get_test_tenant())):
        response = endpoint.get("/debug/es/indices")
        result = response.json()
        assert response.status_code == 200
        alias = Resource()['version'].get_write_index()
        assert alias in result.keys()


def test_should_return_server_time():
    response = endpoint.get("/debug/server/time")
    result = response.json()
    assert response.status_code == 200
    try:
        datetime.strptime(result, '%Y-%m-%dT%H:%M:%S.%f+00:00')
    except ValueError:
        assert False


def test_debug_option():
    properties = {}

    source_id = str(uuid4())
    session_id = str(uuid4())
    try:
        assert _create_event_source(source_id, 'rest').status_code == 200

        payload = {
            "source": {
                "id": source_id
            },
            "session": {
                "id": session_id
            },
            "events": [
                {
                    "type": type,
                    "properties": properties,
                    "options": {"save": True},
                    "context": {"test": 1}
                }
            ],
            "options": {"debugger": True}
        }

        response = endpoint.post("/track", data=payload)
        assert response.status_code == 200

        result = response.json()
        assert isinstance(result['events'], list)
        assert 'id' in result['profile']
        assert 'id' in result['session']
        assert 'response' in result
        assert 'ux' in result
        assert 'errors' in result
        assert 'warnings' in result
        assert 'response' in result
        assert 'task' in result
    finally:
        assert endpoint.delete(f'/session/{session_id}').status_code == 200
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]