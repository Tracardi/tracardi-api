from tracardi.service.dependency.adapters.big_data_adapter import *
from tracardi.service.collector.load.profile import load_profile
from tracardi.common.time.date import now_in_utc

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Response

from tracardi.domain.event_metadata import EventMetadata, EventPayloadMetadata
from tracardi.domain.metadata import ProfileMetadata
from tracardi.domain.payload.event_payload import EventPayload
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.domain.time import EventTime, ProfileTime, Time
from tracardi.service.wf.domain.flow_history import FlowHistory
from tracardi.service.wf.domain.work_flow import WorkFlow
from tracardi.domain.flow_meta_data import FlowMetaData
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.event_session import EventSession
from tracardi.domain.flow import Flow
from tracardi.service.wf.domain.flow_graph import FlowGraph
from tracardi.domain.flow import FlowRecord
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session, SessionMetadata, SessionTime
from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.service.storage.mysql.interface import workflow_dao
from tracardi.service.storage.mysql.interface import workflow_trigger_dao

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


async def _load_record(id: str) -> Optional[FlowRecord]:
    return await workflow_dao.load_by_id(id)


async def _upsert_flow(workflow: Flow, rearrange_nodes: Optional[bool] = False):
    """
    Creates draft of workflow. If there is production version of the workflow it stays intact.
    """
    # Frontend edge-id is long. Save space and md5 it.

    if workflow.flowGraph is not None:
        workflow.flowGraph.shorten_edge_ids()

    if rearrange_nodes is True:
        workflow.arrange_nodes()

        # Check if origin flow exists

    flow_record = await _load_record(workflow.id)  # type: FlowRecord

    if flow_record is None:
        flow_record = workflow.get_empty_workflow_record(workflow.type)

    flow_record.draft = workflow.model_dump(mode='json')
    flow_record.timestamp = now_in_utc()

    result = await workflow_dao.insert(flow_record)

    return result, flow_record


@router.post("/flow/draft/nodes/rearrange",
             tags=["flow"],
             response_model=Flow,
             include_in_schema=tracardi.expose_gui_api)
async def rearrange_flow(flow: Flow):
    """
    Rearranges the send workflow nodes.
    """

    # Frontend edge-id is long. Save space and md5 it.

    if flow.flowGraph is not None:
        flow.flowGraph.shorten_edge_ids()

    flow.arrange_nodes()

    return flow


@router.post("/flow/draft",
             tags=["flow"],
             include_in_schema=tracardi.expose_gui_api)
async def upsert_workflow(workflow: Flow, rearrange_nodes: Optional[bool] = False):
    result, flow_record = await _upsert_flow(workflow, rearrange_nodes)

    return result


@router.get("/flow/draft/{id}", tags=["flow"], response_model=Optional[Flow], include_in_schema=tracardi.expose_gui_api)
async def load_flow_draft(id: str, response: Response):
    """
    Loads draft version of flow with given ID (str)
    """

    flow_record = await _load_record(id)

    if flow_record is None:
        response.status_code = 404
        return None

    # Return draft if exists
    if flow_record.draft:
        return Flow.from_workflow_record(flow_record)

    return flow_record.get_empty_workflow(id)


@router.get("/flow/metadata/{id}",
            tags=["flow"],
            response_model=Optional[FlowRecord],
            include_in_schema=tracardi.expose_gui_api)
async def get_flow_details(id: str):
    """
    Returns flow metadata of flow with given ID (str)
    """
    flow_record = await _load_record(id)

    if flow_record is None:
        raise HTTPException(status_code=404, detail="Missing flow record {}".format(id))

    return flow_record


@router.post("/flow/metadata",
             tags=["flow"],
             include_in_schema=tracardi.expose_gui_api)
async def upsert_flow_details(flow_metadata: FlowMetaData):
    """
    Adds new flow metadata for flow with given id (str)
    """


    flow_record = await workflow_dao.load_in_current_context(flow_metadata.id)

    if flow_record is None:

        # create new

        flow_record = FlowRecord(**flow_metadata.model_dump())
        flow_record.timestamp = now_in_utc()
        flow_record.draft = Flow(
            id=flow_metadata.id,
            timestamp=flow_record.timestamp,
            name=flow_metadata.name,
            description=flow_metadata.description,
            type=flow_metadata.type
        ).model_dump(mode='json')

        return await workflow_dao.insert(flow_record)

    else:
        if isinstance(flow_record.draft, dict):

            flow_record.draft['name'] = flow_metadata.name
            flow_record.draft['description'] = flow_metadata.description
            flow_record.draft['tags'] = flow_metadata.tags

            return await workflow_dao.update_by_id(flow_metadata.id, new_data=dict(
                name=flow_metadata.name,
                description=flow_metadata.description,
                tags=",".join(flow_metadata.tags),
                type=flow_metadata.type,
                draft=flow_record.draft
            ))

        else:

            return await workflow_dao.update_by_id(flow_metadata.id, new_data=dict(
                name=flow_metadata.name,
                description=flow_metadata.description,
                tags=",".join(flow_metadata.tags),
                type=flow_metadata.type
            ))


