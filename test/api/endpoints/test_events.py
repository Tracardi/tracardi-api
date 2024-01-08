from uuid import uuid4

from test.api.endpoints.test_event_source_endpoint import _create_event_source
from test.utils import Endpoint
from tracardi.service.events import get_predefined_event_types

endpoint = Endpoint()

def test_collection_of_default_events():
    result = get_predefined_event_types()

    source_id = str(uuid4())

    try:
        assert _create_event_source(source_id, 'rest').status_code == 200

        for event_type, data in result:
            print(f"Testing {event_type}", flush=True)
            payload = {
                "source": {
                    "id": source_id
                },
                "session": {
                    "id": str(uuid4())
                },
                "events": [
                    {
                        "type": event_type,
                        "properties": data['properties']
                    }
                ]
            }

            response = endpoint.post("/track", data=payload)

            if response.status_code != 200:
                assert "Error for event type" == event_type

    finally:
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]

