from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.api.auth.permissions import Permissions
from tracardi.event_server.utils.memory_cache import MemoryCache, CacheItem
from app.config import server
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import storage_manager
from tracardi.service.storage.elastic_client import ElasticClient
from tracardi.service.storage.indices_manager import check_indices_mappings_consistency

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer"]))]
)

memory_cache = MemoryCache()


@router.get("/storage/mapping/check", tags=["storage"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def check_indices_mapping_consistency():
    return await check_indices_mappings_consistency()


@router.get("/storage/mapping/{index}/metadata", tags=["storage"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_index_mapping(index: str):
    """
    Returns metadata of given index (str)
    """
    memory_key = f"{index}-mapping-cache"
    if memory_key not in memory_cache:
        mapping = await storage_manager(index).get_mapping()
        fields = mapping.get_field_names()
        memory_cache[memory_key] = CacheItem(data=fields, ttl=5)  # result is cached for 5 seconds
    return {"result": memory_cache[memory_key].data, "total": len(memory_cache[memory_key].data)}


@router.get("/storage/mapping/{index}", tags=["storage"], include_in_schema=server.expose_gui_api, response_model=list)
async def get_index_mapping(index: str):
    """
    Returns mapping of given index (str)
    """
    mapping = await storage.driver.raw.mapping(index)
    return mapping.get_field_names()


@router.get("/storage/task/{task_id}", tags=["storage"], include_in_schema=server.expose_gui_api)
async def storage_task_status(task_id: str):
    """
    Returns the status of storage task.
    """

    return await storage.driver.raw.task_status(task_id)


@router.get("/storage/reindex/{source}/{destination}", tags=["storage"], include_in_schema=server.expose_gui_api)
async def reindex_data(source: str, destination: str, wait_for_completion: bool = True):
    """
    Copies data from one index to another.
    """

    return await storage.driver.raw.reindex(source, destination, wait_for_completion)


@router.delete("/storage/index/{index_name}", tags=["storage"], include_in_schema=server.expose_gui_api)
async def delete_index(index_name: str):
    """
    Deletes storage index
    """

    es = ElasticClient.instance()
    return await es.remove_index(index_name)


""" Snapshots """


@router.get("/storage/snapshot-repository/{name}", tags=["storage"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_snapshot_repository(name: str):
    """
    List repository snapshots
    """

    return await storage.driver.snapshot.get_snapshot_repository(repo=name)


@router.get("/storage/snapshot-repository/status/{name}", tags=["storage"], include_in_schema=server.expose_gui_api,
            response_model=dict)
async def get_snapshot_repository_status(name: Optional[str] = "_all"):
    """
    Lists available snapshots withing the repository name. Use _all as a name to get all repos snapshots.
    """

    return await storage.driver.snapshot.get_repository_snapshots(repo=name)
