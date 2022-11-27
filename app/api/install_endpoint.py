import logging
import os
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from app.config import server

from tracardi.config import tracardi, elastic
from tracardi.domain.credentials import Credentials
from tracardi.domain.user import User
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.setup.setup_indices import create_indices, update_current_version
from tracardi.service.setup.setup_plugins import add_plugins
from tracardi.service.storage.driver import storage
from tracardi.service.storage.index import resources
from app.setup.on_start import update_api_instance

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
    return await add_plugins()


@router.post("/install", tags=["installation"], include_in_schema=server.expose_gui_api, response_model=dict)
async def install(credentials: Optional[Credentials]):

    if tracardi.installation_token and tracardi.installation_token != credentials.token:
        raise HTTPException(status_code=403, detail="Installation forbidden. Invalid installation hash.")

    if credentials.needs_admin:
        if credentials.empty() or not credentials.username_as_email():
            raise HTTPException(status_code=403, detail="Installation forbidden. Invalid admin account "
                                                        "login or password. Login must be a valid email and password "
                                                        "can not be empty.")

    info = await storage.driver.raw.health()

    if 'number_of_data_nodes' in info and int(info['number_of_data_nodes']) == 1:
        os.environ['ELASTIC_INDEX_REPLICAS'] = "0"
        elastic.replicas = "0"
        logger.warning("Elasticsearch replicas decreased to 0 due to only one data node in the cluster.")

    result = {"created": await create_indices(), 'admin': False}

    # Update install history

    await update_current_version()

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

        result['admin'] = True

    else:
        logger.warning("There is at least one admin account. New admin account not created.")
        result['admin'] = True

    if result['admin'] is True and server.update_plugins_on_start_up is not False:
        logger.info(
            f"Updating plugins on startup due to: UPDATE_PLUGINS_ON_STARTUP={server.update_plugins_on_start_up}")
        result['plugins'] = await add_plugins()

    # add current instance to be visible
    await update_api_instance()

    return result
