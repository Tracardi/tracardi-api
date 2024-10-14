from typing import Optional

from fastapi import APIRouter, Depends

from app.service.grouping import get_grouped_result
from tracardi.domain.event_redirect import EventRedirect
from tracardi.exceptions.log_handler import get_logger
from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.service.storage.mysql.mapping.event_redirect_mapping import map_to_event_redirect
from tracardi.service.storage.mysql.service.event_redirect_service import EventRedirectService

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
    ers = EventRedirectService()
    records = await ers.load_all(query, offset=start, limit=limit)
    return get_grouped_result("Redirects", records, map_to_event_redirect)


@router.post("/event-redirect",
             tags=["event-redirect"],
             include_in_schema=tracardi.expose_gui_api)
async def save_redirect(data: EventRedirect):
    """
        Saves redirect configuration
    """

    ers = EventRedirectService()

    await ers.insert(data)

    return True


@router.get("/event-redirect/{id}",
            tags=["event-redirect"],
            include_in_schema=tracardi.expose_gui_api)
async def get_redirect(id: str):
    """
        Returns redirect configuration or NULL if none
    """
    id = id.strip()

    ers = EventRedirectService()
    record = await ers.load_by_id(id)

    if not record.exists():
        return None

    return record.map_to_object(map_to_event_redirect)


@router.delete("/event-redirect/{id}",
               tags=["event-redirect"],
               include_in_schema=tracardi.expose_gui_api)
async def delete_redirect(id: str):
    """
    Deletes redirect configuration
    """
    id = id.strip()

    ers = EventRedirectService()

    result = await ers.delete_by_id(id)

    return result
