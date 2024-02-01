from test.utils import Endpoint

endpoint = Endpoint()


def test_should_handle_multiple_sessions():
    user_email = 'test.email@example.com'
    user_pass = "example pass"

    start_token = endpoint.token

    try:
        user_id = None
        data = {
            "password": user_pass,
            "name": "full name",
            "email": user_email,
            "roles": ["admin", "marketer", "developer"],
            "disabled": False
        }
        response = endpoint.post("/user", data)
        assert response.status_code == 200
        result = response.json()
        user_id = result['ids'][0]

        assert result["saved"] == 1

        token1 = endpoint.auth(user_email, user_pass)
        token2 = endpoint.auth(user_email, user_pass)

        # todo this fails because auth returns the same token
        # todo it must be fixed
        assert token1 != token2

        endpoint.set_token(token1)
        response = endpoint.get("/settings")
        assert response.status_code == 200

        endpoint.set_token(token2)
        response = endpoint.get("/settings")
        assert response.status_code == 200

        endpoint.set_token(token1)
        endpoint.post("/user/logout")
        response = endpoint.get("/settings")
        assert response.status_code == 401

        endpoint.set_token(token2)
        response = endpoint.get("/settings")
        assert response.status_code == 200
        endpoint.post("/user/logout")
        response = endpoint.get("/settings")
        assert response.status_code == 401

    finally:
        endpoint.auth(user_email, user_pass)
        if user_id:
            endpoint.delete(f"/user/{user_id}")
        endpoint.set_token(start_token)
