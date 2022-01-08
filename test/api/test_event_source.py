from uuid import uuid4

from ..utils import Endpoint

endpoint = Endpoint()


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
    id = str(uuid4())

    try:
        response = create_event_source(id, "javascript")
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


def test_resources_by_tag():
    response = endpoint.get('/event-sources/by_type')
    assert response.status_code == 200
    result = response.json()
    assert 'total' in result
    assert 'grouped' in result
