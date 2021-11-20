import asyncio
import hashlib
from collections import defaultdict
from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from tracardi.exceptions.exception import StorageException

from tracardi.domain.console import Console
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor, StorageForBulk
from tracardi_graph_runner.domain.flow_history import FlowHistory
from tracardi_graph_runner.domain.work_flow import WorkFlow
from tracardi_plugin_sdk.domain.console import Log

from .auth.authentication import get_current_user
from .grouper import search
from tracardi.domain.context import Context
from tracardi.domain.enum.yes_no import YesNo
from tracardi.domain.flow_meta_data import FlowMetaData
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.flow import Flow, FlowGraphDataRecord
from tracardi_graph_runner.domain.flow import Flow as GraphFlow
from tracardi.domain.flow_action_plugin import FlowActionPlugin
from tracardi.domain.plugin_import import PluginImport
from tracardi.domain.record.flow_action_plugin_record import FlowActionPluginRecord
from tracardi.domain.flow import FlowRecord

from tracardi.domain.profile import Profile
from tracardi.domain.rule import Rule
from tracardi.domain.session import Session
from tracardi.domain.settings import Settings
from tracardi.domain.resource import Resource
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from ..config import server
from ..setup.on_start import add_plugin

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/flow/draft", tags=["flow"], response_model=BulkInsertResult, include_in_schema=server.expose_gui_api)
async def upsert_flow_draft(draft: Flow):
    try:

        # Frontend edge id is log. Save space and md5 it.

        if draft.flowGraph is not None:
            draft.flowGraph.shorten_edge_ids()

        # Check if origin flow exists

        entity = Entity(id=draft.id)
        draft_record = await StorageFor(entity).index('flow').load(FlowRecord)  # type: FlowRecord

        if draft_record is None:
            # If not exists create new one
            origin = Flow.new(draft.id)
            origin.description = "Created during workflow draft save."
            record = FlowRecord.encode(origin)
            await StorageFor(record).index().save()
        else:
            # If exists decode origin flow
            origin = draft_record.decode()

        # Append draft
        origin.encode_draft(draft)
        flow_record = FlowRecord.encode(origin)

        return await StorageFor(flow_record).index().save()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/draft/{id}", tags=["flow"], response_model=Flow, include_in_schema=server.expose_gui_api)
async def load_flow_draft(id: str):
    try:

        # Check if origin flow exists

        entity = Entity(id=id)
        draft_record = await StorageFor(entity).index('flow').load(FlowRecord)  # type: FlowRecord

        if draft_record is None:
            raise ValueError("Flow `{}` does not exists.".format(id))

        # Return draft if exists
        if draft_record.draft:
            return draft_record.decode_draft()

        return draft_record.decode()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flows", tags=["flow"], include_in_schema=server.expose_gui_api)
