from fastapi import APIRouter, Depends, HTTPException
from app.config import server
from app.api.auth.authentication import get_current_user
from tracardi.domain.event_payload_validator import EventPayloadValidator
from tracardi.service.storage.driver import storage
from elasticsearch import ElasticsearchException
from typing import Optional


router = APIRouter(
    dependencies=[
        Depends(get_current_user)
    ],
    prefix="/event"
)


@router.post("/validation-schema", tags=["event", "validation"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_schema(schema: EventPayloadValidator):
    try:
        result = await storage.driver.validation_schema.add_schema(schema)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"added": result.saved}


@router.delete("/validation-schema/{event_type}", tags=["event", "validation"], include_in_schema=server.expose_gui_api,
               response_model=dict)
async def del_schema(event_type: str):
    try:
        result = await storage.driver.validation_schema.del_schema(event_type)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 1 if result is not None and result["result"] == "deleted" else 0}


@router.get("/validation-schemas/{start=0}/{limit=10}", tags=["event", "validation"], include_in_schema=server.expose_gui_api,
            response_model=list)
async def list_schemas(start: Optional[int] = 0, limit: Optional[int] = 10):
    try:
        result = await storage.driver.validation_schema.load_schemas(start, limit)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return list(result)

