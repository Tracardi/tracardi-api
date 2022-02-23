from ..utils import Endpoint

endpoint = Endpoint()


def test_post_event_tag_add():
    try:
        data = {
            "type": "test-type",
            "tags": ["tag1", "tag2", "tag3"]
        }
        result = endpoint.post("/event/tag/add", data)

        assert result.status_code == 200

    finally:
        endpoint.delete("/event/tag/delete/test-type")


def test_delete_event_tag():
    try:
        data = {
            "type": "test-type",
            "tags": ["tag1", "tag2", "tag3"]
        }
        result = endpoint.post("/event/tag/add", data)

        assert result.status_code == 200

        data = {
            "type": "test-type",
            "tags": ["tag1", "tag2"]
        }
        result = endpoint.delete("/event/tag/delete", data)
        result = result.json()

        assert result["removed"] == 2
        assert result["total"] == 1
    finally:
        endpoint.delete("/event/tag/delete/test-type")


def test_get_event_tag():
    result = endpoint.get("/event/tag/get")


def test_put_update_tags():
    result = endpoint.put("/event/tag/type/page-view")
    result = result.json()

    assert "total" in result


def test_delete_event_tags():
    result = endpoint.delete("/event/tag/delete/test-type")
    result = result.json()

    assert "deleted" in result
