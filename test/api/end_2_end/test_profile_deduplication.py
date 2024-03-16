from tracardi.context import ServerContext, Context
from test.utils import get_test_tenant
from tracardi.service.profile_deduplicator import deduplicate_profile
from tracardi.service.storage.elastic.interface.event import refresh_event_db, delete_event_from_db, load_event_from_db
from tracardi.service.storage.elastic.interface.session import refresh_session_db, load_session_from_db
from tracardi.service.tracking.storage.profile_storage import load_profile
from tracardi.service.tracking.storage.session_storage import load_session

with ServerContext(Context(production=False, tenant=get_test_tenant())):

    from datetime import datetime, timedelta
    from uuid import uuid4
    from test.utils import Endpoint
    import pytest

    from test.api.endpoints.test_event_source_endpoint import _create_event_source
    from tracardi.domain.profile import Profile
    from tracardi.exceptions.exception import DuplicatedRecordException
    from tracardi.service.storage.driver.elastic import profile as profile_db
    from tracardi.service.storage.elastic_client import ElasticClient
    from tracardi.service.storage.factory import storage_manager
    from tracardi.service.storage.index import Resource

    endpoint = Endpoint()
    month = datetime.now().month
    year = datetime.now().year
    prev_month = (datetime.now() - timedelta(days=32)).month
    curr_profile_index = Resource().get_index_constant('profile').get_write_index()
    prev_profile_index = curr_profile_index.replace(f"-{year}-{month}", f"-{year}-{prev_month}")
    curr_session_index = Resource().get_index_constant('session').get_write_index()
    prev_session_index = curr_session_index.replace(f"-{year}-{month}", f"-{year}-{prev_month}")
    curr_event_index = Resource().get_index_constant('event').get_write_index()
    prev_event_index = curr_event_index.replace(f"-{year}-{month}", f"-{year}-{prev_month}")

    async def _save(index, records):
        es = ElasticClient.instance()
        return await es.insert(index, records)


    async def _create_track(source_id, session_index, session_id, profile_index, profile_id, event_index, event_props):
        session = await _save(session_index, records=[{
            '_id': session_id,
            "id": session_id,
            "metadata": {
                "time": {
                    "insert": f"{year}-{month:02d}-03T14:35:15.838328",
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
            '_id': profile_id,
            "id": profile_id,
            "ids": [profile_id],
            "metadata": {
                "time": {
                    "insert": f"{year}-{month:02d}-03T14:35:15.838328",
                    "visit": {
                        "current": f"{year}-{month:02d}-03T14:35:15.838328",
                        "count": 1
                    }
                }
            },
            'active': True,
            'traits': {
                'private': {
                    "value": str(uuid4()),
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
                '_id': event_id,
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

        await refresh_session_db()
        await profile_db.refresh()
        await refresh_event_db()

        return profile, session, events


    async def test_should_not_duplicate_events():
        with ServerContext(Context(production=False, tenant=get_test_tenant())):
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

                await profile_db.refresh()
                await refresh_session_db()
                await refresh_event_db()

                await load_session(session_id)
                await load_profile(profile_id)

            finally:
                assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
                assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
                assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]
                for event_id in events:
                    await delete_event_from_db(event_id)

                await profile_db.refresh()
                await refresh_session_db()
                await refresh_event_db()


    async def test_should_deduplicate_profile():
        with ServerContext(Context(production=False, tenant=get_test_tenant())):
            profile_id = str(uuid4())
            source_id = str(uuid4())
            session_id = str(uuid4())

            assert _create_event_source(source_id, "rest").status_code == 200

            profile1, session1, events1 = await _create_track(source_id,
                                                              prev_session_index,
                                                              session_id,
                                                              prev_profile_index,
                                                              profile_id,
                                                              prev_event_index,
                                                              event_props=[
                                                                  {"prop1": 1}, {"prop2": 2}
                                                              ])

            profile2, session2, events2 = await _create_track(source_id,
                                                              curr_session_index,
                                                              session_id,
                                                              curr_profile_index,
                                                              profile_id,
                                                              curr_event_index,
                                                              event_props=[
                                                                  {"prop3": 3}, {"prop4": 4}
                                                              ])

            assert profile1 == profile2
            assert session1 == session2

            with pytest.raises(DuplicatedRecordException):
                # Trows error duplicate record
                await load_profile(profile_id)

            # When record is duplicated also session gets duplicated
            with pytest.raises(DuplicatedRecordException):
                await load_session_from_db(session_id)

            profile_records = await storage_manager('profile').load_by("ids", profile_id, limit=10)

            assert profile_records.total == 2
            profiles = profile_records.to_domain_objects(Profile)

            indices = [profile.get_meta_data().index for profile in profiles if profile.has_meta_data()]

            # Assert that profile is in 2 indices
            assert len(set(indices)) == 2

            profile = await deduplicate_profile(profile1)
            await profile_db.refresh()

            record = await load_profile(profile.id)
            assert record is not None
            assert record.get_meta_data() is not None


    async def test_should_deduplicate_profile_on_server():
        with ServerContext(Context(production=False, tenant=get_test_tenant())):
            profile_id = str(uuid4())
            source_id = str(uuid4())
            session_id = str(uuid4())

            assert _create_event_source(source_id, "rest").status_code == 200

            profile1, session1, events1 = await _create_track(source_id,
                                                              prev_session_index,
                                                              session_id,
                                                              prev_profile_index,
                                                              profile_id,
                                                              prev_event_index,
                                                              event_props=[
                                                                  {"prop1": 1}, {"prop2": 2}
                                                              ])

            profile2, session2, events2 = await _create_track(source_id,
                                                              curr_session_index,
                                                              session_id,
                                                              curr_profile_index,
                                                              profile_id,
                                                              curr_event_index,
                                                              event_props=[
                                                                  {"prop3": 3}, {"prop4": 4}
                                                              ])

            assert profile1 == profile2
            assert session1 == session2

            with pytest.raises(DuplicatedRecordException):
                await load_profile(profile_id)

            # When record is duplicated also session gets duplicated
            with pytest.raises(DuplicatedRecordException):
                await load_session_from_db(session_id)

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
                    "events": [
                        {"type": "dedup-1"},
                        {"type": "dedup-2", "options": {"save": False}},
                        {"type": "dedup-3"}
                    ],
                    "options": {
                        "debugger": True
                    }
                }

                response = endpoint.post("/track", data=payload)

                assert response.status_code == 200

                await profile_db.refresh()
                await refresh_session_db()
                await refresh_event_db()

                # Should be no errors
                await load_profile(profile_id)
                await load_session(session_id)

                for event_id in events1 + events2:
                    event = await load_event_from_db(event_id)
                    assert event['id'] == event_id

            finally:
                assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
                assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
                assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]
                for event_id in events1 + events2:
                    await delete_event_from_db(event_id)

                await profile_db.refresh()
                await refresh_session_db()
                await refresh_event_db()

