from uuid import uuid4
from ...api.test_source import create_event_source
from ...utils import Endpoint, get_profile, get_session

endpoint = Endpoint()


def test_session_not_exists_profile_not_exists():
    source_id = str(uuid4())
    session_id = str(uuid4())
    profile_id = str(uuid4())

    try:
        assert get_session(session_id).status_code == 404  # No session
        assert get_profile(profile_id).status_code == 404  # No profile
        assert create_event_source(source_id, 'javascript').status_code == 200

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

        if 'debugging' not in result:
            raise ValueError(
                'Could not perform test due to bad server configuration. No debugging allowed. '
                'Start Tracardi wiht TRACK_DEBUG=yes.')

        assert result['debugging']['session']['saved'] == 1
        assert result['debugging']['events']['saved'] == 1
        assert result['debugging']['profile']['saved'] == 1

        # IMPORTANT: when there is no profile in storage it must be recreated.
        # this is very important security feature.

        new_profile_id = result['profile']['id']
        assert new_profile_id != profile_id

        assert result['debugging']['session']['ids'][0] == session_id

        assert endpoint.get(f'/profiles/refresh').status_code == 200
        assert endpoint.get(f'/sessions/refresh').status_code == 200

        assert endpoint.get(f'/session/{session_id}').status_code == 200  # Session exists
        assert endpoint.get(f'/profile/{new_profile_id}').status_code == 200  # Profile exists
        assert endpoint.delete(f'/profile/{new_profile_id}').status_code == 200

    finally:
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
        assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]
