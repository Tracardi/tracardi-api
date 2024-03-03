import logging
import os
import sys
import traceback
from datetime import datetime
import sentry_sdk

from app.middleware.context import ContextRequestMiddleware
from tracardi.service.elastic.connection import wait_for_connection
from tracardi.service.license import License, SCHEDULER, IDENTIFICATION, COMPLIANCE, RESHAPING, REDIRECTS, VALIDATOR, \
    LICENSE, MULTI_TENANT
from tracardi.service.logging.formater import CustomFormatter
from tracardi.service.storage.mysql.service.mysql_installation import wait_for_mysql_connection
from tracardi.service.storage.redis_client import wait_for_redis_connection

_local_dir = os.path.dirname(__file__)
sys.path.append(f"{_local_dir}/api/proto/stubs")

from starlette.responses import JSONResponse
from time import time
from app.config import server
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from app.api import (
    rule_endpoint,
    resource_endpoint,
    event_endpoint,
    profile_endpoint,
    flow_endpoint,
    generic_endpoint,
    segments_endpoint,
    tql_endpoint,
    health_endpoint,
    session_endpoint,
    plugins_endpoint,
    settings_endpoint,
    event_source_endpoint,
    test_endpoint,
    consent_type_endpoint,
    flow_action_endpoint,
    flows_endpoint,
    info_endpoint,
    user_endpoint,
    debug_endpoint,
    log_endpoint,
    tracardi_pro_endpoint,
    event_type_predefined,
    import_endpoint,
    task_endpoint,
    storage_endpoint,
    destination_endpoint,
    user_account_endpoint,
    install_endpoint,
    delete_indices_endpoint,
    setting_endpoint,
    migration_endpoint,
    report_endpoint,
    live_segments_endpoint,
    console_log_endpoint,
    event_type_mapping,
    bridge_endpoint,
    entity_endpoint,
    customer_endpoint,
    event_to_profile,
    cache_endpoint,
    configuration_endpoint,
    github_endpoint,
    maintanace_endpoint
)
from app.api.track import event_server_endpoint
from tracardi.config import tracardi
from tracardi.exceptions.log_handler import get_logger
from tracardi.service.storage.elastic_client import ElasticClient
from app.api.licensed_endpoint import get_router



# Licensed software
if License.has_service(SCHEDULER):
    from com_tracardi.endpoint import scheduler_endpoint
else:
    scheduler_endpoint = get_router(prefix="/scheduler")

if License.has_service(IDENTIFICATION):
    from com_tracardi.endpoint import identification_point_endpoint
else:
    identification_point_endpoint = get_router(prefix="/identification")

if License.has_service(COMPLIANCE):
    from com_tracardi.endpoint import event_data_compliance_endpoint
else:
    consent_data_compliance_endpoint = get_router(prefix="/consent/compliance")

if License.has_service(RESHAPING):
    from com_tracardi.endpoint import event_reshaping_schema_endpoint
else:
    event_reshaping_schema_endpoint = get_router(prefix="/event-reshape-schema")

if License.has_service(REDIRECTS):
    from com_tracardi.endpoint import event_source_redirects
else:
    event_source_redirects = get_router(prefix="/event-redirect")

if License.has_service(VALIDATOR):
    from com_tracardi.endpoint import event_validator_endpoint
else:
    event_validator_endpoint = get_router(prefix="/event-validator")

if License.has_service(LICENSE):
    from com_tracardi.config import com_tracardi_settings
    from com_tracardi.endpoint import event_to_profile_copy
    from com_tracardi.endpoint import event_props_to_event_traits_copy
    from com_tracardi.endpoint import metric_endpoint
    from com_tracardi.endpoint import field_update_log_endpoint
    from com_tracardi.endpoint import activation_endpoint
    from com_tracardi.endpoint import event_data_compliance_endpoint
    from com_tracardi.endpoint import deploy_endpoint
    from com_tracardi.endpoint import audience_endpoint
    from com_tracardi.endpoint import subscription_endpoint
