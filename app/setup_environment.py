import asyncio

from com_tracardi.config import com_tracardi_settings
from com_tracardi.service.pulsar.pulsar_set_up import PulsarSetup
from tracardi.exceptions.log_handler import get_logger
from tracardi.service.elastic.connection import wait_for_connection
from tracardi.service.license import License
from tracardi.service.storage.redis_client import wait_for_redis_connection

logger = get_logger(__name__)


async def run_setup():

    wait_for_redis_connection()

    await wait_for_connection(no_of_tries=10)

    if License.has_license():
        pulsar = PulsarSetup(
            broker_host=com_tracardi_settings.pulsar_host,
            service_host=com_tracardi_settings.pulsar_manager_host,
            token=com_tracardi_settings.pulsar_auth_token
        )

        await pulsar.auto_setup()
        clusters = [cluster async for cluster in pulsar.client.list_clusters()]
        logger.debug(f"Pulsar clusters {clusters}")
        tenants = [tenant async for tenant in pulsar.client.list_tenants()]
        logger.debug(f"Pulsar tenants {tenants}")
        namespaces = [namespace async for namespace in pulsar.client.list_namespaces('tracardi')]
        logger.debug(f"Pulsar namespaces {namespaces}")


asyncio.run(run_setup())
