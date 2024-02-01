from test.utils import Endpoint


endpoint = Endpoint()


def test_should_get_and_edit_account():

    user_payload = {
        "password": "test",
        "name": "Test account",
        "email": "test_email@test.com",
        "roles": ["marketer"],
        "disabled": False
    }
    user_id = None
    try:
        result = endpoint.post("/user", user_payload)
        assert result.status_code == 200

        data = result.json()

        user_id = data['ids'][0]

        endpoint.set_credentials(user_payload["email"], user_payload["password"])
        result = endpoint.get("/user-account")
        assert result.status_code == 200
        assert result.json()["email"] == user_payload["email"]
        assert result.json()["name"] == user_payload["name"]
        prev_password = result.json()["password"]

        result = endpoint.post("/user-account", {"name": "Full name", "password": "123"})
        assert result.status_code == 200

        result = endpoint.get("/user-account")
        assert result.status_code == 200
        assert result.json()["email"] == user_payload["email"]
        assert result.json()["name"] == "Full name"
        assert result.json()["password"] != prev_password

    finally:
        endpoint.set_credentials()
        if user_id:
            print(endpoint.delete(f"/user/{user_id}"))