else:
    event_to_profile_copy = get_router(prefix="/events/copy")
    event_props_to_event_traits_copy = get_router(prefix="/events/index")
    metric_endpoint = get_router(prefix="/metric")
    field_update_log_endpoint = get_router(prefix="/field/update")
    activation_endpoint = get_router(prefix="/activation")
    event_data_compliance_endpoint = get_router(prefix="/consent/compliance")
    deploy_endpoint = get_router(prefix="/deploy")
    audience_endpoint = get_router(prefix="/audience")
    subscription_endpoint = get_router(prefix="/subscription")


if License.has_service(MULTI_TENANT):
    from com_tracardi.endpoint import tenant_install_endpoint

logger = get_logger(__name__)

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
    openapi_tags=tags_metadata if tracardi.expose_gui_api else None,
    docs_url='/docs' if server.api_docs else None,
    redoc_url='/redoc' if server.api_docs else None,
    contact={
        "name": "Risto Kowaczewski",
        "url": "http://github.com/tracardi/tracardi",
        "email": "office@tracardi.com",
    }
)

application.add_middleware(ContextRequestMiddleware)

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

demo = os.path.join(_local_dir, "demo")
if os.path.exists(demo) and os.environ.get("DEMO", None) == 'yes':
    application.mount("/demo",
                      StaticFiles(
                          html=True,
                          directory=os.path.join(_local_dir, "demo")),
                      name="demo")

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

application.include_router(activation_endpoint.router)
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
application.include_router(event_type_mapping.router)
application.include_router(event_source_redirects.router)
application.include_router(bridge_endpoint.router)
application.include_router(entity_endpoint.router)
application.include_router(event_data_compliance_endpoint.router)
application.include_router(identification_point_endpoint.router)
application.include_router(scheduler_endpoint.router)
application.include_router(metric_endpoint.router)
application.include_router(customer_endpoint.router)
application.include_router(event_to_profile.router)
application.include_router(event_to_profile_copy.router)
application.include_router(event_props_to_event_traits_copy.router)
application.include_router(event_type_predefined.router)
application.include_router(setting_endpoint.router)
application.include_router(field_update_log_endpoint.router)
application.include_router(cache_endpoint.router)
application.include_router(deploy_endpoint.router)
application.include_router(audience_endpoint.router)
application.include_router(subscription_endpoint.router)
application.include_router(configuration_endpoint.router)
application.include_router(github_endpoint.router)
application.include_router(maintanace_endpoint.router)

if License.has_service(MULTI_TENANT):
    application.include_router(tenant_install_endpoint.router)

@application.on_event("startup")
async def app_starts():
    logging.getLogger("uvicorn.access").handlers[0].setFormatter(CustomFormatter())

    await wait_for_mysql_connection()
    wait_for_redis_connection()
    await wait_for_connection()

    if server.performance_tracking is not None:
        sentry_sdk.init(
            dsn=server.performance_tracking,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0,
        )

    if License.has_service(LICENSE):
        logger.info(f"TRACARDI async processing:  {com_tracardi_settings.async_processing}.")
        logger.info(f"TRACARDI multi-tenancy:  {tracardi.multi_tenant}.")
        logger.info(f"TRACARDI multi-tenancy API:  {tracardi.multi_tenant_manager_url}.")

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
            f"Commercial Licensed issued for: {license.owner}, expires: {datetime.fromtimestamp(license.expires) if license.expires > 0 else 'Perpetual'} ",
            flush=True)

        print(f"Services {list(license.get_service_ids())}", flush=True)
    else:
        print("License: MIT + “Commons Clause” License Condition v1.0", flush=True)


@application.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:

        start_time = time()

        # Todo Here throttler

        response = await call_next(request)
        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        if 'x-context' in request.headers:
            response.headers["X-Context"] = request.headers.get('x-context')

        return response

    except Exception as e:
        traceback.print_exc()
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:application", host="0.0.0.0", port=8686, log_level='info', workers=1)
