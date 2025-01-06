from fastapi import APIRouter, Depends
from tracardi.common.time.date import now_in_utc
from tracardi.config import tracardi
from tracardi.service.adapter.bigdata.adapter_selector import bd_raw_adapter
from app.api.auth.permissions import Permissions

_bd_raw_adapter = bd_raw_adapter()

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)


@router.get("/debug/es/indices", tags=["debug"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def get_elastic_indices():
    """
    Returns list of Elasticsearch indices
    """
    return await _bd_raw_adapter.list_indices()


@router.get("/debug/server/time", tags=["debug"], include_in_schema=tracardi.expose_gui_api)
async def get_server_time():
    """
    Returns current server time.
    """

    return now_in_utc()
