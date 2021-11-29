from fastapi import APIRouter, Depends, HTTPException
from app.api.auth.authentication import get_current_user
from app.config import server
from pydantic import BaseModel, validator

from tracardi.domain.storage_result import StorageResult
from tracardi.service.storage.driver import storage
from elasticsearch import ElasticsearchException
from tracardi.domain.consent_schema import ConsentSchema
from uuid import UUID


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


router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.post("/consent/type", tags=["consent"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_consent_type(data: ConsentTypePayload):
    try:
        result = await storage.driver.consent_type.add_consent(id=data.name.lower().replace(" ", "-"), **data.dict())
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@router.delete("/consent/type/{consent_id}", tags=["consent"], include_in_schema=server.expose_gui_api, response_model=dict)
async def delete_consent_type(consent_id: str):
    try:
        result = await storage.driver.consent_type.delete_by_id(consent_id)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 1 if result is not None and "result" in result and result["result"] == "deleted" else 0}


@router.get("/consents/type/{start}/{limit}", tags=["consent"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_consent_types(start: int = 0, limit: int = 10):
    try:
        result = await storage.driver.consent_type.load(start=start, limit=limit)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"total": len(result), "result": list(result)}

# todo after second thought this should be removed
# todo consent should be a part of workflow
# @router.post("/consent/profile/{profile_id}", tags=["consent"], include_in_schema=server.expose_gui_api, response_model=dict)
# async def add_consent(profile_id: UUID, consent: ConsentSchema):
#     try:
#         profile_to_modify = await storage.driver.profile.load_by_id(str(profile_id))
#         if profile_to_modify is None:
#             raise HTTPException(status_code=500, detail="There is no profile with id: {}".format(profile_id))
#
#         profile_to_modify.consents[consent.id] = consent.content[consent.id]
#         result = await storage.driver.profile.save_profile(profile_to_modify)
#     except ElasticsearchException as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     return result
