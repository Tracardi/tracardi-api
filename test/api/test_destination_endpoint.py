import json

from tracardi.domain.destination import DestinationConfig
from tracardi.domain.resource import Resource
from ..utils import Endpoint

endpoint = Endpoint()


def _add_destination(destination_id):
    data = {
        "id": destination_id,
        "name": "test-destination",
        "description": "",
        "condition": "payload@a==1",
        "mapping": {},
        "destination": {
            "package": "package",
            "form": {},
            "init": {
                "a": 1
            }
        },
        "enabled": True,
        "resource": {
            "id": "abc"
        },
        "tags": ["tag1", "tag2"]
    }
    response = endpoint.post('/destination', data=data)
    assert response.status_code == 200
    return response, data


def test_should_save_destination():
    destination_id = 'abc'
    try:
        response, _ = _add_destination(destination_id)
        result = response.json()
        assert response.status_code == 200
        assert result['saved'] == 1
        assert destination_id in result['ids']
    finally:
        response = endpoint.delete(f'/destination/{destination_id}')
        assert response.status_code == 200


def test_should_fail_destination_save_on_incorrect_data():
    destination_id = 'abc'
    try:
        response = endpoint.post('/destination', data={
            "id": destination_id,
            "name": "test-destination",
            "description": "",
            "condition": "incorrect",
            "destination": {
                "package": "package",
            },
            "enabled": True,
            "resource": {
                "id": "abc"
            }
        })
        assert response.status_code == 422
    finally:
        response = endpoint.delete(f'/destination/{destination_id}')
        assert response.status_code == 404


def test_should_fail_destination_save_on_incorrect_condition():
    destination_id = 'abc'
    try:
        response = endpoint.post('/destination', data={
        })
        assert response.status_code == 422
    finally:
        response = endpoint.delete(f'/destination/{destination_id}')
        assert response.status_code == 404


def test_should_get_destination():
    destination_id = 'abc'
    try:
        _, data = _add_destination(destination_id)
        response = endpoint.get(f'/destination/{destination_id}')
        assert response.status_code == 200

        result = response.json()
        data['id'] = destination_id
        assert result == data

    finally:
        response = endpoint.delete(f'/destination/{destination_id}')
        assert response.status_code == 200


def test_should_return_404_on_missing_destination():
    try:
        response = endpoint.get(f'/destination/missing-id')
        assert response.status_code == 404
        assert response.json() is None

    finally:
        response = endpoint.delete(f'/destination/missing-id')
        assert response.status_code == 404


def test_should_return_destinations():
    try:
        _, data1 = _add_destination("id1")
        _, data1 = _add_destination("id2")
        response = endpoint.get(f'/destinations')
        assert response.status_code == 200
        result = response.json()
        assert result['total'] == 2
        # there is no sorting so the order is unknown
        assert result['result'][0]['id'] in ['id1', 'id2']
        assert result['result'][1]['id'] in ['id1', 'id2']
    finally:
        response = endpoint.delete(f'/destination/id1')
        assert response.status_code == 200
        response = endpoint.delete(f'/destination/id2')
        assert response.status_code == 200


def test_should_return_empty_destinations():
    response = endpoint.get(f'/destinations')
    assert response.status_code == 200
    result = response.json()
    assert result['total'] == 0
    assert result['result'] == []


def test_should_return_destinations_types():
    response = endpoint.get(f'/destinations/type')
    assert response.status_code == 200
    result = response.json()
    assert 'tracardi.process_engine.destination.http_connector.HttpConnector' in result.keys()
    assert 'tracardi.process_engine.destination.mautic_connector.MauticConnector' in result.keys()


def test_should_return_destinations_by_tag():
    try:
        _, data1 = _add_destination("id1")
        _, data1 = _add_destination("id2")
        response = endpoint.get(f'/destinations/by_tag')
        assert response.status_code == 200
        result = response.json()
        assert list(result['grouped'].keys()) == ['tag1', 'tag2']
        assert result['grouped']['tag1'][0]['id'] in ['id1', 'id2']
        assert result['grouped']['tag2'][0]['id'] in ['id1', 'id2']
    finally:
        response = endpoint.delete(f'/destination/id1')
        assert response.status_code == 200
        response = endpoint.delete(f'/destination/id2')
        assert response.status_code == 200


def test_should_return_destinations_resources():
    resource = Resource(
        id="res1",
        timestamp="2022-01-01",
        type='http',
        name="res1",
        credentials={},
        destination=DestinationConfig(package='tracardi.process_engine.destination.http_connector.HttpConnector')
    )
    response = endpoint.post('/resource', data=json.loads(resource.json()))
    assert response.status_code == 200
    try:
        _, data1 = _add_destination("id1")
        _, data1 = _add_destination("id2")
        response = endpoint.get(f'/destinations/entity')
        assert response.status_code == 200
        result = response.json()
        assert 'res1' in result
        assert result['res1']['id'] == 'res1'
        assert result['res1']['destination'][
                   'package'] == 'tracardi.process_engine.destination.http_connector.HttpConnector'
    finally:
        response = endpoint.delete(f'/destination/id1')
        assert response.status_code == 200
        response = endpoint.delete(f'/destination/id2')
        assert response.status_code == 200
        response = endpoint.delete(f'/resource/res1')
        assert response.status_code == 200
