from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response

from app.api.auth.local import is_localhost_only
from app.service.grouping import get_grouped_result
from tracardi.domain.test import Test
from tracardi.service.storage.index import Resource
from tracardi.service.storage.mysql.mapping.test_mapping import map_to_test
from tracardi.service.storage.mysql.service.test_service import TestService
from tracardi.service.storage.redis.driver.redis_client import RedisClient
from tracardi.service.storage.elastic.driver.elastic_client import ElasticClient

from app.api.auth.permissions import Permissions
from tracardi.config import tracardi
from tracardi.service.storage.elastic.interface import raw as raw_db
from datetime import datetime

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer", "developer"]))]
)

ts = TestService()

# Health check router - NO authentication, NO tenant required, localhost-only
health_router = APIRouter(
    prefix="/health",
    tags=["health"],
    dependencies=[Depends(is_localhost_only)]
)

def _redis_connection_test():
    client = RedisClient()
    pong = client.ping()
    return pong

@router.get("/test/redis", tags=["test"], include_in_schema=tracardi.expose_gui_api)
async def ping_redis():
    """
    Tests connection between Redis instance and Tracardi instance. Accessible for roles: "admin"
    """
    pong = _redis_connection_test()
    if pong is not True:
        raise ConnectionError("Redis did not respond.")
    return {"status": "healthy", "service": "redis"}

@router.get("/test/elasticsearch", tags=["test"], include_in_schema=tracardi.expose_gui_api)
async def get_es_cluster_health():
    """
    Tests connection between Elasticsearch and Tracardi by returning cluster info. Accessible for roles: "admin"
    """
    health = await raw_db.health()
    if not isinstance(health, dict):
        raise ConnectionError("Elasticsearch did not pass health check.")
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

# Local Health Checks

@health_router.get("/redis", include_in_schema=True)
async def health_check_redis():
    """
    Health check for Redis connection.

    - **Localhost only**: Only accessible from 127.0.0.1
    - **No authentication required**
    - **No tenant ID required**

    Returns:
        - 200 OK if Redis is healthy
        - 500 if Redis connection fails
    """
    try:
        pong = _redis_connection_test()
        if pong is not True:
            raise ConnectionError("Redis did not respond.")
        return {"status": "healthy", "service": "redis"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis health check failed: {str(e)}")


@health_router.get("/elasticsearch", include_in_schema=True)
async def health_check_elasticsearch():
    """
    Health check for Elasticsearch connection.

    - **Localhost only**: Only accessible from 127.0.0.1
    - **No authentication required**
    - **No tenant ID required**

    Returns:
        - 200 OK with cluster health if Elasticsearch is healthy
        - 500 if Elasticsearch connection fails
    """
    try:
        health = await raw_db.health()
        if not isinstance(health, dict):
            raise ConnectionError("Elasticsearch did not pass health check.")
        return {
            "status": "healthy",
            "service": "elasticsearch",
            "cluster_status": health.get("status"),
            "details": health
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Elasticsearch health check failed: {str(e)}")


@health_router.get("", include_in_schema=True)
@health_router.get("/", include_in_schema=True)
async def health_check_all(response: Response):
    """
    Combined health check for all services.

    - **Localhost only**: Only accessible from 127.0.0.1
    - **No authentication required**
    - **No tenant ID required**

    Returns:
        - 200 OK with status of all services
        - 207 Multi-Status if some services are unhealthy
    """
    results = {
        "redis": {"status": "unknown"},
        "elasticsearch": {"status": "unknown"}
    }

    overall_healthy = True

    # Check Redis
    try:
        pong = _redis_connection_test()
        if pong is True:
            results["redis"] = {"status": "healthy"}
        else:
            results["redis"] = {"status": "unhealthy", "error": "No pong response"}
            overall_healthy = False
    except Exception as e:
        results["redis"] = {"status": "unhealthy", "error": str(e)}
        overall_healthy = False

    # Check Elasticsearch
    try:
        health = await raw_db.health()
        if isinstance(health, dict):
            results["elasticsearch"] = {
                "status": "healthy",
                "cluster_status": health.get("status")
            }
        else:
            results["elasticsearch"] = {"status": "unhealthy", "error": "Invalid health response"}
            overall_healthy = False
    except Exception as e:
        results["elasticsearch"] = {"status": "unhealthy", "error": str(e)}
        overall_healthy = False

    response_data = {
        "overall_status": "healthy" if overall_healthy else "degraded",
        "services": results
    }

    # Return 200 if all healthy, 207 if some are unhealthy
    response.status_code = 200 if overall_healthy else 207

    return response_data