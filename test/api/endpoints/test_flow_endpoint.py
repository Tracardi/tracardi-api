import json
from uuid import uuid4

from tracardi.process_engine.action.v1.flow.start.start_action import StartAction

from tracardi.domain.flow import Flow
from tracardi.process_engine.action.v1.end_action import EndAction
from tracardi.service.wf.domain.debug_info import DebugInfo
from tracardi.service.wf.service.builders import action

from test.utils import Endpoint

endpoint = Endpoint()


def _create_flow(id, name, desc):
    data = {
        "id": id,
        "name": name,
        "description": desc,
        "enabled": True,
        "tags": [
            "General", "Test"
        ],
        "draft": "",
        "production": "",
        "lock": False
    }

    return endpoint.post('/flow/metadata', data=data)


def test_should_return_404_on_get_flow_if_none():
    flow_id = str(uuid4())
    response = endpoint.get(f'/flow/draft/{flow_id}')
    assert response.status_code == 404
    assert response.json() is None


def test_should_return_404_on_delete_flow_if_none():
    flow_id = str(uuid4())
    response = endpoint.delete(f'/flow/{flow_id}')
    assert response.status_code == 404
    assert response.json() is None


def test_should_refresh_flow():
    assert endpoint.get('/flows/refresh').status_code == 200


def test_should_not_fail_on_rearrange():
    data = Flow(id=str(uuid4()), name="test", type='collection')
    assert endpoint.post('/flow/draft/nodes/rearrange', data=json.loads(data.model_dump_json())).status_code == 200


def check_flow_bool(id, lock, type='lock', field='lock'):
    on_off = 'yes' if lock else 'no'

    response = endpoint.get(f'/flow/{id}/{type}/{on_off}')
    assert response.status_code == 200
    result = response.json()
    assert result == {'saved': 1, 'errors': [], 'ids': [id]}

    # flush data to elastic
    assert endpoint.get('/flows/refresh').status_code == 200

    # read flow
    response = endpoint.get(f'/flow/metadata/{id}')
    assert response.status_code == 200
    if response.status_code == 200:
        result = response.json()
        assert result[field] is lock
    else:
        raise Exception("Could not read flow id {}".format(id))


def test_should_load_flows():
    result = endpoint.get('/flows')
    result = result.json()
    assert 'total' in result
    assert 'result' in result


def test_should_create_flow():
    id = str(uuid4())

    try:
        # delete flow
        assert endpoint.delete(f'/flow/{id}').status_code in [200, 404]

        # add flow

        response = _create_flow(id, "Test flow", "Opis")
        assert {'saved': 1, 'errors': [], 'ids': [id]} == response.json()

        # flush data to elastic
        assert endpoint.get('/flows/refresh').status_code == 200

        # read saved flow

        response = endpoint.get(f'/flow/metadata/{id}')
        assert response.status_code == 200
        if response.status_code == 200:
            result = response.json()
            assert result['id'] == id
            assert result['name'] == 'Test flow'

            # delete flow
            assert endpoint.delete(f'/flow/{id}').status_code == 200

            # flush data to elastic
            assert endpoint.get('/flows/refresh').status_code == 200

            # response = endpoint.get(f'/flow/metadata/{id}')
            # print(response.content)
            # check if do not exist
            assert endpoint.get(f'/flow/metadata/{id}').status_code == 404

    finally:
        assert endpoint.delete(f'/flow/{id}').status_code in [200, 404]
        assert endpoint.get('/flows/refresh').status_code == 200


def test_get_flow_ok():
    id = str(uuid4())

    # delete flow
    assert endpoint.delete(f'/flow/{id}').status_code in [200, 404]

    # flush data to elastic
    assert endpoint.get('/flows/refresh').status_code == 200

    # check if do not exist
    assert endpoint.get(f'/flow/draft/{id}').status_code == 404
    assert endpoint.get(f'/flow/production/{id}').status_code == 404


