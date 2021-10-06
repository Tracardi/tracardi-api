from collections import defaultdict
from typing import Optional

from time import sleep

from fastapi import APIRouter
from fastapi import HTTPException, Depends

from tracardi.domain.enum.type_enum import TypeEnum
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor, StorageForBulk

from .auth.authentication import get_current_user
from .grouper import search
from tracardi.domain.resource import Resource, ResourceRecord
from tracardi.domain.entity import Entity
from tracardi.domain.enum.indexes_source_bool import IndexesSourceBool
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from ..config import server

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/resources/type/{type}",
            tags=["resource"],
            response_model=dict,
            include_in_schema=server.expose_gui_api)
async def get_resource_types(type: TypeEnum) -> dict:
    """
    Returns a list of source types. Each source requires a source type to define what kind of data is
    that source holding.
    """

    try:
        types = {
            "web-page": {
                "user": None,
                "password": None
            },
            "rabbitmq": {
                "uri": "amqp://127.0.0.1:5672//",
                "timeout": 5,
                "virtual_host": None,
                "port": None
            },
            "kafka": {},
            "smtp-server": {
                "smtp": None,
                "port": None,
                "username": None,
                "password": None
            },
            "ip-geo-locator": {
                "host": None,
                "license": None,
                "accountId": None
            },
            "postgresql": {
                "host": "localhost",
                "port": 5439,
                "user": None,
                "password": None,
                "database": None
            },
            "pushover": {
                "token": None,
                "user": None
            },
            "redshift": {
                "host": "localhost",
                "port": 5439,
                "user": None,
                "password": None,
                "database": None
            },
            "mysql": {
                "host": "localhost",
                "port": 3306,
                "user": None,
                "password": None,
                "database": None
            },
            "mqtt": {},
            "twillo": {
                "token": None,
            },
            "redis": {
                "url": None,
                "user": None,
                "password": None
            },
            "mongodb": {
                "uri": "mongodb://127.0.0.1:27017/",
                "timeout": 5000
            },
            "api-token": {
                "token": None
            },
        }
        if type.value == 'name':
            types = list(types.keys())

        return {"total": len(types),
                "result": types}

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


# @router.get("/resources/by_id",
#             tags=["resource"],
#             include_in_schema=server.expose_gui_api)
# async def list_resources_by_id():
#     try:
#         result = await StorageForBulk().index('resource').load()
#         total = result.total
#         result = {r['id']: r['name'] for r in result}
#
#         return {
#             "total": total,
#             "result": result
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources/by_tag",
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
            if isinstance(resource.tags, list):
                for group in resource.tags:
                    groups[group].append(resource)
            elif isinstance(resource.tags, str):
                groups[resource.tags].append(resource)

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

        # return await record.storage().save()
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
            response_model=Resource,
            include_in_schema=server.expose_gui_api)
async def get_resource_by_id(id: str) -> Optional[Resource]:
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

    raise HTTPException(status_code=404, detail="Resource id: {} does not exist.".format(id))


@router.post("/resource", tags=["resource"],
             response_model=BulkInsertResult,
             include_in_schema=server.expose_gui_api)
async def upsert_resource(resource: Resource):
    sleep(1)
    try:
        record = ResourceRecord.encode(resource)
        # return await record.storage().save()
        return await StorageFor(record).index().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/resource/{id}", tags=["resource"],
               response_model=dict,
               include_in_schema=server.expose_gui_api)
async def delete_resource(id: str):
    try:
        entity = Entity(id=id)
        result = await StorageFor(entity).index("resource").delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if result is None:
        raise HTTPException(status_code=404, detail="Resource id: {} does not exist.".format(id))

    return result


@router.get("/resources/refresh",
            tags=["resource"],
            include_in_schema=server.expose_gui_api)
async def refresh_resources():
    return await storage.driver.resource.refresh()
