from ..utils import Endpoint
from uuid import uuid4


endpoint = Endpoint()


def test_should_work():
    try:
        data = {
            "password": "password",
            "full_name": "full name",
            "email": "test.email@example.com",
            "roles": ["admin", "marketer", "developer"],
            "disabled": False,
            "id": "1d29217f-b636-4c54-a133-db1d6f66e696"
        }
        result = endpoint.post("/user", data)
        result = result.json()

        assert result["inserted"] == 1

        endpoint.get("/users/0/100")

        endpoint.get("/user/1d29217f-b636-4c54-a133-db1d6f66e696")

        data = {
            "password": "password2",
            "full_name": "Full name 2",
            "email": "test.email2@example.com",
            "roles": ["developer", "marketer"],
            "disabled": True
        }

        result = endpoint.post("/users/1d29217f-b636-4c54-a133-db1d6f66e696/edit", data)
        result = result.json()

        assert result["inserted"] == 1

        result = endpoint.delete("/user/1d29217f-b636-4c54-a133-db1d6f66e696")
        result = result.json()

        assert result["deleted"] == 1
    except Exception as e:
        endpoint.delete("/user/1d29217f-b636-4c54-a133-db1d6f66e696")
        raise e
