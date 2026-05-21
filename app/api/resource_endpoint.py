from typing import Optional
from fastapi import APIRouter, Depends

from tracardi.domain.enum.type_enum import TypeEnum
from tracardi.exceptions.log_handler import get_logger
from tracardi.service.setup.setup_resources import get_type_of_resources
from tracardi.domain.resource import Resource
from .auth.permissions import Permissions
from tracardi.config import tracardi

import tracardi.service.storage.mysql.interface as mysql

logger = get_logger(__name__)

router = APIRouter()


async def _load_record(id: str) -> Optional[Resource]:
    return await mysql.resource_dao.load_resource_by_id(id)


async def _store_record(resource: Resource):
    return await mysql.resource_dao.insert_resource(resource)


@router.get("/resources/type/{type}",
            tags=["resource"],
            response_model=dict,
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def resource_types_list(type: TypeEnum) -> dict:
    """
    Returns a list of source types. Each source requires a source type to define what kind of data is
    that source holding.

    * Endpoint /resources/type/name will return only names and id.
    * Endpoint /resources/type/configuration will return all data.
    """

    resources = sorted(list(get_type_of_resources()), key=lambda x: x[0])

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
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def list_resources_names_by_tag(tag: str):
    """
    Returns list of resources that have defined tag. This list contains only id and name.
    """
    resources, total = await mysql.resource_dao.load_resources_entities_by_tag(tag)

    return {
        "total": total,
        "result": resources
    }


@router.get("/resources/entity",
            tags=["resource"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def list_all_resources():
    resources, total = await mysql.resource_dao.load_all_resource_entities(limit=250)
    return {
        "total": total,
        "result": resources
    }


@router.get("/resources",
            tags=["resource"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def list_resources():
    resources, total = await mysql.resource_dao.load_all_resources()
    return {
        "total": total,
        "result": resources
    }


@router.get("/resources/by_type",
            tags=["resource"],
            dependencies=[Depends(Permissions(roles=["admin", "developer", "marketer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def list_resources_by_type(query: str = None, limit: int = 200):
    resources, _ = await mysql.resource_dao.load_all_resources(search=query, limit=limit)

    total = await mysql.resource_dao.count_resources(query)

    return {
        "total": max([len(resources), total]),
        "grouped": {"Resources": resources}
    }


@router.get("/resource/{id}",
            tags=["resource"],
            response_model=Optional[Resource],
            dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
            include_in_schema=tracardi.expose_gui_api)
async def get_resource_by_id(id: str) -> Optional[Resource]:
    """
    Returns source data with given id.
    """

    return await mysql.resource_dao.load_resource_by_id(id)


@router.post("/resource",
             tags=["resource"],
             dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
             include_in_schema=tracardi.expose_gui_api)
async def upsert_resource(resource: Resource):
    return await _store_record(resource)


@router.delete("/resource/{id}",
               tags=["resource"],
               dependencies=[Depends(Permissions(roles=["admin", "developer"]))],
               include_in_schema=tracardi.expose_gui_api)
async def delete_resource(id: str):
    return await mysql.resource_dao.delete_resource_by_id(id)
