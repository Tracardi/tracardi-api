import tracardi.service.storage.mysql.interface as mysql

from typing import Optional, Dict
from fastapi import APIRouter, Response, Depends
from tracardi.service.destination.utils import get_destination_types
from .auth.permissions import Permissions
from tracardi.domain.resource import Resource
from tracardi.domain.destination import Destination
from tracardi.service.storage.mysql.mapping.resource_mapping import map_to_resource
from tracardi.service.storage.mysql.service.resource_service import ResourceService
from tracardi.config import tracardi
from tracardi.service.license import License

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.post("/destination", tags=["destination"], include_in_schema=tracardi.expose_gui_api)
async def save_destination(destination: Destination):
    """
    Upserts destination data.
    """
    await mysql.destination_dao.insert_destination(destination)


@router.get("/destination/{id}", tags=["destination"], response_model=Optional[Destination],
            include_in_schema=tracardi.expose_gui_api)
async def get_destination(id: str, response: Response):
    """
    Returns destination or None if destination does not exist.
    """

    destination = await mysql.destination_dao.load_destination_by_id(id)

    if not destination:
        response.status_code = 404
        return None

    return destination


@router.get("/destinations/type", tags=["destination"], response_model=dict, include_in_schema=tracardi.expose_gui_api)
async def get_destinations_type_list():
    """
    Returns destination types.
    """
    return {key: value for key, value in get_destination_types()}


@router.get("/destinations/by_tag", tags=["destination"], response_model=dict,
            include_in_schema=tracardi.expose_gui_api)
async def get_destinations(query: str = None, start: int = 0, limit: int = 100) -> dict:
    destinations, total = await mysql.destination_dao.load_all_destinations(query, start, limit)

    return {
        "total": total,
        "grouped": {
            "Destinations": destinations
        }
    }


@router.delete("/destination/{id}", tags=["destination"], include_in_schema=tracardi.expose_gui_api)
async def delete_destination_by_id(id: str):
    """
    Deletes destination with given id
    """
    await mysql.destination_dao.delete_destination(id)

    return True


@router.get("/destinations/entity",
            tags=["resource"],
            response_model=Dict[str, Resource],
            include_in_schema=tracardi.expose_gui_api)
async def list_destination_resources():
    rs = ResourceService()
    records = await rs.load_resource_with_destinations()

    result = {}
    for resource in records.map_to_objects(map_to_resource):
        if resource.is_destination():
            if resource.destination.pro is True and not License.has_license():
                continue
            result[resource.id] = resource
    return result
