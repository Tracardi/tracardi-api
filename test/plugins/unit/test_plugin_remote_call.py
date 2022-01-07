import pytest

from ...utils import Endpoint
from tracardi.process_engine.action.v1.connectors.api_call.plugin import RemoteCallAction
from tracardi.service.plugin.service.plugin_runner import run_plugin


def test_remote_call_ok():
    endpoint = Endpoint()
    init = {
        "url": "http://localhost:8686/healthcheck",
        "method": "post",
        "timeout": 1,
        "headers": [
            ("Authorization", endpoint.token),
            ("x-AAA", "test")
        ],
        "body": {"type":"plain/text", "content": "test body"}
    }
    payload = {}
    results = run_plugin(RemoteCallAction, init, payload)
    response, error = results.output

    assert response.value['status'] == 200
    assert response.value['content'] == init['body']['content']


def test_remote_call_invalid_cookie():
    init = {
        "url": "http://localhost:8686/healthcheck",
        "method": "post",
        "timeout": 1,
        "headers": [
            ("x-AAA", "test")
        ],
        "cookies": {"a": [
            "a"
        ]},
        "body":  {"type":"plain/text", "content": "test body"}
    }

    payload = {}

    try:
        run_plugin(RemoteCallAction, init, payload)
    except ValueError:
        assert True
