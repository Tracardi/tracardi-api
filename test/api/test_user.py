from ..utils import Endpoint


endpoint = Endpoint()


def test_should_add_read_and_delete_user():
    user_email = 'test.email@example.com'
    try:

        endpoint.delete(f"/user/{user_email}")

        data = {
            "password": "password",
            "full_name": "full name",
            "email": user_email,
            "roles": ["admin", "marketer", "developer"],
            "disabled": False
        }
        result = endpoint.post("/user", data)
        result = result.json()

        assert result["inserted"] == 1

        endpoint.get("/users/0/100")

        endpoint.get(f"/user/{user_email}")

        data = {
            "password": "password2",
            "full_name": "Full name 2",
            "email": user_email,
            "roles": ["developer", "marketer"],
            "disabled": True
        }

        result = endpoint.post(f"/users/{user_email}/edit", data)
        result = result.json()

        assert result["inserted"] == 1

        result = endpoint.delete(f"/user/{user_email}")
        result = result.json()

        assert result["deleted"] == 1

    finally:
        endpoint.delete(f"/user/{user_email}")

