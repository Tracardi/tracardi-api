from datetime import datetime

from test.utils import Endpoint

endpoint = Endpoint()


def test_should_return_indices():
    response = endpoint.get("/debug/es/indices")
    result = response.json()
    assert response.status_code == 200
    assert 'tracardi-version' in result.keys()


def test_should_return_server_time():
    response = endpoint.get("/debug/server/time")
    result = response.json()
    assert response.status_code == 200
    try:
        datetime.strptime(result, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        assert False
