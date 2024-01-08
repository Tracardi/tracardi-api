from uuid import uuid4

from tracardi.process_engine.action.v1.flow.start.start_action import StartAction

from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.domain.flow import Flow
from tracardi.process_engine.action.v1.end_action import EndAction
from tracardi.process_engine.action.v1.increase_visits_action import IncreaseVisitsAction
from tracardi.process_engine.action.v1.traits.append_trait_action import AppendTraitAction
from tracardi.process_engine.action.v1.traits.copy_trait_action import CopyTraitAction
from test.api.endpoints.test_event_source_endpoint import _create_event_source
from tracardi.service.wf.service.builders import action
from test.utils import Endpoint

endpoint = Endpoint()


def test_source_rule_and_flow():
    source_id = str(uuid4())
    profile_id = str(uuid4())
    flow_id_1 = str(uuid4())
    rule_id_1 = str(uuid4())
    flow_id_2 = str(uuid4())
    rule_id_2 = str(uuid4())
    event_type = 'my-event'
    session_id = str(uuid4())

    try:
        # Create resource
        assert _create_event_source(source_id, type='rest').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        response = endpoint.post('/rule', data={
            "id": rule_id_1,
            "name": "Profile override rule-1",
            "event_type": {
                "id": event_type,
                "name": event_type
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

        response = endpoint.post('/rule', data={
            "id": rule_id_2,
            "name": "Profile override rule-1",
            "event_type": {
                "id": event_type,
                "name": event_type
            },
            "flow": {
                "id": flow_id_2,
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
        copy_trait1 = action(CopyTraitAction, init={
            "traits": {
                "set": {
                    "profile@traits.a": "event@properties.a"
                }
            }
        })
        append_trait = action(AppendTraitAction, init={
            "append": {
                "profile@traits.b": "event@properties.a"
            }
        })
        increase_views = action(IncreaseViewsAction)
        increase_visits = action(IncreaseVisitsAction)
        end = action(EndAction)

        flow = Flow.build("Profile override flow test - 1", id=flow_id_1)
        flow += start('payload') >> increase_views('payload')
        flow += start('payload') >> copy_trait1('payload')
        flow += copy_trait1('payload') >> end('payload')
        flow += start('payload') >> append_trait('payload')
        flow += append_trait('payload') >> end('payload')
        flow += increase_views('payload') >> end('payload')

        assert endpoint.post('/flow/production', data=flow.model_dump()).status_code == 200

        copy_trait2 = action(CopyTraitAction, init={
            "traits": {
                "set": {
                    "profile@traits.a": "event@properties.b"
                }
            }
        })
        append_trait = action(AppendTraitAction, init={
            "append": {
                "profile@traits.b": "event@properties.b"
            }
        })
        flow = Flow.build("Profile override flow test - 2", id=flow_id_2)
        flow += start('payload') >> increase_views('payload')
        flow += start('payload') >> increase_visits('payload')
        flow += start('payload') >> copy_trait2('payload')
        flow += start('payload') >> append_trait('payload')
        flow += append_trait('payload') >> end('payload')
        flow += copy_trait2('payload') >> end('payload')
        flow += increase_views('payload') >> end('payload')
        flow += increase_visits('payload') >> end('payload')

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
        assert endpoint.get('/profiles/refresh').status_code == 200

        # New profile id is returned
        profile_id = result['profile']['id']

        response = endpoint.get(f'/profile/{profile_id}')
        assert response.status_code == 200
        result = response.json()

        assert result['stats']['visits'] == 1
        assert result['stats']['views'] == 2
        assert result['traits']['a'] in [1, 2]
        assert len(set(result['traits']['b']).difference({1, 2})) == 0

        profile_id = result['id']

    finally:
        assert endpoint.get('/profiles/refresh').status_code == 200
        assert endpoint.get('/sessions/refresh').status_code == 200
        assert endpoint.get('/rules/refresh').status_code == 200
        assert endpoint.get('/flows/refresh').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]
        assert endpoint.delete(f'/flow/{flow_id_1}').status_code in [200, 404]
        assert endpoint.delete(f'/flow/{flow_id_2}').status_code in [200, 404]
        assert endpoint.delete(f'/rule/{rule_id_1}').status_code in [200, 404]
        assert endpoint.delete(f'/rule/{rule_id_2}').status_code in [200, 404]
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
