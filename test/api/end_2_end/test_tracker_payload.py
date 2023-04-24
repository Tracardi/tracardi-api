from uuid import uuid4
from test.api.endpoints.test_event_source_endpoint import _create_event_source
from test.utils import Endpoint

endpoint = Endpoint()


def test_track_payload():

    source_id = str(uuid4())
    session_id = str(uuid4())

    try:
        response = _create_event_source(source_id, "rest")
        assert response.status_code == 200

        payload = {
            "source": {
                "id": source_id
            },
            "session": {
                "id": session_id
            },
            "events": [{"type": "page-view"}, {"type": "page-view", "options": {"save": False}}],
            "options": {
                "debugger": True
            }
        }

        response = endpoint.post("/track", data=payload)
        assert response.status_code == 200

        result = response.json()
        if 'event' not in result:
            raise ValueError(
                'Could not perform test due to bad server configuration. No debugging allowed. '
                'Start Tracardi with TRACK_DEBUG=yes.')

        assert len(result['event']['ids']) == 3  # Event, Session opened, Profile Created

        assert 'id' in result['profile']

        assert endpoint.get('/profiles/refresh').status_code == 200
        assert endpoint.get('/sessions/refresh').status_code == 200
        profile_id = result['profile']['id']

        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200

    finally:

        assert endpoint.get(f'/sessions/refresh').status_code == 200
        assert endpoint.get(f'/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
