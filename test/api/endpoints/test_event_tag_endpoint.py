from test.utils import Endpoint

endpoint = Endpoint()


def test_should_replace_event_tag():
    try:
        data = {
            "type": "test-type",
            "tags": ["tag1", "tag2", "tag3"]
        }
        response = endpoint.post("/event-tag/replace", data)
        assert response.status_code == 200
        result = response.json()
        assert 'replaced' in result
        assert result['replaced'] == 1
    finally:
        assert endpoint.delete("/event-tag/test-type").status_code in [200, 404]


def test_should_add_event_tag():
    try:
        data = {
            "type": "test-type",
            "tags": ["tag1", "tag2", "tag3"]
        }
        response = endpoint.post("/event-tag", data)
        assert response.status_code == 200
        result = response.json()

        assert 'new' in result
        assert result['new'] == 1

    finally:
        assert endpoint.delete("/event-tag/test-type").status_code in [200, 404]


def test_should_delete_event_tag():
    try:
        data = {
            "type": "test-type",
            "tags": ["tag1", "tag2", "tag3"]
        }
        result = endpoint.post("/event-tag", data)

        assert result.status_code == 200

        data = {
            "type": "test-type",
            "tags": ["tag1", "tag2"]
        }
        result = endpoint.delete("/event-tag", data)
        result = result.json()

        assert result["removed"] == 2
        assert result["total"] == 1
    finally:
        assert endpoint.delete("/event-tag/test-type").status_code == 200
        assert endpoint.delete("/event-tag/test-type").status_code == 404
        data = {
            "type": "test-type",
            "tags": ["tag1", "tag2"]
        }
        assert endpoint.delete("/event-tag", data).status_code == 404


def test_should_refresh_event_tag():
    response = endpoint.get("/event-tags/refresh")
    assert response.status_code == 200


def test_should_flush_event_tag():
    response = endpoint.get("/event-tags/flush")
    assert response.status_code == 200


def test_get_event_tag():
    response = endpoint.get("/event-tag")
    assert response.status_code == 200


def test_should_update_tags():
    response = endpoint.put("/event-tag/type/page-view")
    assert response.status_code == 200
    result = response.json()

    assert "total" in result
