from ..utils import Endpoint

endpoint = Endpoint()


def test_event_histogram_data_ok():
    result = endpoint.post('/event/select/histogram')
    result = result.json()
    print(result)


def test_event_range_data_ok():
    result = endpoint.post('/event/select/range')
    result = result.json()
    print(result)


def test_event_select_data_ok():
    result = endpoint.post('/event/select', data={})
    result = result.json()
    assert 'total' in result
    assert 'result' in result
