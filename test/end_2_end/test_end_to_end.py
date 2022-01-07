from time import sleep
from uuid import uuid4

from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.domain.flow import Flow
from tracardi.process_engine.action.v1.end_action import EndAction
from tracardi.process_engine.action.v1.start_action import StartAction
from tracardi.process_engine.action.v1.debug_payload_action import DebugPayloadAction
from ..api.test_event_source import create_event_source
from tracardi.service.wf.service.builders import action
from ..utils import Endpoint

endpoint = Endpoint()


def test_source_rule_and_flow():

    source_id = 'source-id'
    flow_id = "flow-id"
    rule_id = "rule-id"
    event_type = 'my-event'
    session_id = str(uuid4())

    # Remove flow

    assert endpoint.delete(f'/flow/{flow_id}').status_code == 200

    # Remove resource
    assert endpoint.delete(f'/event-source/{flow_id}').status_code in [200, 404]
    assert endpoint.get('/event-sources/refresh').status_code == 200

    # Create resource
    assert create_event_source(source_id, type='javascript', name="End2End test").status_code == 200
    assert endpoint.get('/event-sources/refresh').status_code == 200

    response = endpoint.post('/rule', data={
        "id": rule_id,
        "name": "End2End rule",
        "event": {
            "type": event_type
        },
        "flow": {
            "id": flow_id,
            "name": "End2End test"
        },
        "source": {
            "id": source_id,
            "name": "my source"
        },
        "enabled": True
    })
    print(response.json())
    assert response.status_code == 200
    assert endpoint.get('/rules/refresh').status_code == 200

    # Create flow

    debug = action(DebugPayloadAction, {
        "event": {
            "type": event_type,
        }
    })

    start = action(StartAction)
    increase_views = action(IncreaseViewsAction)
    end = action(EndAction)

    flow = Flow.build("End2End - flow", id=flow_id)
    flow += debug('event') >> start('payload')
    flow += start('payload') >> increase_views('payload')
    flow += increase_views('payload') >> end('payload')

    assert endpoint.post('/flow/production', data=flow.dict()).status_code == 200
    assert endpoint.get('/flows/refresh').status_code == 200

    segment_id = "segment-id"

    assert endpoint.post('/segment', data={
        "id": segment_id,
        "name": "Test segment",
        "condition": "profile@stats.views>0",
        "eventType": event_type
    }).status_code == 200
    assert endpoint.get('/segments/refresh').status_code == 200

    # Assert rule

    sleep(.5)
    response = endpoint.get(f'/rule/{rule_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['source']['id'] == source_id
    assert result['flow']['id'] == flow_id
    assert result['event']['type'] == event_type

    # Assert flow
    assert endpoint.get(f'/flow/production/{flow_id}').status_code == 200

    # Run /track

    payload = {
        "source": {
            "id": source_id
        },
        "session": {
            "id": session_id
        },
        "events": [{"type": event_type, "options": {"save": True}}],
        "options": {"profile": True}
    }

    response = endpoint.post("/track", data=payload)
    assert response.status_code == 200
    result = response.json()

    # Get created profile

    profile_id = result['profile']['id']

    # Wait for data to populate

    assert endpoint.get('/profiles/refresh').status_code == 200

    # Get created profile

    response = endpoint.get(f'/profile/{profile_id}')
    assert response.status_code == 200
    result = response.json()

    assert result['stats']['views'] == 1
    assert 'test-segment' in result['segments']

    # Remove flow
    assert endpoint.delete(f'/flow/{flow_id}').status_code == 200

