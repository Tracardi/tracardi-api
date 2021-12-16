import logging
import os

import asyncio
from time import time

import elasticsearch
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Depends
from starlette.staticfiles import StaticFiles
from app.api import token_endpoint, rule_endpoint, resource_endpoint, event_endpoint, \
    profile_endpoint, flow_endpoint, generic_endpoint, project_endpoint, \
    credentials_endpoint, segments_endpoint, \
    tql_endpoint, health_endpoint, session_endpoint, instance_endpoint, plugins_endpoint, test_endpoint, \
    settings_endpoint, event_source_endpoint, \
    purchases_endpoint, event_tag_endpoint, consent_type_endpoint, flow_action_endpoint, flows_endpoint, info_endpoint,\
    user_endpoint, pro_endpoint
from app.api.auth.authentication import get_current_user
from app.api.graphql.profile import graphql_profiles
from app.api.scheduler import tasks_endpoint
from app.api.track import event_server_endpoint
from app.config import server
from app.setup.on_start import add_plugins, update_api_instance
from tracardi.config import tracardi
from tracardi.service.storage.elastic_client import ElasticClient
from app.setup.indices_setup import create_indices
from tracardi.service.storage.index import resources

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('app.main')
logger.setLevel(tracardi.logging_level)

_local_dir = os.path.dirname(__file__)

tags_metadata = [
    {
        "name": "profile",
        "description": "Manage profiles. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Profile external docs",
            "url": "https://github/atompie/docs/en/docs",
        },
    },
    {
        "name": "resource",
        "description": "Manage data resources. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Resource external docs",
            "url": "https://github/atompie/docs/en/docs",
        },
    },
    {
        "name": "rule",
        "description": "Manage flow rule triggers. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Rule external docs",
            "url": "https://github/atompie/docs/en/docs",
        },
    },
    {
        "name": "flow",
        "description": "Manage flows. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Flows external docs",
            "url": "https://github/atompie/docs/en/docs",
        },
    },
    {
        "name": "event",
        "description": "Manage events. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Events external docs",
            "url": "https://github/atompie/docs/en/docs",
        },
    },
    {
        "name": "authorization",
        "description": "OAuth authorization.",
    },
    {
        "name": "tracker",
        "description": "Read more about TRACARDI event server in documentation. http://localhost:8686/manual/en/site",
        "externalDocs": {
            "description": "External docs",
            "url": "https://github/atompie/docs/en/docs",
        },
    }
]

application = FastAPI(
    title="Tracardi Customer Data Platform Project",
    description="TRACARDI open-source customer data platform offers you excellent control over your customer data with its broad set of features",
    version="0.6.0",
    openapi_tags=tags_metadata if server.expose_gui_api else None,
    contact={
        "name": "Risto Kowaczewski",
        "url": "http://github.com/atompie/tracardi",
        "email": "office@tracardi.com",
    },

)

application.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

application.mount("/tracker",
                  StaticFiles(
                      html=True,
                      directory=os.path.join(_local_dir, "tracker")),
                  name="tracker")

application.mount("/manual",
                  StaticFiles(
                      html=True,
                      directory=os.path.join(_local_dir, "../manual")),
                  name="manual")

application.include_router(event_server_endpoint.router)
application.include_router(tql_endpoint.router)
application.include_router(segments_endpoint.router)
application.include_router(credentials_endpoint.router)
application.include_router(project_endpoint.router)
application.include_router(resource_endpoint.router)
application.include_router(rule_endpoint.router)
application.include_router(flow_endpoint.router)
application.include_router(flows_endpoint.router)
application.include_router(flow_action_endpoint.router)
application.include_router(event_endpoint.router)
application.include_router(profile_endpoint.router)
application.include_router(token_endpoint.router)
application.include_router(generic_endpoint.router)
application.include_router(health_endpoint.router)
application.include_router(session_endpoint.router)
application.include_router(tasks_endpoint.router)
application.include_router(instance_endpoint.router)
application.include_router(plugins_endpoint.router)
application.include_router(test_endpoint.router)
application.include_router(settings_endpoint.router)
application.include_router(purchases_endpoint.router)
application.include_router(event_tag_endpoint.router)
application.include_router(consent_type_endpoint.router)
application.include_router(info_endpoint.router)
application.include_router(user_endpoint.router)
application.include_router(event_source_endpoint.router)
application.include_router(pro_endpoint.router)

# GraphQL

application.include_router(graphql_profiles,
                           prefix="/graphql/profile",
                           # dependencies=[Depends(get_current_user)],
                           tags=["graphql"])


@application.on_event("startup")
async def app_starts():
    while True:
        try:
            if server.reset_plugins is True:
                es = ElasticClient.instance()
                index = resources.resources['action']
                if await es.exists_index(index.get_write_index()):
                    await es.remove_index(index.get_read_index())

            await create_indices()
            await update_api_instance()
            if server.update_plugins_on_start_up is not False:
                await add_plugins()

            break
        except elasticsearch.exceptions.ConnectionError:
            await asyncio.sleep(5)

    report_i_am_alive()
    logger.info("START UP exits.")


@application.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    if server.make_slower_responses > 0:
        await asyncio.sleep(server.make_slower_responses)
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@application.on_event("shutdown")
async def app_shutdown():
    elastic = ElasticClient.instance()
    await elastic.close()


def report_i_am_alive():
    async def heartbeat():
        while True:
            await asyncio.sleep(server.heartbeat_every)
            await update_api_instance()

    asyncio.create_task(heartbeat())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:application", host="0.0.0.0", port=8686, log_level="info")
