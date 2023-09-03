import datetime
import logging
import os
from typing import Optional
from fastapi import APIRouter, HTTPException
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.service.installation import install_system, check_installation
from tracardi.service.tracker import track_event
from app.config import server
from tracardi.config import tracardi
from tracardi.domain.credentials import Credentials
from tracardi.domain.event_source import EventSource
from tracardi.domain.named_entity import NamedEntity
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.fake_data_maker.generate_payload import generate_payload
from tracardi.service.plugin.plugin_install import install_default_plugins
from tracardi.service.setup.data.defaults import open_rest_source_bridge
from tracardi.service.setup.setup_indices import add_ids
from tracardi.service.storage.driver.elastic import raw as raw_db
from tracardi.service.storage.driver.elastic import event_source as event_source_db
from tracardi.service.storage.index import Resource

router = APIRouter()
logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


@router.get("/install", tags=["installation"], include_in_schema=server.expose_gui_api, response_model=dict)
async def check_if_installation_complete():
    """
    Returns list of missing and updated indices
    """
    return await check_installation()


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
            channel="Internal",
            description="Internal event source for random data.",
            bridge=NamedEntity(**open_rest_source_bridge.dict()),
            timestamp=datetime.datetime.utcnow(),
            tags=["internal"],
            groups=["Internal"]
        )

        await raw_db.bulk_upsert(
            Resource().get_index_constant('event-source').get_write_index(),
            list(add_ids([event_source.model_dump()])))

        await event_source_db.refresh()

        for i in range(0, 10):
            payload = generate_payload(source=open_rest_source_bridge.id)

            await track_event(
                TrackerPayload(**payload),
                "0.0.0.0",
                allowed_bridges=['internal'])


@router.post("/install", tags=["installation"], include_in_schema=server.expose_gui_api)
async def install(credentials: Optional[Credentials]):

    try:
        return await install_system(credentials, server.update_plugins_on_start_up)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