# TODO obsolete delete
@router.post("/flow/draft/metadata", tags=["flow"],
             include_in_schema=tracardi.expose_gui_api)
async def upsert_flow_draft_details(flow_metadata: FlowMetaData):
    """
    Adds new draft metadata to flow with defined ID (str)
    """

    return await workflow_dao.update_by_id(flow_metadata.id, new_data=dict(
        name=flow_metadata.name,
        description=flow_metadata.description,
        tags=",".join(flow_metadata.tags),
        type=flow_metadata.type
    ))


@router.get("/flow/{id}/lock/{lock}", tags=["flow"],
            include_in_schema=tracardi.expose_gui_api)
async def update_flow_lock(id: str, lock: str):
    return await workflow_dao.update_by_id(id, new_data=dict(
        lock=lock.lower() == 'yes'
    ))


@router.post("/flow/debug", tags=["flow"],
             include_in_schema=tracardi.expose_gui_api)
async def debug_flow(flow: FlowGraph, event_id: Optional[str] = None):
    """
        Debugs flow sent in request body
    """

    _now = now_in_utc()

    if event_id is None:
        profile = Profile(id="@debug-profile-id",
                          metadata=ProfileMetadata(
                              time=ProfileTime(
                                  create=_now,
                                  insert=_now
                              )
                          ))
        session = Session(id="@debug-session-id",
                          metadata=SessionMetadata(
                              time=SessionTime(
                                  create=_now,
                                  insert=_now,
                                  timestamp=datetime.timestamp(_now)
                              )
                          ))
        event_session = EventSession(
            id=session.id,
            start=session.metadata.time.insert,
            duration=session.metadata.time.duration
        )
        session.set_new()
        source = Entity(id="@debug-source-id")

        event = Event(
            metadata=EventMetadata(time=EventTime()),
            id='@debug-event-id',
            name="Debug event id",
            type="@debug-event-type",
            source=source,
            session=event_session,
            profile=profile,
            context={}
        )

    else:
        # TODO EOFE - End of FlatEvent
        event: Event = await bd_event_adapter.load_event_from_db(event_id)

        if event is None:
            raise ValueError(f"Could not find event id {event_id}.")

        source = event.source

        if event.has_profile():
            # TODO EOFP - End of FlatProfile
            profile = await load_profile(event.profile.id)
            if profile is None:
                raise ValueError(f"Could not find profile id {event.profile.id} attached to event id {event_id}. "
                                 f"Debugging will fail if profile is expected.")
        else:
            profile = None

        if event.has_session():
            flat_session = await bd_session_adapter.load_flat_session_from_db(event.session.id)
            if flat_session is None:
                raise ValueError(
                    f"Event id {event.id} points to session {event.session.id}, but it does not exists. "
                    f"Please retry in 15s.")

            event_session = EventSession(
                id=flat_session.id,
                start=flat_session['metadata.time.insert'],
                duration=flat_session['metadata.time.duration']
            )
            session = Session(**flat_session)
        else:
            session = None
            event_session = None

    tracker_payload = TrackerPayload(
        source=source,
        session=event_session,
        metadata=EventPayloadMetadata(time=Time()),
        profile=profile,
        context={},
        request={},
        properties={},
        events=[EventPayload(id=event.id, type=event.type, properties=event.properties)]
    )

    tracker_payload.set_ephemeral(True)

    workflow = WorkFlow(
        FlowHistory(history=[]),
        tracker_payload=tracker_payload
    )

    ux = []

    flow_invoke_result = await workflow.invoke(flow, event, profile, session, ux, debug=True)

    profile_save_result = None

    # Pass logs to central log
    flow_invoke_result.register_logs_in_logger()

    return {
        'logs': [],
        "debugInfo": flow_invoke_result.debug_info.model_dump(),
        "update": profile_save_result,
        "ux": ux
    }


@router.delete("/flow/{id}", tags=["flow"],
               response_model=dict,
               include_in_schema=tracardi.expose_gui_api)
async def delete_flow(id: str):
    """
    Deletes flow with given id (str)
    """

    # TODO use constrains

    # TODO could be a transaction

    # Delete rule before flow
    await workflow_trigger_dao.delete_by_workflow_id(id)
    # Delete flow
    await workflow_dao.delete_by_id(id)

    return {
        "rule": True,
        "flow": True
    }
