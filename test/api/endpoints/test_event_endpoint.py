from time import sleep
from uuid import uuid4

from tracardi.config import tracardi
from .test_event_source_endpoint import _create_event_source
from test.utils import Endpoint

endpoint = Endpoint()


def _make_event(type, properties=None, session_id=None, source_id=None):
    if properties is None:
        properties = {}

    if source_id is None:
        source_id = "@test-source"

    assert _create_event_source(source_id, 'rest').status_code == 200

    payload = {
        "source": {
            "id": source_id
        },
        "session": {
            "id": str(uuid4()) if session_id is None else session_id
        },
        "events": [
            {
                "type": type,
                "properties": properties,
                "options": {"save": True},
                "context": {"test": 1}
            }
        ],
        "options": {"debugger": True}
    }

    response = endpoint.post("/track", data=payload)
    assert response.status_code == 200
    assert endpoint.get('/events/refresh').status_code == 200
    assert endpoint.get('/sessions/refresh').status_code == 200
    assert endpoint.get('/profiles/refresh').status_code == 200

    result = response.json()

    event_id = result['event']['ids'][0]
    profile_id = result['profile']['id']

    return response, payload, event_id, profile_id


def test_should_refresh_data():
    response = endpoint.get('/events/refresh')
    assert response.status_code == 200


def test_should_flash_data():
    response = endpoint.get('/events/flush')
    assert response.status_code == 200


def test_should_count_events():
    response = endpoint.get('/event/count')
    assert response.status_code == 200
    result = response.json()
    count = result['count']

    assert isinstance(count, int)

    source_id = str(uuid4())
    session_id = str(uuid4())
    response, _, event_id, profile_id = _make_event("test", source_id=source_id, session_id=session_id)

    try:
        response = endpoint.get('/event/count')
        assert response.status_code == 200
        result = response.json()
        count1 = result['count']

        assert count1 == count + 1

    finally:
        response = endpoint.delete(f'/event/{event_id}')
        assert response.status_code == 200

        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200
        assert endpoint.get('/profiles/refresh').status_code == 200

        assert endpoint.delete(f'/event-source/{source_id}').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/session/{session_id}').status_code == 200


def test_should_return_avg_request_time():
    response = endpoint.get('/event/avg/requests')
    assert response.status_code == 200
    result = response.json()
    count = result

    assert isinstance(count, float)


def test_should_return_process_time():
    response = endpoint.get('/event/avg/process-time')
    assert response.status_code == 200
    result = response.json()

    if result['records'] == 0:
        assert result['avg'] is None
        assert isinstance(result['records'], int)
    else:
        assert isinstance(result['avg'], float)
        assert isinstance(result['records'], int)


def test_should_return_event_meta():
    response = endpoint.get('/events/metadata/type?limit=1000')
    assert response.status_code == 200
    result = response.json()

    assert result['total'] >= 0
    assert isinstance(result['result'], list)

    if result['total'] < 1000:
        source_id = str(uuid4())
        session_id = str(uuid4())
        response, _, event_id, profile_id = _make_event("test", source_id=source_id, session_id=session_id)

        try:

            response = endpoint.get('/events/metadata/type?limit=1000')
            assert response.status_code == 200
            result = response.json()
            assert 'test' in result['result']

        finally:
            assert endpoint.delete(f'/event/{event_id}').status_code == 200
            assert endpoint.get('/events/refresh').status_code == 200

            assert endpoint.delete(f'/event-source/{source_id}').status_code == 200
            assert endpoint.get('/event-sources/refresh').status_code == 200

            assert endpoint.delete(f'/profile/{profile_id}').status_code == 200
            assert endpoint.get('/profiles/refresh').status_code == 200

            assert endpoint.delete(f'/session/{session_id}').status_code == 200


