from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from app.config import server
from app.service.grouping import group_records
from tracardi.domain.event_payload_validator import EventTypeManager, EventPayloadValidatorRecord
from tracardi.service.storage.driver import storage
from elasticsearch import ElasticsearchException
from typing import Optional

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
    prefix="/event-type"
)


@router.put("/management/refresh", tags=["event-type", "validation"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def refresh_event_type_prerequisites():
    """
    Refreshes event type prerequisites and validation schema index
    """
    try:
        return await storage.driver.event_management.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/management", tags=["event-type", "validation"], include_in_schema=server.expose_gui_api,
             response_model=dict)
async def add_event_type_prerequisites(event_type_metadata: EventTypeManager):
    """
    Creates new event type prerequisites and validation schema in database
    """
    try:
        result = await storage.driver.event_management.add_event_type_metadata(event_type_metadata)
        await storage.driver.event_management.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"added": result.saved}


@router.get("/management/{event_type}", tags=["event-type", "validation"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_event_type_prerequisites(event_type: str):
    """
    Returns event type prerequisites and validation schema for given event type
    """
    try:
        record = await storage.driver.event_management.get_event_type_metadata(event_type)
        if record is None:
            raise HTTPException(status_code=404, detail=f"Validation schema for {event_type} not found.")
        return EventTypeManager.decode(EventPayloadValidatorRecord(**record))
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/management/{event_type}", tags=["event-type", "validation"], include_in_schema=server.expose_gui_api,
               response_model=dict)
async def del_event_type_prerequisites(event_type: str):
    """
    Deletes event type prerequisites and validation schema for given event type
    """
    try:
        result = await storage.driver.event_management.del_event_type_metadata(event_type)
        await storage.driver.event_management.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 1 if result is not None and result["result"] == "deleted" else 0}


@router.get("/management", tags=["event-type", "validation"], include_in_schema=server.expose_gui_api,
            response_model=list)
async def list_event_type_prerequisites(start: Optional[int] = 0, limit: Optional[int] = 10):
    """
    Lists event type prerequisites and validation schemas according to given start (int) and limit (int) parameters
    """
    try:
        result = await storage.driver.event_management.load_event_type_metadata(start, limit)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return list(result)


@router.get("/management/search/by_tag", tags=["event-type", "validation"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def list_event_type_prerequisites_by_tag(query: str = None, start: Optional[int] = 0, limit: Optional[int] = 10):
    """
    Lists event type prerequisites and validation schemas by tag, according to given start (int), limit (int) and query (str)
    """
    try:
        result = await storage.driver.event_management.load_events_type_metadata(start, limit)
        return group_records(result, query, group_by='tags', search_by='name', sort_by='name')
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
