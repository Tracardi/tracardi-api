from ..utils import Endpoint


endpoint = Endpoint()


def test_should_get_and_edit_account():
    user_payload = {
        "password": "test",
        "full_name": "Test account",
        "email": "test_email@test.com",
        "roles": ["marketer"],
        "disabled": False
    }

    try:
        result = endpoint.post("/user", user_payload)
        assert result.status_code == 200

        endpoint.set_credentials(user_payload["email"], user_payload["password"])
        result = endpoint.get("/user-account")
        assert result.status_code == 200
        assert result.json()["email"] == user_payload["email"]
        assert result.json()["full_name"] == user_payload["full_name"]
        prev_password = result.json()["password"]

        result = endpoint.post("/user-account", {"full_name": "Full name", "password": "123"})
        assert result.status_code == 200

        result = endpoint.get("/user-account")
        assert result.status_code == 200
        assert result.json()["email"] == user_payload["email"]
        assert result.json()["full_name"] == "Full name"
        assert result.json()["password"] != prev_password

    finally:
        endpoint.set_credentials()
        endpoint.delete("/user/test_email@test.com")
