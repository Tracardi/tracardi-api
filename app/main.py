import os, sys
from datetime import datetime

from tracardi.service.license import License, SCHEDULER

_local_dir = os.path.dirname(__file__)
sys.path.append(f"{_local_dir}/api/proto/stubs")

import logging
import asyncio
from random import randint
from starlette.responses import JSONResponse
from time import time
from app.config import server
from app.api.auth.permissions import Permissions
from tracardi.service.elastic.connection import wait_for_connection
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Depends
from starlette.staticfiles import StaticFiles
from app.api import rule_endpoint, resource_endpoint, event_endpoint, \
    profile_endpoint, flow_endpoint, generic_endpoint, \
    segments_endpoint, \
    tql_endpoint, health_endpoint, session_endpoint, instance_endpoint, plugins_endpoint, \
    settings_endpoint, event_source_endpoint, test_endpoint, \
    consent_type_endpoint, flow_action_endpoint, flows_endpoint, info_endpoint, \
    user_endpoint, debug_endpoint, log_endpoint, tracardi_pro_endpoint, \
    import_endpoint, \
    task_endpoint, storage_endpoint, destination_endpoint, user_log_endpoint, user_account_endpoint, install_endpoint, \
    delete_indices_endpoint, migration_endpoint, report_endpoint, live_segments_endpoint, event_validator_endpoint, \
    event_reshaping_schema_endpoint, console_log_endpoint, event_type_management, event_source_redirects, last_flow_ws, \
    bridge_endpoint, entity_endpoint, consent_data_compliance_endpoint, identification_point_endpoint
from app.api.graphql.profile import graphql_profiles
from app.api.track import event_server_endpoint
from app.setup.on_start import update_api_instance, clear_dead_api_instances
from tracardi.config import tracardi
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.storage.elastic_client import ElasticClient

# Licensed software
if License.has_service(SCHEDULER):
    from app.api import scheduler_endpoint


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)

print(f"""
88888888888 8888888b.         d8888  .d8888b.         d8888 8888888b.  8888888b. 8888888 
    888     888   Y88b       d88888 d88P  Y88b       d88888 888   Y88b 888   Y88b  888   
    888     888    888      d88P888 888    888      d88P888 888    888 888    888  888   
    888     888   d88P     d88P 888 888            d88P 888 888   d88P 888    888  888   
    888     8888888P"     d88P  888 888           d88P  888 8888888P"  888    888  888   
    888     888 T88b     d88P   888 888    888   d88P   888 888 T88b   888    888  888   
    888     888  T88b   d8888888888 Y88b  d88P  d8888888888 888  T88b  888   d88P  888   
    888     888   T88b d88P     888  "Y8888P"  d88P     888 888   T88b 8888888P" 8888888
    
{str(tracardi.version)}""", flush=True)
if License.has_license():
    license = License.check()

    print(
        f"Commercial Licensed issued for: {license.owner}, expires: {datetime.fromtimestamp(license.expires) if license.expires > 0 else 'Perpetual'} ", flush=True)

    print(f"Services {list(license.get_service_ids())}", flush=True)
else:
    print(f"License: MIT + “Commons Clause” License Condition v1.0", flush=True)

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
    title="Tracardi Customer Data Platform",
    description="The TRACARDI open-source customer data platform provides exceptional control over customer "
                "data through its comprehensive set of features.",
    version=str(tracardi.version),
    openapi_tags=tags_metadata if server.expose_gui_api else None,
    docs_url='/docs' if server.api_docs else None,
    redoc_url='/redoc' if server.api_docs else None,
    contact={
        "name": "Risto Kowaczewski",
        "url": "http://github.com/tracardi/tracardi",
        "email": "office@tracardi.com",
    },

)

application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

application.mount("/tracker",
                  StaticFiles(
                      html=True,
                      directory=os.path.join(_local_dir, "tracker")),
                  name="tracker")

documentation = os.path.join(_local_dir, "../site")

if os.path.exists(documentation):
    application.mount("/documentation",
                      StaticFiles(
                          html=True,
                          directory=documentation),
                      name="documentation")

md_docs = os.path.join(_local_dir, "../docs")

