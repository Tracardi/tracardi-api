from tracardi.context import Context, ServerContext

from test.utils import Endpoint, get_test_tenant
from uuid import uuid4


with ServerContext(Context(production=False, tenant=get_test_tenant())):
    endpoint = Endpoint()


    def _create_event_source(id, type, config=None):
        if config is None:
            config = {}

        event_source = dict(
            id=id,
            bridge=dict(id="778ded05-4ff3-4e08-9a86-72c0195fa95d", name="Test Api"),
            type=type,
            name=id,
            timestamp="2022-01-07T16:18:09.278Z",
            enabled=True,
            config=config
        )

        response = endpoint.post('/event-source', data=event_source)
        assert response.status_code in [200, 500, 422]
        return response


    def test_should_return_event_sources_by_tag():
        response = endpoint.get('/event-sources/by_type')
        assert response.status_code == 200
        result = response.json()
        assert 'total' in result
        assert 'grouped' in result


    def test_should_return_event_sources_types():
        response = endpoint.get('/event-sources/type/name')
        assert response.status_code == 200
        result = response.json()
        assert 'total' in result
        assert 'result' in result
        assert 'rest' in result['result']

        response = endpoint.get('/event-sources/type/configuration')
        assert response.status_code == 200
        result = response.json()
        assert 'total' in result
        assert 'result' in result
        assert 'rest' in result['result']
        assert 'tags' in result['result']['rest']


    def test_should_return_404_on_get_event_source_if_none():
        event_source_id = str(uuid4())
        response = endpoint.get(f'/event-source/{event_source_id}')
        assert response.status_code == 404
        assert response.json() is None


    def test_should_return_404_on_delete_event_source_if_none():
        event_source_id = str(uuid4())
        response = endpoint.delete(f'/event-source/{event_source_id}')
        assert response.status_code == 404
        assert response.json() is None


    def test_unknown_event_source_type():
        response = _create_event_source("2", "unknown-type")
        assert response.status_code == 422


    def test_event_source_create_ok():
        id = str(uuid4())

        try:
            response = _create_event_source(id, "rest")
            result = response.json()
            assert response.status_code == 200
            assert result == {'errors': [], 'ids': [id], 'saved': 1}

            # refresh result and see if there is new data
            assert endpoint.get('/event-sources/refresh').status_code == 200

            # get new data
            response = endpoint.get(f'/event-source/{id}')
            assert response.status_code == 200
            result = response.json()
            assert result is not None

        finally:
            assert endpoint.delete(f'/event-source/{id}').status_code in [200, 404]


    def test_should_refresh_event_sources():
        response = endpoint.get('/event-sources/refresh')
        assert response.status_code == 200


    def test_should_return_list_of_event_sources():
        id = str(uuid4())

        try:
            _create_event_source(id, "rest")
            response = endpoint.get('/event-sources/entity')
            assert response.status_code == 200
            result = response.json()
            assert 'total' in result
            assert 'result' in result
            assert len(result['result']) > 0
        finally:
            assert endpoint.delete(f'/event-source/{id}').status_code in [200, 404]
