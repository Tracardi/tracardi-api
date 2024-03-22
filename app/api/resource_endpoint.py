from typing import Optional
from fastapi import APIRouter, Depends

from tracardi.domain.enum.type_enum import TypeEnum
from tracardi.exceptions.log_handler import get_logger
from tracardi.service.setup.setup_resources import get_type_of_resources
from tracardi.service.storage.mysql.map_to_named_entity import map_to_named_entity
from tracardi.service.storage.mysql.mapping.resource_mapping import map_to_resource
from tracardi.service.storage.mysql.service.resource_service import ResourceService
from tracardi.domain.resource import Resource
from .auth.permissions import Permissions
from tracardi.config import tracardi
from ..service.grouping import get_result_dict, get_grouped_result

logger = get_logger(__name__)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)

rs = ResourceService()

async def _load_record(id: str) -> Optional[Resource]:
    record = await rs.load_by_id(id)
    return record.map_to_object(map_to_resource)


async def _store_record(resource: Resource):
    return await rs.insert(resource)


@router.get("/resources/type/{type}",
            tags=["resource"],
            response_model=dict,
            include_in_schema=tracardi.expose_gui_api)
async def resource_types_list(type: TypeEnum) -> dict:
    """
    Returns a list of source types. Each source requires a source type to define what kind of data is
    that source holding.

    * Endpoint /resources/type/name will return only names and id.
    * Endpoint /resources/type/configuration will return all data.
    """

    resources = sorted(list(get_type_of_resources()))

    if type.value == 'name':
        resource_types = {id: value['name'] for id, value in resources}
    else:
        resource_types = {id: value for id, value in resources}

    return {
        "total": len(resource_types),
        "result": resource_types
    }


@router.get("/resources/entity/tag/{tag}",
            tags=["resource"],
            include_in_schema=tracardi.expose_gui_api)
async def list_resources_names_by_tag(tag: str):
    """
    Returns list of resources that have defined tag. This list contains only id and name.
    """
    records = await rs.load_by_tag(tag)
    return get_result_dict(records, map_to_named_entity, lambda table_row: table_row.enabled is True)


@router.get("/resources/entity",
            tags=["resource"],
            include_in_schema=tracardi.expose_gui_api)
async def list_all_resources():

    records = await rs.load_all(limit=250)
    return get_result_dict(records, map_to_named_entity)


@router.get("/resources",
            tags=["resource"],
            include_in_schema=tracardi.expose_gui_api)
async def list_resources():
    records = await rs.load_all()
    return get_result_dict(records, map_to_resource)


@router.get("/resources/by_type",
            tags=["resource"],
            include_in_schema=tracardi.expose_gui_api)
async def list_resources_by_type(query: str = None, limit:int = 200):
    records = await rs.load_all(search=query, limit=limit)

    return get_grouped_result("Resources", records, map_to_resource)

@router.get("/resource/{id}",
            tags=["resource"],
            response_model=Optional[Resource],
            include_in_schema=tracardi.expose_gui_api)
async def get_resource_by_id(id: str) -> Optional[Resource]:
    """
    Returns source data with given id.
    """
    record = await rs.load_by_id(id)
    return record.map_to_object(map_to_resource)


@router.post("/resource", tags=["resource"],
             include_in_schema=tracardi.expose_gui_api)
async def upsert_resource(resource: Resource):
    return await _store_record(resource)


@router.delete("/resource/{id}", tags=["resource"],
               include_in_schema=tracardi.expose_gui_api)
async def delete_resource(id: str):
    return await rs.delete_by_id(id)


