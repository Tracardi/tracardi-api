from test.utils import Endpoint

endpoint = Endpoint()

def test_should_not_return_token_if_wrong_login_or_password():
    data = {
        "username": "a@a.pl",
        "password": "wrong"
    }
    response = endpoint.request("/user/token", data)
    assert response.status_code == 400

    data = {
        "username": "wrong@a.pl",
        "password": "a"
    }
    response = endpoint.request("/user/token", data)
    assert response.status_code == 400

    # Log out should be possible event if not logged in.
    response = endpoint.post("/user/logout")

    assert response.status_code == 200

def test_should_return_token_and_log_out():
    data = {
        "username": "a@a.pl",
        "password": "a"
    }
    response = endpoint.request("/user/token", data)
    assert response.status_code == 200

    result = response.json()

    assert result["access_token"]
    assert result["token_type"] == "bearer"
    assert result["roles"]

    response = endpoint.post("/user/logout")

    assert response.status_code == 200


def test_should_return_token():
    data = {
        "username": "a@a.pl",
        "password": "a"
    }
    response = endpoint.request("/user/token", data)
    assert response.status_code == 200
