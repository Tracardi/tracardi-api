from ..utils import Endpoint

endpoint = Endpoint()


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


def test_source_create_ok():
    id = "1"

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


def test_resource_get_ok():
    response = endpoint.delete('/resource/2')
    assert response.status_code in [404, 200]

    response = endpoint.get('/resource/2')
    assert response.status_code == 404


def test_source_toggle_on_off_ok():
    # Enable on

    result = endpoint.get('/resource/1/enabled/on').json()
    assert result == {'saved': 1, 'errors': [], 'ids': ['1']}

    result = endpoint.get('/resource/1').json()
    assert result['enabled'] is True

    # Enable off

    result = endpoint.get('/resource/1/enabled/off').json()
    assert result == {'saved': 1, 'errors': [], 'ids': ['1']}

    result = endpoint.get('/resource/1').json()
    assert result['enabled'] is False

    # Consent on

    result = endpoint.get('/resource/1/consent/on').json()
    assert result == {'saved': 1, 'errors': [], 'ids': ['1']}

    result = endpoint.get('/resource/1').json()
    assert result['consent'] is True

    # Consent off

    result = endpoint.get('/resource/1/consent/off').json()
    assert result == {'saved': 1, 'errors': [], 'ids': ['1']}

    result = endpoint.get('/resource/1').json()
    assert (result['consent'] is False)


def test_source_delete_ok():
    response = endpoint.delete('/resource/1')
    if response.status_code == 200:
        result = response.json()
        assert result['result'] == 'deleted'
    else:
        response = endpoint.delete('/resource/1')
        assert response.status_code == 404


def test_resources_refresh():
    response = endpoint.get('/resources/refresh')
    assert response.status_code == 200


def test_resources_by_tag():
    response = endpoint.get('/resources/by_type')
    assert response.status_code == 200
    result = response.json()
    assert 'total' in result
    assert 'grouped' in result
