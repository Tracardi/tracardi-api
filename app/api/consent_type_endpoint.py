from fastapi import APIRouter, Depends, HTTPException
from app.api.auth.authentication import get_current_user
from app.config import server
from app.service.grouping import group_records

from tracardi.domain.consent_type import ConsentType
from tracardi.service.storage.driver import storage
from elasticsearch import ElasticsearchException

router = APIRouter()


@router.post("/consent/type", tags=["consent"], include_in_schema=server.expose_gui_api, response_model=dict)
async def add_consent_type(data: ConsentType, depends=Depends(get_current_user)):
    try:
        result = await storage.driver.consent_type.add_consent(id=data.name.lower().replace(" ", "-"), **data.dict())
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@router.get("/consent/type/{consent_id}", tags=["consent"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_consent_type(consent_id: str, depends=Depends(get_current_user)):
    try:
        return await storage.driver.consent_type.get_by_id(consent_id)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/consent/type/{consent_id}", tags=["consent"], include_in_schema=server.expose_gui_api,
               response_model=dict)
async def delete_consent_type(consent_id: str, depends=Depends(get_current_user)):
    try:
        result = await storage.driver.consent_type.delete_by_id(consent_id)
        await storage.driver.consent_type.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 1 if result is not None and "result" in result and result["result"] == "deleted" else 0}


@router.get("/consents/type", tags=["consent"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_consent_types(start: int = 0, limit: int = 100, depends=Depends(get_current_user)):
    try:
        result = await storage.driver.consent_type.load_all(start=start, limit=limit)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"total": len(result), "result": list(result)}


@router.get("/consents/type/enabled", tags=["consent"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_enabled_consent_types(limit: int = 100):
    try:
        result = await storage.driver.consent_type.load_all_active(limit=limit)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"total": len(result), "result": list(result)}


@router.get("/consents/type/refresh", tags=["consent"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def refresh_consent_types(depends=Depends(get_current_user)):
    try:
        return await storage.driver.consent_type.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/consents/type/by_tag", tags=["consent"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_consent_types(query: str = None, start: int = 0, limit: int = 10):
    try:
        result = await storage.driver.consent_type.load_all(start=start, limit=limit)
        return group_records(result, query, group_by='id', search_by='name', sort_by='name')
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
