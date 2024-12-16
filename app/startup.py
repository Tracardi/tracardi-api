import logging
from contextlib import asynccontextmanager

from datetime import datetime
import sentry_sdk

from tracardi.service.adapter.logger.logger_adapter import log_format_adapter
from tracardi.service.cluster.settings import GlobalSettingsBroadcaster
from tracardi.service.elastic.connection import wait_for_connection
from tracardi.service.license import License
from tracardi.service.storage.elastic.interface.client import elastic_close
from tracardi.service.storage.mysql.service.mysql_installation import wait_for_mysql_connection
from tracardi.service.storage.redis.connection import wait_for_redis_connection

from tracardi.config import server
from fastapi import FastAPI

from tracardi.config import tracardi
from tracardi.exceptions.log_handler import get_logger

if License.has_license():
    from com_tracardi.config import com_tracardi_settings

logger = get_logger(__name__)

_log_format_adapter = log_format_adapter()


async def app_starts():
    logging.getLogger("uvicorn.access").handlers[0].setFormatter(_log_format_adapter)

    logger.info(f"Waiting for Mysql...")

    await wait_for_mysql_connection()

    logger.info(f"Waiting for Redis...")

    wait_for_redis_connection()

    logger.info(f"Waiting for Elasticsearch...")

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

    print(f"""
    88888888888 8888888b.         d8888  .d8888b.         d8888 8888888b.  8888888b. 8888888
        888     888   Y88b       d88888 d88P  Y88b       d88888 888   Y88b 888   Y88b  888
        888     888    888      d88P888 888    888      d88P888 888    888 888    888  888
        888     888   d88P     d88P 888 888            d88P 888 888   d88P 888    888  888
        888     8888888P"     d88P  888 888           d88P  888 8888888P"  888    888  888
        888     888 T88b     d88P   888 888    888   d88P   888 888 T88b   888    888  888
        888     888  T88b   d8888888888 Y88b  d88P  d8888888888 888  T88b  888   d88P  888
        888     888   T88b d88P     888  "Y8888P"  d88P     888 888   T88b 8888888P" 8888888
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
        print(f"TRACARDI multi-tenancy API:  {tracardi.multi_tenant_manager_url}.", flush=True)
    else:
        print(f"{str(tracardi.version)} (Tag: {tracardi.image_tag}) (Multi-Tenant: {tracardi.multi_tenant}", flush=True)
        print("License: MIT + “Commons Clause” License Condition v1.0", flush=True)

    if tracardi.enable_global_settings:
        bs = GlobalSettingsBroadcaster()
        bs.start_background_listener()

    logger.info("Starting Cluster Settings Broadcaster...")
    logger.info(f"APM (Auto Profile Merging): {tracardi.is_apm_on()}")
    logger.info(f"LOGGING_FORMAT: {_log_format_adapter}")


async def app_shutdown():
    await elastic_close()


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await app_starts()
    yield
    await app_shutdown()
