import asyncio
import logging
import os

from tracardi.config import tracardi
from tracardi.exceptions.exception import StorageException
from tracardi.domain.api_instance import ApiInstance
from tracardi.service.module_loader import pip_install, load_callable, import_package
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor
from tracardi_plugin_sdk.domain.register import Plugin


__local_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)
logger.setLevel(tracardi.logging_level)


async def add_plugin(module, install=False, upgrade=False):
    try:

        # upgrade
        if install and upgrade:
            pip_install(module.split(".")[0], upgrade=True)

        try:
            # import
            module = import_package(module)
        except ImportError as e:
            # install
            if install:
                pip_install(module.split(".")[0])
                module = import_package(module)
            else:
                raise e

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

        await asyncio.sleep(0)
        logger.info(f"Module `{plugin_data.spec.module}` was REGISTERED.")
        return await storage.driver.action.save_plugin(plugin_data)

    except ModuleNotFoundError as e:
        logger.error(f"Module `{module}` was NOT INSTALLED as it raised an error `{str(e)}`.")


async def add_plugins():
    plugins = [
        'tracardi.process_engine.action.v1.debug_payload_action',
        'tracardi.process_engine.action.v1.start_action',
        'tracardi.process_engine.action.v1.end_action',
        'tracardi.process_engine.action.v1.raise_error_action',
        'tracardi.process_engine.action.v1.inject_action',

        'tracardi.process_engine.action.v1.increase_views_action',
        'tracardi.process_engine.action.v1.increase_visits_action',
        'tracardi.process_engine.action.v1.increment_action',
        'tracardi.process_engine.action.v1.decrement_action',

        'tracardi.process_engine.action.v1.if_action',
        'tracardi.process_engine.action.v1.new_visit_action',
        'tracardi.process_engine.action.v1.new_profile_action',
        'tracardi.process_engine.action.v1.template_action',

        'tracardi.process_engine.action.v1.detect_client_agent_action',

        'tracardi.process_engine.action.v1.traits.copy_trait_action',
        'tracardi.process_engine.action.v1.traits.append_trait_action',
        'tracardi.process_engine.action.v1.traits.cut_out_trait_action',
        'tracardi.process_engine.action.v1.traits.delete_trait_action',

        'tracardi.process_engine.action.v1.operations.update_profile_action',
        'tracardi.process_engine.action.v1.operations.merge_profiles_action',
        'tracardi.process_engine.action.v1.operations.segment_profile_action',
        'tracardi.process_engine.action.v1.operations.update_event_action',

        'tracardi.process_engine.action.v1.microservice.profile_metrics',

        # Plugins
        'tracardi_key_counter.plugin',
        'tracardi.process_engine.action.v1.traits.reshape_payload_action',
        'tracardi.process_engine.action.v1.detect_client_agent_action',
        'tracardi_url_parser.plugin',
        'tracardi_string_splitter.plugin',
        'tracardi.process_engine.action.v1.events.event_counter.plugin',

        'tracardi.process_engine.action.v1.strings.string_operations.plugin',
        'tracardi.process_engine.action.v1.strings.regex_match.plugin',
        'tracardi.process_engine.action.v1.strings.regex_validator.plugin',

        # Time
        'tracardi.process_engine.action.v1.time.sleep_action',
        'tracardi.process_engine.action.v1.time.today_action',
        'tracardi_day_night_split.plugin',
        'tracardi.process_engine.action.v1.time.local_time_span.plugin',

        # Connectors
        'tracardi_rabbitmq_publisher.plugin',

        'tracardi_weather.plugin',
        'tracardi_maxmind_geolite2.plugin',
        'tracardi_remote_call.plugin',
        'tracardi_discord_webhook.plugin',
        'tracardi_zapier_webhook.plugin',

        'tracardi_mongodb_connector.plugin',
        'tracardi_mysql_connector.plugin',
        'tracardi_postgresql_connector.plugin',
        'tracardi_string_validator.plugin',

        'tracardi_fullcontact_webhook.plugin',
        'tracardi_sentiment_analysis.plugin',
        'tracardi_text_classification.plugin',
        'tracardi_smtp_connector.plugin',
        'tracardi_event_scheduler.plugin',
        'tracardi_pushover_webhook.plugin',
        'tracardi_language_detection.plugin',
        'tracardi.process_engine.action.v1.segments.profile_segmentation.plugin',
        'tracardi_aws_sqs.plugin',
        'tracardi_resource.plugin',
        'tracardi_json_from_objects.plugin'

    ]
    for plugin in plugins:
        await add_plugin(plugin, install=False, upgrade=False)


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
