from uuid import uuid4
from test.api.endpoints.test_event_source_endpoint import _create_event_source
from test.utils import Endpoint, create_session, create_profile, get_session, get_profile

endpoint = Endpoint()


def test_session_exists_profile_exists():
    source_id = str(uuid4())
    session_id = str(uuid4())
    profile_id = str(uuid4())

    try:
        create_session(session_id, profile_id)
        create_profile(profile_id)

        # Assert session and profile exists

        assert get_session(session_id).status_code == 200
        assert get_profile(profile_id).status_code == 200
        assert _create_event_source(source_id, 'rest').status_code == 200

        response = endpoint.post("/track", data={
            "source": {
                "id": source_id
            },
            "session": {
                "id": session_id
            },
            "profile": {
                "id": profile_id
            },
            "events": [{"type": "page-view", "options": {"save": True}}],
            "options": {
                "debugger": True
            }
        })
        result = response.json()

        assert endpoint.get(f'/profiles/refresh').status_code == 200
        assert endpoint.get(f'/sessions/refresh').status_code == 200

        if 'event' not in result:
            raise ValueError(
                'Could not perform test due to bad server configuration. No debugging allowed. '
                'Start Tracardi with TRACK_DEBUG=yes.')

        assert result['session']['saved'] == 0  # session is not saved because it did not change
        assert result['event']['saved'] == 1
        assert result['profile']['saved'] == 0  # profile is not saved because it exists

        # IMPORTANT: Everything is ok session and profile exists.

        new_profile_id = result['profile']['id']
        assert new_profile_id == profile_id

    finally:
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]
        assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