async def get_flows(query: str = None):
    try:
        result = await StorageForBulk().index('flow').load()
        total = result.total
        result = [FlowRecord(**r) for r in result]

        # Filtering
        if query is not None and len(query) > 0:
            query = query.lower()
            if query:
                result = [r for r in result if query in r.name.lower() or search(query, r.projects)]

        return {
            "total": total,
            "result": result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flows/refresh", tags=["flow"], include_in_schema=server.expose_gui_api)
async def refresh_flows():
    try:
        return await storage.driver.flow.refresh()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flows/by_tag", tags=["flow"], include_in_schema=server.expose_gui_api)
async def get_grouped_flows(query: str = None):
    try:
        result = await StorageForBulk().index('flow').load()
        total = result.total
        result = [FlowRecord(**r) for r in result]

        # Filtering
        if query is not None and len(query) > 0:
            query = query.lower()
            if query:
                result = [r for r in result if query in r.name.lower() or search(query, r.projects)]

        # Grouping
        groups = defaultdict(list)
        for flow in result:  # type: FlowRecord
            if isinstance(flow.projects, list):
                for group in flow.projects:
                    groups[group].append(flow)
            elif isinstance(flow.projects, str):
                groups[flow.projects].append(flow)

        # Sort
        groups = {k: sorted(v, key=lambda r: r.name, reverse=False) for k, v in groups.items()}

        return {
            "total": total,
            "grouped": groups
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


@router.get("/flow/{id}", tags=["flow"], response_model=Flow, include_in_schema=server.expose_gui_api)
async def get_flow(id: str):
    try:
        flow = Entity(id=id)
        flow_record = await StorageFor(flow).index("flow").load(FlowRecord)
        result = flow_record.decode() if flow_record is not None else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is not None:
        return result

    raise HTTPException(status_code=404, detail="Flow id: `{}` does not exist.".format(id))


@router.post("/flow", tags=["flow"], response_model=BulkInsertResult, include_in_schema=server.expose_gui_api)
async def upsert_flow(flow: Flow):
    try:
        flow_record = FlowRecord.encode(flow)
        return await StorageFor(flow_record).index().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flow/metadata", tags=["flow"], response_model=BulkInsertResult, include_in_schema=server.expose_gui_api)
async def upsert_flow_details(flow_metadata: FlowMetaData):
    try:
        entity = Entity(id=flow_metadata.id)
        flow_record = await StorageFor(entity).index("flow").load(FlowRecord)  # type: FlowRecord
        if flow_record:
            flow_record.name = flow_metadata.name
            flow_record.description = flow_metadata.description
            flow_record.enabled = flow_metadata.enabled
            flow_record.projects = flow_metadata.projects
        else:
            # new record
            flow_record = FlowRecord(
                id=flow_metadata.id,
                name=flow_metadata.name,
                description=flow_metadata.description,
                enabled=flow_metadata.enabled,
                flowGraph=FlowGraphDataRecord(nodes=[], edges=[]),
                projects=flow_metadata.projects
            )

        return await StorageFor(flow_record).index().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/metadata/refresh", tags=["flow"], include_in_schema=server.expose_gui_api)
async def flow_refresh():
    return await storage.driver.flow.refresh()


@router.get("/flow/metadata/flush", tags=["flow"], include_in_schema=server.expose_gui_api)
async def flow_refresh():
    return await storage.driver.flow.flush()


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
            draft = flow_record.decode_draft()

            draft.name = flow_metadata.name
            draft.description = flow_metadata.description
            draft.enabled = flow_metadata.enabled
            draft.projects = flow_metadata.projects

            flow_record.encode_draft(draft)

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
            profile,
            event
        )
        debug_info, log_list = await workflow.invoke(flow, debug=True)

        console_log = []
        profile_save_result = None
        try:
            # Store logs in one console log
            for log in log_list:  # type: Log
                console = Console(
                    origin="node",
                    event_id=workflow.event.id,
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
                event_id=workflow.event.id,
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


@router.get("/flow/action/plugin/{id}",
            tags=["flow", "action"],
            response_model=FlowActionPlugin,
            include_in_schema=server.expose_gui_api)
async def get_plugin(id: str):
    """
    Returns FlowActionPlugin object.
    """
    try:
        action = Entity(id=id)
        record = await StorageFor(action).index("action").load(FlowActionPluginRecord)  # type: FlowActionPluginRecord
        return record.decode()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/action/plugin/{id}/hide/{state}", tags=["flow", "action"],
            response_model=BulkInsertResult, include_in_schema=server.expose_gui_api)
async def get_plugin_state(id: str, state: YesNo):
    """
    Returns FlowActionPlugin object.
    """

    try:

        action = Entity(id=id)
        record = await StorageFor(action).index("action").load(FlowActionPluginRecord)  # type: FlowActionPluginRecord
        action = record.decode()
        action.settings.hidden = Settings.as_bool(state)
        return await StorageFor(FlowActionPluginRecord.encode(action)).index().save()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/action/plugin/{id}/enable/{state}", tags=["flow", "action"],
            response_model=BulkInsertResult, include_in_schema=server.expose_gui_api)
