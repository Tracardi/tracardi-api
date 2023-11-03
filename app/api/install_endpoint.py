import logging
import os
from typing import Optional
from fastapi import APIRouter, HTTPException

from app.config import server
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.service.installation import install_system, check_installation
from tracardi.service.tracker import track_event
from tracardi.config import tracardi
from tracardi.domain.credentials import Credentials
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.fake_data_maker.generate_payload import generate_payload
from tracardi.service.plugin.plugin_install import install_default_plugins

router = APIRouter()
logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


@router.get("/install", tags=["installation"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def check_if_installation_complete():
    """
    Returns list of missing and updated indices
    """
    return await check_installation()


@router.get("/install/plugins", tags=["installation"], include_in_schema=tracardi.expose_gui_api, response_model=dict)
async def install_plugins():
    return await install_default_plugins()


@router.get("/install/demo", tags=["installation"], include_in_schema=tracardi.expose_gui_api)
async def install_demo_data():
    # Demo
    if os.environ.get("DEMO", 'no') == 'yes':

        for i in range(0, 10):
            payload = generate_payload(source=tracardi.demo_source)

            await track_event(
                TrackerPayload(**payload),
                "0.0.0.0",
                allowed_bridges=['internal'])


@router.post("/install", tags=["installation"], include_in_schema=tracardi.expose_gui_api)
async def install(credentials: Optional[Credentials]):

    try:
        return await install_system(credentials, server.update_plugins_on_start_up)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

