from fastapi import APIRouter, Depends
from app.api.auth.permissions import Permissions
from tracardi.config import tracardi

from tracardi.domain.consent_type import ConsentType
from tracardi.service.storage.mysql.mapping.consent_type_mapping import map_to_consent_type
from tracardi.service.storage.mysql.service.consent_type_service import ConsentTypeService

router = APIRouter()


@router.post("/consent/type", tags=["consent"],
             dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
             include_in_schema=tracardi.expose_gui_api)
async def add_consent_type(data: ConsentType):
    """
    Adds new consent type to the database. Accessible for roles: "admin", "marketer", "developer"
    """

    data.id = data.name.lower().replace(" ", "-")

    cts = ConsentTypeService()
    await cts.insert(data)

    return True


@router.get("/consent/type/{consent_id}", dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
            tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=ConsentType)
async def get_consent_type(consent_id: str):
    """
    Returns consent type with given id (lowercase name with dashes instead of spaces).
    Accessible for roles: "admin", "marketer", "developer"
    """

    cts = ConsentTypeService()
    return (await cts.load_by_id(consent_id)).map_to_object(map_to_consent_type)



@router.delete("/consent/type/{consent_id}",
               dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))], tags=["consent"],
               include_in_schema=tracardi.expose_gui_api)
async def delete_consent_type(consent_id: str):
    """
    Deletes consent type with given id (lowercase name with dashes instead of spaces),
    Accessible for roles: "admin", "marketer", "developer"
    """

    cts = ConsentTypeService()
    return await cts.delete_by_id(consent_id)



@router.get("/consents/type", dependencies=[Depends(Permissions(roles=["admin", "marketer", "developer"]))],
            tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_consent_types(start: int = 0, limit: int = 200):
    """
    Lists consent types with defined start (int) and limit (int),
    Accessible for roles: "admin", "marketer", "developer"
    """
    cts = ConsentTypeService()
    result = await cts.load_all(limit=limit, offset=start)

    return {
        "total": result.count(),
        "result": list(result.map_to_objects(map_to_consent_type))
    }


@router.get("/consents/type/by_tag", tags=["consent"], include_in_schema=tracardi.expose_gui_api,
            response_model=dict)
async def get_consent_types(query: str = None, start: int = 0, limit: int = 10):
    """
    Returns consent types grouped by query on name field.
    """
    cts = ConsentTypeService()
    result = await cts.load_all(offset=start, limit=limit)
    return {
        "total": result.count(),
        "grouped": {
            "Consent types": list(result.map_to_objects(map_to_consent_type))
        }
    }



@router.get("/consents/type/ids", tags=["consent"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def get_consent_ids(query: str = None, limit: int = 100):
    """
    Returns list of all enabled consent ids
    """

    cts = ConsentTypeService()
    records = await cts.load_keys(limit=limit)

    return {
        "total": records.count(),
        "result": [id for id in records.rows]
    }