def test_should_return_events_by_type_for_profile():
    profile_id = 'missing'
    response = endpoint.get(f'/events/by_type/profile/{profile_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['total'] >= 0
    assert 'aggregations' in result
    assert result['no_of_aggregates'] > 0
    assert 'by_type' in result['aggregations']

    event_type = str(uuid4())
    session_id = str(uuid4())
    source_id = str(uuid4())
    response1, _, event_id, profile_id = _make_event(event_type, session_id=session_id, source_id=source_id)
    response2, _, event_id1, profile_id1 = _make_event(event_type, session_id=session_id, source_id=source_id)

    try:
        # 2nd profile is not saved
        assert profile_id1 == profile_id1

        response = endpoint.get(f'/events/by_type/profile/{profile_id}')
        assert response.status_code == 200
        result = response.json()

        assert result['total'] >= 0
        assert 'aggregations' in result
        assert 'by_type' in result['aggregations']
        aggregation = dict(result['aggregations']['by_type'][0])
        assert event_type in aggregation
        assert aggregation[event_type] >= 2

    finally:
        assert endpoint.delete(f'/event/{event_id}').status_code == 200
        assert endpoint.delete(f'/event/{event_id1}').status_code == 200
        assert endpoint.get('/events/refresh').status_code == 200

        assert endpoint.delete(f'/event-source/{source_id}').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200
        assert endpoint.get('/profiles/refresh').status_code == 200

        assert endpoint.delete(f'/session/{session_id}').status_code == 200


def test_should_return_events_by_type():
    response = endpoint.get(f'/events/by_type')
    assert response.status_code == 200
    result = response.json()

    assert isinstance(result, list)

    event_type = str(uuid4())
    session_id = str(uuid4())
    source_id = str(uuid4())
    response, _, event_id, profile_id = _make_event(event_type, session_id=session_id, source_id=source_id)
    response, _, event_id1, profile_id1 = _make_event(event_type, session_id=session_id, source_id=source_id)

    try:
        response = endpoint.get(f'/events/by_type')
        assert response.status_code == 200
        result = response.json()
        result = {item['name']: item['value'] for item in result}
        assert event_type in result
        assert result[event_type] >= 2
    finally:
        assert endpoint.delete(f'/event/{event_id}').status_code == 200
        assert endpoint.delete(f'/event/{event_id1}').status_code == 200
        assert endpoint.get('/events/refresh').status_code == 200

        assert endpoint.delete(f'/event-source/{source_id}').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200
        assert endpoint.get('/profiles/refresh').status_code == 200

        assert endpoint.delete(f'/session/{session_id}').status_code == 200


def test_should_return_events_by_tag():
    response = endpoint.get(f'/events/by_tag')
    assert response.status_code == 200
    result = response.json()

    assert isinstance(result, list)

    event_type = str(uuid4())
    event_tag = str(uuid4())
    session_id = str(uuid4())
    source_id = str(uuid4())
    response, _, event_id, profile_id = _make_event(event_type, session_id=session_id, source_id=source_id)
    response, _, event_id1, profile_id1 = _make_event(event_type, session_id=session_id, source_id=source_id)

    data = {
        "id": str(uuid4()),
        "name": "test",
        "event_type": event_type,
        "tags": [event_tag]
    }
    response = endpoint.post("/event-type/management", data)
    assert response.status_code == 200
    sleep(1)
    response = endpoint.get("/events/refresh")
    assert response.status_code == 200

    try:
        response = endpoint.get(f'/events/by_tag')
        assert response.status_code == 200
        result = response.json()
        result = {item['name']: item['value'] for item in result}
        assert event_tag in result
        assert result[event_tag] >= 1

    finally:
        response = endpoint.delete(f'/event/{event_id}')
        assert response.status_code == 200
        response = endpoint.delete(f'/event/{event_id1}')
        assert response.status_code == 200
        assert endpoint.get('/events/refresh').status_code == 200

        assert endpoint.delete(f"/event-tag/{event_tag}").status_code in [200, 404]

        assert endpoint.delete(f'/event-source/{source_id}').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200
        assert endpoint.get('/profiles/refresh').status_code == 200

        assert endpoint.delete(f'/session/{session_id}').status_code == 200


def test_should_return_events_by_status():
    response = endpoint.get(f'/events/by_status')
    assert response.status_code == 200
    result = response.json()

    assert isinstance(result, list)

    event_type = str(uuid4())
    session_id = str(uuid4())
    source_id = str(uuid4())
    response, _, event_id, profile_id = _make_event(event_type, session_id=session_id, source_id=source_id)
    response, _, event_id1, profile_id1 = _make_event(event_type, session_id=session_id, source_id=source_id)

    try:
        response = endpoint.get(f'/events/by_status')
        assert response.status_code == 200
        result = response.json()
        result = {item['name']: item['value'] for item in result}
        assert 'collected' in result
        assert result['collected'] >= 2
    finally:
        response = endpoint.delete(f'/event/{event_id}')
        assert response.status_code == 200
        assert endpoint.delete(f'/event/{event_id1}').status_code == 200
        assert endpoint.get('/events/refresh').status_code == 200

        assert endpoint.delete(f'/event-source/{source_id}').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200
        assert endpoint.get('/profiles/refresh').status_code == 200

        assert endpoint.delete(f'/session/{session_id}').status_code == 200


def test_should_return_events_by_source():
    response = endpoint.get(f'/events/by_source?buckets_size=100')
    assert response.status_code == 200
    result = response.json()

    assert isinstance(result, list)

    event_type = str(uuid4())
    session_id = str(uuid4())
    source_id = str(uuid4())
    response, _, event_id, profile_id = _make_event(event_type, session_id=session_id, source_id=source_id)
    response, _, event_id1, profile_id1 = _make_event(event_type, session_id=session_id, source_id=source_id)

    try:
        response = endpoint.get(f'/events/by_source?buckets_size=100')
        assert response.status_code == 200
        result = response.json()
        result = {item['name']: item['value'] for item in result}
        assert source_id in result
        assert result[source_id] >= 2
    finally:
        assert endpoint.delete(f'/event/{event_id}').status_code == 200
        assert endpoint.delete(f'/event/{event_id1}').status_code == 200
        assert endpoint.get('/events/refresh').status_code == 200

        assert endpoint.delete(f'/event-source/{source_id}').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200

        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200
        assert endpoint.get('/profiles/refresh').status_code == 200

        assert endpoint.delete(f'/session/{session_id}').status_code == 200


def test_should_return_debug_info():
    event_type = str(uuid4())
    session_id = str(uuid4())
    source_id = str(uuid4())
    response, _, event_id, profile_id = _make_event(event_type, session_id=session_id, source_id=source_id)

    try:
        response = endpoint.get(f'/event/debug/{event_id}')
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, list)
    finally:
        assert endpoint.delete(f'/event-source/{source_id}').status_code == 200
        assert endpoint.delete(f'/event/{event_id}').status_code == 200
        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200
        assert endpoint.delete(f'/session/{session_id}').status_code == 200

        assert endpoint.get('/events/refresh').status_code == 200
        assert endpoint.get('/profiles/refresh').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200
        assert endpoint.get('/sessions/refresh').status_code == 200


