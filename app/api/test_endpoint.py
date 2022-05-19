import asyncio

from fastapi import APIRouter, Depends
from tracardi.service.storage.redis_client import RedisClient
from tracardi.service.storage.elastic_client import ElasticClient

from app.api.auth.permissions import Permissions
from app.config import server
from app.service.data_generator import generate_fake_data, generate_random_date
from tracardi.domain.event_source import EventSource
from tracardi.service.storage.driver import storage
from fastapi import HTTPException

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin"]))]
)


@router.get("/test/resource", tags=["test"], include_in_schema=server.expose_gui_api)
async def create_test_data():
    """
    Creates test resource data and saves it to database. Accessible for roles: "admin"
    """
    resource = EventSource(
        id="@test-resource",
        type="web-page",
        name="Test resource",
        description="This resource is created for test purposes.",
        tags=['test']
    )
    return await storage.driver.event_source.save(resource)


@router.get("/test/data", tags=["test"], include_in_schema=server.expose_gui_api)
async def make_fake_data():
    """
    Creates fake data and saves it to database. Accessible for roles: "admin"
    """
    for index, data in generate_fake_data().items():
        for record in data:
            record = record.dict()
            if index in ['event', 'session']:
                record['metadata']['time']['insert'] = generate_random_date()
            await storage.driver.raw.index(index).upsert(record)


@router.get("/test/redis", tags=["test"], include_in_schema=server.expose_gui_api)
async def ping_redis():
    """
    Tests connection between Redis instance and Tracardi instance. Accessible for roles: "admin"
    """
    client = RedisClient()
    try:
        pong = client.client.ping()
        if pong is not True:
            raise HTTPException(status_code=500, detail="Redis did not respond.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test/elasticsearch", tags=["test"], include_in_schema=server.expose_gui_api)
async def get_es_cluster_health():
    """
    Tests connection between Elasticsearch and Tracardi by returning cluster info. Accessible for roles: "admin"
    """
    es = ElasticClient.instance()
    try:
        health = await es.cluster.health()
        if not isinstance(health, dict):
            raise HTTPException(status_code=500, detail="Elasticsearch did not pass health check.")
        return health

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
