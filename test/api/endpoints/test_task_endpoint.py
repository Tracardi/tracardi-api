from test.utils import Endpoint

endpoint = Endpoint()


def _add_task(task=None):
    if task is None:
        task = {
            "id": "test-id",
            "name": "test-name",
            "task_id": "test-task",
            "timestamp": "2022-08-25T20:18:09.278Z",
            "status": 'pending',
            "progress": 1.1,
            "type": "test",
            "params": {
                "name": "test-name",
                "age": 0
            }
        }

        response = endpoint.post("/task", task)
        result = response.json()

        assert not result["errors"]
        assert result["ids"] == ["test-id"]
        assert response.status_code == 200

        return response


def test_should_load_task():
    try:
        _add_task()

        result = endpoint.get("/tasks")
        result = result.json()

        assert result["grouped"]
        assert result["grouped"]["Tasks"]

    finally:
        endpoint.delete("/task/test-task")


def test_should_return_task_by_type():
    try:
        _add_task()

        result = endpoint.get("/tasks/type/test")
        result = result.json()

        assert result["grouped"]["Tasks"][0]["type"] == "test"
    finally:
        endpoint.delete("/task/test-task")


def test_should_delete_task_by_id():
    try:
        _add_task()

        result = endpoint.delete("/task/test-task")
        assert result.status_code == 200

    finally:
        endpoint.delete("/task/test-task")


def test_should_add_new_task():
    try:
        response = _add_task()
        result = response.json()

        assert not result["errors"]
        assert result["saved"] == 1
        assert result["ids"] == ["test-id"]

        task = {
            "id": "test-id1",
            "name": "second-task",
            "task_id": "test-task",
            "timestamp": "2022-08-25T20:18:09.278Z",
            "status": 'pending',
            "progress": 1.1,
            "type": "test",
            "params": {
                "name": "john",
                "age": 25}
        }

        response = endpoint.post("/task", task)
        result = response.json()
        assert not result["errors"]
        assert result["saved"] == 1
        assert result["ids"] == ["test-id1"]

    finally:
        endpoint.delete("/task/test-task")
