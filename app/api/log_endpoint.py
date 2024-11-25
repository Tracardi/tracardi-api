from fastapi import APIRouter, Depends
from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.service.storage.elastic.interface import log as log_db

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["maintainer"]))]
)


@router.get("/log/alerts", tags=["logs"], include_in_schema=tracardi.expose_gui_api)
async def get_log_alerts():
    """
    Returns list of all Tracardi API logs counts.
    """
    return await log_db.group_by_level()
