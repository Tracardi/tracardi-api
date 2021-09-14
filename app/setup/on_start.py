import asyncio
import hashlib
import importlib
import logging
import os
from datetime import datetime
from uuid import uuid4
from tracardi.exceptions.exception import StorageException
from tracardi.domain.api_instance import ApiInstance
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor
from tracardi_plugin_sdk.domain.register import Plugin

from .module_loader import load_callable, pip_install
from ..utils.network import local_ip

__local_dir = os.path.dirname(__file__)
logger = logging.getLogger('setup.on_start')
logger.setLevel(logging.INFO)


async def add_plugin(module, install=False, upgrade=False):
    try:

        # upgrade
        if install and upgrade:
            pip_install(module.split(".")[0], upgrade=True)

        try:
            # import
            module = importlib.import_module(module)
        except ImportError as e:
            # install
            if install:
                pip_install(module.split(".")[0])
                module = importlib.import_module(module)
            else:
                raise e

        # module = import_and_install(module, upgrade)

        # loads and installs dependencies
        plugin = load_callable(module, 'register')
        plugin_data = plugin()  # type: Plugin

        if len(plugin_data.spec.inputs) > 1:
            raise ValueError(
                "Node can not have more then 1 input port. Found {} that is {}".format(
                    plugin_data.spec.inputs,
                    len(plugin_data.spec.inputs)
                ))

        # Action plugin id is a hash of its module and className

        action_id = plugin_data.spec.module + plugin_data.spec.className
        action_id = hashlib.md5(action_id.encode()).hexdigest()
        await asyncio.sleep(0)
        logger.info(f"Module `{plugin_data.spec.module}` was REGISTERED.")
        return await storage.driver.plugin.save_plugin(action_id, plugin_data)

    except ModuleNotFoundError as e:
        logger.error(f"Module `{module}` was NOT INSTALLED as it raised an error `{str(e)}`.")


async def add_plugins():
    plugins = [
        'tracardi.process_engine.action.v1.debug_payload_action',
        'tracardi.process_engine.action.v1.start_action',
        'tracardi.process_engine.action.v1.end_action',
        'tracardi.process_engine.action.v1.inject_action',

        'tracardi.process_engine.action.v1.increase_views_action',
        'tracardi.process_engine.action.v1.increase_visits_action',
        'tracardi.process_engine.action.v1.increment_action',
        'tracardi.process_engine.action.v1.decrement_action',

        'tracardi.process_engine.action.v1.read_session_action',
        'tracardi.process_engine.action.v1.read_profile_action',
        'tracardi.process_engine.action.v1.read_event_action',

        'tracardi.process_engine.action.v1.if_action',
        'tracardi.process_engine.action.v1.new_visit_action',
        'tracardi.process_engine.action.v1.new_profile_action',

        'tracardi.process_engine.action.v1.detect_client_agent_action',

        'tracardi.process_engine.action.v1.traits.copy_trait_action',
        'tracardi.process_engine.action.v1.traits.append_trait_action',
        'tracardi.process_engine.action.v1.traits.cut_out_trait_action',
        'tracardi.process_engine.action.v1.traits.delete_trait_action',

        'tracardi.process_engine.action.v1.operations.update_profile_action',
        'tracardi.process_engine.action.v1.operations.merge_profiles_action',
        'tracardi.process_engine.action.v1.operations.segment_profile_action',

        # Plugins
        'tracardi_key_counter.plugin',
        'tracardi.process_engine.action.v1.traits.reshape_payload_action',
        'tracardi.process_engine.action.v1.detect_client_agent_action',
        'tracardi_url_parser.plugin',

        # Time
        'tracardi.process_engine.action.v1.time.sleep_action',
        'tracardi.process_engine.action.v1.time.today_action',
        'tracardi_day_night_split.day_night_split_action',
        'tracardi_local_timespan.plugin',

        # Connectors
        'tracardi_rabbitmq_publisher.plugin',

        'tracardi_weather.plugin',
        'tracardi_maxmind_geolite2.plugin',
        'tracardi_remote_call.plugin',
        'tracardi_discord_webhook.plugin',
        'tracardi_zapier_webhook.plugin',

        'tracardi_mongodb_connector.plugin',
        'tracardi_mysql_connector.plugin',
        'tracardi_redshift_connector.plugin',
        'tracardi_postgresql_connector.plugin',

    ]
    for plugin in plugins:
        await add_plugin(plugin, install=False, upgrade=False)


async def register_api_instance():
    api_instance = ApiInstance(id=str(uuid4()), ip=local_ip)
    try:
        result = await StorageFor(api_instance).index().save()
        if result.saved == 1:
            logger.info(f"This API instance was REGISTERED as `{api_instance.id}`")
        return result
    except StorageException as e:
        logger.error(f"API instance `{api_instance.id}` was NOT REGISTERED due to ERROR `{str(e)}`")
        raise e


async def update_api_instance():
    api_instance = ApiInstance(
        id=str(uuid4()),
        ip=local_ip,
        timestamp=datetime.utcnow()
    )
    try:
        result = await StorageFor(api_instance).index().save()
        if result.saved == 1:
            logger.info(f"HEARTBEAT. API instance id `{api_instance.id}` was UPDATED.")
        return result
    except StorageException as e:
        logger.error(f"API instance `{api_instance.id}` was NOT UPDATED due to ERROR `{str(e)}`")
        raise e
