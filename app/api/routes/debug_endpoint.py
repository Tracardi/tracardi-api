from fastapi import APIRouter, Depends
from tracardi.common.time.date import now_in_utc
from tracardi.config import tracardi
from tracardi.service.dependency.adapters.big_data_adapter import *
from app.api.auth.permissions import Permissions


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)


@router.get("/debug/es/indices", tags=["debug"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def get_elastic_indices():
    """
    Returns list of Elasticsearch indices
    """
    return await bd_raw_adapter.list_indices()


@router.get("/debug/server/time", tags=["debug"], include_in_schema=tracardi.expose_gui_api)
async def get_server_time():
    """
    Returns current server time.
    """

    return now_in_utc()
