from test.utils import Endpoint

endpoint = Endpoint()


def test_should_return_settings():
    response = endpoint.get("/settings")
    assert response.status_code == 200
    result = response.json()
    for setting in result:
        assert 'label' in setting
        assert 'value' in setting
