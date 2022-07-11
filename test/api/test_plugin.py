import json
from uuid import uuid4

from tracardi.domain.flow_action_plugin import FlowActionPlugin
from tracardi.service.plugin.domain.register import Plugin, MetaData, Spec
from ..utils import Endpoint

endpoint = Endpoint()


def test_should_not_get_missing_plugin():
    missing_plugin_id = '1'
    assert endpoint.get(f'/flow/action/plugin/{missing_plugin_id}').status_code == 404


def test_should_get_existing_plugin():
    plugin_id = str(uuid4())
    payload = FlowActionPlugin(
        id=plugin_id,
        plugin=Plugin(
            metadata=MetaData(name="Test"),
            spec=Spec(
                className="test",
                module="test"
            )
        )
    )

    data = json.loads(json.dumps(payload.dict(), default=str))

    response = endpoint.post(f'/flow/action/plugin', data=data)
    assert response.status_code == 200
    result = response.json()
    plugin_id = result['ids'][0]

    assert endpoint.get(f'/flows/refresh').status_code == 200

    response = endpoint.get(f'/flow/action/plugin/{plugin_id}')
    assert response.status_code == 200
    result = response.json()
    record = FlowActionPlugin(**result)
    assert record.plugin.spec.module == payload.plugin.spec.module
    assert record.plugin.spec.className == payload.plugin.spec.className
    assert record.plugin.metadata.name == payload.plugin.metadata.name

    assert endpoint.get(f'/flow/action/plugin/{plugin_id}').status_code == 200
