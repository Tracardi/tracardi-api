from uuid import uuid4

from test.api.endpoints.test_event_source_endpoint import _create_event_source
from test.utils import Endpoint

endpoint = Endpoint()

source_id = str(uuid4())

assert _create_event_source(source_id, 'rest').status_code == 200

payload = {
    "source": {
        "id": source_id
    },
    "session": {
        "id": str(uuid4())
    },
    "events": [
        {
            "type": "test-event-1",
            "options": {"save": True},
            "context": {"test": 1}
        },
        {
            "type": "test-event-2",
            "context": {"test": 2}
        }
    ],
    "options": {"debugger": True}
}

response = endpoint.post("/track", data=payload)
print(response.json())
assert response.status_code == 200
result = response.json()