def test_should_return_event_console_log():
    event_type = str(uuid4())
    session_id = str(uuid4())
    source_id = str(uuid4())
    response, _, event_id, profile_id = _make_event(event_type, session_id=session_id, source_id=source_id)

    try:
        response = endpoint.get(f'/event/logs/{event_id}')
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, dict)
        assert 'result' in result
        assert 'total' in result
    finally:
        assert endpoint.delete(f'/event-source/{source_id}').status_code == 200
        assert endpoint.delete(f'/event/{event_id}').status_code == 200
        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200
        assert endpoint.delete(f'/session/{session_id}').status_code == 200

        assert endpoint.get('/events/refresh').status_code == 200
        assert endpoint.get('/profiles/refresh').status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200
        assert endpoint.get('/sessions/refresh').status_code == 200


# ---------------

def test_should_return_event_histogram_data():
    response = endpoint.post(
        '/event/select/histogram',
        data={"minDate": {"absolute": None, "delta": {"type": "minus", "value": -1, "entity": "month"}, "now": None},
              "maxDate": {"absolute": None, "delta": None},
              "where": "",
              "limit": 30})
    result = response.json()
    assert 'total' in result


def test_should_return_event_range_data_ok():
    response = endpoint.post(
        '/event/select/range/page/0',
        data={"minDate": {"absolute": None, "delta": {"type": "minus", "value": -1, "entity": "month"}, "now": None},
              "maxDate": {"absolute": None, "delta": None},
              "where": "",
              "limit": 30})
    result = response.json()
    assert 'total' in result


def test_should_return_event_select_data_ok():
    result = endpoint.post('/event/select', data={})
    result = result.json()
    assert 'total' in result
    assert 'result' in result


def test_should_return_event_select_limit_data_ok():
    result = endpoint.post('/event/select', data={"limit": 4})
    result = result.json()
    assert 'total' in result
    assert 'result' in result

    assert isinstance(result['result'], list)
    assert isinstance(result['total'], int)
    assert len(result['result']) <= 4


def test_should_response_404_none():
    response = endpoint.get('/event/does-not-exist')
    result = response.json()
    assert response.status_code == 404
    assert result is None


def test_should_get_one_event():
    event_type = str(uuid4())
    session_id = str(uuid4())
    source_id = str(uuid4())
    response, payload, event_id, profile_id = _make_event(event_type, session_id=session_id, source_id=source_id)

    try:
        response = endpoint.get(f'/event/{event_id}')
        assert response.status_code == 200
        result = response.json()

        if tracardi.track_debug:
            assert result['event']['id'] == event_id
            assert result['event']['profile']['id'] == profile_id
        assert result['event']['properties'] == payload['events'][0]['properties']
        assert result['event']['type'] == payload['events'][0]['type']
    finally:
        response = endpoint.delete(f'/event/{event_id}')
        assert response.status_code == 200
        assert endpoint.get('/events/refresh').status_code == 200
        response = endpoint.delete(f'/event-source/{source_id}')
        assert response.status_code == 200
        assert endpoint.get('/event-sources/refresh').status_code == 200
        assert endpoint.delete(f'/profile/{profile_id}').status_code == 200
        assert endpoint.get('/profiles/refresh').status_code == 200

        assert endpoint.delete(f'/session/{session_id}').status_code == 200
