from uuid import uuid4
from ...api.test_event_source import create_event_source
from ...utils import Endpoint, create_session, get_session, get_profile

endpoint = Endpoint()


def test_session_exists_profile_not_exists():

    source_id = str(uuid4())
    session_id = str(uuid4())
    profile_id = str(uuid4())

    try:
        assert create_event_source(source_id, 'javascript').status_code == 200

        create_session(session_id)

        assert get_session(session_id).status_code == 200
        assert get_profile(profile_id).status_code == 404  # No profile

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
            "events": [{"type": "page-view", "options": {"save": False}}],
            "options": {
                "debugger": True
            }
        })
        result = response.json()
        assert result['debugging']['session']['saved'] == 1  # session is saved again because
        # new profile is created and session has to be updated.
        assert result['debugging']['events']['saved'] == 0
        assert result['debugging']['profile']['saved'] == 1

        assert endpoint.get(f'/profiles/refresh').status_code == 200
        assert endpoint.get(f'/sessions/refresh').status_code == 200

        # IMPORTANT: when there is no profile in storage it must be recreated.
        # this is very important security feature.

        new_profile_id = result['profile']['id']

        assert new_profile_id != profile_id
        assert endpoint.delete(f'/profile/{new_profile_id}').status_code == 200

    finally:
        assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]

