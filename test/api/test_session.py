from uuid import uuid4

from tracardi_tests.utils.utils import Endpoint

endpoint = Endpoint()


def test_get_session():
    session_id = str(uuid4())
    assert endpoint.get(f'/session/{session_id}').status_code == 404
