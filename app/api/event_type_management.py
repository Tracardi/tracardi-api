import asyncio

from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from app.config import server
from app.service.grouping import group_records
from tracardi.domain.event_type_metadata import EventTypeMetadata
from tracardi.service.storage.driver.elastic import event_management as event_management_db
from tracardi.service.storage.driver.elastic import event as event_db
from typing import Optional


router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
    prefix="/event-type"
)


@router.put("/management/refresh", tags=["event-type"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def refresh_event_type_metadata():
    """
    Refreshes event type metadata
    """
    return await event_management_db.refresh()


@router.post("/management", tags=["event-type"], include_in_schema=server.expose_gui_api,
             response_model=dict)
async def add_event_type_metadata(event_type_metadata: EventTypeMetadata):

    """
    Creates new event type metadata in database
    """

    # Save tags
    result = await event_management_db.save(event_type_metadata)
    await event_management_db.refresh()

    if result.errors:
        raise ValueError(result.errors)

    # Update events for new tags in background

    task = event_db.update_tags(
        event_type=event_type_metadata.event_type,
        tags=event_type_metadata.tags)

    asyncio.create_task(task)

    return result


@router.get("/management/{event_type}",
            tags=["event-type"],
            include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_event_type_metadata(event_type: str):
    """
    Returns event type metadata for given event type
    """
    record = await event_management_db.get_event_type_metadata(event_type)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Metadata for {event_type} not found.")
    return record


@router.delete("/management/{event_type}", tags=["event-type"], include_in_schema=server.expose_gui_api,
               response_model=dict)
async def del_event_type_metadata(event_type: str):
    """
    Deletes event type metadata for given event type
    """
    result = await event_management_db.del_event_type_metadata(event_type)
    await event_management_db.refresh()

    return {"deleted": 1 if result is not None and result["result"] == "deleted" else 0}


@router.get("/management", tags=["event-type"], include_in_schema=server.expose_gui_api,
            response_model=list)
async def list_event_type_metadatas(start: Optional[int] = 0, limit: Optional[int] = 200):
    """
    List of event type metadata.
    """

    result = await event_management_db.load_events_type_metadata(start, limit)
    return list(result)


@router.get("/management/search/by_tag", tags=["event-type"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def list_event_type_metadatas_by_tag(query: str = None, start: Optional[int] = 0, limit: Optional[int] = 200):
    """
    Lists event type metadata by tag, according to given start (int), limit (int) and query (str)
    """
    result = await event_management_db.load_events_type_metadata(start, limit)
    return group_records(result, query, group_by='tags', search_by='name', sort_by='name')

