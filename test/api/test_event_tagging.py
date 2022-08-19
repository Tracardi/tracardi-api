from time import sleep
from uuid import uuid4

from tracardi.domain.event_tag import EventTag
from .test_event_source_endpoint import _create_event_source
from ..utils import Endpoint

endpoint = Endpoint()


def test_should_tag_event():
    source_id = str(uuid4())
    event_type = "test-event-1"
    tag = 'tag-0'
    new_tag = 'new-tag-1'
    try:

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
                    "type": event_type,
                    "options": {"save": True},
                    "context": {"test": 1}
                }
            ],
            "options": {"profile": True, "debugger": True}
        }

        response = endpoint.post("/track", data=payload)
        assert response.status_code == 200

        result = response.json()

        assert endpoint.get(f'/events/flush').status_code == 200
        assert endpoint.get(f'/events/refresh').status_code == 200

        response = endpoint.post('/event-tag', data={"type": event_type, "tags": [tag]})
        assert response.status_code == 200

        assert endpoint.get(f'/event-tags/flush').status_code == 200
        assert endpoint.get(f'/event-tags/refresh').status_code == 200

        # Refresh updated tagged events

        assert endpoint.get(f'/events/flush').status_code == 200
        assert endpoint.get(f'/events/refresh').status_code == 200

        # Events

        if 'debugging' in result:
            assert 'events' in result['debugging']
            assert 'ids' in result['debugging']['events']

            assert len(result['debugging']['events']['ids']) == 1
            event_1, = result['debugging']['events']['ids']

            result = endpoint.get(f'/event/{event_1}')
            result = result.json()

            assert result['event']['tags']['values'] == [tag]
            assert result['event']['tags']['count'] == 1

        # send another event - it should be tagged

        sleep(2)

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
                    "properties": {"a": 1},
                    "options": {"save": True},
                    "context": {"test": 1}
                }
            ],
            "options": {"profile": True, "debugger": True}
        }

        response = endpoint.post("/track", data=payload)
        assert response.status_code == 200

        assert endpoint.get(f'/events/flush').status_code == 200
        assert endpoint.get(f'/events/refresh').status_code == 200

        result = response.json()

        if 'debugging' in result:
            assert 'events' in result['debugging']
            assert 'ids' in result['debugging']['events']

            assert len(result['debugging']['events']['ids']) == 1
            event_1, = result['debugging']['events']['ids']

            result = endpoint.get(f'/event/{event_1}')
            result = result.json()

            assert result['event']['tags']['values'] == [tag]
            assert result['event']['tags']['count'] == 1

            # replace tag

            response = endpoint.post('/event-tag/replace', data=EventTag(type=event_type, tags=[new_tag]).dict())
            assert response.status_code == 200

            assert endpoint.get(f'/event-tags/flush').status_code == 200
            assert endpoint.get(f'/event-tags/refresh').status_code == 200

            # Refresh updated tagged events

            assert endpoint.get(f'/events/flush').status_code == 200
            assert endpoint.get(f'/events/refresh').status_code == 200

            result = endpoint.get(f'/event/{event_1}')
            result = result.json()

            assert result['event']['tags']['values'] == [new_tag]
            assert result['event']['tags']['count'] == 1

    finally:
        assert endpoint.delete(f'/event-source/{source_id}').status_code in [200, 404]
        assert endpoint.delete(f'/event-tag/{event_type}').status_code in [200, 404]

        assert endpoint.get(f'/event-tags/flush').status_code == 200
        assert endpoint.get(f'/event-tags/refresh').status_code == 200


def test_should_delete_tag_event():
    response = endpoint.post('/event-tag', data={"type": "event-type-1", "tags": ["type-1"]})
    assert response.status_code == 200

    assert endpoint.get(f'/event-tags/flush').status_code == 200
    assert endpoint.get(f'/event-tags/refresh').status_code == 200

    assert endpoint.delete(f'/event-tag/event-type-1').status_code == 200
