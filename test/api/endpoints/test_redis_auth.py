from test.utils import Endpoint

endpoint = Endpoint()


def test_should_handle_multiple_sessions():
    user_email = 'test.email@example.com'
    user_pass = "example pass"

    start_token = endpoint.token

    # Check settings to find out if the test can be run.
    response = endpoint.get("/settings")
    assert response.status_code == 200
    available_settings = response.json()
    tokens_in_redis = [setting['value'] for setting in available_settings if setting['label'] == 'TOKENS_IN_REDIS']

    if len(tokens_in_redis) != 1:
        raise ValueError("Could not find TOKENS_IN_REDIS setting.")

    tokens_in_redis = tokens_in_redis[0]

    if tokens_in_redis is True:

        try:

            response = endpoint.delete(f"/user/{user_email}")

            assert response.status_code in [404, 200]

            data = {
                "password": user_pass,
                "full_name": "full name",
                "email": user_email,
                "roles": ["admin", "marketer", "developer"],
                "disabled": False
            }
            response = endpoint.post("/user", data)
            assert response.status_code == 200
            result = response.json()

            assert result["inserted"] == 1

            token1 = endpoint.auth(user_email, user_pass)
            token2 = endpoint.auth(user_email, user_pass)

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
            endpoint.delete(f"/user/{user_email}")
            endpoint.set_token(start_token)
    else:
        print("Token in redis tests skipped. TOKENS_IN_REDIS does not equal True.")
