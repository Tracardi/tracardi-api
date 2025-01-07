from system.adapter.os.bigdata.elastic.installer.setup_indices import bd_raw_adapter
from tracardi.context import ServerContext, Context

from test.utils import Endpoint, get_test_tenant

endpoint = Endpoint()


def _check_if_has_installed_indices():
    with ServerContext(Context(production=False, tenant=get_test_tenant())):
        response = endpoint.get('/test/elasticsearch/indices')
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, dict)

        installed_indices = result.keys()

        for name, resource in bd_raw_adapter.get_installed_resources():
            assert resource.get_write_index() in installed_indices


def test_es_indices():
    _check_if_has_installed_indices()


def test_redis_connection():
    response = endpoint.get('/test/redis')
    assert response.status_code == 200


def test_es_connection():
    response = endpoint.get('/test/elasticsearch')
    assert response.status_code == 200
    result = response.json()
    assert 'cluster_name' in result
    assert 'status' in result
