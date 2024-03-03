from typing import Optional, Dict

from fastapi import APIRouter, Response, Depends
from .auth.permissions import Permissions
from app.service.grouping import get_grouped_result
from tracardi.domain.resource import Resource
from tracardi.domain.destination import Destination
from tracardi.service.storage.mysql.mapping.destination_mapping import map_to_destination
from tracardi.service.storage.mysql.mapping.resource_mapping import map_to_resource
from tracardi.service.storage.mysql.service.destination_service import DestinationService
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

    ds = DestinationService()
    await ds.insert(destination)


@router.get("/destination/{id}", tags=["destination"], response_model=Optional[Destination],
            include_in_schema=tracardi.expose_gui_api)
async def get_destination(id: str, response: Response):
    """
    Returns destination or None if destination does not exist.
    """

    ds = DestinationService()
    record = await ds.load_by_id(id)

    if not record.exists():
        response.status_code = 404
        return None

    return record.map_to_object(map_to_destination)


@router.get("/destinations/type", tags=["destination"], response_model=dict, include_in_schema=tracardi.expose_gui_api)
async def get_destinations_type_list():
    """
    Returns destination types.
    """
    return {key: value for key, value in DestinationService.get_destination_types()}


@router.get("/destinations/by_tag", tags=["destination"], response_model=dict, include_in_schema=tracardi.expose_gui_api)
async def get_destinations_by_tag(query: str = None, start: int = 0, limit: int = 100) -> dict:
    ds = DestinationService()
    records = await ds.load_all(query, start, limit)

    if not records.exists():
        return {
            "total": 0,
            "grouped": {}
        }

    return get_grouped_result("Destinations", records, map_to_destination)


@router.delete("/destination/{id}", tags=["destination"], include_in_schema=tracardi.expose_gui_api)
async def delete_destination(id: str):
    """
    Deletes destination with given id
    """

    ds = DestinationService()
    await ds.delete_by_id(id)

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
