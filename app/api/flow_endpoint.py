import asyncio
from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from tracardi.exceptions.exception import StorageException
from tracardi.domain.console import Console
from tracardi.service.secrets import encrypt
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor
from tracardi_graph_runner.domain.flow_history import FlowHistory
from tracardi_graph_runner.domain.work_flow import WorkFlow
from tracardi_plugin_sdk.domain.console import Log
from .auth.authentication import get_current_user
from tracardi.domain.context import Context
from tracardi.domain.flow_meta_data import FlowMetaData
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.flow import Flow
from tracardi_graph_runner.domain.flow import Flow as GraphFlow
from tracardi.domain.flow import FlowRecord
from tracardi.domain.profile import Profile
from tracardi.domain.rule import Rule
from tracardi.domain.session import Session
from tracardi.domain.resource import Resource
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from ..config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/flow/metadata/refresh", tags=["flow"], include_in_schema=server.expose_gui_api)
async def flow_refresh():
    return await storage.driver.flow.refresh()


@router.get("/flow/metadata/flush", tags=["flow"], include_in_schema=server.expose_gui_api)
async def flow_flush():
    return await storage.driver.flow.flush()


@router.post("/flow/draft", tags=["flow"], response_model=BulkInsertResult, include_in_schema=server.expose_gui_api)
async def upsert_flow_draft(draft: Flow):
    """
    Creates draft of workflow. If there is production version of the workflow it stays intact.
    """
    try:

        # Frontend edge id is log. Save space and md5 it.

        if draft.flowGraph is not None:
            draft.flowGraph.shorten_edge_ids()

        # Check if origin flow exists

        entity = Entity(id=draft.id)
        flow_record = await StorageFor(entity).index('flow').load(FlowRecord)  # type: FlowRecord

        if flow_record is None:
            flow_record = draft.get_empty_workflow_record()

        flow_record.draft = encrypt(draft.dict())

        return await StorageFor(flow_record).index().save()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/draft/{id}", tags=["flow"], response_model=Flow, include_in_schema=server.expose_gui_api)
async def load_flow_draft(id: str):
    try:
        entity = Entity(id=id)
        flow_record = await StorageFor(entity).index('flow').load(FlowRecord)  # type: FlowRecord
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if flow_record is None:
        raise HTTPException(status_code=404, detail="Workflow `{}` does not exists.".format(id))

    try:
        # Return draft if exists
        if flow_record.draft:
            return flow_record.get_draft_workflow()

        # Fallback to production version
        if flow_record.production:
            return flow_record.get_production_workflow()

        return flow_record.get_empty_workflow(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/production/{id}", tags=["flow"], response_model=Flow, include_in_schema=server.expose_gui_api)
async def get_flow(id: str):
    try:
        flow = Entity(id=id)
        flow_record = await StorageFor(flow).index("flow").load(FlowRecord)  # type: FlowRecord
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if flow_record is None:
        raise HTTPException(status_code=404, detail="Flow id: `{}` does not exist.".format(id))

    try:
        if flow_record.production:
            return flow_record.get_production_workflow()

        return flow_record.get_empty_workflow(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flow/production", tags=["flow"], response_model=BulkInsertResult,
             include_in_schema=server.expose_gui_api)
async def upsert_flow(flow: Flow):
    """
        Creates production version of workflow. If there is a draft version of the workflow it is overwritten
        by the production version. This may be the subject to change.
    """
    try:
        old_flow_record = await storage.driver.flow.load_record(flow.id)
        flow_record = flow.get_production_workflow_record()
        flow_record.backup = old_flow_record.production
        return await StorageFor(flow_record).index().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/metadata/{id}", tags=["flow"], response_model=FlowRecord, include_in_schema=server.expose_gui_api)
async def get_flow_details(id: str):
    try:
        entity = Entity(id=id)
        flow_record = await StorageFor(entity).index("flow").load(FlowRecord)  # type: FlowRecord
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if flow_record is None:
        raise HTTPException(status_code=404, detail="Missing flow record {}".format(id))

    return flow_record


@router.post("/flow/metadata", tags=["flow"], response_model=BulkInsertResult, include_in_schema=server.expose_gui_api)
async def upsert_flow_details(flow_metadata: FlowMetaData):
    try:
        entity = Entity(id=flow_metadata.id)
        flow_record = await StorageFor(entity).index("flow").load(FlowRecord)  # type: FlowRecord
        if flow_record is None:
            flow_record = FlowRecord(**flow_metadata.dict())
        else:
            flow_record.name = flow_metadata.name
            flow_record.description = flow_metadata.description
            flow_record.enabled = flow_metadata.enabled
            flow_record.projects = flow_metadata.projects

        return await StorageFor(flow_record).index().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flow/draft/metadata", tags=["flow"], response_model=BulkInsertResult,
             include_in_schema=server.expose_gui_api)
