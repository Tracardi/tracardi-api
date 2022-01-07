from uuid import uuid4
from ...api.test_event_source import create_event_source
from ...utils import Endpoint, create_session

endpoint = Endpoint()


async def test_session_exists_profile_exists():
    source_id = 'test-source'
    session_id = str(uuid4())
    profile_id = str(uuid4())

    await create_session(session_id, profile_id)

    response = endpoint.post('/profiles/import', data=[{"id": profile_id}])
    result = response.json()
    assert result["saved"] == 1
    assert response.status_code == 200

    # Assert session and profile exists

    assert endpoint.get(f'/session/{session_id}').status_code == 200
    assert endpoint.get(f'/profile/{profile_id}').status_code == 200
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

    assert result['debugging']['session']['saved'] == 0  # session is not saved because it did not change
    assert result['debugging']['events']['saved'] == 1
    assert result['debugging']['profile']['saved'] == 0  # profile is not saved because it exists

    # IMPORTANT: Everything is ok session and profile exists.

    new_profile_id = result['profile']['id']
    assert new_profile_id == profile_id

    assert endpoint.delete(f'/profile/{new_profile_id}').status_code == 200


