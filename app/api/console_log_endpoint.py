from fastapi import APIRouter, Depends

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.service.adapter.bigdata.adapter_selector import bd_log_adapter


router = APIRouter()
_log_adapter = bd_log_adapter()

@router.get("/event/logs/{event_id}", tags=["log"], include_in_schema=tracardi.expose_gui_api)
async def get_event_logs(event_id: str, sort: str = None):
    """
    Returns event logs for event with given ID
    """

    if sort in ['asc', 'desc']:
        sort = [{
            "date": sort
        }]

    records, total = await _log_adapter.load_by_event(event_id, sort=sort)
    return {
        "result": records,
        "total": total
    }


@router.get("/node/logs/{node_id}", tags=["log"],
            include_in_schema=tracardi.expose_gui_api)
async def get_node_logs(node_id: str, sort: str = None):
    """
    Returns node console log.
    """

    if sort in ['asc', 'desc']:
        sort = [{
            "date": sort
        }]

    records, total = await _log_adapter.load_by_node(node_id, sort=sort)

    return {
        "result": records,
        "total": total
    }


@router.get("/flow/logs/{flow_id}", tags=["log"],
            include_in_schema=tracardi.expose_gui_api)
async def get_flow_logs(flow_id: str, sort: str = None):
    """
    Returns flow console log.
    """
    if sort in ['asc', 'desc']:
        sort = [{
            "date": sort
        }]

    records, total = await _log_adapter.load_by_flow(flow_id, sort=sort)

    return {
        "result": records,
        "total": total
    }


@router.get("/profile/logs/{profile_id}", tags=["log"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_profile_logs(profile_id: str, sort: str = None):
    """
    Gets logs for profile with given ID (str)
    """

    if sort in ['asc', 'desc']:
        sort = [{
            "date": sort
        }]

    records, total = await _log_adapter.load_by_profile(profile_id, sort=sort)
    return {
        "result": list(records),
        "total": total
    }


@router.get("/log/alerts", tags=["log"], include_in_schema=tracardi.expose_gui_api)
async def get_log_alerts():
    """
    Returns list of all Tracardi API logs counts.
    """
    return await _log_adapter.group_by_level()
