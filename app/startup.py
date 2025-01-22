import logging
from contextlib import asynccontextmanager

from datetime import datetime
import sentry_sdk

from tracardi.service.dependency import *
from tracardi.service.adapter.logger.logger_adapter import log_format_adapter
from tracardi.service.cluster.settings import GlobalSettingsBroadcaster
from tracardi.service.license import License
from tracardi.service.storage.mysql.service.mysql_installation import wait_for_mysql_connection
from tracardi.service.storage.redis.connection import wait_for_redis_connection

from tracardi.config import server, memory_cache
from app import state
from fastapi import FastAPI

from tracardi.config import tracardi
from tracardi.common.logging.log_handler import get_logger

if License.has_license():
    from com_tracardi.config import com_tracardi_settings

logger = get_logger(__name__)

_log_format_adapter = log_format_adapter()


api_ready = False

async def app_starts():
    logging.getLogger("uvicorn.access").handlers[0].setFormatter(_log_format_adapter)

    logger.info(f"Waiting for Mysql...")

    await wait_for_mysql_connection()

    logger.info(f"Waiting for Redis...")

    wait_for_redis_connection()

    logger.info(f"Waiting for Elasticsearch...")

    await bd_install_adapter.wait_for_connection()

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

    print(f"""
 ███████████                                                      █████  ███ 
░░░░░███░░░░                                                     ░░███  ░░░  
    ░███     ████████   ██████    ██████   ██████   ████████   ███████  ████ 
    ░███    ░░███░░███ ░░░░░███  ███░░███ ░░░░░███ ░░███░░███ ███░░███ ░░███ 
    ░███     ░███ ░░░   ███████ ░███ ░░░   ███████  ░███ ░░░ ░███ ░███  ░███ 
    ░███     ░███      ███░░███ ░███  ███ ███░░███  ░███     ░███ ░███  ░███ 
    █████    █████    ░░████████░░██████ ░░████████ █████    ░░████████ █████
   ░░░░░    ░░░░░      ░░░░░░░░  ░░░░░░   ░░░░░░░░ ░░░░░      ░░░░░░░░ ░░░░░ 
""", flush=True)

    if License.has_license():
        license = License.check()

        print(
            f"{str(tracardi.version)} (Tag: {tracardi.image_tag}) (Multi-Tenant: {tracardi.multi_tenant}) (Adapters: {tracardi.cache_adapter},{com_tracardi_settings.queue_adapter})",
            flush=True)
        print(
            f"Commercial Licensed issued for: {license.owner}, expires: {datetime.fromtimestamp(license.expires) if license.expires > 0 else 'Perpetual'} ",
            flush=True)
        print(f"TRACARDI Services {list(license.get_service_ids())}", flush=True)

    else:
        print(f"{str(tracardi.version)} (Tag: {tracardi.image_tag}) (Multi-Tenant: {tracardi.multi_tenant}", flush=True)
        print("License: MIT + “Commons Clause” License Condition v1.0", flush=True)

    if tracardi.enable_global_settings:
        bs = GlobalSettingsBroadcaster()
        bs.start_background_listener()

    logger.info("Starting Cluster Settings Broadcaster...")
    logger.info(f"AUTO_PROFILE_MERGING: {tracardi.is_apm_on()}")
    logger.info(f"LOGGING_FORMAT: {_log_format_adapter}")
    logger.info(f"ENABLE_WORKFLOW: {tracardi.enable_workflow}")
    logger.info(f"ENABLE_EVENT_DESTINATIONS: {tracardi.enable_event_destinations}")
    logger.info(f"ENABLE_PROFILE_DESTINATIONS: {tracardi.enable_profile_destinations}")
    logger.info(f"ENABLE_EVENT_RESHAPING: {tracardi.enable_event_reshaping}")
    logger.info(f"ENABLE_DATA_COMPLIANCE: {tracardi.enable_data_compliance}")
    logger.info(f"ENABLE_EVENT_VALIDATION: {tracardi.enable_event_validation}")
    logger.info(f"ENABLE_EVENT_MAPPING: {tracardi.enable_event_mapping}")
    logger.info(f"ENABLE_EVENT_TO_PROFILE_MAPPING: {tracardi.enable_event_to_profile_mapping}")
    logger.info(f"ENABLE_IDENTIFICATION_POINTS: {tracardi.enable_identification_points}")
    logger.info(f"ENABLE_FIELD_UPDATE_LOG: {tracardi.enable_field_update_log}")
    logger.info(f"ENABLE_ERRORS_ON_RESPONSE: {tracardi.enable_errors_on_response}")
    logger.info(f"ENABLE_EVENT_SOURCE_CHECK: {tracardi.enable_event_source_check}")
    logger.info(f"ENABLE_AUDIENCES: {tracardi.enable_audiences}")
    logger.info(f"MULTI_TENANT_MANAGER_URL:  {tracardi.multi_tenant_manager_url}.")
    logger.info(f"EVENT_MAPPING_CACHE_TTL: {memory_cache.event_mapping_cache_ttl}")
    logger.info(f"EVENT_RESHAPING_CACHE_TTL: {memory_cache.event_reshaping_cache_ttl}")
    logger.info(f"EVENT_VALIDATION_CACHE_TTL: {memory_cache.event_validation_cache_ttl}")
    logger.info(f"EVENT_DESTINATION_CACHE_TTL: {memory_cache.event_destination_cache_ttl}")
    logger.info(f"EVENT_TO_PROFILE_COPING_TTL: {memory_cache.event_to_profile_coping_ttl}")
    logger.info(f"PROFILE_DESTINATION_CACHE_TTL: {memory_cache.profile_destination_cache_ttl}")
    logger.info(f"DATA_COMPLIANCE_CACHE_TTL: {memory_cache.data_compliance_cache_ttl}")
    logger.info(f"IDENTIFICATION_POINTS_CACHE_TTL: {memory_cache.identification_points_cache_ttl}")
    logger.info(f"EVENT_SOURCE_CACHE_TTL: {memory_cache.source_ttl}")

async def app_shutdown():
    await bd_install_adapter.close()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await app_starts()
    state.server_ready = True
    yield
    await app_shutdown()
