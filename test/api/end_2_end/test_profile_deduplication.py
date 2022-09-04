from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from test.api.endpoints.test_event_source_endpoint import _create_event_source
from test.utils import Endpoint
from tracardi.exceptions.exception import DuplicatedRecordException
from tracardi.service.storage.driver import storage
from tracardi.service.storage.elastic_client import ElasticClient
from tracardi.service.storage.index import resources

endpoint = Endpoint()
month = datetime.now().month
year = datetime.now().year
prev_month = (datetime.now() - timedelta(days=32)).month
curr_profile_index = resources.get_index('profile').get_write_index()
prev_profile_index = curr_profile_index.replace(f"-{year}-{month}", f"-{year}-{prev_month}")
curr_session_index = resources.get_index('session').get_write_index()
prev_session_index = curr_session_index.replace(f"-{year}-{month}", f"-{year}-{prev_month}")
curr_event_index = resources.get_index('event').get_write_index()
prev_event_index = curr_event_index.replace(f"-{year}-{month}", f"-{year}-{prev_month}")


async def _save(index, records):
    es = ElasticClient.instance()
    return await es.insert(index, records)


async def _create_track(source_id, session_index, session_id, profile_index, profile_id, event_index, event_props):
    session = await _save(session_index, records=[{
        "_id": session_id,
        "id": session_id,
        "metadata": {
            "time": {
                "insert": f"{year}-{month:02d}-03T14:35:15.838328",
                "visit": {
                    "current": f"{year}-{month:02d}-03T14:35:15.838328",
                    "count": 1
                }
            }
        },
        "profile": {
            "id": profile_id
        },
        'context': {
            "value1": 1,
            "orig_session": session_id
        }
    }])

    assert session.saved == 1
    session = session.ids[0]

    profile = await _save(profile_index, records=[{
        "_id": profile_id,
        "id": profile_id,
        "metadata": {
            "time": {
                "insert": f"{year}-{month:02d}-03T14:35:15.838328",
                "visit": {
                    "current": f"{year}-{month:02d}-03T14:35:15.838328",
                    "count": 1
                }
            }
        },
        'traits': {
            'private': {
                "value1": 1,
            },
            'public': {

            }}
    }])

    assert profile.saved == 1
    profile = profile.ids[0]

    events = []
    for prop in event_props:
        event_id = str(uuid4())
        event = await _save(event_index, records=[{
            "_id": event_id,
            "id": event_id,
            "metadata": {
                "time": {
                    "insert": f"{year}-{month:02d}-03T14:35:15.838328"
                },
                "status": "processed"
            },
            "type": "event1",
            "source": {
                "id": source_id
            },
            "session": {
                "id": session_id
            },
            "profile": {
                "id": profile_id
            },
            'properties': prop
        }])
        assert event.saved == 1
        events.append(event.ids[0])

    await storage.driver.session.refresh()
    await storage.driver.profile.refresh()
    await storage.driver.event.refresh()

    return profile, session, events


async def test_should_not_duplicate_events():
    profile_id = str(uuid4())
    session_id = str(uuid4())
    source_id = str(uuid4())

    assert _create_event_source(source_id, "rest").status_code == 200

    # Create event in previous month index
    profile, session, events = await _create_track(source_id, prev_session_index, session_id, prev_profile_index,
                                                   profile_id, prev_event_index,
                                                   event_props=[
                                                       {"prop1": 1}, {"prop2": 2}
                                                   ])
    assert profile == profile_id
    assert session == session_id

    # Now track with the same profile id.
    try:

        payload = {
            "source": {
                "id": source_id
            },
            "session": {
                "id": session_id
            },
            "profile": {
                "id": profile_id
            },
            "events": [{"type": "page-view1"}, {"type": "page-view2", "options": {"save": False}}],
            "options": {
                "debugger": True
            }
        }

        response = endpoint.post("/track", data=payload)
        assert response.status_code == 200

        await storage.driver.profile.refresh()
        await storage.driver.session.refresh()
        await storage.driver.event.refresh()

        await storage.driver.session.load_by_id(session_id)
        await storage.driver.profile.load_by_id(profile_id)

    finally:
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        # assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
        # assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]
        # for event_id in events:
        #     await storage.driver.event.delete_by_id(event_id)
        #
        # await storage.driver.profile.refresh()
        # await storage.driver.session.refresh()
        # await storage.driver.event.refresh()


async def test_should_deduplicate_profile():
    profile_id = str(uuid4())
    source_id = str(uuid4())
    session_id = str(uuid4())

    assert _create_event_source(source_id, "rest").status_code == 200

    profile1, session1, events1 = await _create_track(source_id, prev_session_index, session_id, prev_profile_index,
                                                      profile_id, prev_event_index,
                                                      event_props=[
                                                          {"prop1": 1}, {"prop2": 2}
                                                      ])

    profile2, session2, events2 = await _create_track(source_id, curr_session_index, session_id, curr_profile_index,
                                                      profile_id, curr_event_index,
                                                      event_props=[
                                                          {"prop3": 3}, {"prop4": 4}
                                                      ])

    assert profile1 == profile2
    assert session1 == session2

    with pytest.raises(DuplicatedRecordException):
        await storage.driver.session.load_by_id(session_id)

    with pytest.raises(DuplicatedRecordException):
        await storage.driver.profile.load_by_id(profile_id)

    # Now track the duplicated profile. It should de duplicate the session and profile

    try:

        payload = {
            "source": {
                "id": source_id
            },
            "session": {
                "id": session_id
            },
            "profile": {
                "id": profile_id
            },
            "events": [{"type": "page-view1"}, {"type": "page-view2", "options": {"save": False}}],
            "options": {
                "debugger": True
            }
        }

        response = endpoint.post("/track", data=payload)
        assert response.status_code == 200

        await storage.driver.profile.refresh()
        await storage.driver.session.refresh()
        await storage.driver.event.refresh()

        await storage.driver.profile.load_by_id(profile_id)
        await storage.driver.session.load_by_id(session_id)

        for event_id in events1 + events2:
            event = await storage.driver.event.load(event_id)
            assert event['id'] == event_id

    finally:
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
        assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]
        for event_id in events1 + events2:
            await storage.driver.event.delete_by_id(event_id)

        await storage.driver.profile.refresh()
        await storage.driver.session.refresh()
        await storage.driver.event.refresh()
