from uuid import uuid4

from test.utils import Endpoint
from tracardi.domain.live_segment import WorkflowSegmentationTrigger

endpoint = Endpoint()


def test_should_create_and_delete_live_segment():
    segment_id = str(uuid4())
    try:
        response = endpoint.post('/segment/live', data={
            "id": segment_id,
            "name": "Test segment",
            "enabled": True,
            "workflow": {
                "id": "1",
                "name": "test"
            }
        })
        assert response.status_code == 200

        assert endpoint.get('/segments/live/refresh').status_code == 200

        response = endpoint.get(f'/segment/live/{segment_id}')

        assert response.status_code == 200
        result = response.json()

        segment = WorkflowSegmentationTrigger(**result)
        assert segment.workflow.id == '1'
        assert segment.workflow.name == 'test'
        assert segment.name == 'Test segment'
        assert segment.enabled

        response = endpoint.get('/segments/live')
        assert response.status_code == 200
        result = response.json()

        assert result['total'] >= 1
        assert isinstance(result['grouped']['Live segmentation'], list)

        WorkflowSegmentationTrigger(**result['grouped']['Live segmentation'][0])

    finally:
        assert endpoint.delete(f'/segment/live/{segment_id}').status_code in [200, 404]

