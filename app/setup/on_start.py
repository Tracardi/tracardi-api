import logging
import os

from tracardi.config import tracardi
from tracardi.exceptions.exception import StorageException
from tracardi.domain.api_instance import ApiInstance
from tracardi.exceptions.log_handler import log_handler
from tracardi.service.storage.factory import StorageFor


__local_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)
logger.addHandler(log_handler)


async def update_api_instance():
    api_instance = ApiInstance()

    try:
        result = await StorageFor(api_instance.get_record()).index().save()
        if result.saved == 1:
            logger.info(f"HEARTBEAT. API instance id `{api_instance.get_record().id}` was UPDATED.")
        return result
    except StorageException as e:
        logger.error(f"API instance `{api_instance.get_record().id}` was NOT UPDATED due to ERROR `{str(e)}`")
        raise e
    finally:
        api_instance.reset()
