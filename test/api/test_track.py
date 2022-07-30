from uuid import uuid4

from .test_source import create_event_source
from ..utils import Endpoint

endpoint = Endpoint()


def test_should_register_correct_event():
    source_id = str(uuid4())

    try:

        assert create_event_source(source_id, 'rest').status_code == 200

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
            "options": {"profile": True, "debugger": True}
        }

        response = endpoint.post("/track", data=payload)
        assert response.status_code == 200
        result = response.json()

        assert 'profile' in result
        assert 'id' in result['profile']
        assert 'traits' in result['profile']

        if 'debugging' in result:
            assert 'events' in result['debugging']
            assert 'ids' in result['debugging']['events']

            assert len(result['debugging']['events']['ids']) == 2

            event_1, event_2 = result['debugging']['events']['ids']

            endpoint.get(f'/events/refresh')

            # Event 1

            result = endpoint.get(f'/event/{event_1}')
            result = result.json()
            assert result['event']['id'] == event_1
            assert result['event']['context']['test'] == 1

            # Event 2

            result = endpoint.get(f'/event/{event_2}')
            result = result.json()
            assert result['event']['id'] == event_2
            assert result['event']['context']['test'] == 2

    finally:
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
