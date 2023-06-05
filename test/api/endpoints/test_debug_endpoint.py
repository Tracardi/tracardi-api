from datetime import datetime

from tracardi.context import ServerContext, Context

from test.utils import Endpoint, get_test_tenant
from tracardi.service.storage.index import Resource

endpoint = Endpoint()


def test_should_return_indices():
    with ServerContext(Context(production=False, tenant=get_test_tenant())):
        response = endpoint.get("/debug/es/indices")
        result = response.json()
        assert response.status_code == 200
        alias = Resource()['version'].get_write_index()
        assert alias in result.keys()


def test_should_return_server_time():
    response = endpoint.get("/debug/server/time")
    result = response.json()
    assert response.status_code == 200
    try:
        datetime.strptime(result, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        assert False
