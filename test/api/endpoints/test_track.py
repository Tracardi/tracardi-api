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

        assert 'event' in result
        assert 'ids' in result['event']

        assert len(result['event']['ids']) == 2
        event_1, event_2 = result['event']['ids']
        session_id = result['session']['id']
        try:
            endpoint.get(f'/events/refresh')

            # Event 1

            response = endpoint.get(f'/event/{event_1}')
            result = response.json()
            assert result['event']['id'] == event_1
            assert result['event']['context']['test'] == 1

            # Event 2

            response = endpoint.get(f'/event/{event_2}')
            result = response.json()
            assert result['event']['id'] == event_2
            assert result['event']['context']['test'] == 2

            endpoint.get(f'/sessions/refresh')
            response = endpoint.get(f'/session/{session_id}')
            result = response.json()
            assert 'id' in result
            assert result['id'] == session_id

            endpoint.get(f'/profiles/refresh')
            response = endpoint.get(f'/profile/{profile_id}')
            result = response.json()
            assert 'id' in result
            assert result['id'] == profile_id

        finally:
            assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
            assert endpoint.delete(f'/event/{event_1}').status_code in [200, 404]
            assert endpoint.delete(f'/event/{event_2}').status_code in [200, 404]
            assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]

    finally:
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
