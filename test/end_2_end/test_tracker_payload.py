from uuid import uuid4
from ..api.test_event_source import create_event_source
from ..utils import Endpoint

endpoint = Endpoint()


def test_track_payload():

    source_id = str(uuid4())
    session_id = str(uuid4())

    try:
        response = create_event_source(source_id, "javascript")
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
        assert result['debugging']['events']['saved'] == 1
        assert len(result['debugging']['events']['errors']) == 0
        assert len(result['debugging']['events']['ids']) == 1
        assert 'id' in result['profile']

        assert endpoint.get('/profiles/refresh').status_code == 200
        assert endpoint.get('/sessions/refresh').status_code == 200
        profile_id = result['profile']['id']

        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200

    finally:
        assert endpoint.delete(f'/resource/{source_id}').status_code in [200, 404]
        assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
