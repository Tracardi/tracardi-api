import json
import os
from tracardi.service.storage.elastic import Elastic
from tracardi.service.storage.index import resources, Index
import logging
from app.setup.on_start import add_plugins

__local_dir = os.path.dirname(__file__)

index_mapping = {
    'action': {
        "on-start": add_plugins  # Callable to fill the index
    }
}

logger = logging.getLogger('tracardi.create_indices')


async def create_indices():
    es = Elastic.instance()
    for key, index in resources.resources.items():  # type: str, Index

        if index.mapping:
            map_file = index.mapping
        else:
            map_file = 'mappings/default-dynamic-index.json'

        with open(os.path.join(__local_dir, map_file)) as file:
            map = json.load(file)
            if not await es.exists_index(index.get_write_index()):

                result = await es.create_index(index.get_write_index(), map)
                if 'acknowledged' not in result or result['acknowledged'] is not True:
                    logger.log(level=logging.ERROR,
                               msg="New index `{}` was not created. The following result was returned {}".format(
                                   index.get_write_index(),
                                   result
                               ))
                else:
                    logger.log(level=logging.INFO, msg="New index `{}` created.".format(index.get_write_index()))

                if key in index_mapping and 'on-start' in index_mapping[key]:
                    if index_mapping[key]['on-start'] is not None:
                        on_start = index_mapping[key]['on-start']
                        if callable(on_start):
                            await on_start()


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_indices())