def test_should_update_flow_metadata():
    id = str(uuid4())

    try:
        # delete flow
        assert endpoint.delete(f'/flow/{id}').status_code in [200, 404]

        # flush data to elastic
        assert endpoint.get('/flows/refresh').status_code == 200

        # create flow
        response = _create_flow(id, "Test flow", "Opis")
        assert response.status_code == 200
        result = response.json()
        assert result == {'saved': 1, 'errors': [], 'ids': [id]}

        # flush data to elastic
        assert endpoint.get('/flows/refresh').status_code == 200

        response = endpoint.get(f'/flow/production/{id}')
        assert response.status_code == 200
        if response.status_code == 200:
            result = response.json()
            assert result['id'] == id
            assert result['name'] == 'Test flow'
        else:
            raise Exception("Could not read flow")

        response = endpoint.get(f'/flow/draft/{id}')
        assert response.status_code == 200
        if response.status_code == 200:
            result = response.json()
            assert result['id'] == id
            assert result['name'] == 'Test flow'
        else:
            raise Exception("Could not read flow")

        response = endpoint.post('/flow/metadata', data={
            "id": id,
            "name": "New name",
            "description": "New Description",
            "enabled": False,
            "tags": [
                "New"
            ]
        })

        result = response.json()
        assert response.status_code == 200
        assert result == {'saved': 1, 'errors': [], 'ids': [id]}

        # flush data to elastic
        assert endpoint.get('/flows/refresh').status_code == 200

        # get updated flow

        response = endpoint.get(f'/flow/metadata/{id}')
        assert response.status_code == 200
        if response.status_code == 200:
            result = response.json()
            assert result['id'] == id
            assert result['name'] == 'New name'
            assert result['description'] == 'New Description'
            assert "New" in result['tags']
        else:
            raise Exception("Could not read flow")

    finally:
        assert endpoint.delete(f'/flow/{id}').status_code in [200, 404]


def test_should_enable_flow_lock():
    id = str(uuid4())

    try:
        assert endpoint.delete(f'/flow/{id}').status_code == 404

        # create flow
        response = _create_flow(id, "Test flow", "Opis")
        assert response.status_code == 200

        # read flow
        check_flow_bool(id, True, type='lock', field='lock')
        check_flow_bool(id, False, type='lock', field='lock')

    finally:
        assert endpoint.delete(f'/flow/{id}').status_code in [200, 404]


# todo flow delete deletes also rules.


def test_flow_code_api():
    id = str(uuid4())

    try:

        # Add event

        start = action(StartAction)
        end = action(EndAction)

        flow = Flow.build("Test wf as a code", id=id)
        flow += start('payload') >> end('payload')

        response = endpoint.post('/flow/draft', data=flow.model_dump())
        assert response.status_code == 200
        result = response.json()
        assert result['saved'] == 1
        assert id in result['ids']

    finally:
        assert endpoint.delete(f'/flow/{id}').status_code in [200, 404]


def test_should_save_draft_metadata():
    flow_id = None
    try:
        flow_id = str(uuid4())
        response = _create_flow(flow_id, "Test flow", "Opis")
        assert response.status_code == 200

        payload = {
            "id": flow_id,
            "name": "string",
            "description": "string",
            "enabled": True,
            "tags": [
                "General"
            ]
        }
        assert endpoint.post('/flow/draft/metadata', data=payload).status_code == 200
        assert endpoint.get('/flows/refresh').status_code == 200

        response = endpoint.get(f'/flow/draft/{flow_id}')
        assert response.status_code == 200
        result = response.json()
        assert result['name'] == payload['name']
    finally:
        if flow_id:
            assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]


def test_should_not_make_production_flow_out_of_missing_workflow():
    flow_id = str(uuid4())
    start = action(StartAction)
    end = action(EndAction)

    flow = Flow.build("Workflow", id=flow_id)
    flow += start('payload') >> end('payload')

    response = endpoint.post('/flow/production', data=flow.model_dump())
    assert response.status_code == 406


def test_should_restore_production_flow():
    flow_id = str(uuid4())

    try:
        start = action(StartAction)
        end1 = action(EndAction)
        end2 = action(EndAction)

        flow = Flow.build("Workflow", id=flow_id)
        flow += start('payload') >> end1('payload')

        # Make draft
        assert endpoint.post('/flow/draft', data=flow.model_dump()).status_code == 200

        # Make production

        assert endpoint.post('/flow/production', data=flow.model_dump()).status_code == 200

        # Change draft
        flow1 = Flow.build("Workflow changed", id=flow_id)
        flow1 += start('payload') >> end1('payload')
        flow1 += start('payload') >> end2('payload')

        # Rearrange

        response = endpoint.post('/flow/draft/nodes/rearrange', data=json.loads(flow1.model_dump_json()))
        assert response.status_code == 200
        rearranged_flow = response.json()

        # Save

        assert endpoint.post('/flow/draft', data=rearranged_flow).status_code == 200

        # Make production

        assert endpoint.post('/flow/production', data=flow1.model_dump()).status_code == 200

        # Get production

        response = endpoint.get(f'/flow/production/{flow_id}')
        assert response.status_code == 200
        result = response.json()
        assert len(result['flowGraph']['nodes']) == 3

        # Restore production

        response = endpoint.get(f'/flow/production/{flow_id}/restore')
        assert response.status_code == 200

        result = response.json()

        assert len(result['flowGraph']['nodes']) == 2

    finally:
        assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]


