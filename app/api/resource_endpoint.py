import logging
from collections import defaultdict
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Response

from tracardi.config import tracardi
from tracardi.domain.enum.type_enum import TypeEnum
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.setup.setup_resources import get_type_of_resources
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor, StorageForBulk
from tracardi.service.wf.domain.named_entity import NamedEntity
from app.service.grouper import search
from tracardi.domain.resource import Resource, ResourceRecord
from tracardi.domain.entity import Entity
from tracardi.domain.enum.indexes_source_bool import IndexesSourceBool
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from .auth.permissions import Permissions
from ..config import server

logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "developer"]))]
)


@router.get("/resources/type/{type}",
            tags=["resource"],
            response_model=dict,
            include_in_schema=server.expose_gui_api)
async def resource_types_list(type: TypeEnum) -> dict:
    """
    Returns a list of source types. Each source requires a source type to define what kind of data is
    that source holding.

    * Endpoint /resources/type/name will return only names and id.
    * Endpoint /resources/type/configuration will return all data.
    """

    try:

        if type.value == 'name':
            resource_types = {id: value['name'] for id, value in get_type_of_resources()}
        else:
            resource_types = {id: value for id, value in get_type_of_resources()}

        return {
            "total": len(resource_types),
            "result": resource_types
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources/entity/tag/{tag}",
            tags=["resource"],
            include_in_schema=server.expose_gui_api)
async def list_resources_names_by_tag(tag: str):
    """
    Returns list of resources that have defined tag. This list contains only id and name.
    """

    try:
        result = await storage.driver.resource.load_by_tag(tag)
        total = result.total
        result = [NamedEntity(**r) for r in result]

        return {
            "total": total,
            "result": list(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources/tag/{tag}",
            tags=["resource"],
            include_in_schema=server.expose_gui_api)
async def list_resources_by_tag(tag: str):
    """
    Returns list of resources that have defined tag. This list contains all data along with credentials.
    """
    try:
        result = await storage.driver.resource.load_by_tag(tag)
        total = result.total
        result = [ResourceRecord(**r).decode() for r in result]

        return {
            "total": total,
            "result": list(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources/entity",
            tags=["resource"],
            include_in_schema=server.expose_gui_api)
async def list_resources():
    try:
        result = await StorageForBulk().index('resource').load()
        total = result.total
        result = [NamedEntity(**r) for r in result]

        return {
            "total": total,
            "result": list(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources",
            tags=["resource"],
            include_in_schema=server.expose_gui_api)
async def list_resources():
    try:
        result = await StorageForBulk().index('resource').load()
        total = result.total
        result = [ResourceRecord.construct(Resource.__fields_set__, **r).decode() for r in result]

        return {
            "total": total,
            "result": list(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources/by_type",
            tags=["resource"],
            include_in_schema=server.expose_gui_api)
async def list_resources(query: str = None):
    try:

        result = await StorageForBulk().index('resource').load()

        total = result.total
        result = [ResourceRecord.construct(Resource.__fields_set__, **r).decode() for r in result]

        # Filtering
        if query is not None and len(query) > 0:
            query = query.lower()
            if query:
                result = [r for r in result if query in r.name.lower() or search(query, r.type)]

        # Grouping
        groups = defaultdict(list)
        for resource in result:  # type: Resource
            if isinstance(resource.groups, list):
                if len(resource.groups) == 0:
                    groups["general"].append(resource)
                else:
                    for group in resource.groups:
                        groups[group].append(resource)
            elif isinstance(resource.groups, str):
                groups[resource.groups].append(resource)

        # Sort
        groups = {k: sorted(v, key=lambda r: r.name, reverse=False) for k, v in groups.items()}

        return {
            "total": total,
            "grouped": groups
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resource/{id}/{type}/on",
            tags=["resource"],
            response_model=dict,
            include_in_schema=server.expose_gui_api)
async def set_resource_property_on(id: str, type: IndexesSourceBool):
    try:
        entity = Entity(id=id)

        record = await StorageFor(entity).index("resource").load(ResourceRecord)  # type: ResourceRecord

        resource = record.decode()
        resource_data = resource.dict()
        resource_data[type.value] = True
        resource = Resource.construct(_fields_set=resource.__fields_set__, **resource_data)
        record = ResourceRecord.encode(resource)

        return await StorageFor(record).index().save()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resource/{id}/{type}/off",
            tags=["resource"],
            response_model=dict,
            include_in_schema=server.expose_gui_api)
async def set_resource_property_off(id: str, type: IndexesSourceBool):
    try:
        entity = Entity(id=id)

        record = await StorageFor(entity).index("resource").load(ResourceRecord)  # type: ResourceRecord

        resource = record.decode()
        resource_data = resource.dict()
        resource_data[type.value] = False
        resource = Resource.construct(_fields_set=resource.__fields_set__, **resource_data)
        record = ResourceRecord.encode(resource)

        return await StorageFor(record).index().save()
        # return await record.storage().save()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resource/{id}",
            tags=["resource"],
            response_model=Optional[Resource],
            include_in_schema=server.expose_gui_api)
async def get_resource_by_id(id: str, response: Response) -> Optional[Resource]:
    """
    Returns source data with given id.

    """

    try:
        entity = Entity(id=id)
        record = await StorageFor(entity).index("resource").load(ResourceRecord)  # type: ResourceRecord
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if record is not None:
        return record.decode()

    response.status_code = 404
    return None


@router.post("/resource", tags=["resource"],
             response_model=BulkInsertResult,
             include_in_schema=server.expose_gui_api)
async def upsert_resource(resource: Resource):
    try:
        record = ResourceRecord.encode(resource)
        return await StorageFor(record).index().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/resource/{id}", tags=["resource"],
               response_model=dict,
               include_in_schema=server.expose_gui_api)
async def delete_resource(id: str, response: Response):
    try:
        result = await StorageFor(Entity(id=id)).index("resource").delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        response.status_code = 404
        return None

    try:
        await storage.driver.resource.refresh()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources/refresh",
            tags=["resource"],
            include_in_schema=server.expose_gui_api)
async def refresh_resources():
    return await storage.driver.resource.refresh()
