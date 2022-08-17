from fastapi import APIRouter, Depends, HTTPException
from app.api.auth.permissions import Permissions
from app.config import server
from app.service.grouping import group_records

from tracardi.domain.consent_type import ConsentType
from tracardi.service.storage.driver import storage
from elasticsearch import ElasticsearchException
from tracardi.service.storage.factory import StorageForBulk

router = APIRouter()


@router.post("/consent/type", tags=["consent"],
             dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
             include_in_schema=server.expose_gui_api, response_model=dict)
async def add_consent_type(data: ConsentType):
    """
    Adds new consent type to the database. Accessible for roles: "admin", "marketer", "developer"
    """
    try:
        result = await storage.driver.consent_type.add_consent(id=data.name.lower().replace(" ", "-"), **data.dict())
        await storage.driver.consent_type.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@router.get("/consent/type/{consent_id}", dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
            tags=["consent"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_consent_type(consent_id: str):
    """
    Returns consent type with given id (lowercase name with dashes instead of spaces).
    Accessible for roles: "admin", "marketer", "developer"
    """
    try:
        return await storage.driver.consent_type.get_by_id(consent_id)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/consent/type/{consent_id}",
               dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))], tags=["consent"],
               include_in_schema=server.expose_gui_api,
               response_model=dict)
async def delete_consent_type(consent_id: str):
    """
    Deletes consent type with given id (lowercase name with dashes instead of spaces),
    Accessible for roles: "admin", "marketer", "developer"
    """
    try:
        result = await storage.driver.consent_type.delete_by_id(consent_id)
        await storage.driver.consent_type.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"deleted": 1 if result is not None and "result" in result and result["result"] == "deleted" else 0}


@router.get("/consents/type", dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
            tags=["consent"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_consent_types(start: int = 0, limit: int = 100):
    """
    Lists consent types with defined start (int) and limit (int),
    Accessible for roles: "admin", "marketer", "developer"
    """
    try:
        result = await storage.driver.consent_type.load_all(start=start, limit=limit)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"total": len(result), "result": list(result)}


@router.get("/consents/type/enabled", tags=["consent"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_enabled_consent_types(limit: int = 100):
    """
    Lists only enabled consent types with defined limit (int)
    """
    try:
        result = await storage.driver.consent_type.load_all_active(limit=limit)
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"total": len(result), "result": list(result)}


@router.put("/consents/type/refresh", dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
            tags=["consent"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def refresh_consent_types():
    """
    Refreshes database consent type index. Accessible for roles: "admin", "marketer", "developer"
    """
    try:
        return await storage.driver.consent_type.refresh()
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/consents/type/by_tag", tags=["consent"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_consent_types(query: str = None, start: int = 0, limit: int = 10):
    """
    Returns consent types grouped by query on name field.
    """
    try:
        result = await storage.driver.consent_type.load_all(start=start, limit=limit)
        return group_records(result, query, group_by='tags', search_by='name', sort_by='name')
    except ElasticsearchException as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/consents/type/ids", tags=["consent"], include_in_schema=server.expose_gui_api, response_model=dict)
async def get_consent_ids(query: str = None, limit: int = 1000):
    """
    Returns list of all enabled consent ids
    """
    result = await StorageForBulk().index('consent-type').storage.query({
        "query": {
            "term": {
                "enabled": True
            }
        },
        "size": "0",
            "aggs": {
                "uniq": {
                    "terms": {
                        "field": "id",
                        "size": limit
                    }
                }
            }
    })
    return {
        "total": result.total,
        "result": [consent["key"] for consent in result.aggregations("uniq").buckets()]
    }
