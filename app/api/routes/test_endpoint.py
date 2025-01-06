from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from app.service.grouping import get_grouped_result
from tracardi.domain.test import Test
from tracardi.service.adapter.bigdata.adapter_selector import bd_raw_adapter
from tracardi.service.adapter.cache_adaper_selector import cache_adapter
from tracardi.service.storage.index import Resource
from tracardi.service.storage.mysql.mapping.test_mapping import map_to_test
from tracardi.service.storage.mysql.service.test_service import TestService
from tracardi.service.storage.elastic.driver.elastic_client import ElasticClient

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from datetime import datetime

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer", "developer"]))]
)

ts = TestService()
_cache = cache_adapter()
_bd_raw_adapter = bd_raw_adapter()

@router.get("/test/redis", tags=["test"], include_in_schema=tracardi.expose_gui_api)
async def ping_redis():
    """
    Tests connection between Redis instance and Tracardi instance. Accessible for roles: "admin"
    """
    pong = _cache.ping()
    if pong is not True:
        raise ConnectionError("Redis did not respond.")


@router.get("/test/elasticsearch", tags=["test"], include_in_schema=tracardi.expose_gui_api)
async def get_es_cluster_health():
    """
    Tests connection between Elasticsearch and Tracardi by returning cluster info. Accessible for roles: "admin"
    """

    health = await _bd_raw_adapter.health()
    if not isinstance(health, dict):
        raise ConnectionError("Elasticsearch did not pass health check.")
    settings = await _bd_raw_adapter.get_settings()
    if settings:
        health['settings'] = settings
    return health


@router.get("/test/elasticsearch/indices", tags=["test"], include_in_schema=tracardi.expose_gui_api)
async def get_es_indices():
    """
    Returns list of indices in elasticsearch cluster. Accessible for roles: "admin"
    """

    if tracardi.multi_tenant:
        raise HTTPException(status_code=405, detail="This section is not allowed for multi-tenant server.")

    resource_aliases = Resource().list_aliases()

    es = ElasticClient.instance()
    result = await es.list_indices()
    output = {}
    for key in result:

        if key[0] == '.':
            continue

        current_index_aliases = list(result[key]["aliases"].keys())

        index = result[key]
        index["settings"]["index"]["creation_date"] = \
            datetime.utcfromtimestamp(int(result[key]["settings"]["index"]["creation_date"]) // 1000)
        index["connected"] = bool(set(current_index_aliases).intersection(resource_aliases))
        index["head"] = len(current_index_aliases) != 1 or not current_index_aliases[0].endswith('.prev')

        output[key] = index

    return output

@router.get("/test/{id}", tags=["deployment"], include_in_schema=tracardi.expose_gui_api)
async def get_test(id: str):
    record = await ts.load_by_id(id)
    if not record.exists():
        raise HTTPException(status_code=404, detail=f"Test with ID {id} not found.")

    return record.map_to_object(map_to_test)


@router.get("/test", tags=["deployment"], include_in_schema=tracardi.expose_gui_api)
async def list_tests(query: Optional[str] = None, limit: int = 200):
    records = await ts.load_all(search=query, limit=limit)

    return get_grouped_result("Tests", records, map_to_test)


@router.post("/test", tags=["deployment"], include_in_schema=tracardi.expose_gui_api)
async def add_test(test: Test):
    return await ts.upsert(test)


@router.delete("/test/{id}", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def delete_test(id: str):
    """
    Deletes test from the database
    """
    return await ts.delete_by_id(id)


@router.get("/es/shards/unassigned", tags=["report"], include_in_schema=tracardi.expose_gui_api)
async def shards(index: str):
    client = ElasticClient.instance()
    shards =  await client.shards()

    unassigned = [shard for shard in shards if shard["state"] == "UNASSIGNED"]

    result = []
    for shard in unassigned:
        response = await client.cluster.allocation_explain(
            body={
                "index": shard['index'],
                "shard": shard['shard'],
                "primary": shard['prirep'] == 'p'
            }
        )
        result.append({
            "shard": shard,
            "info": response
        })
    return result