def test_should_not_restore_draft_from_production_if_no_production():
    flow_id = str(uuid4())

    try:
        start = action(StartAction)
        end1 = action(EndAction)
        end2 = action(EndAction)

        flow = Flow.build("Workflow", id=flow_id)
        flow += start('payload') >> end1('payload')

        # Make draft

        assert endpoint.post('/flow/draft', data=flow.model_dump()).status_code == 200

        # Get draft

        response = endpoint.get(f'/flow/draft/{flow_id}')
        assert response.status_code == 200
        result = response.json()
        assert len(result['flowGraph']['nodes']) == 2

        # Change draft

        flow1 = Flow.build("Workflow changed", id=flow_id)
        flow1 += start('payload') >> end1('payload')
        flow1 += start('payload') >> end2('payload')

        assert endpoint.post('/flow/draft', data=flow1.model_dump()).status_code == 200

        # Check if draft changed

        response = endpoint.get(f'/flow/draft/{flow_id}')
        assert response.status_code == 200
        result = response.json()
        assert len(result['flowGraph']['nodes']) == 3

        # Restore draft

        response = endpoint.get(f'/flow/draft/{flow_id}/restore')

        # No production

        assert response.status_code == 406

    finally:
        assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]


def test_should_restore_draft_from_production_flow():
    flow_id = str(uuid4())

    try:
        start = action(StartAction)
        end1 = action(EndAction)
        end2 = action(EndAction)

        flow = Flow.build("Workflow", id=flow_id)
        flow += start('payload') >> end1('payload')

        # Make draft

        assert endpoint.post('/flow/draft', data=flow.model_dump()).status_code == 200

        # Make production

        assert endpoint.post('/flow/production', data=flow.model_dump()).status_code == 200

        # Get draft

        response = endpoint.get(f'/flow/draft/{flow_id}')
        assert response.status_code == 200
        result = response.json()
        assert len(result['flowGraph']['nodes']) == 2

        # Change draft

        flow1 = Flow.build("Workflow changed", id=flow_id)
        flow1 += start('payload') >> end1('payload')
        flow1 += start('payload') >> end2('payload')

        assert endpoint.post('/flow/draft', data=flow1.model_dump()).status_code == 200

        # Check if draft changed

        response = endpoint.get(f'/flow/draft/{flow_id}')
        assert response.status_code == 200
        result = response.json()
        assert len(result['flowGraph']['nodes']) == 3

        # Restore draft

        response = endpoint.get(f'/flow/draft/{flow_id}/restore')
        assert response.status_code == 200

        # Check if restored

        result = response.json()

        assert len(result['flowGraph']['nodes']) == 2

    finally:
        assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]


def test_should_not_create_draft_metadata_if_flow_missing():
    flow_id = str(uuid4())
    data = {
        "id": flow_id,
        "name": "test WF",
        "description": "test WF",
        "enabled": True,
        "tags": [
            "General", "Test"
        ],
        "draft": "",
        "production": "",
        "lock": False
    }

    response = endpoint.post('/flow/draft/metadata', data=data)
    assert response.status_code == 404


def test_should_create_draft_metadata():
    flow_id = str(uuid4())

    try:
        data = {
            "id": flow_id,
            "name": "test WF",
            "description": "test WF",
            "enabled": True,
            "tags": [
                "General", "Test"
            ],
            "draft": "",
            "production": "",
            "lock": False
        }

        assert endpoint.post('/flow/metadata', data=data).status_code == 200

        data['name'] = 'changed'
        response = endpoint.post('/flow/draft/metadata', data=data)
        assert response.status_code == 200

        # Get flow draft

        response = endpoint.get(f'/flow/draft/{flow_id}')
        assert response.status_code == 200
        result = response.json()
        assert result['name'] == 'changed'
    finally:
        assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]


def test_should_lock_workflow():
    def _lock(state, expect):
        response = endpoint.get(f"/flow/{flow_id}/lock/{state}")
        assert response.status_code == 200
        result = response.json()
        assert result['saved'] == 1
        assert result['ids'][0] == flow_id

        response = endpoint.get(f'/flow/draft/{flow_id}')
        assert response.status_code == 200
        result = response.json()
        assert result['lock'] is expect

    flow_id = str(uuid4())

    try:
        _create_flow(flow_id, "Test flow", "Opis")

        # Lock

        _lock('yes', expect=True)

        # UnLock

        _lock('no', expect=False)

    finally:
        assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]


def test_should_debug_workflow():
    flow_id = str(uuid4())

    try:
        start = action(StartAction)
        end = action(EndAction)

        flow = Flow.build("Workflow", id=flow_id)
        flow += start('payload') >> end('payload')

        # Make draft

        assert endpoint.post('/flow/draft', data=flow.model_dump()).status_code == 200

        response = endpoint.post('/flow/debug', data=flow.model_dump())
        assert response.status_code == 200
        result = response.json()
        assert 'logs' in result
        assert isinstance(result['logs'], list)
        assert 'debugInfo' in result
        DebugInfo(**result['debugInfo'])

    finally:
        assert endpoint.delete(f'/flow/{flow_id}').status_code in [200, 404]
