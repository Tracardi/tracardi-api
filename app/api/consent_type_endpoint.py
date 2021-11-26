from fastapi import APIRouter, Depends, HTTPException
from app.api.auth.authentication import get_current_user
from app.config import server
from pydantic import BaseModel, validator
from uuid import UUID, uuid4
from tracardi.service.storage.driver import storage
from elasticsearch import ElasticsearchException


class ConsentTypePayload(BaseModel):
    name: str
    description: str
    revokable: bool
    default_value: str

    @validator("default_value")
    def default_value_validator(cls, v):
        if v not in ("grant", "deny"):
            raise ValueError("'default_value' must be either 'grant' or 'deny'")
        return v


class ConsentType(ConsentTypePayload):
    id: UUID = uuid4()


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/consent", tags=["consent"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_consent_type(data: ConsentTypePayload):
    try:
        result = await storage.driver.consent_type.add_consent(**ConsentType(**data.dict()).dict())
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@router.delete("/consent/{consent_id}", tags=["consent"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_consent_type(consent_id: UUID):
    try:
        result = await storage.driver.consent_type.delete_by_id(consent_id)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 1 if result is not None and "result" in result and result["result"] == "deleted" else 0}


@router.get("/consents/{start}/{limit}", tags=["consent"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_consent_types(start: int = 0, limit: int = 10):
    try:
        result = await storage.driver.consent_type.load(start=start, limit=limit)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"total": len(result), "result": list(result)}
