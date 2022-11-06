from tracardi.service.storage.driver import storage
from fastapi import APIRouter, Depends, HTTPException
from app.config import server
from .auth.permissions import Permissions
from tracardi.service.event_validation_schema_cache import EventValidationSchemaCache
from tracardi.domain.event_validator import EventValidator
from ..service.grouping import group_records

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


cache = EventValidationSchemaCache()


@router.put("/event-validator/flush", tags=["validation"], include_in_schema=server.expose_gui_api)
async def flush_validators():
    await storage.driver.event_validation.flush()


@router.put("/event-validator/refresh", tags=["validation"], include_in_schema=server.expose_gui_api)
async def refresh_validators():
    await storage.driver.event_validation.refresh()


@router.post("/event-validator", tags=["validation"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_validator(data: EventValidator):
    result = await storage.driver.event_validation.upsert(data)
    cache.upsert_item(data)
    return {"saved": result.saved}


@router.delete("/event-validator", tags=["validation"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_validator(id: str, event_type: str):
    result = await storage.driver.event_validation.delete(id)
    cache.delete_item(id, event_type)
    return {"deleted": result.deleted}


@router.get("/event-validator", tags=["validation"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_validator(id: str):
    result = await storage.driver.event_validation.load(id)
    if not result:
        raise HTTPException(status_code=404, detail=f"No event validation with ID {id} found.")

    return {"result": result}


@router.get("/event-validators", tags=["validation"], include_in_schema=server.expose_gui_api, response_model=dict)
async def load_validators(limit: int = 100, query: str = None):
    result, total = await storage.driver.event_validation.load_all(limit)
    return group_records(result, query, group_by='tags', search_by='name', sort_by='name')
