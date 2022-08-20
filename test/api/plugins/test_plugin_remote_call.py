from uuid import uuid4

from tracardi.domain.resource import ResourceCredentials
from tracardi.service.wf.domain.node import Node
from test.api.endpoints.test_resource import create_resource
from test.utils import Endpoint
from tracardi.process_engine.action.v1.connectors.api_call.plugin import RemoteCallAction
from tracardi.service.plugin.service.plugin_runner import run_plugin

endpoint = Endpoint()


def test_remote_call_ok():
    resource_id = str(uuid4())
    try:

        credentials = {
            "url": "http://localhost:8686/"
        }

        credentials = ResourceCredentials(
            test=credentials, production=credentials
        )

        create_resource(resource_id, "api", config=credentials.dict())

        response = endpoint.get(f'/resource/{resource_id}')
        assert response.status_code == 200
        result = response.json()
        assert result is not None
        assert result['credentials']['test'] == credentials.test

        init = {
            "source": {"id": resource_id, "name": "TEST API Call"},
            "endpoint": "/healthcheck",
            "method": "post",
            "timeout": 1,
            "headers": [
                ("Authorization", endpoint.token),
            ],
            "body": {"type": "plain/text", "content": "test body"}
        }
        payload = {}
        response = run_plugin(RemoteCallAction, init, payload, node=Node(id="1", className="classname", module="module"))
        result = response.output

        assert result.port == 'response'
        assert result.value['status'] == 200
        assert result.value['content'] == init['body']['content']
    finally:
        assert endpoint.delete(f'/resource/{resource_id}').status_code in [200, 404]


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
        "body": {"type": "plain/text", "content": "test body"}
    }

    payload = {}

    try:
        run_plugin(RemoteCallAction, init, payload)
    except ValueError:
        assert True
