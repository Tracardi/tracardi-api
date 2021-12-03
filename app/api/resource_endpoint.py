from collections import defaultdict
from typing import Optional

from time import sleep

from fastapi import APIRouter
from fastapi import HTTPException, Depends

from tracardi.domain.enum.type_enum import TypeEnum
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor, StorageForBulk
from tracardi_graph_runner.domain.named_entity import NamedEntity

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
            "tracardi-pro": {
                "config": {
                    "url": "http://localhost:12345",
                    "username": "admin",
                    "password": "admin"
                },
                "tags": ['pro', 'api']
            },
            "web-page": {
                "config": {
                    "user": None,
                    "password": None
                },
                "tags": ['web-page']
            },
            "api": {
                "config": {
                    "url": None,
                    "username": None,
                    "password": None
                },
                "tags": ['api']
            },
            "rabbitMQ": {
                "config": {
                    "uri": "amqp://127.0.0.1:5672//",
                    "timeout": 5,
                    "virtual_host": None,
                    "port": None
                },
                "tags": ['rabbitmq', 'queue']
            },
            "aws": {
                "config": {
                    "aws_access_key_id": None,
                    "aws_secret_access_key": None,
                },
                "tags": ['aws', 'cloud', 'token']
            },
            "kafka": {
                "config": {},
                "tags": ['kafka', 'queue']
            },
            "smtp-server": {
                "config": {
                    "smtp": None,
                    "port": None,
                    "username": None,
                    "password": None
                },
                "tags": ['mail', 'smtp']
            },
            "ip-goe-locator": {
                "config": {
                    "host": "geolite.info",
                    "license": None,
                    "accountId": None
                },
                "tags": ['api', 'geo-locator']
            },
            "postgresql": {
                "config": {
                    "host": "localhost",
                    "port": 5432,
                    "user": "postgres",
                    "password": None,
                    "database": None
                },
                "tags": ['database', 'postresql']
            },
            "pushover": {
                "config": {
                    "token": None,
                    "user": None
                },
                "tags": ['pushover', 'message']
            },
            "mysql": {
                "config": {
                    "host": "localhost",
                    "port": 3306,
                    "user": None,
                    "password": None,
                    "database": None
                },
                "tags": ['mysql', 'database']
            },
            "mqtt": {
                "config": {
                    "url": None,
                    "port": None
                },
                "tags": ['mqtt', 'queue']
            },
            "twillo": {
                "config": {
                    "token": None
                },
                "tags": ['token', 'twillo']
            },
            "redis": {
                "config": {
                    "url": None,
                    "user": None,
                    "password": None
                },
                "tags": ['redis']
            },
            "mongodb": {
                "config": {
                    "uri": "mongodb://127.0.0.1:27017/",
                    "timeout": 5000
                },
                "tags": ['mongodb', 'database', 'nosql']
            },
            "token": {
                "config": {
                    "token": None
                },
                "tags": ['token']
            }
        }
        if type.value == 'name':
            types = list(types.keys())

        return {"total": len(types),
                "result": types}

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
            if isinstance(resource.type, list):
                for group in resource.type:
                    groups[group].append(resource)
            elif isinstance(resource.type, str):
                groups[resource.type].append(resource)

        # Sort
        groups = {k: sorted(v, key=lambda r: r.name, reverse=False) for k, v in groups.items()}

        return {
            "total": total,
            "grouped": groups
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources/entity/tag/{tag}",
            tags=["resource"],
            include_in_schema=server.expose_gui_api)
async def get_resource_gey_tag(tag: str = None):
    try:

        # todo fetch resources by tag
        pass

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
    try:
        record = ResourceRecord.encode(resource)
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
