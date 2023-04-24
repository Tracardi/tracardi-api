from uuid import uuid4

from tracardi.process_engine.action.v1.flow.start.start_action import StartAction

from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.domain.flow import Flow
from tracardi.process_engine.action.v1.end_action import EndAction
from test.api.endpoints.test_event_source_endpoint import _create_event_source
from tracardi.service.wf.service.builders import action
from test.utils import Endpoint

endpoint = Endpoint()


def test_should_count_multiple_page_views_from_one_api_call():

    """
    Makes one api call with 30 page-views. Creates Workflow with view increase.
    Check if stats.views == 30.
    """

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
            "name": "Multiple events in one track",
            "event_type": {
                "id": event_type,
                "name": event_type
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

        start = action(StartAction)
        increase_views = action(IncreaseViewsAction)
        end = action(EndAction)

        flow = Flow.build("Profile quick update - test", id=flow_id)
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
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                    {"type": event_type},
                ],
                "options": {}
            }

        response = endpoint.post("/track", data=payload)

        assert endpoint.get(f'/profiles/refresh').status_code == 200
        assert endpoint.get(f'/sessions/refresh').status_code == 200

        assert response.status_code == 200
        result = response.json()
        profile_id = result['profile']['id']

        response = endpoint.get(f'/profile/{profile_id}')
        assert response.status_code == 200
        result = response.json()
        assert result['stats']['views'] == 30

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
        assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]

