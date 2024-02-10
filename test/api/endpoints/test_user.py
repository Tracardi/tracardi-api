from uuid import uuid4

from tracardi.domain.user_payload import UserPayload
from test.utils import Endpoint


endpoint = Endpoint()


def test_should_add_read_and_delete_user():
    user_email = f'{str(uuid4())[:5]}@example.com'
    user_id = None

    try:

        data = {
            "password": "password",
            "name": "full name",
            "email": user_email,
            "roles": ["admin", "marketer", "developer"],
            "disabled": False
        }

        data = UserPayload(**data)
        
        response = endpoint.post("/user", data.model_dump())
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
            "name": "Full name 2",
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
        if user_id:
            endpoint.delete(f"/user/{user_id}")

