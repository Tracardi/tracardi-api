from tracardi_tests.utils.utils import Endpoint

endpoint = Endpoint()


def create_event_source(id, type, name="Test", config=None):
    if config is None:
        config = {}

    event_source = dict(
        id=id,
        type=type,
        name=name,
        timestamp="2022-01-07T16:18:09.278Z",
        enabled=True,
        config=config
    )

    return endpoint.post('/event-source', data=event_source)


def test_unknown_event_source_type():
    assert create_event_source("2", "unknown-type").status_code == 500


def test_event_source_types():
    response = endpoint.get('/event-sources/type/name')
    assert response.status_code == 200
    result = response.json()

    if result:
        assert 'total' in result
        assert 'result' in result


def test_event_source_create_ok():
    id = "1"

    response = create_event_source(id, "javascript")
    result = response.json()
    assert response.status_code == 200
    assert result == {'errors': [], 'ids': ['1'], 'saved': 1}

    # refresh result and see if there is new data
    response = endpoint.get('/event-sources/refresh')
    assert response.status_code == 200

    # get new data
    response = endpoint.get(f'/event-source/{id}')
    assert response.status_code == 200
    result = response.json()
    assert result is not None


def test_resource_get_ok():
    response = endpoint.delete('/event-source/2')
    print(response.json(), response.status_code)
    assert response.status_code in [404, 200]

    response = endpoint.get('/event-source/2')
    print(response.json(), response.status_code)
    assert response.status_code == 404


def test_resources_by_tag():
    response = endpoint.get('/event-sources/by_type')
    assert response.status_code == 200
    result = response.json()
    assert 'total' in result
    assert 'grouped' in result
