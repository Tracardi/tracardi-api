from test.utils import Endpoint


endpoint = Endpoint()


def test_should_add_read_and_delete_user():
    user_email = 'test.email@example.com'
    try:

        data = {
            "password": "password",
            "full_name": "full name",
            "email": user_email,
            "roles": ["admin", "marketer", "developer"],
            "disabled": False
        }
        response = endpoint.post("/user", data)
        assert response.status_code == 200

        result = response.json()
        user_id = result['ids'][0]

        assert result["saved"] == 1

        response = endpoint.get("/users/0/100")
        assert response.status_code == 200

        response = endpoint.get(f"/user/{user_id}")
        assert response.status_code == 200

        data = {
            "password": "password2",
            "full_name": "Full name 2",
            "email": user_email,
            "roles": ["developer", "marketer"],
            "disabled": True
        }

        # update
        response = endpoint.post(f"/user/{user_id}", data)
        assert response.status_code == 200
        result = response.json()

        assert result['inserted'] == 1

        result = endpoint.delete(f"/user/{user_id}")
        result = result.json()

        assert result["deleted"] == 1

    finally:
        endpoint.delete(f"/user/{user_id}")

