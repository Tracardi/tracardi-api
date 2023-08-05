from fastapi import APIRouter, Depends, HTTPException

from tracardi.config import tracardi
from tracardi.service.storage.index import Resource
from tracardi.service.storage.redis_client import RedisClient
from tracardi.service.storage.elastic_client import ElasticClient

from app.api.auth.permissions import Permissions
from app.config import server
# from app.service.data_generator import generate_fake_data, generate_random_date
# from tracardi.domain.event_source import EventSource
# from tracardi.service.storage.driver.elastic import event_source as event_source_db
from tracardi.service.storage.driver.elastic import raw as raw_db
from datetime import datetime

router = APIRouter(
    dependencies=[Depends(Permissions(roles=["admin", "maintainer", "developer"]))]
)


# # Not in tests
# @router.get("/test/resource", tags=["test"], include_in_schema=server.expose_gui_api)
# async def create_test_data():
#     """
#     Creates test resource data and saves it to database. Accessible for roles: "admin"
#     """
#     resource = EventSource(
#         id="@test-resource",
#         type=["web-page"],
#         name="Test resource",
#         description="This resource is created for test purposes.",
#         tags=['test']
#     )
#     return await event_source_db.save(resource)


# # not in test
# @router.get("/test/data", tags=["test"], include_in_schema=server.expose_gui_api)
# async def make_fake_data():
#     """
#     Creates fake data and saves it to database. Accessible for roles: "admin"
#     """
#     for index, data in generate_fake_data().items():
#         for record in data:
#             record = record.dict()
#             if index in ['event', 'session']:
#                 record['metadata']['time']['insert'] = generate_random_date()
#             await raw_db.index(index).upsert(record)


@router.get("/test/redis", tags=["test"], include_in_schema=server.expose_gui_api)
async def ping_redis():
    """
    Tests connection between Redis instance and Tracardi instance. Accessible for roles: "admin"
    """
    client = RedisClient()
    pong = client.ping()
    if pong is not True:
        raise ConnectionError("Redis did not respond.")


@router.get("/test/elasticsearch", tags=["test"], include_in_schema=server.expose_gui_api)
async def get_es_cluster_health():
    """
    Tests connection between Elasticsearch and Tracardi by returning cluster info. Accessible for roles: "admin"
    """
    health = await raw_db.health()
    if not isinstance(health, dict):
        raise ConnectionError("Elasticsearch did not pass health check.")
    return health


@router.get("/test/elasticsearch/indices", tags=["test"], include_in_schema=server.expose_gui_api)
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
