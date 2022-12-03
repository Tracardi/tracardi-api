from uuid import uuid4

from tracardi.process_engine.action.v1.flow.start.start_action import StartAction
from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.domain.flow import Flow
from tracardi.process_engine.action.v1.end_action import EndAction
from test.api.endpoints.test_event_source_endpoint import _create_event_source
from tracardi.service.wf.service.builders import action
from test.utils import Endpoint

endpoint = Endpoint()


def test_source_rule_and_flow():
    source_id = str(uuid4())
    flow_id = str(uuid4())
    rule_id = str(uuid4())
    event_type = 'my-event'
    session_id = str(uuid4())
    segment_id = str(uuid4())

    try:

        # Remove flow

        assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]
        assert endpoint.delete(f'/rule/{rule_id}').status_code in [200, 404]
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        response = endpoint.delete(f'/session/{session_id}')
        if response.status_code == 200:
            assert endpoint.get('/sessions/refresh').status_code == 200

        # Refresh
        assert endpoint.get('/event-sources/refresh').status_code == 200
        assert endpoint.get('/rules/refresh').status_code == 200
        assert endpoint.get('/flows/refresh').status_code == 200

        # Create resource
        assert _create_event_source(source_id, type='rest').status_code == 200
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

        assert response.status_code == 200
        assert endpoint.get('/rules/refresh').status_code == 200

        # Create flow

        start = action(StartAction)
        increase_views = action(IncreaseViewsAction)
        end = action(EndAction)

        flow = Flow.build("End2End flow", id=flow_id)
        flow += start('payload') >> increase_views('payload')
        flow += increase_views('payload') >> end('payload')

        flow.arrange_nodes()

        for edge in flow.flowGraph.edges:
            assert flow.flowGraph.get_node_by_id(edge.source).position.y < \
                   flow.flowGraph.get_node_by_id(edge.target).position.y - 100  # Y coordinate increases to the bottom

        assert endpoint.post('/flow/production', data=flow.dict()).status_code == 200
        assert endpoint.get('/flows/refresh').status_code == 200

        result = endpoint.post('/segment', data={
            "id": segment_id,
            "name": "Test segment",
            "condition": "profile@stats.views>0",
            "eventType": [event_type]
        })
        assert result.status_code == 200
        assert endpoint.get('/segments/refresh').status_code == 200

        # Assert rule

        # sleep(.5)
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
            "options": {}
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

        # Delete profile

        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200

    finally:
        assert endpoint.get(f'/profiles/refresh').status_code == 200
        assert endpoint.get(f'/sessions/refresh').status_code == 200
        assert endpoint.get(f'/rules/refresh').status_code == 200
        assert endpoint.get(f'/flows/refresh').status_code == 200
        assert endpoint.get(f'/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]
        assert endpoint.delete(f'/rule/{rule_id}').status_code in [200, 404]
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        assert endpoint.delete(f'/session/{session_id}').status_code in [200, 404]
        assert endpoint.delete(f'/segment/{segment_id}').status_code in [200, 404]
