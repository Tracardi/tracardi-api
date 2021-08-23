import asyncio
import hashlib
import os

from tracardi_plugin_sdk.domain.register import Plugin

from tracardi.domain.flow_action_plugin import FlowActionPlugin
from tracardi.domain.record.flow_action_plugin_record import FlowActionPluginRecord
from tracardi.process_engine.module_loader import load_callable

__local_dir = os.path.dirname(__file__)


async def add_plugin(module, upgrade=False):
    try:
        # loads and installs dependencies
        plugin = await load_callable(module, 'register', upgrade)
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
        action_plugin = FlowActionPlugin(id=action_id, plugin=plugin_data)
        record = FlowActionPluginRecord.encode(action_plugin)
        return await record.storage().save()

    except ModuleNotFoundError as e:
        print(str(e))
        # todo log.


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

        # 'tracardi.process_engine.action.new_event_action',
        # 'tracardi.process_engine.action.remote_call_action',

        # Plugins
        'tracardi_key_counter.plugin',
        'tracardi.process_engine.action.v1.reshape_payload_action',
        'tracardi.process_engine.action.v1.detect_client_agent_action',
        'tracardi.process_engine.action.v1.sleep_action',
        'tracardi_day_night_split.day_night_split_action',

        # Connectors
        'tracardi_rabbitmq_publisher.plugin',
        'tracardi_weather.plugin',
        'tracardi_mongodb_connector.plugin',
        'tracardi_maxmind_geolite2.plugin',
        'tracardi_remote_call.plugin',
        'tracardi_discord_webhook.plugin',
        'tracardi_zapier_webhook.plugin'

    ]

    for plugin in plugins:
        await add_plugin(plugin, upgrade=True)
