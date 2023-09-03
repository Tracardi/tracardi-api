import threading
from uuid import uuid4

from tracardi.process_engine.action.v1.flow.start.start_action import StartAction

from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.domain.flow import Flow
from tracardi.process_engine.action.v1.end_action import EndAction
from test.api.endpoints.test_event_source_endpoint import _create_event_source
from tracardi.service.wf.service.builders import action
from test.utils import Endpoint

endpoint = Endpoint()


def should_correctly_update_profile_on_concurrent_events():

    """
    Will fail is there is no redis
    """

    response = endpoint.get("/settings")
    assert response.status_code == 200
    result = response.json()
    sync_profile_tracks = [setting['value'] for setting in result if setting['label'] == 'SYNC_PROFILE_TRACKS'].pop()
    if sync_profile_tracks:

        source_id = str(uuid4())
        profile_id = str(uuid4())
        flow_id = str(uuid4())
        rule_id = str(uuid4())
        event_type = 'my-event'
        session_id = str(uuid4())

        try:
            # Delete profile
            assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]

            # Delete flows and rules
            # assert endpoint.delete(f'/rule/{rule_id_1}').status_code in [200, 404]
            assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]

            # Create resource
            assert _create_event_source(source_id, type='rest').status_code == 200
            assert endpoint.get('/event-sources/refresh').status_code == 200

            response = endpoint.post('/rule', data={
                "id": rule_id,
                "name": "Profile override rule-1",
                "event": {
                    "type": event_type
                },
                "flow": {
                    "id": flow_id,
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

            start = action(StartAction)
            increase_views = action(IncreaseViewsAction)
            end = action(EndAction)

            flow = Flow.build("Profile quick update - test", id=flow_id)
            flow += start('payload') >> increase_views('payload')
            flow += increase_views('payload') >> end('payload')

            assert endpoint.post('/flow/production', data=flow.model_dump()).status_code == 200
            assert endpoint.get('/flows/refresh').status_code == 200

            # Send event
            payload = {
                "source": {
                    "id": source_id
                },
                "session": {
                    "id": session_id
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
            assert endpoint.get('/profiles/refresh').status_code == 200
            assert endpoint.get('/sessions/refresh').status_code == 200

            print(result)

            # created profile_id
            profile_id = result['profile']['id']

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
                    "options": {}
                }],
                "options": {"debugger": True}
            }

            def post_request(payload, x):
                response = endpoint.post("/track", data=payload)
                assert response.status_code == 200
                print('response {} `{}`'.format(x, response.json()))

            threads = {}
            for x in range(0, 10):
                print("Thread", x)
                if x in [2, 3, 8]:
                    if x in [2, 8]:
                        pid = '282828282'
                    else:
                        pid = '3333333'

                    payload_new = {
                        "source": {
                            "id": source_id
                        },
                        "session": {
                            "id": pid
                        },
                        "profile": {
                            "id": pid
                        },
                        "events": [{
                            "type": event_type,
                            "properties": {
                                "a": 1,
                                "b": 2
                            },
                            "options": {}
                        }],
                        "options": {"debugger": True}
                    }
                    print("random", pid)
                    threads[x] = threading.Thread(target=post_request, args=(payload_new, x), daemon=True)
                    threads[x].start()
                else:
                    threads[x] = threading.Thread(target=post_request, args=(payload, x), daemon=True)
                    threads[x].start()

            for _, t in threads.items():
                t.join()

            assert endpoint.get('/profiles/refresh').status_code == 200
            assert endpoint.get('/sessions/refresh').status_code == 200

            response = endpoint.get(f'/profile/{profile_id}')
            assert response.status_code == 200
            result = response.json()
            print(result['stats']['views'])
            # == 11

        finally:
            pass
            # assert endpoint.get(f'/profiles/refresh').status_code == 200
            # assert endpoint.get(f'/sessions/refresh').status_code == 200
            # assert endpoint.get(f'/rules/refresh').status_code == 200
            # assert endpoint.get(f'/flows/refresh').status_code == 200
            # assert endpoint.get(f'/event-sources/refresh').status_code == 200
            #
            # assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]
            # assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]
            # assert endpoint.delete(f'/rule/{rule_id}').status_code in [200, 404]
            # assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404, 500]
            # assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
    else:
        print("Quick update of profile skipped. SYNC_PROFILE_TRACKS not configured.")


should_correctly_update_profile_on_concurrent_events()