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


async def _save(index, records):
    es = ElasticClient.instance()
    return await es.insert(index, records)


async def test_should_deduplicate_profile():
    month = datetime.now().month
    year = datetime.now().year

    prev_month = (datetime.now() - timedelta(days=32)).month

    curr_profile_index = resources.get_index('profile').get_write_index()
    prev_profile_index = curr_profile_index.replace(f"-{year}-{month}", f"-{year}-{prev_month}")

    curr_session_index = resources.get_index('session').get_write_index()
    prev_session_index = curr_session_index.replace(f"-{year}-{month}", f"-{year}-{prev_month}")

    curr_event_index = resources.get_index('event').get_write_index()
    prev_event_index = curr_event_index.replace(f"-{year}-{month}", f"-{year}-{prev_month}")

    profile_id = str(uuid4())
    source_id = str(uuid4())
    session_id = str(uuid4())
    event_id1 = str(uuid4())
    event_id2 = event_id1
    event_id3 = str(uuid4())

    print("profile_id", profile_id)
    print("session_id", session_id)

    # Create duplicates sessions

    session1 = await _save(curr_session_index, records=[{
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
        }
    }])

    session2 = await _save(prev_session_index, records=[{
        "_id": session_id,
        "id": session_id,
        "metadata": {
            "time": {
                "insert": f"{year}-{prev_month:02d}-03T14:35:15.838328",
                "visit": {
                    "current": f"{year}-{prev_month:02d}-03T14:35:15.838328",
                    "count": 1
                }
            }
        },
        "profile": {
            "id": profile_id
        },
        'context': {
            "value2": 2,
        }
    }])

    await storage.driver.session.refresh()

    assert session1.saved == 1
    assert session2.saved == 1
    assert session1.ids == session2.ids

    with pytest.raises(DuplicatedRecordException):
        await storage.driver.session.load(session_id)

    # Create duplicates profiles

    profile1 = await _save(curr_profile_index, records=[{
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

    profile2 = await _save(prev_profile_index, records=[{
        "_id": profile_id,
        "id": profile_id,
        "metadata": {
            "time": {
                "insert": f"{year}-{prev_month:02d}-03T14:35:15.838328",
                "visit": {
                    "current": f"{year}-{prev_month:02d}-03T14:35:15.838328",
                    "count": 2
                }
            }
        },
        'traits': {
            'private': {
                "value2": 2,
            },
            'public': {
                "value3": 3
            }}
    }])

    assert profile1.saved == 1
    assert profile2.saved == 1
    assert profile1.ids == profile2.ids

    await storage.driver.profile.refresh()

    with pytest.raises(DuplicatedRecordException):
        await storage.driver.profile.load_by_id(profile_id)

    event1 = await _save(curr_event_index, records=[{
        "_id": event_id1,
        "id": event_id1,
        "metadata": {
            "time": {
                "insert": f"{year}-{month:02d}-03T14:35:15.838328"
            }
        },
        "type": "event1",
        "source": {
            "id": source_id
        },
        "profile": {
            "id": profile_id
        },
        'properties': {
            'prop1': 1
        }
    }])

    event2 = await _save(prev_event_index, records=[{
        "_id": event_id2,
        "id": event_id2,
        "metadata": {
            "time": {
                "insert": f"{year}-{prev_month:02d}-03T14:35:15.838328"
            }
        },
        "type": "event2",
        "source": {
            "id": source_id
        },
        "profile": {
            "id": profile_id
        },
        'properties': {
            'prop1': 2
        }
    }])

    event3 = await _save(prev_event_index, records=[{
        "_id": event_id3,
        "id": event_id3,
        "metadata": {
            "time": {
                "insert": f"{year}-{prev_month:02d}-03T14:35:15.838328"
            }
        },
        "type": "event2",
        "source": {
            "id": source_id
        },
        "profile": {
            "id": profile_id
        },
        'properties': {
            'prop3': 3
        }
    }])

    assert event1.saved == 1
    assert event2.saved == 1
    assert event3.saved == 1
    await storage.driver.event.refresh()

    # Now track the duplicated profile

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
            "profile": {
                "id": profile_id
            },
            "events": [{"type": "page-view"}, {"type": "page-view", "options": {"save": False}}],
            "options": {
                "debugger": True
            }
        }

        response = endpoint.post("/track", data=payload)
        assert response.status_code == 200

        result = response.json()

        await storage.driver.profile.refresh()
        await storage.driver.session.refresh()
        await storage.driver.event.refresh()

        await storage.driver.profile.load_by_id(profile_id)
        await storage.driver.session.load(session_id)
        # await storage.driver.event.load(event_id2)
        # await storage.driver.event.load(event_id1)

    finally:
        assert endpoint.get(f'/sessions/refresh').status_code == 200
        assert endpoint.get(f'/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
