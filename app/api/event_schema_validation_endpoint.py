from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from app.config import server
from app.service.grouping import group_records
from tracardi.domain.event_payload_validator import EventPayloadValidator, EventPayloadValidatorRecord
from tracardi.service.storage.driver import storage
from elasticsearch import ElasticsearchException
from typing import Optional

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
    prefix="/event"
)


@router.put("/validation-schema/refresh", tags=["event", "validation"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def refresh_schema():
    """
    Refreshes event validation schema index
    """
    try:
        return await storage.driver.validation_schema.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validation-schema", tags=["event", "validation"], include_in_schema=server.expose_gui_api,
             response_model=dict)
async def add_schema(schema: EventPayloadValidator):
    """
    Creates new event validation schema in database
    """
    try:
        result = await storage.driver.validation_schema.add_schema(schema)
        await storage.driver.validation_schema.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"added": result.saved}


@router.get("/validation-schema/{event_type}", tags=["event", "validation"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_schema(event_type: str):
    """
    Returns event validation schema for given event type
    """
    try:
        record = await storage.driver.validation_schema.get_schema(event_type)
        if record is None:
            raise HTTPException(status_code=404, detail=f"Validation schema for {event_type} not found.")
        return EventPayloadValidator.decode(EventPayloadValidatorRecord(**record))
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/validation-schema/{event_type}", tags=["event", "validation"], include_in_schema=server.expose_gui_api,
               response_model=dict)
async def del_schema(event_type: str):
    """
    Deletes event validation schema for given event type
    """
    try:
        result = await storage.driver.validation_schema.del_schema(event_type)
        await storage.driver.validation_schema.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 1 if result is not None and result["result"] == "deleted" else 0}


@router.get("/validation-schemas", tags=["event", "validation"], include_in_schema=server.expose_gui_api,
            response_model=list)
async def list_schemas(start: Optional[int] = 0, limit: Optional[int] = 10):
    """
    Lists event validation schemas according to given start (int) and limit (int) parameters
    """
    try:
        result = await storage.driver.validation_schema.load_schemas(start, limit)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return list(result)


@router.get("/validation-schemas/by_tag", tags=["event", "validation"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def list_schemas_by_tag(query: str = None, start: Optional[int] = 0, limit: Optional[int] = 10):
    """
    Lists event validation schemas by tag, according to given start (int), limit (int) and query (str)
    """
    try:
        result = await storage.driver.validation_schema.load_schemas(start, limit)
        return group_records(result, query, group_by='tags', search_by='name', sort_by='name')
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
