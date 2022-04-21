import logging
import os

from tracardi.config import tracardi
from tracardi.exceptions.exception import StorageException
from tracardi.domain.api_instance import ApiInstance
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.storage.elastic_client import ElasticClient
from tracardi.service.storage.factory import StorageFor
from tracardi.service.storage.index import resources
from tracardi.service.storage.driver import storage

__local_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


async def update_api_instance():
    api_instance = ApiInstance()

    try:
        es = ElasticClient.instance()

        if "api-instance" not in resources.resources:
            logger.error(f"API instance index misconfiguration. Index does not exist.")
            return

        index = resources.resources["api-instance"]
        index = index.get_write_index()

        if await es.exists_index(index):
            result = await StorageFor(api_instance.get_record()).index().save()
            if result.saved == 1:
                logger.info(f"HEARTBEAT. API instance id `{api_instance.get_record().id}` was UPDATED.")
            return result
        else:
            logger.warning(f"API instance index does not exist. Instance will be updated next time")

    except StorageException as e:
        logger.error(f"API instance `{api_instance.get_record().id}` was NOT UPDATED due to ERROR `{str(e)}`")
        raise e
    finally:
        api_instance.reset()


async def clear_dead_api_instances():
    try:
        es = ElasticClient.instance()

        if await es.exists_index("tracardi-api-instance"):
            clearing_result = await storage.driver.api_instance.remove_dead_instances()
            logger.info(f"Performed dead API instances removal. Total of {clearing_result['deleted']} dead instances "
                        f"removed.")
        else:
            logger.warning(f"API instance index does not exist. Dead instances will be deleted next time")

    except StorageException as e:
        logger.error(f"Dead API instances could not be removed due to an ERROR `{str(e)}`")
