from tracardi.config import tracardi
from ..utils import Endpoint

endpoint = Endpoint()


def test_should_not_delete_currently_used_version():
    version = tracardi.version.version
    response = endpoint.delete(f'/indices/version/{version}')
    assert response.status_code == 409


def test_should_delete_not_currently_used_version():
    version = "some-version"
    response = endpoint.delete(f'/indices/version/{version}')
    result = response.json()
    assert response.status_code == 200
    assert result == {}

