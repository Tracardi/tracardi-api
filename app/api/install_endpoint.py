import datetime
import logging
import os
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.service.tracker import track_event

from app.config import server

from tracardi.config import tracardi, elastic
from tracardi.context import ServerContext, Context, get_context
from tracardi.domain.credentials import Credentials
from tracardi.domain.event_source import EventSource
from tracardi.domain.named_entity import NamedEntity
from tracardi.domain.user import User
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.fake_data_maker.generate_payload import generate_payload
from tracardi.service.plugin.plugin_install import install_default_plugins
from tracardi.service.setup.data.defaults import open_rest_source_bridge
from tracardi.service.setup.setup_indices import create_schema, install_default_data, \
    run_on_start, add_ids
from tracardi.service.storage.driver import storage
from tracardi.service.storage.index import resources

router = APIRouter()
logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


@router.get("/install", tags=["installation"], include_in_schema=server.expose_gui_api, response_model=dict)
async def check_if_installation_complete():
    """
    Returns list of missing and updated indices
    """

    is_schema_ok, indices = await storage.driver.system.is_schema_ok()

    # Missing admin
    existing_aliases = [idx[1] for idx in indices if idx[0] == 'existing_alias']
    index = resources.get_index_constant('user')
    if index.get_index_alias() in existing_aliases:
        admins = await storage.driver.user.search_by_role('admin')
    else:
        admins = None

    has_admin_account = admins is not None and admins.total > 0

    return {
        "schema_ok": is_schema_ok,
        "admin_ok": has_admin_account
    }


@router.get("/install/plugins", tags=["installation"], include_in_schema=server.expose_gui_api, response_model=dict)
async def install_plugins():
    return await install_default_plugins()


@router.get("/install/demo", tags=["installation"], include_in_schema=server.expose_gui_api)
async def install_demo_data():
    # Demo
    if os.environ.get("DEMO", None) == 'yes':

        event_source = EventSource(
            id=open_rest_source_bridge.id,
            type=["internal"],
            name="Test random data",
            channel="System",
            description="Internal event source for random data.",
            bridge=NamedEntity(**open_rest_source_bridge.dict()),
            timestamp=datetime.datetime.utcnow(),
            tags=["internal"],
            groups=["Internal"]
        )

        await storage.driver.raw.bulk_upsert(
            resources.get_index_constant('event-source').get_write_index(),
            list(add_ids([event_source.dict()])))

        await storage.driver.event_source.refresh()

        for i in range(0, 10):
            payload = generate_payload(source=open_rest_source_bridge.id)

            await track_event(
                TrackerPayload(**payload),
                "0.0.0.0",
                allowed_bridges=['internal'])


@router.post("/install", tags=["installation"], include_in_schema=server.expose_gui_api)
async def install(credentials: Optional[Credentials]):
    if tracardi.installation_token and tracardi.installation_token != credentials.token:
        raise HTTPException(status_code=403, detail="Installation forbidden. Invalid installation token.")

    info = await storage.driver.raw.health()

    if 'number_of_data_nodes' in info and int(info['number_of_data_nodes']) == 1:
        os.environ['ELASTIC_INDEX_REPLICAS'] = "0"
        elastic.replicas = "0"
        logger.warning("Elasticsearch replicas decreased to 0 due to only one data node in the cluster.")

    if credentials.needs_admin:
        if credentials.empty() or not credentials.username_as_email():
            raise HTTPException(status_code=403,
                                detail="Installation forbidden. Invalid admin account "
                                       "login or password. Login must be a valid email and password "
                                       "can not be empty.")

    # Install defaults

    async def _install():
        schema_result = await create_schema(resources.get_index_mappings(), credentials.update_mapping)

        await run_on_start()

        await install_default_data()

        return {
            "created": schema_result,
            "admin": False
        }

    # Install staging
    with ServerContext(get_context().switch_context(production=False)):
        staging_install_result = await _install()

        # Add admin
        admins = await storage.driver.user.search_by_role('admin')

        if credentials.needs_admin and admins.total == 0:
            user = User(
                id=str(uuid4()),
                password=credentials.password,
                roles=['admin', 'maintainer'],
                email=credentials.username,
                full_name="Default Admin"
            )

            if not await storage.driver.user.check_if_exists(credentials.username):
                await storage.driver.user.add_user(user)
                logger.info("Default admin account created.")

            staging_install_result['admin'] = True

        else:
            logger.warning("There is at least one admin account. New admin account not created.")
            staging_install_result['admin'] = True

        if staging_install_result['admin'] is True and server.update_plugins_on_start_up is not False:
            logger.info(
                f"Updating plugins on startup due to: UPDATE_PLUGINS_ON_STARTUP={server.update_plugins_on_start_up}")
            staging_install_result['plugins'] = await install_default_plugins()

    # Install production
    with ServerContext(get_context().switch_context(production=True)):
        production_install_result = await _install()

    # Demo
    if os.environ.get("DEMO", None) == 'yes':

        # Demo

        event_source = EventSource(
            id=open_rest_source_bridge.id,
            type=["internal"],
            name="Test random data",
            channel="System",
            description="Internal event source for random data.",
            bridge=NamedEntity(**open_rest_source_bridge.dict()),
            timestamp=datetime.datetime.utcnow(),
            tags=["internal"],
            groups=["Internal"]
        )

        await storage.driver.raw.bulk_upsert(
            resources.get_index_constant('event-source').get_write_index(),
            list(add_ids([event_source.dict()])))

        await storage.driver.event_source.refresh()

        for i in range(0, 150):
            payload = generate_payload(source=open_rest_source_bridge.id)

            print(await track_event(
                TrackerPayload(**payload),
                "0.0.0.0",
                allowed_bridges=['internal']))

    return staging_install_result, production_install_result
