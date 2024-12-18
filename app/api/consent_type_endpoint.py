from fastapi import APIRouter, Depends
from app.api.auth.permissions import Permissions
from tracardi.config import tracardi

from tracardi.domain.consent_type import ConsentType
import tracardi.service.storage.mysql.interface.consent_type as consent_type_dao

router = APIRouter()


@router.post("/consent/type", tags=["consent"],
             dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
             include_in_schema=tracardi.expose_gui_api)
async def add_consent_type(data: ConsentType):
    """
    Adds new consent type to the database. Accessible for roles: "admin", "marketer", "developer"
    """

    data.id = data.name.lower().replace(" ", "-")

    await consent_type_dao.insert(data)

    return True


@router.get("/consent/type/{consent_id}", dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
            tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=ConsentType)
async def get_consent_type(consent_id: str):
    """
    Returns consent type with given id (lowercase name with dashes instead of spaces).
    Accessible for roles: "admin", "marketer", "developer"
    """

    return await consent_type_dao.load_by_id(consent_id)


@router.delete("/consent/type/{consent_id}",
               dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))], tags=["consent"],
               include_in_schema=tracardi.expose_gui_api)
async def delete_consent_type(consent_id: str):
    """
    Deletes consent type with given id (lowercase name with dashes instead of spaces),
    Accessible for roles: "admin", "marketer", "developer"
    """

    return await consent_type_dao.delete_by_id(consent_id)


@router.get("/consents/type", dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
            tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_consent_types(start: int = 0, limit: int = 200):
    """
    Lists consent types with defined start (int) and limit (int),
    Accessible for roles: "admin", "marketer", "developer"
    """
    result, total = await consent_type_dao.load(limit=limit, offset=start)
    return {
        "total": total,
        "result": result
    }


@router.get("/consents/types", tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
# Obsolete
@router.get("/consents/type/by_tag", tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_consent_types(query: str = None, start: int = 0, limit: int = 10):
    """
    Returns consent types grouped by query on name field.
    """
    result, total = await consent_type_dao.load(search=query, offset=start, limit=limit)
    return {
        "total": total,
        "grouped": {
            "Consent types": result
        }
    }

@router.get("/consents/type/enabled", tags=["consent"], include_in_schema=tracardi.expose_gui_api)
@router.get("/consents/type/ids", tags=["consent"], include_in_schema=tracardi.expose_gui_api)
async def get_consent_ids(query: str = None, limit: int = 100):
    """
    Returns list of all enabled consent ids
    """

    records, total = await consent_type_dao.load_enabled(limit=limit)

    return {
        "total": total,
        "result": records
    }
