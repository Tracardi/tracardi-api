from uuid import uuid4

from test.utils import Endpoint

endpoint = Endpoint()


def test_should_return_404_on_get_session_if_none():
    session_id = str(uuid4())
    response = endpoint.get(f'/session/{session_id}')
    assert response.status_code == 404
    assert response.json() is None


def test_should_return_404_on_delete_session_if_none():
    session_id = str(uuid4())
    response = endpoint.delete(f'/session/{session_id}')
    assert response.status_code == 404
    assert response.json() is None
