from ..utils import Endpoint

endpoint = Endpoint()


def test_create_and_delete_segment():
    segment_id = "segment-id"
    try:
        response = endpoint.post('/segment', data={
            "id": segment_id,
            "name": "Test segment",
            "condition": "profile@stat.views>0",
            "eventType": 'my-event'
        })

        assert response.status_code == 200

    finally:
        assert endpoint.delete(f'/segment/{segment_id}').status_code in [200, 404]