async def upsert_flow_details(flow_metadata: FlowMetaData):
    try:
        entity = Entity(id=flow_metadata.id)
        flow_record = await StorageFor(entity).index("flow").load(FlowRecord)  # type: FlowRecord

        if flow_record is None:
            raise ValueError("Flow `{}` does not exist.".format(flow_metadata.id))

        flow_record.enabled = flow_metadata.enabled
        flow_record.name = flow_metadata.name
        flow_record.description = flow_metadata.description
        flow_record.projects = flow_metadata.projects

        if flow_record.draft:
            draft_workflow = flow_record.get_draft_workflow()

            draft_workflow.name = flow_metadata.name
            draft_workflow.description = flow_metadata.description
            draft_workflow.enabled = flow_metadata.enabled
            draft_workflow.projects = flow_metadata.projects

            flow_record.production = encrypt(draft_workflow.dict())

        return await StorageFor(flow_record).index().save()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/{id}/lock/{lock}", tags=["flow"],
            response_model=BulkInsertResult,
            include_in_schema=server.expose_gui_api)
async def update_flow_lock(id: str, lock: str):
    try:
        entity = Entity(id=id)
        flow_record = await StorageFor(entity).index("flow").load(FlowRecord)  # type: FlowRecord

        if flow_record is None:
            raise ValueError("Flow `{}` does not exist.".format(id))

        flow_record.lock = True if lock.lower() == 'yes' else False
        return await StorageFor(flow_record).index().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/{id}/enable/{lock}", tags=["flow"],
            response_model=BulkInsertResult,
            include_in_schema=server.expose_gui_api)
async def update_flow_lock(id: str, lock: str):
    try:
        entity = Entity(id=id)
        flow_record = await StorageFor(entity).index("flow").load(FlowRecord)  # type: FlowRecord

        if flow_record is None:
            raise ValueError("Flow `{}` does not exist.".format(id))

        flow_record.enabled = True if lock.lower() == 'yes' else False
        return await StorageFor(flow_record).index().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flow/debug", tags=["flow"],
             include_in_schema=server.expose_gui_api)
async def debug_flow(flow: GraphFlow):
    """
        Debugs flow sent in request body
    """
    try:

        profile = Profile(id="@debug-profile-id")
        session = Session(id="@debug-session-id")
        session.operation.new = True
        event = Event(
            id='@debug-event-id',
            type="@debug-event-type",
            source=Resource(id="@debug-source-id", type="web-page"),
            session=session,
            profile=profile,
            context=Context()
        )

        workflow = WorkFlow(
            FlowHistory(history=[]),
            session,
            profile
        )
        debug_info, log_list, event = await workflow.invoke(flow, event, debug=True)

        console_log = []  # type: List[Console]
        profile_save_result = None
        try:
            # Store logs in one console log
            for log in log_list:  # type: Log
                console = Console(
                    origin="node",
                    event_id=event.id,
                    flow_id=flow.id,
                    module=log.module,
                    class_name=log.class_name,
                    type=log.type,
                    message=log.message
                )
                console_log.append(console)

            if profile.operation.needs_update():
                profile_save_result = await StorageFor(profile).index().save()

        except StorageException as e:
            console = Console(
                origin="profile",
                event_id=event.id,
                flow_id=flow.id,
                module='tracardi_api.flow_endpoint',
                class_name='log.class_name',
                type='debug_flow',
                message=str(e)
            )
            console_log.append(console)

        # await console_log.bulk().save()

        return {
            'logs': [log.dict() for log in console_log],
            "debugInfo": debug_info.dict(),
            "update": profile_save_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/flow/{id}", tags=["flow"], response_model=dict, include_in_schema=server.expose_gui_api)
async def delete_flow(id: str):
    try:
        # delete rule before flow
        crud = StorageFor.crud('rule', Rule)
        rule_delete_task = asyncio.create_task(crud.delete_by('flow.id.keyword', id))

        flow = Entity(id=id)
        flow_delete_task = asyncio.create_task(StorageFor(flow).index("flow").delete())

        return {
            "rule": await rule_delete_task,
            "flow": await flow_delete_task
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
