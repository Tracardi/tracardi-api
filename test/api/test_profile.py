from uuid import uuid4
from ..utils import Endpoint

endpoint = Endpoint()


def test_get_profile():
    profile_id = str(uuid4())
    assert endpoint.get(f'/profile/{profile_id}').status_code == 404

    response = endpoint.post('/profiles/import', data=[{"id": profile_id}])
    result = response.json()
    assert result["saved"] == 1
    assert response.status_code == 200

    assert endpoint.get('/profiles/refresh').status_code == 200

    assert endpoint.get(f'/profile/{profile_id}').status_code == 200

