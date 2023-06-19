from fastapi import APIRouter, Depends

from app.api.auth.permissions import Permissions
from app.config import server

from tracardi.service.storage.driver.storage.driver import bridge as bridge_db

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/bridges", tags=["bridge"], include_in_schema=server.expose_gui_api)
async def get_data_bridges():
    """
    Returns list of available data bridges
    """
    result = await bridge_db.load_all()
    return result.dict()


@router.get("/bridges/entity", tags=["bridge"], include_in_schema=server.expose_gui_api)
async def get_data_bridges():
    """
    Returns list of available data bridges
    """
    result = await bridge_db.load_all()

    result = [
        {
            "id": bridge['id'],
            "name": bridge['name'],
            "type": bridge['type'],
            "manual": bridge['manual'] if 'manual' in bridge else None
        } for bridge in result
    ]
    return {
        "total": len(result),
        "result": result
    }


@router.get("/bridge/{bridge_id}", tags=["bridge"], include_in_schema=server.expose_gui_api)
async def get_data_bridges(bridge_id: str):
    """
    Returns data bridge
    """
    return await bridge_db.load_by_id(bridge_id)
