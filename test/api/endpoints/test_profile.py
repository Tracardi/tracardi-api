from uuid import uuid4
from test.utils import Endpoint

endpoint = Endpoint()


def test_should_return_404_on_get_profile_if_none():
    profile_id = str(uuid4())
    response = endpoint.get(f'/profile/{profile_id}')
    assert response.status_code == 404
    assert response.json() is None


def test_should_return_404_on_delete_profile_if_none():
    profile_id = str(uuid4())
    response = endpoint.delete(f'/profile/{profile_id}')
    assert response.status_code == 404
    assert response.json() is None


def test_should_load_profile():
    profile_id = str(uuid4())
    try:
        assert endpoint.get(f'/profile/{profile_id}').status_code == 404

        response = endpoint.post('/profiles/import', data=[{"id": profile_id}])
        result = response.json()
        assert result["saved"] == 1
        assert response.status_code == 200

        assert endpoint.get('/profiles/refresh').status_code == 200
        assert endpoint.get(f'/profile/{profile_id}').status_code == 200

    finally:
        assert endpoint.delete(f'/profile/{profile_id}').status_code in [200,404]
        assert endpoint.get('/profiles/refresh').status_code == 200
