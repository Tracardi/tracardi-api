from collections import defaultdict
from typing import Optional
from fastapi import APIRouter
from fastapi import HTTPException, Depends

from app.service.grouper import search
from tracardi.domain.enum.yes_no import YesNo
from tracardi.domain.flow_action_plugin import FlowActionPlugin
from tracardi.domain.settings import Settings
from tracardi.service.storage.mysql.mapping.plugin_mapping import map_to_flow_action_plugin
from tracardi.service.storage.mysql.service.action_plugin_service import ActionPluginService
from .auth.permissions import Permissions
from tracardi.config import tracardi

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/flow/action/plugin/{id}",
            tags=["flow", "action"],
            response_model=FlowActionPlugin,
            include_in_schema=tracardi.expose_gui_api)
async def get_plugin(id: str):
    """
    Returns FlowActionPlugin object.
    """

    aps = ActionPluginService()
    record = await aps.load_by_id(plugin_id=id)
    if not record.exists():
        raise HTTPException(detail=f"Missing plugin id '{id}'", status_code=404)
    return record.map_to_object(map_to_flow_action_plugin)


@router.get("/flow/action/plugin/{id}/hide/{state}", tags=["flow", "action"],
            include_in_schema=tracardi.expose_gui_api)
async def get_plugin_state(id: str, state: YesNo):
    """
    Returns FlowActionPlugin object.
    """

    aps = ActionPluginService()
    return await aps.update_by_id(
        data={
            "settings_hidden": Settings.as_bool(state)
        },
        plugin_id=id
    )


@router.get("/flow/action/plugin/{id}/enable/{state}", tags=["flow", "action"],
            include_in_schema=tracardi.expose_gui_api)
async def set_plugin_enabled_disabled(id: str, state: YesNo):
    """
    Sets FlowActionPlugin enabled or disabled.
    """

    aps = ActionPluginService()
    return await aps.update_by_id(
        data={
            "settings_enabled": Settings.as_bool(state)
        },
        plugin_id=id
    )


@router.put("/flow/action/plugin/{id}/icon/{icon}", tags=["flow", "action"],
            include_in_schema=tracardi.expose_gui_api)
async def edit_plugin_icon(id: str, icon: str):
    """
    Edits icon for action with given ID
    """

    aps = ActionPluginService()
    return await aps.update_by_id(
        data={
            "plugin_metadata_icon": icon
        },
        plugin_id=id
    )


@router.put("/flow/action/plugin/{id}/name/{name}", tags=["flow", "action"],
            include_in_schema=tracardi.expose_gui_api)
async def edit_plugin_name(id: str, name: str):
    """
    Edits name for action with given ID
    """

    aps = ActionPluginService()
    return await aps.update_by_id(
        data={
            "plugin_metadata_name": name
        },
        plugin_id=id
    )


@router.delete("/flow/action/plugin/{id}", tags=["flow", "action"],
               include_in_schema=tracardi.expose_gui_api)
async def delete_plugin(id: str):
    """
    Deletes FlowActionPlugin object.
    """

    aps = ActionPluginService()
    return await aps.delete_by_id(plugin_id=id)


@router.get("/flow/action/plugins", tags=["flow", "action"],
            include_in_schema=tracardi.expose_gui_api)
async def get_plugins_list(flow_type: Optional[str] = None, query: Optional[str] = None):
    """
    Returns a list of available plugins.
    """

    aps = ActionPluginService()

    _current_plugin = None
    if flow_type is None:
        records = await aps.load_all()
    else:
        if flow_type not in ['collection', 'segmentation']:
            raise HTTPException(detail='Incorrect workflow type.', status_code=404)
        records = await aps.filter(purpose=flow_type)

    if not records.exists():
        raise HTTPException(detail="Could not load any plugins", status_code=404)

    _result = list(records.map_to_objects(map_to_flow_action_plugin))

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
