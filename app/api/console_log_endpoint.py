from fastapi import APIRouter, Depends

from app.api.auth.permissions import Permissions
from app.config import server
from tracardi.domain.console import Console

from tracardi.service.storage.driver import storage

router = APIRouter()


@router.get("/event/logs/{event_id}", tags=["console_log"], include_in_schema=server.expose_gui_api)
async def get_event_logs(event_id: str, sort: str = None):
    """
    Returns event logs for event with given ID
    """

    storage_records = await storage.driver.console_log.load_by_event(event_id, sort=sort)
    return {
        "result": [Console.decode_record(log) for log in storage_records],
        "total": storage_records.total
    }


@router.get("/node/logs/{node_id}", tags=["console_log"],
            include_in_schema=server.expose_gui_api)
async def get_node_logs(node_id: str, sort: str = None):
    """
    Returns node console log.
    """

    if sort in ['asc', 'desc']:
        sort = [{
            "metadata.timestamp": sort
        }]

    storage_records = await storage.driver.console_log.load_by_node(node_id, sort=sort)

    return {
        "result": [Console.decode_record(log) for log in storage_records],
        "total": storage_records.total
    }


@router.get("/flow/logs/{flow_id}", tags=["console_log"],
            include_in_schema=server.expose_gui_api)
async def get_flow_logs(flow_id: str, sort: str = None):
    """
    Returns flow console log.
    """

    storage_records = await storage.driver.console_log.load_by_flow(flow_id, sort=sort)

    return {
        "result": [Console.decode_record(log) for log in storage_records],
        "total": storage_records.total
    }


@router.get("/profile/logs/{id}", tags=["profile"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=server.expose_gui_api)
async def get_profile_logs(id: str, sort: str = None):
    """
    Gets logs for profile with given ID (str)
    """
    storage_records = await storage.driver.console_log.load_by_profile(id, sort=sort)
    return {
        "result": [Console.decode_record(log) for log in storage_records],
        "total": storage_records.total
    }
