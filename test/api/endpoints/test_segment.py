from test.utils import Endpoint
from tracardi.domain.segment import Segment

endpoint = Endpoint()


def test_create_and_delete_segment():
    segment_id = "segment-id"
    try:
        response = endpoint.post('/segment', data={
            "id": segment_id,
            "name": "Test segment",
            "condition": "profile@stat.views>0",
            "eventType": ['my-event']
        })
        assert response.status_code == 200

        assert endpoint.get('/segments/refresh').status_code == 200

        response = endpoint.get(f'/segment/{segment_id}')

        assert response.status_code == 200
        result = response.json()

        segment = Segment(**result)
        assert segment.name == 'Test segment'
        assert segment.enabled
        assert segment.eventType == ['my-event']
        assert segment.condition == "profile@stat.views>0"

        response = endpoint.get(f'/segments')
        assert response.status_code == 200
        result = response.json()

        assert result['total'] >= 1
        assert isinstance(result['grouped']['my-event'], list)

        Segment(**result['grouped']['my-event'][0])

    finally:
        assert endpoint.delete(f'/segment/{segment_id}').status_code in [200, 404]
