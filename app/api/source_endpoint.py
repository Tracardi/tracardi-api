from collections import defaultdict
from time import sleep

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from .auth.authentication import get_current_user
from .grouper import search
from tracardi.domain.resource import Resource, ResourceRecord
from tracardi.domain.entity import Entity
from tracardi.domain.enum.indexes_source_bool import IndexesSourceBool
from tracardi.domain.resources import Resources
from tracardi.domain.value_object.bulk_insert_result import BulkInsertResult
from tracardi.event_server.service.persistence_service import PersistenceService
from tracardi.service.storage.elastic_storage import ElasticStorage

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)


@router.get("/resources/types", tags=["resource"], response_model=dict)
async def get_source_types() -> dict:
    """
    Returns a list of source types. Each source requires a source type to define what kind of data is
    that source holding.
    """

    try:
        return {"total": 10,
                "result": [
                    "web-page",
                    "mysql",
                    "rabbitmq",
                    "kafka",
                    "smtp-server",
                    "ip-geo-locator",
                    "postgresql",
                    "redshif",
                    "twillo",
                    "redis",
                    "mongodb"
                ]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources", tags=["resource"])
async def list_sources():
    try:
        resources = Resources()
        result = await resources.bulk().load()
        total = result.total
        result = [ResourceRecord.construct(Resource.__fields_set__, **r).decode() for r in result]

        return {
            "total": total,
            "result": list(result)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources/by_tag", tags=["resource"])
async def list_sources(query: str = None):
    try:
        resources = Resources()
        result = await resources.bulk().load()
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
            if isinstance(resource.origin, list):
                for group in resource.origin:
                    groups[group].append(resource)
            elif isinstance(resource.origin, str):
                groups[resource.origin].append(resource)

        # Sort
        groups = {k: sorted(v, key=lambda r: r.name, reverse=False) for k, v in groups.items()}

        return {
            "total": total,
            "grouped": groups
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resource/{id}/{type}/on", tags=["resource"], response_model=dict)
async def set_source_property_on(id: str, type: IndexesSourceBool):
    try:
        entity = Entity(id=id)

        record = await entity.storage("source").load(ResourceRecord)  # type: ResourceRecord

        resource = record.decode()
        resource_data = resource.dict()
        resource_data[type.value] = True
        resource = Resource.construct(_fields_set=resource.__fields_set__, **resource_data)
        record = ResourceRecord.encode(resource)

        return await record.storage().save()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resource/{id}/{type}/off", tags=["resource"], response_model=dict)
async def set_source_property_off(id: str, type: IndexesSourceBool):
    try:
        entity = Entity(id=id)

        record = await entity.storage("source").load(ResourceRecord)  # type: ResourceRecord

        resource = record.decode()
        resource_data = resource.dict()
        resource_data[type.value] = False
        resource = Resource.construct(_fields_set=resource.__fields_set__, **resource_data)
        record = ResourceRecord.encode(resource)

        return await record.storage().save()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resource/{id}", tags=["resource"], response_model=Resource)
async def get_source_by_id(id: str) -> Resource:
    """
    Returns source data with given id.

    """

    try:
        entity = Entity(id=id)
        record = await entity.storage("source").load(ResourceRecord)  # type: ResourceRecord
        return record.decode()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resource", tags=["resource"], response_model=BulkInsertResult)
async def upsert_source(resource: Resource):
    sleep(1)
    try:
        record = ResourceRecord.encode(resource)
        return await record.storage().save()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/resource/{id}", tags=["resource"], response_model=dict)
async def delete_source(id: str):
    try:
        entity = Entity(id=id)
        return await entity.storage("source").delete()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resources/refresh", tags=["resource"])
async def refresh_sources():
    service = PersistenceService(ElasticStorage(index_key='source'))
    return await service.refresh()
