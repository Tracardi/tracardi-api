import os
import traceback

from app.middleware.context import ContextRequestMiddleware
from app.startup import app_lifespan
from tracardi.service.adapter.logger.logger_adapter import log_format_adapter
from tracardi.service.license import License, SCHEDULER, IDENTIFICATION, COMPLIANCE, RESHAPING, VALIDATOR, \
    LICENSE, MULTI_TENANT

_local_dir = os.path.dirname(__file__)

from starlette.responses import JSONResponse
from time import time
from tracardi.config import server
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from app.api.routes import cache_endpoint, console_log_endpoint, session_endpoint, user_account_endpoint, \
    plugins_endpoint, profile_endpoint, resource_endpoint, test_endpoint, tracardi_pro_endpoint, debug_endpoint, \
    event_type_predefined, event_endpoint, tql_endpoint, user_endpoint, storage_endpoint, task_endpoint, \
    settings_endpoint, entity_endpoint, report_endpoint, import_endpoint
from app.api.routes.consent import customer_endpoint, consent_type_endpoint
from app.api.routes.mapping import event_mapping_endpoint, event_to_profile_endpoint
from app.api.routes.data import generic_endpoint
from app.api.routes.management import health_endpoint, info_endpoint, install_endpoint, maintanace_endpoint, \
    migration_endpoint, delete_indices_endpoint, configuration_endpoint
from app.api.routes.outbound import destination_endpoint
from app.api.routes.inbound import bridge_endpoint, event_source_endpoint, event_source_redirects
from app.api.routes.gui import github_endpoint, feed_endpoint, setting_endpoint
from app.api.routes.workflow import flow_action_endpoint, flow_endpoint, rule_endpoint, flows_endpoint
from app.api.routes.track import event_server_endpoint
from tracardi.config import tracardi
from tracardi.exceptions.log_handler import get_logger
from app.api.routes.licensed_endpoint import get_router

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

if License.has_service(VALIDATOR):
    from com_tracardi.endpoint import event_validator_endpoint
else:
    event_validator_endpoint = get_router(prefix="/event-validator")

if License.has_service(LICENSE):
    from com_tracardi.endpoint import field_update_log_endpoint
    from com_tracardi.endpoint import event_data_compliance_endpoint
    from com_tracardi.endpoint import deploy_endpoint

    if tracardi.enable_audiences:
        from com_tracardi.endpoint import audience_endpoint
        from com_tracardi.endpoint import activation_endpoint

    from com_tracardi.endpoint import subscription_endpoint
    from com_tracardi.endpoint import queue_endpoint
    # from com_tracardi.endpoint import enhancer_endpoint
    from com_tracardi.endpoint import track as com_track
    from com_tracardi.endpoint import upload_endpoint
    from com_tracardi.endpoint import pcp_endpoint
else:
    metric_endpoint = get_router(prefix="/metric")
    field_update_log_endpoint = get_router(prefix="/field/update")

    event_data_compliance_endpoint = get_router(prefix="/consent/compliance")
    deploy_endpoint = get_router(prefix="/deploy")
    if tracardi.enable_audiences:
        audience_endpoint = get_router(prefix="/audience")
        activation_endpoint = get_router(prefix="/activation")

    subscription_endpoint = get_router(prefix="/subscription")
    queue_endpoint = get_router(prefix="/queue")
    # enhancer_endpoint = get_router(prefix="/enhancer")

if License.has_service(MULTI_TENANT):
    from com_tracardi.endpoint import tenant_install_endpoint

logger = get_logger(__name__)

tags_metadata = [
    {
        "name": "profile",
        "description": "Manage profiles. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Profile external docs",
            "url": "http://manual.tracardi.com",
        },
    },
    {
        "name": "resource",
        "description": "Manage data resources. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Resource external docs",
            "url": "http://manual.tracardi.com",
        },
    },
    {
        "name": "rule",
        "description": "Manage flow rule triggers. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Rule external docs",
            "url": "http://manual.tracardi.com",
        },
    },
    {
        "name": "flow",
        "description": "Manage flows. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Flows external docs",
            "url": "http://manual.tracardi.com",
        },
    },
    {
        "name": "event",
        "description": "Manage events. Read more about core concepts of TRACARDI in documentation.",
        "externalDocs": {
            "description": "Events external docs",
            "url": "http://manual.tracardi.com",
        },
    },
    {
        "name": "authorization",
        "description": "OAuth authorization.",
    },
    {
        "name": "tracker",
        "description": "Read more about TRACARDI event server in documentation. http://manual.tracardi.com",
        "externalDocs": {
            "description": "External docs",
            "url": "http://manual.tracardi.com",
        },
    }
]

application = FastAPI(
    lifespan=app_lifespan,
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

md_docs = os.path.join(_local_dir, "../docs/docs")

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
application.include_router(event_reshaping_schema_endpoint.router)
application.include_router(event_validator_endpoint.router)
application.include_router(console_log_endpoint.router)
application.include_router(event_mapping_endpoint.router)
application.include_router(event_source_redirects.router)
application.include_router(bridge_endpoint.router)
application.include_router(entity_endpoint.router)
application.include_router(event_data_compliance_endpoint.router)
application.include_router(identification_point_endpoint.router)
application.include_router(scheduler_endpoint.router)
application.include_router(customer_endpoint.router)
application.include_router(event_to_profile_endpoint.router)
application.include_router(event_type_predefined.router)
application.include_router(setting_endpoint.router)
application.include_router(field_update_log_endpoint.router)
application.include_router(cache_endpoint.router)
application.include_router(deploy_endpoint.router)
application.include_router(subscription_endpoint.router)
application.include_router(configuration_endpoint.router)
application.include_router(github_endpoint.router)
application.include_router(maintanace_endpoint.router)
application.include_router(queue_endpoint.router)
application.include_router(feed_endpoint.router)
# application.include_router(enhancer_endpoint.router)

if tracardi.enable_audiences:
    application.include_router(audience_endpoint.router)
    application.include_router(activation_endpoint.router)

if License.has_service(LICENSE):
    application.include_router(com_track.router)
    application.include_router(upload_endpoint.router)
    application.include_router(pcp_endpoint.router)

if License.has_service(MULTI_TENANT):
    application.include_router(tenant_install_endpoint.router)

_log_format_adapter = log_format_adapter()


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:application", host="0.0.0.0", port=8686, log_level=server.server_logging_level, workers=1)
