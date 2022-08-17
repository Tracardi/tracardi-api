import logging
import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from app.config import server
from elasticsearch import ElasticsearchException

from tracardi.config import tracardi, elastic
from tracardi.domain.credentials import Credentials
from tracardi.domain.user import User
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.setup.setup_indices import create_indices, update_current_version
from tracardi.service.setup.setup_plugins import add_plugins
from tracardi.service.storage.driver import storage
from tracardi.service.storage.index import resources
from tracardi.service.storage.indices_manager import get_indices_status
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
    # Missing indices

    _indices = [item async for item in get_indices_status()]
    missing_indices = [idx[1] for idx in _indices if idx[0] == 'missing_index']
    existing_indices = [idx[1] for idx in _indices if idx[0] == 'existing_index']
    missing_templates = [idx[1] for idx in _indices if idx[0] == 'missing_template']
    missing_aliases = [idx[1] for idx in _indices if idx[0] == 'missing_alias']
    existing_aliases = [idx[1] for idx in _indices if idx[0] == 'existing_alias']
    # existing_templates = [idx[1] for idx in _indices if idx[0] == 'existing_template']

    # Missing admin

    index = resources.get_index('user')
    if index.get_index_alias() in existing_aliases:
        admins = await storage.driver.user.search_by_role('admin')
        admins = admins.dict()
    else:
        admins = {
            "total": 0,
            "result": []
        }

    is_schema_ok = not missing_indices and not missing_aliases and not missing_aliases
    has_admin_account = admins['total'] > 0

    return {
        "missing": missing_indices,
        "admins": admins,
        "missing_template": missing_templates,
        "missing_alias": missing_aliases,
        "schema_ok": is_schema_ok,
        "admin_ok": has_admin_account
    }


@router.get("/install/plugins", tags=["installation"], include_in_schema=server.expose_gui_api, response_model=dict)
async def install_plugins():
    return await add_plugins()


@router.post("/install", tags=["installation"], include_in_schema=server.expose_gui_api, response_model=dict)
async def install(credentials: Optional[Credentials]):
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

    if admins.total == 0:
        if credentials.not_empty() and credentials.username_as_email():

            user = User(
                id=credentials.username,
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
