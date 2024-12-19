from fastapi import APIRouter, Depends

from app.api.auth.permissions import Permissions

from tracardi.config import tracardi
from tracardi.service.storage.mysql.mapping.bridge_mapping import map_to_bridge
from tracardi.service.storage.mysql.service.database_service import DatabaseService
from tracardi.service.storage.mysql.service.bridge_service import BridgeService
from tracardi.service.setup.setup_bridges import os_default_bridges
from tracardi.service.license import License, LICENSE
if License.has_service(LICENSE):
    from com_tracardi.db.bootstrap.default_bridges import commercial_default_bridges

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/bridge/reinstall", tags=["bridge"], include_in_schema=tracardi.expose_gui_api)
async def reinstall_bridges():
    ds = DatabaseService()
    await ds.bootstrap()

    await BridgeService.reinstall(default_bridges=os_default_bridges)
    if License.has_service(LICENSE):
        await BridgeService.reinstall(default_bridges=commercial_default_bridges)


@router.get("/bridges", tags=["bridge"], include_in_schema=tracardi.expose_gui_api)
async def get_data_bridges():
    """
    Returns list of available data bridges
    """
    bs = BridgeService()
    results = await bs.load_all()
    result = list(results.map_to_objects(map_to_bridge))
    return {
        "total": len(result),
        "result": result
    }


@router.get("/bridges/entity", tags=["bridge"], include_in_schema=tracardi.expose_gui_api)
async def get_data_bridges():
    """
    Returns list of available data bridges
    """

    bs = BridgeService()
    results = await bs.load_all()

    result = [
        {
            "id": bridge.id,
            "name": bridge.name,
            "type": bridge.type,
            "manual": bridge.manual
        } for bridge in results.rows
    ]

    # Todo then remove the sorting

    return {
        "total": len(result),
        "result": sorted(result, key=lambda x: x['name'])
    }


@router.get("/bridge/{bridge_id}", tags=["bridge"], include_in_schema=tracardi.expose_gui_api)
async def get_data_bridges(bridge_id: str):
    """
    Returns data bridge
    """
    bs = BridgeService()
    result = await bs.load_by_id(bridge_id)
    return result.map_to_object(map_to_bridge)
