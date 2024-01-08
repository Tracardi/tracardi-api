from uuid import uuid4

from test.api.endpoints.test_event_source_endpoint import _create_event_source
from test.utils import Endpoint

endpoint = Endpoint()

source_id = "850b12c1-cd04-4d09-b9a4-e7c961bcb224"
session_id = str(uuid4())
profile_id = "12e947df-f26c-4640-9bf3-61a177011320"

for _ in range(3):

    session_id = str(uuid4())
    print(profile_id)

    payload1 = {
        "source": {
            "id": source_id
        },
        "session": {
            "id": session_id
        },
        "profile": {
            "id": profile_id
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
        "profile": {
            "id": profile_id
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
