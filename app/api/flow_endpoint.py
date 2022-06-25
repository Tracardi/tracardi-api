import asyncio
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, Response
from tracardi.domain.enum.production_draft import ProductionDraft
from tracardi.domain.event_metadata import EventMetadata, EventTime
from tracardi.exceptions.exception import StorageException
from tracardi.domain.console import Console
from tracardi.service.secrets import encrypt
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor
from tracardi.service.wf.domain.flow_history import FlowHistory
from tracardi.service.wf.domain.work_flow import WorkFlow
from tracardi.service.plugin.domain.console import Log
from tracardi.domain.flow_meta_data import FlowMetaData
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event, EventSession
from tracardi.domain.flow import Flow
from tracardi.service.wf.domain.flow import Flow as GraphFlow
from tracardi.domain.flow import FlowRecord
from tracardi.domain.profile import Profile
from tracardi.domain.rule import Rule
from tracardi.domain.session import Session, SessionMetadata
from tracardi.domain.resource import Resource
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from .auth.permissions import Permissions
from ..config import server

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/flows/refresh", tags=["flow"], include_in_schema=server.expose_gui_api)
async def flow_refresh():
    return await storage.driver.flow.refresh()


@router.post("/flow/draft", tags=["flow"], response_model=BulkInsertResult, include_in_schema=server.expose_gui_api)
async def upsert_flow_draft(draft: Flow):
    """
    Creates draft of workflow. If there is production version of the workflow it stays intact.
    """
    try:

        # Frontend edge-id is long. Save space and md5 it.

        if draft.flowGraph is not None:
            draft.flowGraph.shorten_edge_ids()

        # Check if origin flow exists

        flow_record = await storage.driver.flow.load_record(draft.id)  # type: FlowRecord

        if flow_record is None:
            flow_record = draft.get_empty_workflow_record()

        flow_record.draft = encrypt(draft.dict())

        return await storage.driver.flow.save_record(flow_record)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/draft/{id}", tags=["flow"], response_model=Optional[Flow], include_in_schema=server.expose_gui_api)
async def load_flow_draft(id: str, response: Response):

    """
    Loads draft version of flow with given ID (str)
    """
    try:
        flow_record = await storage.driver.flow.load_record(id)  # type: FlowRecord
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if flow_record is None:
        response.status_code = 404
        return None

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
async def get_flow(id: str, response: Response):
    """
    Returns production version of flow with given ID (str)
    """
    try:
        flow_record = await storage.driver.flow.load_record(id)  # type: FlowRecord
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if flow_record is None:
        response.status_code = 404
        return None

    try:
        if flow_record.production:
            return flow_record.get_production_workflow()

        return flow_record.get_empty_workflow(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/{production_draft}/{id}/restore", tags=["flow"], response_model=Flow,
            include_in_schema=server.expose_gui_api)
async def restore_production_flow_backup(id: str, production_draft: ProductionDraft):
    """
    Returns previous version of production flow with given ID (str)
    """
    try:
        flow_record = await storage.driver.flow.load_record(id)  # type: FlowRecord
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if flow_record is None:
        raise HTTPException(status_code=404, detail="Flow id: `{}` does not exist.".format(id))

    try:

        if production_draft.value == ProductionDraft.production:
            flow_record.restore_production_from_backup()
        else:
            flow_record.restore_draft_from_production()

        result = await storage.driver.flow.save_record(flow_record)
        if result.saved == 1:
            if production_draft.value == ProductionDraft.production:
                return flow_record.get_production_workflow()
            return flow_record.get_draft_workflow()

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
    """
    Returns flow metadata of flow with given ID (str)
    """
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

    """
    Adds new flow metadata for flow with given id (str)
    """
    try:
        entity = Entity(id=flow_metadata.id)
        flow_record = await StorageFor(entity).index("flow").load(FlowRecord)  # type: FlowRecord
        if flow_record is None:

            # create new

            flow_record = FlowRecord(**flow_metadata.dict())
            flow_record.draft = encrypt(Flow(
                id = flow_metadata.id,
                name= flow_metadata.name,
                description= flow_metadata.description
            ).dict())
            flow_record.production = encrypt(Flow(
                id=flow_metadata.id,
                name=flow_metadata.name,
                description=flow_metadata.description
            ).dict())

        else:

            # update

            draft_flow = flow_record.get_draft_workflow()
            draft_flow.name = flow_metadata.name
            flow_record.draft = encrypt(draft_flow.dict())

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
    """
    Adds new draft metadata to flow with defined ID (str)
    """
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

            flow_record.draft = encrypt(draft_workflow.dict())

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

        flow_record.set_lock(True if lock.lower() == 'yes' else False)
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

        flow_record.set_enabled(True if lock.lower() == 'yes' else False)
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
        session = Session(id="@debug-session-id", metadata=SessionMetadata())
        event_session = EventSession(
            id=session.id,
            start=session.metadata.time.insert,
            duration=session.metadata.time.duration
        )
        session.operation.new = True

        event = Event(
            metadata=EventMetadata(time=EventTime()),
            id='@debug-event-id',
            type="@debug-event-type",
            source=Resource(id="@debug-source-id", type="web-page"),
            session=event_session,
            profile=profile,
            context={}
        )

        workflow = WorkFlow(
            FlowHistory(history=[])
        )

        ux = []

        debug_info, log_list, event, profile, session = await workflow.invoke(flow, event, profile, session, ux, debug=True)

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
                    message=log.message,
                    traceback=log.traceback
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
            "update": profile_save_result,
            "ux": ux
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/flow/{id}", tags=["flow"], response_model=dict, include_in_schema=server.expose_gui_api)
async def delete_flow(id: str, response: Response):
    """
    Deletes flow with given id (str)
    """
    try:
        # delete rule before flow
        crud = StorageFor.crud('rule', Rule)
        rule_delete_result = await crud.delete_by('flow.id.keyword', id)

        flow = Entity(id=id)
        flow_delete_result = await StorageFor(flow).index("flow").delete()

        if flow_delete_result is None:
            response.status_code = 404
            return None

        await storage.driver.flow.refresh()

        return {
            "rule": rule_delete_result,
            "flow": flow_delete_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
