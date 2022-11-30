from test.utils import Endpoint

endpoint = Endpoint()


def test_should_return_page():

    response = endpoint.get("/logs/page/0")
    result = response.json()

    assert response.status_code == 200
    assert isinstance(result["total"], int)
    assert isinstance(result["result"], list)


def test_should_return_logs():

    response = endpoint.get("/logs")
    result = response.json()

    assert response.status_code == 200
    assert isinstance(result["total"], int)
    assert isinstance(result["result"], list)
