import asyncio
from time import time
from uuid import uuid4
import concurrent.futures

from tracardi.process_engine.action.v1.flow.start.start_action import StartAction

from tracardi.domain.settings import SystemSettings

from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.domain.flow import Flow
from tracardi.process_engine.action.v1.end_action import EndAction
from tracardi.process_engine.action.v1.debug_payload_action import DebugPayloadAction
from ..api.test_source import create_event_source
from tracardi.service.wf.service.builders import action
from ..utils import Endpoint

endpoint = Endpoint()


def test_source_rule_and_flow():

    source_id = 'source-id'
    flow_id_1 = "flow-id-1"
    rule_id_1 = "rule-id-1"
    event_type = 'my-event'
    session_id = str(uuid4())
    profile_id = None

    settings = endpoint.get('/setting/SYNC_PROFILE_TRACKS')
    assert settings.status_code == 200
    settings = SystemSettings(**settings.json())

    if settings.value is True:
        try:

            # Create resource
            assert create_event_source(source_id, type='javascript', name="End2End test").status_code == 200
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
            assert endpoint.get('/rules/refresh').status_code == 200

            # Create flows

            debug = action(DebugPayloadAction, init={"event": {"type": event_type}})
            start = action(StartAction)
            increase_views = action(IncreaseViewsAction)
            end = action(EndAction)

            flow = Flow.build("Profile quick update - test", id=flow_id_1)
            flow += debug('event') >> start('payload')
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
                    "options": {"profile": True}
                }

                response = endpoint.post("/track", data=payload)
                assert response.status_code == 200
                result = response.json()
                print(f"{result['profile']['id']}, {result['profile']['stats']['views']}")
                return result

            # create profile_id
            result = call("none")

            assert endpoint.get('/profiles/refresh').status_code == 200
            assert endpoint.get('/sessions/refresh').status_code == 200

            profile_id = result['profile']['id']

            loop = asyncio.get_event_loop()
            executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=100,
            )
            start = time()
            coros = []
            for x in range(0, 20):
                coros.append(loop.run_in_executor(executor, call, profile_id))

            loop.run_until_complete(asyncio.gather(*coros))

            result = call(profile_id)

            assert endpoint.get('/profiles/refresh').status_code == 200
            assert endpoint.get('/sessions/refresh').status_code == 200

            assert result['profile']['stats']['views'] == 22
            print(time() - start)

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
