from typing import Optional

from fastapi import APIRouter, Depends
from app.api.auth.permissions import Permissions
from app.service.grouping import group_records
from tracardi.config import tracardi

from tracardi.domain.consent_type import ConsentType
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from tracardi.service.storage.driver.elastic import consent_type as consent_type_db

router = APIRouter()


@router.post("/consent/type", tags=["consent"],
             dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
             include_in_schema=tracardi.expose_gui_api, response_model=BulkInsertResult)
async def add_consent_type(data: ConsentType):
    """
    Adds new consent type to the database. Accessible for roles: "admin", "marketer", "developer"
    """
    result = await consent_type_db.add_consent(id=data.name.lower().replace(" ", "-"), **data.model_dump())
    await consent_type_db.refresh()
    return result


@router.get("/consent/type/{consent_id}", dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
            tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=Optional[dict])
async def get_consent_type(consent_id: str):
    """
    Returns consent type with given id (lowercase name with dashes instead of spaces).
    Accessible for roles: "admin", "marketer", "developer"
    """
    return await consent_type_db.get_by_id(consent_id)


@router.delete("/consent/type/{consent_id}",
               dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))], tags=["consent"],
               include_in_schema=tracardi.expose_gui_api,
               response_model=dict)
async def delete_consent_type(consent_id: str):
    """
    Deletes consent type with given id (lowercase name with dashes instead of spaces),
    Accessible for roles: "admin", "marketer", "developer"
    """
    result = await consent_type_db.delete_by_id(consent_id)
    await consent_type_db.refresh()
    return {"deleted": 1 if result is not None and "result" in result and result["result"] == "deleted" else 0}


@router.get("/consents/type", dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
            tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_consent_types(start: int = 0, limit: int = 100):
    """
    Lists consent types with defined start (int) and limit (int),
    Accessible for roles: "admin", "marketer", "developer"
    """
    result = await consent_type_db.load_all(start=start, limit=limit)
    return {"total": len(result), "result": list(result)}


@router.get("/consents/type/enabled", tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_enabled_consent_types(limit: int = 100):
    """
    Lists only enabled consent types with defined limit (int)
    """

    result = await consent_type_db.load_all_active(limit=limit)
    return {"total": len(result), "result": list(result)}


@router.put("/consents/type/refresh", dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
            tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def refresh_consent_types():
    """
    Refreshes database consent type index. Accessible for roles: "admin", "marketer", "developer"
    """

    return await consent_type_db.refresh()


@router.get("/consents/type/by_tag", tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_consent_types(query: str = None, start: int = 0, limit: int = 10):
    """
    Returns consent types grouped by query on name field.
    """
    result = await consent_type_db.load_all(start=start, limit=limit)
    return group_records(result, query, group_by='tags', search_by='name', sort_by='name')


@router.get("/consents/type/ids", tags=["consent"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def get_consent_ids(query: str = None, limit: int = 1000):
    """
    Returns list of all enabled consent ids
    """
    result = await consent_type_db.query({
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
