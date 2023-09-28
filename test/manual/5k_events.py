from uuid import uuid4

from test.api.endpoints.test_event_source_endpoint import _create_event_source
from test.utils import Endpoint

endpoint = Endpoint()

source_id = str(uuid4())
session_id = str(uuid4())

assert _create_event_source(source_id, 'rest').status_code == 200

for _ in range(5000):

    session_id = str(uuid4())

    payload1 = {
        "source": {
            "id": source_id
        },
        "session": {
            "id": session_id
        },
        "events": [
            {
                "type": "identification",
                "properties": {
                    "firstname": "risto11"
                }
            }
        ],
        "options": {"debugger": True}
    }

    payload2 = {
        "source": {
            "id": source_id
        },
        "session": {
            "id": session_id
        },
        "events": [
            {
                "type": "test-event-1",
                "options": {"save": True},
                "context": {"test": 1}
            },
            {
                "type": "identification",
                "properties": {
                    "firstname": "risto22"
                }
            },
            {
                "type": "test-event-2",
                "context": {"test": 2}
            }
        ],
        "options": {"debugger": True}
    }

    response1 = endpoint.post("/track", data=payload1)
    assert response1.status_code == 200
    response1 = endpoint.post("/track", data=payload2)
    assert response1.status_code == 200