async def get_plugin_enabled(id: str, state: YesNo):
    """
    Returns FlowActionPlugin object.
    """

    try:

        action = Entity(id=id)
        record = await StorageFor(action).index("action").load(FlowActionPluginRecord)  # type: FlowActionPluginRecord
        action = record.decode()
        action.settings.enabled = Settings.as_bool(state)
        return await StorageFor(FlowActionPluginRecord.encode(action)).index().save()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/action/plugin/{id}", tags=["flow", "action"],
            response_model=FlowActionPlugin, include_in_schema=server.expose_gui_api)
async def get_plugin(id: str):
    """
    Returns FlowActionPlugin object.
    """
    try:
        action = Entity(id=id)
        record = await StorageFor(action).index("action").load(FlowActionPluginRecord)  # type: FlowActionPluginRecord
        return record.decode()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/flow/action/plugin/{id}", tags=["flow", "action"],
               response_model=dict, include_in_schema=server.expose_gui_api)
async def delete_plugin(id: str):
    """
    Deletes FlowActionPlugin object.
    """
    try:
        action = Entity(id=id)
        return await StorageFor(action).index("action").delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/flow/action/plugin", tags=["flow", "action"],
             response_model=BulkInsertResult, include_in_schema=server.expose_gui_api)
async def upsert_plugin(action: FlowActionPlugin):
    """
    Upserts workflow action plugin. Action plugin id is a hash of its module and className so
    if there is a conflict in classes or you pass wrong mdoule and class name then the action
    plugin may be overwritten.
    """

    try:
        action_id = action.plugin.spec.module + action.plugin.spec.className
        action.id = hashlib.md5(action_id.encode()).hexdigest()

        record = FlowActionPluginRecord.encode(action)

        return await StorageFor(record).index().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/action/plugins", tags=["flow", "action"],
            include_in_schema=server.expose_gui_api)
async def get_plugins_list(query: Optional[str] = None):
    """
    Returns a list of available plugins.
    """

    _current_plugin = None
    try:

        result = await StorageForBulk().index('action').load()

        _result = []
        for r in result:
            _current_plugin = r
            _result.append(FlowActionPluginRecord(**r).decode())

        if query is not None and len(query) > 0:
            query = query.lower()

            if query == "*not-hidden":
                _result = [r for r in _result if r.settings.hidden is False]
            if query == "*hidden":
                _result = [r for r in _result if r.settings.hidden is True]
            if query == "*enabled":
                _result = [r for r in _result if r.settings.enabled is True]
            if query == "*disabled":
                _result = [r for r in _result if r.settings.enabled is False]
            if query[0] != '*':
                _result = [r for r in _result if
                           query in r.plugin.metadata.name.lower() or search(query, r.plugin.metadata.group)]

        groups = defaultdict(list)
        for plugin in _result:  # type: FlowActionPlugin
            if isinstance(plugin.plugin.metadata.group, list):
                for group in plugin.plugin.metadata.group:
                    groups[group].append(plugin)
            elif isinstance(plugin.plugin.metadata.group, str):
                groups[plugin.plugin.metadata.group].append(plugin)

        # Sort
        groups = {k: sorted(v, key=lambda r: r.plugin.metadata.name, reverse=False) for k, v in groups.items()}

        return {
            "total": result.total,
            "grouped": groups
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail="{} {}".format(str(e), _current_plugin))


@router.post("/flow/action/plugin/register", tags=["flow", "action"],
             response_model=BulkInsertResult, include_in_schema=server.expose_gui_api)
async def register_plugin_by_module(plugin: PluginImport):
    """
    Registers action plugin by its module. Module must have register method that returns Plugin
    class filled with plugin metadata.
    """

    try:
        result = await add_plugin(plugin.module, install=True, upgrade=plugin.upgrade)
        await storage.driver.action.refresh()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
