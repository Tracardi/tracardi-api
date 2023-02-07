import asyncio
from time import time
from uuid import uuid4
import concurrent.futures

from tracardi.process_engine.action.v1.flow.start.start_action import StartAction

from tracardi.domain.settings import SystemSettings

from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.domain.flow import Flow
from tracardi.process_engine.action.v1.end_action import EndAction
from test.api.endpoints.test_event_source_endpoint import _create_event_source
from tracardi.service.wf.service.builders import action
from test.utils import Endpoint

endpoint = Endpoint()


def test_source_rule_and_flow():

    source_id = 'source-id'
    flow_id_1 = "flow-id-1"
    rule_id_1 = "rule-id-1"
    event_type = 'my-event'
    session_id = str(uuid4())
    profile_id = None

    max_threads = endpoint.get('/setting/SYNC_PROFILE_TRACKS_MAX_REPEATS')
    assert max_threads.status_code == 200
    max_threads = SystemSettings(**max_threads.json())

    max_concurrent_threads = max_threads.value

    try:

        # Create resource
        assert _create_event_source(source_id, type='rest').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        response = endpoint.post('/rule', data={
            "id": rule_id_1,
            "name": "Profile override rule-1",
            "event": {
                "type": event_type
            },
            "flow": {
                "id": flow_id_1,
                "name": "Profile override flow test"
            },
            "source": {
                "id": source_id,
                "name": "my source"
            },
            "enabled": True
        })

        assert response.status_code == 200
        assert endpoint.get('/rules/flash').status_code == 200
        assert endpoint.get('/rules/refresh').status_code == 200

        # Create flows

        start = action(StartAction)
        increase_views = action(IncreaseViewsAction)
        end = action(EndAction)

        flow = Flow.build("Profile quick update - test", id=flow_id_1)
        flow += start('payload') >> increase_views('payload')
        flow += increase_views('payload') >> end('payload')

        assert endpoint.post('/flow/production', data=flow.dict()).status_code == 200
        assert endpoint.get('/flows/refresh').status_code == 200

        # Send event

        def call(profile_id):
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
                "events": [{
                    "type": event_type,
                    "properties": {
                        "a": 1,
                        "b": 2
                    },
                    "options": {"save": True}
                }],
                "options": {}
            }

            response = endpoint.post("/track", data=payload)
            assert response.status_code == 200
            result = response.json()

            assert endpoint.get(f'/profiles/refresh').status_code == 200

            return result

        # create profile_id
        result = call("none")

        assert endpoint.get('/profiles/flash').status_code == 200
        assert endpoint.get('/sessions/flash').status_code == 200

        assert endpoint.get('/profiles/refresh').status_code == 200
        assert endpoint.get('/sessions/refresh').status_code == 200

        profile_id = result['profile']['id']

        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=100,
        )
        start = time()
        coros = []
        for x in range(0, max_concurrent_threads):
            coros.append(loop.run_in_executor(executor, call, profile_id))

        loop.run_until_complete(asyncio.gather(*coros))

        result = call(profile_id)

        assert endpoint.get('/profiles/flash').status_code == 200
        assert endpoint.get('/sessions/flash').status_code == 200

        assert endpoint.get('/profiles/refresh').status_code == 200
        assert endpoint.get('/sessions/refresh').status_code == 200

        # Read profile
        profile_id = result['profile']['id']
        response = endpoint.get(f'/profile/{profile_id}')
        assert response.status_code == 200
        result = response.json()

        assert result['stats']['views'] == max_concurrent_threads + 2

    finally:
        assert endpoint.get(f'/profiles/refresh').status_code == 200
        assert endpoint.get(f'/sessions/refresh').status_code == 200
        assert endpoint.get(f'/rules/refresh').status_code == 200
        assert endpoint.get(f'/flows/refresh').status_code == 200
        assert endpoint.get(f'/event-sources/refresh').status_code == 200

        if profile_id is not None:
            # Delete profile
            assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]

        # Delete flows and rules
        assert endpoint.delete(f'/flow/{flow_id_1}').status_code in [200, 404]
        assert endpoint.delete(f'/rule/{rule_id_1}').status_code in [200, 404]
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
