from datetime import datetime

from fastapi import APIRouter, Depends
from app.config import server
from tracardi.service.storage.driver import storage
from .auth.permissions import Permissions

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)


@router.get("/debug/es/indices", tags=["debug"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_elastic_indices():
    """
    Returns list of Elasticsearch indices
    """
    return await storage.driver.raw.indices()


@router.get("/debug/server/time", tags=["debug"], include_in_schema=server.expose_gui_api)
async def get_server_time():
    """
    Returns current server time.
    """

    return datetime.utcnow()
