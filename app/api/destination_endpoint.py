from typing import Optional

from fastapi import APIRouter, Response, Depends

from tracardi.service.setup.setup_resources import get_destinations
from tracardi.service.storage.driver.elastic import destination as destination_db
from tracardi.service.storage.driver.elastic import resource as resource_db
from tracardi.domain.destination import Destination, DestinationRecord
from .auth.permissions import Permissions
from ..config import server
from ..service.grouping import group_records

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.post("/destination", tags=["destination"], response_model=dict,
             include_in_schema=server.expose_gui_api)
async def save_destination(destination: Destination):
    """
    Upserts destination data.
    """

    record = DestinationRecord.encode(destination)
    result = await destination_db.save(record)
    await destination_db.refresh()
    return result


@router.get("/destination/{id}", tags=["destination"], response_model=Optional[Destination],
            include_in_schema=server.expose_gui_api)
async def get_destination(id: str, response: Response):
    """
    Returns destination or None if destination does not exist.
    """
    destination_record = await destination_db.load(id)

    if destination_record is None:
        response.status_code = 404
        return None

    return destination_record.decode()


@router.get("/destinations", tags=["destination"], response_model=dict,
            include_in_schema=server.expose_gui_api)
async def get_destinations_list():
    """
    Returns destinations.
    """

    storage_result = await destination_db.load_all()
    return storage_result.dict()


@router.get("/destinations/type", tags=["destination"], response_model=dict, include_in_schema=server.expose_gui_api)
async def get_destinations_type_list():
    """
    Returns destination types.
    """
    return {key: value for key, value in get_destinations()}


@router.get("/destinations/by_tag", tags=["destination"], response_model=dict, include_in_schema=server.expose_gui_api)
async def get_destinations_by_tag(query: str = None, start: int = 0, limit: int = 100) -> dict:
    result = await destination_db.load_all(start, limit=limit)
    return group_records(result, query, group_by='tags', search_by='name', sort_by='name')


@router.delete("/destination/{id}", tags=["destination"], include_in_schema=server.expose_gui_api)
async def delete_destination(id: str, response: Response):
    """
    Deletes destination with given id
    """
    result = await destination_db.delete(id)

    if result is None:
        response.status_code = 404
        return None

    await destination_db.refresh()
    return True


@router.get("/destinations/entity",
            tags=["resource"],
            include_in_schema=server.expose_gui_api)
async def list_destination_resources():
    data, total = await resource_db.load_destinations()
    result = {r.id: r for r in data if r.is_destination()}
    return result
