from fastapi import APIRouter, Depends

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi

# from tracardi.service.storage.driver.elastic import bridge as bridge_db
from tracardi.service.storage.mysql.mapping.bridge_mapping import map_to_bridge
from tracardi.service.storage.mysql.service.bridge_service import BridgeService

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


# @router.get("/bridges", tags=["bridge"], include_in_schema=tracardi.expose_gui_api)
# async def get_data_bridges():
#     """
#     Returns list of available data bridges
#     """
#     result = await bridge_db.load_all()
#     return result.dict()


@router.get("/bridges", tags=["bridge"], include_in_schema=tracardi.expose_gui_api)
async def get_data_bridges():
    """
    Returns list of available data bridges
    """
    bs = BridgeService()
    results = await bs.load_all()
    result = list(results.to_objects(map_to_bridge))
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
        } for bridge in results.result
    ]

    # Todo then remove the sorting

    return {
        "total": len(result),
        "result": sorted(result, key=lambda x: x['name'])
    }


# @router.get("/m/bridges/entity", tags=["bridge"], include_in_schema=tracardi.expose_gui_api)
# async def get_data_bridges():
#     """
#     Returns list of available data bridges
#     """
#
#     # Todo Changes for the next major version
#
#     result = await bridge_db.load_all()  # todo add sort={"name": "asc"} and change name to keyword
#
#     result = [
#         {
#             "id": bridge['id'],
#             "name": bridge['name'],
#             "type": bridge['type'],
#             "manual": bridge['manual'] if 'manual' in bridge else None
#         } for bridge in result
#     ]
#
#     # Todo then remove the sorting
#
#     return {
#         "total": len(result),
#         "result": sorted(result, key=lambda x: x['name'])
#     }


# @router.get("/bridge/{bridge_id}", tags=["bridge"], include_in_schema=tracardi.expose_gui_api)
# async def get_data_bridges(bridge_id: str):
#     """
#     Returns data bridge
#     """
#     return await bridge_db.load_by_id(bridge_id)


@router.get("/bridge/{bridge_id}", tags=["bridge"], include_in_schema=tracardi.expose_gui_api)
async def get_data_bridges(bridge_id: str):
    """
    Returns data bridge
    """
    bs = BridgeService()
    result = await bs.load_by_id(bridge_id)
    return result.get_object(map_to_bridge)
