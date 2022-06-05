from uuid import uuid4

from ..utils import Endpoint

endpoint = Endpoint()


def test_should_return_404_on_get_resource_if_none():
    resource_id = str(uuid4())
    response = endpoint.get(f'/resource/{resource_id}')
    assert response.status_code == 404
    assert response.json() is None


def test_should_return_404_on_delete_resource_if_none():
    resource_id = str(uuid4())
    response = endpoint.delete(f'/rule/{resource_id}')
    assert response.status_code == 404
    assert response.json() is None

    assert endpoint.get(f'/resource/{resource_id}').status_code == 404


def create_resource(id, type, name="Test", config=None):
    if config is None:
        config = {}

    resource = dict(
        id=id,
        type=type,
        name=name,
        config=config
    )
    return endpoint.post('/resource', data=resource)


def test_source_types():
    response = endpoint.get('/resources/type/name')
    assert response.status_code == 200
    result = response.json()
    if result:
        assert 'total' in result
        assert 'result' in result


def test_source_list():
    response = endpoint.get('/resources')
    assert response.status_code == 200
    result = response.json()
    if result:
        assert 'total' in result
        assert 'result' in result


def test_should_create_resource():
    id = str(uuid4())

    try:
        response = create_resource(id, "mysql")
        assert response.status_code == 200
        result = response.json()
        assert result == {'saved': 1, 'errors': [], 'ids': [id]}

        # refresh result and see if there is new data
        response = endpoint.get('/resources/refresh')
        assert response.status_code == 200

        # get new data
        response = endpoint.get(f'/resource/{id}')
        assert response.status_code == 200
        result = response.json()
        assert result is not None

    finally:
        assert endpoint.delete(f'/resource/{id}').status_code in [200, 404]


def test_resource_get_ok():
    response = endpoint.delete('/resource/2')
    assert response.status_code in [404, 200]

    response = endpoint.get('/resource/2')
    assert response.status_code == 404


def test_source_toggle_on_off_ok():
    resource_id = str(uuid4())

    try:
        response = create_resource(resource_id, "mysql")
        assert response.status_code == 200
        result = response.json()
        assert result == {'saved': 1, 'errors': [], 'ids': [resource_id]}

        # Enable on

        result = endpoint.get(f'/resource/{resource_id}/enabled/on').json()
        assert result == {'saved': 1, 'errors': [], 'ids': [resource_id]}

        result = endpoint.get(f'/resource/{resource_id}').json()
        assert result['enabled'] is True

        # Enable off

        result = endpoint.get(f'/resource/{resource_id}/enabled/off').json()
        assert result == {'saved': 1, 'errors': [], 'ids': [resource_id]}

        result = endpoint.get(f'/resource/{resource_id}').json()
        assert result['enabled'] is False

    finally:
        assert endpoint.delete(f'/resource/{resource_id}').status_code in [200, 404]


def test_resources_by_tag():
    response = endpoint.get('/resources/by_type')
    assert response.status_code == 200
    result = response.json()
    assert 'total' in result
    assert 'grouped' in result
