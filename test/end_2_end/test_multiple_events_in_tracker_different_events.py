from uuid import uuid4

from tracardi.process_engine.action.v1.flow.start.start_action import StartAction

from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.domain.flow import Flow
from tracardi.process_engine.action.v1.end_action import EndAction
from tracardi.process_engine.action.v1.debug_payload_action import DebugPayloadAction
from ..api.test_source import create_event_source
from tracardi.service.wf.service.builders import action
from ..utils import Endpoint

endpoint = Endpoint()


def test_source_rule_and_flow():
    source_id = str(uuid4())
    profile_id = str(uuid4())
    flow_id = str(uuid4())
    rule_id = str(uuid4())
    event_type = 'my-event'
    session_id = str(uuid4())

    try:
        # Delete profile
        assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]
        assert endpoint.delete(f'/rule/{rule_id}').status_code in [200, 404]
        assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]

        # Create resource
        assert create_event_source(source_id, type='rest', name="End2End test").status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        response = endpoint.post('/rule', data={
            "id": rule_id,
            "name": "Multiple events in one track",
            "event": {
                "type": event_type
            },
            "flow": {
                "id": flow_id,
                "name": "Multiple events in one track"
            },
            "source": {
                "id": source_id,
                "name": "my test source"
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

        flow = Flow.build("Profile quick update - test", id=flow_id)
        flow += debug('event') >> start('payload')
        flow += start('payload') >> increase_views('payload')
        flow += increase_views('payload') >> end('payload')

        assert endpoint.post('/flow/production', data=flow.dict()).status_code == 200
        assert endpoint.get('/flows/refresh').status_code == 200

        # Send event
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
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": str(uuid4())},
                    {"type": event_type},
                ],
                "options": {"profile": True}
            }

        response = endpoint.post("/track", data=payload)

        assert endpoint.get(f'/profiles/refresh').status_code == 200
        assert endpoint.get(f'/sessions/refresh').status_code == 200

        assert response.status_code == 200
        result = response.json()
        profile_id = result['profile']['id']
        assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]

        assert result['profile']['stats']['views'] == 1

    finally:
        # Delete
        assert endpoint.get(f'/profiles/refresh').status_code == 200
        assert endpoint.get(f'/sessions/refresh').status_code == 200
        assert endpoint.get(f'/rules/refresh').status_code == 200
        assert endpoint.get(f'/flows/refresh').status_code == 200
        assert endpoint.get(f'/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]
        assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]
        assert endpoint.delete(f'/rule/{rule_id}').status_code in [200, 404]
        assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]

