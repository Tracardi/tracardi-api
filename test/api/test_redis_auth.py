from ..utils import Endpoint


endpoint = Endpoint()


def test_should_handle_multiple_sessions():
    user_email = 'test.email@example.com'
    user_pass = "example pass"
    try:
        endpoint.delete(f"/user/{user_email}")

        data = {
            "password": user_pass,
            "full_name": "full name",
            "email": user_email,
            "roles": ["admin", "marketer", "developer"],
            "disabled": False
        }
        result = endpoint.post("/user", data)
        result = result.json()

        assert result["inserted"] == 1

        token1 = endpoint.auth(user_email, user_pass)
        token2 = endpoint.auth(user_email, user_pass)

        endpoint.set_token(token1)
        result = endpoint.get("/settings")
        assert result.status_code == 200

        endpoint.set_token(token2)
        result = endpoint.get("/settings")
        assert result.status_code == 200

        endpoint.set_token(token1)
        endpoint.post("/logout")
        result = endpoint.get("/settings")
        assert result.status_code == 403

        endpoint.set_token(token2)
        result = endpoint.get("/settings")
        assert result.status_code == 200
        endpoint.post("/logout")
        result = endpoint.get("/settings")
        assert result.status_code == 403

    finally:
        endpoint.auth(user_email, user_pass)
        endpoint.delete(f"/user/{user_email}")