if os.path.exists(md_docs):
    application.mount("/manual/en/docs",
                      StaticFiles(
                          html=True,
                          directory=md_docs),
                      name="manual")

application.mount("/uix",
                  StaticFiles(
                      html=True,
                      directory=os.path.join(_local_dir, "../uix")),
                  name="uix")

application.include_router(event_server_endpoint.router)
application.include_router(tql_endpoint.router)
application.include_router(segments_endpoint.router)
application.include_router(resource_endpoint.router)
application.include_router(rule_endpoint.router)
application.include_router(flow_endpoint.router)
application.include_router(flows_endpoint.router)
application.include_router(flow_action_endpoint.router)
application.include_router(event_endpoint.router)
application.include_router(profile_endpoint.router)
application.include_router(user_endpoint.auth_router)
application.include_router(generic_endpoint.router)
application.include_router(health_endpoint.router)
application.include_router(session_endpoint.router)
application.include_router(instance_endpoint.router)
application.include_router(plugins_endpoint.router)
application.include_router(test_endpoint.router)
application.include_router(settings_endpoint.router)
application.include_router(consent_type_endpoint.router)
application.include_router(info_endpoint.router)
application.include_router(user_endpoint.router)
application.include_router(event_source_endpoint.router)
application.include_router(debug_endpoint.router)
application.include_router(log_endpoint.router)
application.include_router(tracardi_pro_endpoint.router)
application.include_router(storage_endpoint.router)
application.include_router(destination_endpoint.router)
application.include_router(user_log_endpoint.router)
application.include_router(user_account_endpoint.router)
application.include_router(install_endpoint.router)
application.include_router(import_endpoint.router)
application.include_router(task_endpoint.router)
application.include_router(delete_indices_endpoint.router)
application.include_router(migration_endpoint.router)
application.include_router(report_endpoint.router)
application.include_router(live_segments_endpoint.router)
application.include_router(event_reshaping_schema_endpoint.router)
application.include_router(event_validator_endpoint.router)
application.include_router(console_log_endpoint.router)
application.include_router(event_type_management.router)
application.include_router(event_source_redirects.router)
application.include_router(last_flow_ws.router)
application.include_router(bridge_endpoint.router)
application.include_router(entity_endpoint.router)
application.include_router(consent_data_compliance_endpoint.router)
application.include_router(identification_point_endpoint.router)

if License.has_service(SCHEDULER):
    application.include_router(scheduler_endpoint.router)

# GraphQL

application.include_router(graphql_profiles,
                           prefix="/graphql",
                           include_in_schema=server.expose_gui_api,
                           dependencies=[Depends(Permissions(roles=["admin"]))],
                           tags=["graphql"])


@application.on_event("startup")
async def app_starts():
    logger.info(f"TRACARDI version {str(tracardi.version)} set-up starts.")
    await wait_for_connection(no_of_tries=10)
    report_i_am_alive()
    remove_dead_instances()
    logger.info("TRACARDI set-up finished.")
    logger.info(f"TRACARDI version {str(tracardi.version)} ready to operate.")


@application.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:

        start_time = time()
        if server.make_slower_responses > 0:
            await asyncio.sleep(server.make_slower_responses)

        response = await call_next(request)
        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response

    except Exception as e:
        return JSONResponse(
            status_code=500,
            headers={
                "access-control-allow-credentials": "true",
                "access-control-allow-origin": "*"
            },
            content={"detail": str(e)}
        )


@application.on_event("shutdown")
async def app_shutdown():
    elastic = ElasticClient.instance()
    await elastic.close()


def report_i_am_alive():
    try:
        async def heartbeat():
            while True:
                await update_api_instance()
                await asyncio.sleep(server.heartbeat_every)

        asyncio.create_task(heartbeat())
    except Exception:
        logger.error("Report I_AM_ALIVE could not be saved in storage.", exc_info=True)


def remove_dead_instances():
    async def clear_dead_instances():
        while True:
            await clear_dead_api_instances()
            clear_interval = randint(60 * 15, 60 * 60)
            await asyncio.sleep(clear_interval)

    asyncio.create_task(clear_dead_instances())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:application", host="0.0.0.0", port=8686, log_level='info')
