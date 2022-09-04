from test.utils import Endpoint

endpoint = Endpoint()


def test_should_return_page():

    response = endpoint.get("/logs/page/1")
    result = response.json()

    assert response.status_code == 200
    assert result["total"]
    assert result["result"]


def test_should_return_logs():

    response = endpoint.get("/logs")
    result = response.json()

    assert response.status_code == 200
    assert result["total"]
    assert result["result"]
