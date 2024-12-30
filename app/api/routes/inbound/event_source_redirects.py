from typing import Optional

from fastapi import APIRouter, Depends

from tracardi.domain.event_redirect import EventRedirect
from tracardi.common.logging.log_handler import get_logger
from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.service.storage.mysql.interface import event_redirect_dao

logger = get_logger(__name__)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/event-redirect",
            tags=["event-redirect"],
            include_in_schema=tracardi.expose_gui_api)
# Obsolete
@router.get("/event-redirect/list",
            tags=["event-redirect"],
            include_in_schema=tracardi.expose_gui_api)
async def list_redirects(query: Optional[str] = None, start: int = 0, limit: int = 100):
    """
        Returns list of redirects configurations
    """

    result, total = await event_redirect_dao.load_all(query, offset=start, limit=limit)
    return {
        "total": total,
        "grouped": {
            "Redirects": result
        },
        "cache": None
    }


@router.post("/event-redirect",
             tags=["event-redirect"],
             include_in_schema=tracardi.expose_gui_api)
async def save_redirect(data: EventRedirect):
    """
        Saves redirect configuration
    """

    await event_redirect_dao.insert(data)

    return True


@router.get("/event-redirect/{id}",
            tags=["event-redirect"],
            include_in_schema=tracardi.expose_gui_api)
async def get_redirect(id: str):
    """
        Returns redirect configuration or NULL if none
    """
    id = id.strip()

    return await event_redirect_dao.load_by_id(id)


@router.delete("/event-redirect/{id}",
               tags=["event-redirect"],
               include_in_schema=tracardi.expose_gui_api)
async def delete_redirect(id: str):
    """
    Deletes redirect configuration
    """
    id = id.strip()

    return await event_redirect_dao.delete_by_id(id)
