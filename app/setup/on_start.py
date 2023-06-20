import logging
import os

from tracardi.config import tracardi
from tracardi.exceptions.exception import StorageException
from tracardi.domain.api_instance import ApiInstance
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.storage.driver.elastic import api_instance as api_instance_db

__local_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


async def update_api_instance():
    api_instance = ApiInstance()
    instance = api_instance.get_record()

    try:
        if await api_instance_db.exists():

            result = await api_instance_db.save(instance)
            if result.saved == 1:
                logger.info(f"HEARTBEAT. API instance id `{instance.id}` was UPDATED.")
            return result
        else:
            logger.warning(f"System not installed. Visit GUI to install the system. "
                           f"API instance index does not exist. Instance will be updated next time.")

    except StorageException as e:
        logger.error(f"API instance `{instance.id}` was NOT UPDATED due to ERROR `{str(e)}`")
        raise e
    finally:
        api_instance.reset()


async def clear_dead_api_instances():
    try:
        if not await api_instance_db.exists():
            logger.warning(f"API instance index does not exist. Instance will be cleared next time")
            return

        await api_instance_db.refresh()
        clearing_result = await api_instance_db.remove_dead_instances()

        logger.info(f"Performed dead API instances removal. Total of {clearing_result['deleted']} dead instances "
                    f"removed.")

    except StorageException as e:
        logger.error(f"Dead API instances could not be removed due to an ERROR `{str(e)}`")
