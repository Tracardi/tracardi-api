import logging
import asyncio
import os
from time import time

import elasticsearch
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Depends
from starlette.staticfiles import StaticFiles
from app.api import token_endpoint, rule_endpoint, resource_endpoint, event_endpoint, \
    profile_endpoint, flow_endpoint, generic_endpoint, project_endpoint, \
    credentials_endpoint, segments_endpoint, \
    tql_endpoint, health_endpoint, session_endpoint, instance_endpoint, plugins_endpoint, \
    settings_endpoint, event_source_endpoint, test_endpoint, \
    purchases_endpoint, event_tag_endpoint, consent_type_endpoint, flow_action_endpoint, flows_endpoint, info_endpoint, \
    user_endpoint, pro_endpoint, event_schema_validation_endpoint, debug_endpoint, log_endpoint
from app.api.auth.authentication import get_current_user
from app.api.graphql.profile import graphql_profiles
from app.api.scheduler import tasks_endpoint
from app.api.track import event_server_endpoint
from app.config import server
from app.setup.on_start import add_plugins, update_api_instance
from tracardi.config import tracardi, elastic
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.storage.driver import storage
from tracardi.service.storage.elastic_client import ElasticClient
from app.setup.indices_setup import create_indices
from tracardi.service.storage.index import resources

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('app.main')
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

_local_dir = os.path.dirname(__file__)

tags_metadata = [
    {
        "name": "profile",
        "description": "Manage profiles. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Profile external docs",
            "url": "http://docs.tracardi.com",
        },
    },
    {
        "name": "resource",
        "description": "Manage data resources. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Resource external docs",
            "url": "http://docs.tracardi.com",
        },
    },
    {
        "name": "rule",
        "description": "Manage flow rule triggers. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Rule external docs",
            "url": "http://docs.tracardi.com",
        },
    },
    {
        "name": "flow",
        "description": "Manage flows. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Flows external docs",
            "url": "http://docs.tracardi.com",
        },
    },
    {
        "name": "event",
        "description": "Manage events. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Events external docs",
            "url": "http://docs.tracardi.com",
        },
    },
    {
        "name": "authorization",
        "description": "OAuth authorization.",
    },
    {
        "name": "tracker",
        "description": "Read more about TRACARDI event server in documentation. http://docs.tracardi.com",
        "externalDocs": {
            "description": "External docs",
            "url": "http://docs.tracardi.com",
        },
    }
]

application = FastAPI(
    title="Tracardi Customer Data Platform Project",
    description="TRACARDI open-source customer data platform offers you excellent control over your customer data with "
                "its broad set of features",
    version=tracardi.version,
    openapi_tags=tags_metadata if server.expose_gui_api else None,
    contact={
        "name": "Risto Kowaczewski",
        "url": "http://github.com/tracardi/tracardi",
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

application.mount("/uix",
                  StaticFiles(
                      html=True,
                      directory=os.path.join(_local_dir, "../uix")),
                  name="uix")

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
application.include_router(event_schema_validation_endpoint.router)
application.include_router(debug_endpoint.router)
application.include_router(log_endpoint.router)


# GraphQL

application.include_router(graphql_profiles,
                           prefix="/graphql/profile",
                           # dependencies=[Depends(get_current_user)],
                           tags=["graphql"])


def is_elastic_on_localhost():
    local_hosts = {'127.0.0.1', 'localhost'}
    if isinstance(elastic.host, list):
        return set(elastic.host).intersection(local_hosts)
    return elastic.host in local_hosts


@application.on_event("startup")
async def app_starts():
    logger.info("TRACARDI set-up starts.")
    no_of_tries = 10
    while True:
        try:

            if no_of_tries < 0:
                break

            if server.reset_plugins is True:
                es = ElasticClient.instance()
                index = resources.resources['action']
                if await es.exists_index(index.get_write_index()):
                    try:
                        await es.remove_index(index.get_read_index())
                    except elasticsearch.exceptions.NotFoundError:
                        pass

            await create_indices()
            await update_api_instance()
            if server.update_plugins_on_start_up is not False:
                await add_plugins()

            break

        except elasticsearch.exceptions.ConnectionError as e:
            await asyncio.sleep(5)
            no_of_tries -= 1
            logger.error(
                f"Could not connect to elasticsearch. Number of tries left: {no_of_tries}. Waiting 5s to retry.")
            if is_elastic_on_localhost():
                logger.warning("You are trying to connect to 127.0.0.1. If this instance is running inside docker "
                               "then you can not use localhost as elasticsearch is probably outside the container. Use "
                               "external IP that docker can connect to.")
            logger.error(f"Error details: {str(e)}")

        except Exception as e:
            await asyncio.sleep(1)
            no_of_tries -= 1
            logger.error(f"Could not save data. Number of tries left: {no_of_tries}. Waiting 1s to retry.")
            logger.error(f"Error details: {str(e)}")

    report_i_am_alive()
    logger.info("TRACARDI set-up finished.")


@application.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    if server.make_slower_responses > 0:
        await asyncio.sleep(server.make_slower_responses)
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    # todo this should run in background
    try:
        if log_handler.has_logs():
            await storage.driver.raw.collection('log', log_handler.collection).save()
            log_handler.reset()
    except Exception as e:
        print(str(e))

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
