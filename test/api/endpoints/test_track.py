from uuid import uuid4

from .test_event_source_endpoint import _create_event_source
from test.utils import Endpoint

endpoint = Endpoint()


def test_should_register_correct_event():
    source_id = str(uuid4())

    try:

        assert _create_event_source(source_id, 'rest').status_code == 200

        payload = {
            "source": {
                "id": source_id
            },
            "session": {
                "id": str(uuid4())
            },
            "events": [
                {
                    "type": "test-event-1",
                    "options": {"save": True},
                    "context": {"test": 1}
                },
                {
                    "type": "test-event-2",
                    "context": {"test": 2}
                }
            ],
            "options": {"debugger": True}
        }

        response = endpoint.post("/track", data=payload)
        assert response.status_code == 200
        result = response.json()

        assert 'profile' in result
        assert 'id' in result['profile']
        profile_id = result['profile']['id']

        assert 'events' in result

        assert len(result['events']) == 5  # 2 events + Profile Created, Session Opened, Visit Created.
        session_id = result['session']['id']
        try:
            endpoint.get('/events/refresh')

            # Event 1

            for event_id in result['events']:
                response = endpoint.get(f'/event/{event_id}')
                _result = response.json()
                assert _result['event']['id'] == event_id
                if _result['event']['type'] == "test-event-1":
                    assert _result['event']['context']['test'] == 1
                if _result['event']['type'] == "test-event-2":
                    assert _result['event']['context']['test'] == 2

            endpoint.get('/sessions/refresh')
            response = endpoint.get(f'/session/{session_id}')
            _result = response.json()
            assert 'id' in _result
            assert _result['id'] == session_id

            endpoint.get('/profiles/refresh')
            response = endpoint.get(f'/profile/{profile_id}')
            _result = response.json()
            assert 'id' in _result
            assert _result['id'] == profile_id

        finally:
            assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
            for event_id in result['events']:
                assert endpoint.delete(f'/event/{event_id}').status_code in [200, 404]
            assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]

    finally:
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
