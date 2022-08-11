from ..utils import Endpoint

endpoint = Endpoint()


def test_event_histogram_data_ok():
    response = endpoint.post(
        '/event/select/histogram',
        data={"minDate": {"absolute": None, "delta": {"type": "minus", "value": -1, "entity": "month"}, "now": None},
              "maxDate": {"absolute": None, "delta": None},
              "where": "",
              "limit": 30})
    result = response.json()
    assert 'total' in result


def test_event_range_data_ok():
    response = endpoint.post(
        '/event/select/range/page/0',
        data={"minDate": {"absolute": None, "delta": {"type": "minus", "value": -1, "entity": "month"}, "now": None},
              "maxDate": {"absolute": None, "delta": None},
              "where": "",
              "limit": 30})
    result = response.json()
    assert 'total' in result


def test_event_select_data_ok():
    result = endpoint.post('/event/select', data={})
    result = result.json()
    assert 'total' in result
    assert 'result' in result


def test_event_select_limit_data_ok():
    result = endpoint.post('/event/select', data={"limit": 4})
    result = result.json()
    assert 'total' in result
    assert 'result' in result

    assert len(result['result']) == 4


def test_should_response_404_none():
    response = endpoint.get('/event/does-not-exist')
    result = response.json()
    assert response.status_code == 404
    assert result is None
