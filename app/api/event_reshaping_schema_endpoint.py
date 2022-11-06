from typing import Optional

from tracardi.service.storage.driver import storage
from fastapi import APIRouter, Depends, HTTPException
from app.config import server
from .auth.permissions import Permissions
from tracardi.service.event_reshape_schema_cache import EventReshapeSchemaCache
from tracardi.domain.event_reshaping_schema import EventReshapingSchema
from ..service.grouping import group_records

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)

cache = EventReshapeSchemaCache()


@router.put("/event-reshape-schema/flush", tags=["reshaping"], include_in_schema=server.expose_gui_api)
async def flush_reshape_schemas():
    await storage.driver.event_reshaping.flush()


@router.put("/event-reshape-schema/refresh", tags=["reshaping"], include_in_schema=server.expose_gui_api)
async def refresh_reshape_schemas():
    await storage.driver.event_reshaping.refresh()


@router.post("/event-reshape-schema", tags=["reshaping"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_reshape_schema(data: EventReshapingSchema):
    result = await storage.driver.event_reshaping.upsert(data)
    cache.upsert_item(data)
    await storage.driver.event_reshaping.refresh()
    return {"saved": result.saved}


@router.delete("/event-reshape-schema/{id}", tags=["reshaping"], include_in_schema=server.expose_gui_api)
async def delete_reshape_schema(id: str):
    result = await storage.driver.event_reshaping.delete(id)
    # cache.delete_item(id, event_type)
    await storage.driver.event_reshaping.refresh()
    return result


@router.get("/event-reshape-schema/{id}", tags=["reshaping"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_reshape_schema(id: str):
    result = await storage.driver.event_reshaping.load(id)
    if not result:
        raise HTTPException(status_code=404, detail=f"No event reshaping with ID {id} found.")

    return result


@router.get("/event-reshape-schema", tags=["reshaping"], include_in_schema=server.expose_gui_api, response_model=dict)
async def load_reshape_schemas(limit: Optional[int] = 100, query: Optional[str] = None):
    result = await storage.driver.event_reshaping.load_all(limit)
    return group_records(result, query, group_by='tags', search_by='name', sort_by='name')
