from fastapi import APIRouter, Depends
from tracardi.service.utils.date import now_in_utc
from tracardi.config import tracardi
from tracardi.service.storage.driver.elastic import raw as raw_db
from .auth.permissions import Permissions

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)


@router.get("/debug/es/indices", tags=["debug"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def get_elastic_indices():
    """
    Returns list of Elasticsearch indices
    """
    return await raw_db.indices()


@router.get("/debug/server/time", tags=["debug"], include_in_schema=tracardi.expose_gui_api)
async def get_server_time():
    """
    Returns current server time.
    """

    return now_in_utc()
