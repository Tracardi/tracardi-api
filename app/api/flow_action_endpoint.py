import hashlib
from collections import defaultdict
from typing import Optional
from fastapi import APIRouter
from fastapi import HTTPException, Depends

from tracardi.service.storage.driver.elastic import action as action_db
from app.service.grouper import search
from tracardi.domain.enum.yes_no import YesNo
from tracardi.domain.entity import Entity
from tracardi.domain.flow_action_plugin import FlowActionPlugin
from tracardi.domain.record.flow_action_plugin_record import FlowActionPluginRecord
from tracardi.domain.settings import Settings
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from .auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


async def _load_record(id: str) -> Optional[FlowActionPluginRecord]:
    return FlowActionPluginRecord.create(await action_db.load_by_id(id))


async def _store_record(data: Entity):
    return await action_db.save(data)


@router.get("/flow/action/plugin/{id}", 
            tags=["flow", "action"],
            response_model=FlowActionPlugin, 
            include_in_schema=tracardi.expose_gui_api)
async def get_plugin(id: str):
    """
    Returns FlowActionPlugin object.
    """
    record = await _load_record(id)

    if record is None:
        raise HTTPException(status_code=404, detail=f"Missing plugin id '{id}'")
    return record.decode()


@router.get("/flow/action/plugin/{id}/hide/{state}", tags=["flow", "action"],
            response_model=BulkInsertResult, include_in_schema=tracardi.expose_gui_api)
async def get_plugin_state(id: str, state: YesNo):
    """
    Returns FlowActionPlugin object.
    """
    record = await _load_record(id)
    if record is None:
        raise HTTPException(status_code=406, detail=f"Can not this operation on missing plugin '{id}'")
    action = record.decode()
    action.settings.hidden = Settings.as_bool(state)
    return await _store_record(FlowActionPluginRecord.encode(action))


@router.get("/flow/action/plugin/{id}/enable/{state}", tags=["flow", "action"],
            response_model=BulkInsertResult, include_in_schema=tracardi.expose_gui_api)
async def set_plugin_enabled_disabled(id: str, state: YesNo):
    """
    Sets FlowActionPlugin enabled or disabled.
    """
    record = await _load_record(id)
    if record is None:
        raise HTTPException(status_code=406, detail=f"Can not this operation on missing plugin '{id}'")
    action = record.decode()
    action.settings.enabled = Settings.as_bool(state)
    return await _store_record(FlowActionPluginRecord.encode(action))


@router.put("/flow/action/plugin/{id}/icon/{icon}", tags=["flow", "action"], response_model=BulkInsertResult,
            include_in_schema=tracardi.expose_gui_api)
async def edit_plugin_icon(id: str, icon: str):
    """
    Edits icon for action with given ID
    """
    record = await _load_record(id)
    if record is None:
        raise HTTPException(status_code=406, detail=f"Can not this operation on missing plugin '{id}'")
    action = record.decode()
    action.plugin.metadata.icon = icon
    return await _store_record(FlowActionPluginRecord.encode(action))


@router.put("/flow/action/plugin/{id}/name/{name}", tags=["flow", "action"], response_model=BulkInsertResult,
            include_in_schema=tracardi.expose_gui_api)
async def edit_plugin_name(id: str, name: str):
    """
    Edits name for action with given ID
    """
    record = await _load_record(id)
    if record is None:
        raise HTTPException(status_code=406, detail=f"Can not this operation on missing plugin '{id}'")
    action = record.decode()
    action.plugin.metadata.name = name
    return await _store_record(FlowActionPluginRecord.encode(action))


@router.delete("/flow/action/plugin/{id}", tags=["flow", "action"],
               response_model=dict, include_in_schema=tracardi.expose_gui_api)
async def delete_plugin(id: str):
    """
    Deletes FlowActionPlugin object.
    """
    result = await action_db.delete_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Can not delete missing plugin '{id}'")
    await action_db.refresh()

    return result


@router.post("/flow/action/plugin", tags=["flow", "action"],
             response_model=BulkInsertResult, include_in_schema=tracardi.expose_gui_api)
async def upsert_plugin(action: FlowActionPlugin):
    """
    Upserts workflow action plugin. Action plugin id is a hash of its module and className so
    if there is a conflict in classes or you pass wrong module and class name then the action
    plugin may be overwritten.
    """

    action_id = action.plugin.spec.module + action.plugin.spec.className
    action.id = hashlib.md5(action_id.encode()).hexdigest()

    result = await _store_record(FlowActionPluginRecord.encode(action))
    await action_db.refresh()
    return result


@router.get("/flow/action/plugins", tags=["flow", "action"],
            include_in_schema=tracardi.expose_gui_api)
async def get_plugins_list(flow_type: Optional[str] = None, query: Optional[str] = None):
    """
    Returns a list of available plugins.
    """
    _current_plugin = None
    if flow_type is None:
        result = await action_db.load_all(limit=1000)
    else:
        result = await action_db.filter(purpose=flow_type, limit=500)

    _result = []
    for r in result:
        _current_plugin = r
        _result.append(FlowActionPluginRecord(**r).decode())

    if query is not None:
        if len(query) == 0:
            query = "*not-hidden"

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
                       query in r.plugin.metadata.name.lower()
                       or query in r.plugin.metadata.brand.lower()
                       or search(query, r.plugin.metadata.tags)
                       or search(query, r.plugin.metadata.group)
                       ]

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
        "total": len(_result),
        "grouped": groups
    }
