from test.utils import Endpoint

endpoint = Endpoint()


def test_should_return_token():
    data = {
        "username": "a@a.pl",
        "password": "a"
    }
    response = endpoint.request("/token", data)
    assert response.status_code == 200

    result = response.json()

    assert result["access_token"]
    assert result["token_type"] == "bearer"
    assert result["roles"]


def test_should_successfully_logout():

    response = endpoint.post("/logout")

    assert response.status_code == 200
