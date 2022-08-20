from tracardi.config import tracardi
from tracardi.domain.version import Version
from ..utils import Endpoint

endpoint = Endpoint()


def test_should_return_version():
    response = endpoint.get('/info/version')
    assert response.status_code == 200
    result = response.json()
    assert result == tracardi.version.version


def test_should_return_detailed_version():
    response = endpoint.get('/info/version/details')
    assert response.status_code == 200
    result = response.json()
    version = Version(**result)
    assert version.version == tracardi.version.version
