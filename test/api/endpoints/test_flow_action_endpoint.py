import json
from typing import Tuple
from uuid import uuid4

from requests import Response

from tracardi.domain.flow_action_plugin import FlowActionPlugin
from tracardi.domain.metadata import Metadata
from tracardi.domain.time import Time
from tracardi.service.plugin.domain.register import Plugin, Spec, MetaData
from test.utils import Endpoint

endpoint = Endpoint()


def _create_plugin() -> Tuple[Response, str, FlowActionPlugin]:
    plugin_id = str(uuid4())
    data = FlowActionPlugin(
        id=plugin_id,
        metadata=Metadata(time=Time()),
        plugin=Plugin(
            start=False,
            debug=False,
            spec=Spec(className="class_name", module="module"),
            metadata=MetaData(name="test")
        )
    )
    response = endpoint.post("/flow/action/plugin", data=json.loads(data.model_dump_json()))
    assert response.status_code == 200
    return response, response.json()['ids'][0], data


def test_should_return_404_on_missing_plugin_data():
    plugin_id = "none"
    response = endpoint.get(f'/flow/action/plugin/{plugin_id}')
    assert response.status_code == 404


def test_should_return_406_on_missing_plugin_when_hiding():
    plugin_id = "none"
    state = 'yes'
    response = endpoint.get(f'/flow/action/plugin/{plugin_id}/hide/{state}')
    assert response.status_code == 406


def test_should_return_406_on_missing_plugin_when_enabling():
    plugin_id = "none"
    state = 'yes'
    response = endpoint.get(f'/flow/action/plugin/{plugin_id}/enable/{state}')
    assert response.status_code == 406


def test_should_return_406_on_missing_plugin_when_icon_change():
    plugin_id = "none"
    icon = 'globe'
    response = endpoint.put(f"/flow/action/plugin/{plugin_id}/icon/{icon}")
    assert response.status_code == 406


def test_should_return_406_on_missing_plugin_when_name_change():
    plugin_id = "none"
    name = 'globe'
    response = endpoint.put(f"/flow/action/plugin/{plugin_id}/name/{name}")
    assert response.status_code == 406


def test_should_return_404_on_missing_plugin_when_deleting():
    plugin_id = "none"
    response = endpoint.delete(f"/flow/action/plugin/{plugin_id}")
    assert response.status_code == 404


def test_should_create_plugin():
    plugin_id = None
    try:
        response, plugin_id, _ = _create_plugin()
        result = response.json()
        assert result['saved'] == 1
    finally:
        if plugin_id:
            assert endpoint.delete(f'/flow/action/plugin/{plugin_id}').status_code in [200, 404]


def test_should_return_plugin():
    plugin_id = None
    try:
        response, plugin_id, _ = _create_plugin()
        response = endpoint.get(f'/flow/action/plugin/{plugin_id}')
        assert response.status_code == 200
        result = response.json()
        assert result['id'] == plugin_id
        assert result['plugin']['spec']['className'] == 'class_name'
        assert result['plugin']['spec']['module'] == 'module'
    finally:
        if plugin_id:
            assert endpoint.delete(f'/flow/action/plugin/{plugin_id}').status_code in [200, 404]


def test_should_return_plugins_list():
    response = endpoint.get('/flow/action/plugins')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['total'], int)
    assert 'grouped' in result


def test_should_return_plugins_list_when_queried():
    response = endpoint.get('/flow/action/plugins?query=hash%20data')
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result['total'], int)
    assert 'grouped' in result
    assert 'Operations' in result['grouped']
    # Assumes that hash data plugin is in group operations and is only one.
    assert len(result['grouped']['Operations']) == 1
