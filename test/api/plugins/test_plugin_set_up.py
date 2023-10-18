
from test.api.plugins.test_all_endpoints import _load_plugin_registry_metadata
from tracardi.service.module_loader import load_callable, import_package
from tracardi.domain.resource import Resource, ResourceCredentials
from tracardi.service.module_loader import load_callable, import_package
from tracardi.service.wf.domain.node import Node


async def test_should_set_up_plugin_tag_event_action():
    
    module = import_package("tracardi.process_engine.action.v1.internal.tag_event.plugin")
    plugin_class = load_callable(module, "TagEventAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.internal.tag_event.plugin", 
                       className="TagEventAction")
    await plugin.set_up({'tags': 'tag1,tag2'})


async def test_should_set_up_plugin_last_visit_action():
    
    module = import_package("tracardi.process_engine.action.v1.time.last_profile_visit.plugin")
    plugin_class = load_callable(module, "LastVisitAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.time.last_profile_visit.plugin", 
                       className="LastVisitAction")
    await plugin.set_up(None)


async def test_should_set_up_plugin_telegram_post_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'bot_token': 'bot_token', 'chat_id': 100},
                test={'bot_token': 'bot_token', 'chat_id': 100}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.telegram.post.plugin")
    plugin_class = load_callable(module, "TelegramPostAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.telegram.post.plugin", 
                       className="TelegramPostAction")
    await plugin.set_up({'resource': {'id': 'id', 'name': 'name'}, 'message': 'test'})


async def test_should_set_up_plugin_google_analytics_event_tracker_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'google_analytics_id': 'google_analytics_id'},
                test={'google_analytics_id': 'google_analytics_id'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.google.analytics.plugin")
    plugin_class = load_callable(module, "GoogleAnalyticsEventTrackerAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.google.analytics.plugin", 
                       className="GoogleAnalyticsEventTrackerAction")
    await plugin.set_up({'source': {'id': 'id', 'name': 'name'}, 'category': 'category', 'action': 'action', 'label': 'label', 'value': 'value'})


async def test_should_set_up_plugin_google_analytics_v4_event_tracker_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': 'api_key', 'measurement_id': 'measurement_id'},
                test={'api_key': 'api_key', 'measurement_id': 'measurement_id'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.google.analytics_v4.plugin")
    plugin_class = load_callable(module, "GoogleAnalyticsV4EventTrackerAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.google.analytics_v4.plugin", 
                       className="GoogleAnalyticsV4EventTrackerAction")
    await plugin.set_up({'source': {'id': 'id', 'name': 'name'}, 'name': 'event_name', 'params': 'payload@id'})


async def test_should_set_up_plugin_whois_action():
    
    module = import_package("tracardi.process_engine.action.v1.connectors.whois.plugin")
    plugin_class = load_callable(module, "WhoisAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.whois.plugin", 
                       className="WhoisAction")
    await plugin.set_up({'domain': 'some.com'})


async def test_should_set_up_plugin_contains_pattern_action():
    
    module = import_package("tracardi.process_engine.action.v1.operations.contains_pattern.plugin")
    plugin_class = load_callable(module, "ContainsPatternAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.operations.contains_pattern.plugin", 
                       className="ContainsPatternAction")
    await plugin.set_up({'field': 'payload@field', 'pattern': 'all'})


async def test_should_set_up_plugin_payload_memory_collector():
    
    module = import_package("tracardi.process_engine.action.v1.memory.collect.plugin")
    plugin_class = load_callable(module, "PayloadMemoryCollector")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.memory.collect.plugin", 
                       className="PayloadMemoryCollector")
    await plugin.set_up({'name': 'Test name', 'type': 'list'})


async def test_should_set_up_plugin_password_generator_action():
    
    module = import_package("tracardi.process_engine.action.v1.password_generator_action")
    plugin_class = load_callable(module, "PasswordGeneratorAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.password_generator_action", 
                       className="PasswordGeneratorAction")
    await plugin.set_up({'lowercase': 4, 'max_length': 13, 'min_length': 8, 'special_characters': 2, 'uppercase': 2})


async def test_should_set_up_plugin_week_days_checker():
    
    module = import_package("tracardi.process_engine.action.v1.weekdays_checker_action")
    plugin_class = load_callable(module, "WeekDaysChecker")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.weekdays_checker_action", 
                       className="WeekDaysChecker")
    await plugin.set_up({})


async def test_should_set_up_plugin_start_action():
    
    module = import_package("tracardi.process_engine.action.v1.flow.start.start_action")
    plugin_class = load_callable(module, "StartAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.flow.start.start_action", 
                       className="StartAction")
    await plugin.set_up({'debug': False, 'event_id': None, 'event_type': {'id': '', 'name': ''}, 'event_types': [], 'profile_less': False, 'properties': '{}', 'session_less': False})


async def test_should_set_up_plugin_start_segmentation_action():
    
    module = import_package("tracardi.process_engine.action.v1.flow.start_segmentation.plugin")
    plugin_class = load_callable(module, "StartSegmentationAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.flow.start_segmentation.plugin", 
                       className="StartSegmentationAction")
    await plugin.set_up({'profile_id': 'id'})


async def test_should_set_up_plugin_property_exists_action():
    
    module = import_package("tracardi.process_engine.action.v1.flow.property_exists.plugin")
    plugin_class = load_callable(module, "PropertyExistsAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.flow.property_exists.plugin", 
                       className="PropertyExistsAction")
    await plugin.set_up({'property': 'event@context.page.url'})


async def test_should_set_up_plugin_end_action():
    
    module = import_package("tracardi.process_engine.action.v1.end_action")
    plugin_class = load_callable(module, "EndAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.end_action", 
                       className="EndAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_raise_error_action():
    
    module = import_package("tracardi.process_engine.action.v1.raise_error_action")
    plugin_class = load_callable(module, "RaiseErrorAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.raise_error_action", 
                       className="RaiseErrorAction")
    await plugin.set_up({'message': 'Flow stopped due to error.'})


async def test_should_set_up_plugin_inject_action():
    
    module = import_package("tracardi.process_engine.action.v1.inject_action")
    plugin_class = load_callable(module, "InjectAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.inject_action", 
                       className="InjectAction")
    await plugin.set_up({'destination': 'payload', 'value': '{}'})


async def test_should_set_up_plugin_increase_views_action():
    
    module = import_package("tracardi.process_engine.action.v1.increase_views_action")
    plugin_class = load_callable(module, "IncreaseViewsAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.increase_views_action", 
                       className="IncreaseViewsAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_increase_visits_action():
    
    module = import_package("tracardi.process_engine.action.v1.increase_visits_action")
    plugin_class = load_callable(module, "IncreaseVisitsAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.increase_visits_action", 
                       className="IncreaseVisitsAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_increment_action():
    
    module = import_package("tracardi.process_engine.action.v1.increment_action")
    plugin_class = load_callable(module, "IncrementAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.increment_action", 
                       className="IncrementAction")
    await plugin.set_up({'field': 'profile@stats.counters.test', 'increment': 1})


async def test_should_set_up_plugin_decrement_action():
    
    module = import_package("tracardi.process_engine.action.v1.decrement_action")
    plugin_class = load_callable(module, "DecrementAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.decrement_action", 
                       className="DecrementAction")
    await plugin.set_up({'decrement': 1, 'field': 'profile@stats.counters.test'})


async def test_should_set_up_plugin_if_action():
    
    module = import_package("tracardi.process_engine.action.v1.if_action")
    plugin_class = load_callable(module, "IfAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.if_action", 
                       className="IfAction")
    await plugin.set_up({'condition': 'event@id=="1"'})


async def test_should_set_up_plugin_starts_with_action():
    
    module = import_package("tracardi.process_engine.action.v1.starts_with_action")
    plugin_class = load_callable(module, "StartsWithAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.starts_with_action", 
                       className="StartsWithAction")
    await plugin.set_up({'field': 'event@id', 'prefix': 'test'})


async def test_should_set_up_plugin_ends_with_action():
    
    module = import_package("tracardi.process_engine.action.v1.ends_with_action")
    plugin_class = load_callable(module, "EndsWithAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.ends_with_action", 
                       className="EndsWithAction")
    await plugin.set_up({'field': 'event@id', 'prefix': 'test'})


async def test_should_set_up_plugin_new_visit_action():
    
    module = import_package("tracardi.process_engine.action.v1.new_visit_action")
    plugin_class = load_callable(module, "NewVisitAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.new_visit_action", 
                       className="NewVisitAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_new_profile_action():
    
    module = import_package("tracardi.process_engine.action.v1.new_profile_action")
    plugin_class = load_callable(module, "NewProfileAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.new_profile_action", 
                       className="NewProfileAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_template_action():
    
    module = import_package("tracardi.process_engine.action.v1.template_action")
    plugin_class = load_callable(module, "TemplateAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.template_action", 
                       className="TemplateAction")
    await plugin.set_up({'template': ''})


async def test_should_set_up_plugin_sorted_dict_action():
    
    module = import_package("tracardi.process_engine.action.v1.sort_dictionary")
    plugin_class = load_callable(module, "SortedDictAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.sort_dictionary", 
                       className="SortedDictAction")
    await plugin.set_up({'direction': 'asc', 'data': 'data', 'sort_by': 'key'})


async def test_should_set_up_plugin_get_uuid4_action():
    
    module = import_package("tracardi.process_engine.action.v1.misc.uuid4.plugin")
    plugin_class = load_callable(module, "GetUuid4Action")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.misc.uuid4.plugin", 
                       className="GetUuid4Action")
    await plugin.set_up({})


async def test_should_set_up_plugin_copy_trait_action():
    
    module = import_package("tracardi.process_engine.action.v1.traits.copy_trait_action")
    plugin_class = load_callable(module, "CopyTraitAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.traits.copy_trait_action", 
                       className="CopyTraitAction")
    await plugin.set_up({'traits': {'set': {}}})


async def test_should_set_up_plugin_append_trait_action():
    
    module = import_package("tracardi.process_engine.action.v1.traits.append_trait_action")
    plugin_class = load_callable(module, "AppendTraitAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.traits.append_trait_action", 
                       className="AppendTraitAction")
    await plugin.set_up({'append': {'target1': 'source1', 'target2': 'source2'}, 'remove': {'target': ['item1', 'item2']}})


async def test_should_set_up_plugin_cut_out_trait_action():
    
    module = import_package("tracardi.process_engine.action.v1.traits.cut_out_trait_action")
    plugin_class = load_callable(module, "CutOutTraitAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.traits.cut_out_trait_action", 
                       className="CutOutTraitAction")
    await plugin.set_up({'trait': 'event@...'})


async def test_should_set_up_plugin_delete_trait_action():
    
    module = import_package("tracardi.process_engine.action.v1.traits.delete_trait_action")
    plugin_class = load_callable(module, "DeleteTraitAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.traits.delete_trait_action", 
                       className="DeleteTraitAction")
    await plugin.set_up({'delete': ['event@id']})


async def test_should_set_up_plugin_auto_merge_properties_to_profile_action():
    
    module = import_package("tracardi.process_engine.action.v1.traits.auto_merge_properties_to_profile_action")
    plugin_class = load_callable(module, "AutoMergePropertiesToProfileAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.traits.auto_merge_properties_to_profile_action", 
                       className="AutoMergePropertiesToProfileAction")
    await plugin.set_up({'sub_traits': '', 'traits_type': 'public'})


async def test_should_set_up_plugin_assign_condition_result_plugin():
    
    module = import_package("tracardi.process_engine.action.v1.traits.assign_condition_result.plugin")
    plugin_class = load_callable(module, "AssignConditionResultPlugin")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.traits.assign_condition_result.plugin", 
                       className="AssignConditionResultPlugin")
    await plugin.set_up({'conditions': {}})


async def test_should_set_up_plugin_condition_set_plugin():
    
    module = import_package("tracardi.process_engine.action.v1.traits.condition_set.plugin")
    plugin_class = load_callable(module, "ConditionSetPlugin")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.traits.condition_set.plugin", 
                       className="ConditionSetPlugin")
    await plugin.set_up({'conditions': {}})


async def test_should_set_up_plugin_hash_traits_action():
    
    module = import_package("tracardi.process_engine.action.v1.traits.hash_traits_action")
    plugin_class = load_callable(module, "HashTraitsAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.traits.hash_traits_action", 
                       className="HashTraitsAction")
    await plugin.set_up({'func': 'md5', 'traits': []})


async def test_should_set_up_plugin_mask_traits_action():
    
    module = import_package("tracardi.process_engine.action.v1.traits.mask_traits_action")
    plugin_class = load_callable(module, "MaskTraitsAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.traits.mask_traits_action", 
                       className="MaskTraitsAction")
    await plugin.set_up({'traits': []})


async def test_should_set_up_plugin_join_payloads():
    
    module = import_package("tracardi.process_engine.action.v1.operations.join_payloads.plugin")
    plugin_class = load_callable(module, "JoinPayloads")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.operations.join_payloads.plugin", 
                       className="JoinPayloads")
    await plugin.set_up({'default': True, 'reshape': '{}', 'type': 'dict'})


async def test_should_set_up_plugin_merge_profiles_action():
    
    module = import_package("tracardi.process_engine.action.v1.operations.merge_profiles_action")
    plugin_class = load_callable(module, "MergeProfilesAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.operations.merge_profiles_action", 
                       className="MergeProfilesAction")
    await plugin.set_up({'mergeBy': ['profile@data.contact.email']})


async def test_should_set_up_plugin_update_profile_action():
    
    module = import_package("tracardi.process_engine.action.v1.operations.update_profile_action")
    plugin_class = load_callable(module, "UpdateProfileAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.operations.update_profile_action", 
                       className="UpdateProfileAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_discard_profile_update_action():
    
    module = import_package("tracardi.process_engine.action.v1.operations.discard_profile_update_action")
    plugin_class = load_callable(module, "DiscardProfileUpdateAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.operations.discard_profile_update_action", 
                       className="DiscardProfileUpdateAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_update_session_action():
    
    module = import_package("tracardi.process_engine.action.v1.operations.update_session_action")
    plugin_class = load_callable(module, "UpdateSessionAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.operations.update_session_action", 
                       className="UpdateSessionAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_array_reducer():
    
    module = import_package("tracardi.process_engine.action.v1.operations.reduce_array.plugin")
    plugin_class = load_callable(module, "ArrayReducer")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.operations.reduce_array.plugin", 
                       className="ArrayReducer")
    await plugin.set_up({'array': 'payload@test'})


async def test_should_set_up_plugin_calculator_action():
    
    module = import_package("tracardi.process_engine.action.v1.calculator_action")
    plugin_class = load_callable(module, "CalculatorAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.calculator_action", 
                       className="CalculatorAction")
    await plugin.set_up({'calc_dsl': 'a = profile@id + 1'})


async def test_should_set_up_plugin_mapping_action():
    
    module = import_package("tracardi.process_engine.action.v1.mapping_action")
    plugin_class = load_callable(module, "MappingAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.mapping_action", 
                       className="MappingAction")
    await plugin.set_up({'case_sensitive': False, 'mapping': {'a': 'profile@id'}, 'value': 'x'})


async def test_should_set_up_plugin_random_item_action():
    
    module = import_package("tracardi.process_engine.action.v1.return_random_element_action")
    plugin_class = load_callable(module, "RandomItemAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.return_random_element_action", 
                       className="RandomItemAction")
    await plugin.set_up({'list_of_items': [1, 2, 3, 4, 5]})


async def test_should_set_up_plugin_log_action():
    
    module = import_package("tracardi.process_engine.action.v1.log_action")
    plugin_class = load_callable(module, "LogAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.log_action", 
                       className="LogAction")
    await plugin.set_up({'message': '<log-message>', 'type': 'warning'})


async def test_should_set_up_plugin_html_xpath_scrapper_action():
    
    module = import_package("tracardi.process_engine.action.v1.scrapper.xpath.plugin")
    plugin_class = load_callable(module, "HtmlXpathScrapperAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.scrapper.xpath.plugin", 
                       className="HtmlXpathScrapperAction")
    await plugin.set_up({'content': '', 'xpath': ''})


async def test_should_set_up_plugin_value_threshold_action():
    
    module = import_package("tracardi.process_engine.action.v1.operations.threshold.plugin")
    plugin_class = load_callable(module, "ValueThresholdAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.operations.threshold.plugin", 
                       className="ValueThresholdAction")
    await plugin.set_up({'assign_to_profile': True, 'name': 'test', 'ttl': 1800, 'value': '1'})


async def test_should_set_up_plugin_circular_geo_fence_action():
    
    module = import_package("tracardi.process_engine.action.v1.geo.fence.circular.plugin")
    plugin_class = load_callable(module, "CircularGeoFenceAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.geo.fence.circular.plugin", 
                       className="CircularGeoFenceAction")
    await plugin.set_up({'center_coordinate': {'lat': 0, 'lng': 0}, 'test_coordinate': {'lat': 0, 'lng': 0}, 'radius': 10})


async def test_should_set_up_plugin_geo_distance_action():
    
    module = import_package("tracardi.process_engine.action.v1.geo.distance.plugin")
    plugin_class = load_callable(module, "GeoDistanceAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.geo.distance.plugin", 
                       className="GeoDistanceAction")
    await plugin.set_up({'start_coordinate': {'lat': 0, 'lng': 0}, 'end_coordinate': {'lat': 0, 'lng': 0}})


async def test_should_set_up_plugin_reshape_payload_action():
    
    module = import_package("tracardi.process_engine.action.v1.traits.reshape_payload_action")
    plugin_class = load_callable(module, "ReshapePayloadAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.traits.reshape_payload_action", 
                       className="ReshapePayloadAction")
    await plugin.set_up({'default': True, 'value': '{}'})


async def test_should_set_up_plugin_detect_client_agent_action():
    
    module = import_package("tracardi.process_engine.action.v1.detect_client_agent_action")
    plugin_class = load_callable(module, "DetectClientAgentAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.detect_client_agent_action", 
                       className="DetectClientAgentAction")
    await plugin.set_up({'agent': 'session@context.browser.browser.userAgent'})


async def test_should_set_up_plugin_field_type_action():
    
    module = import_package("tracardi.process_engine.action.v1.traits.field_type_action")
    plugin_class = load_callable(module, "FieldTypeAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.traits.field_type_action", 
                       className="FieldTypeAction")
    await plugin.set_up({'field': 'profile@id'})


async def test_should_set_up_plugin_string_properties_actions():
    
    module = import_package("tracardi.process_engine.action.v1.strings.string_operations.plugin")
    plugin_class = load_callable(module, "StringPropertiesActions")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.strings.string_operations.plugin", 
                       className="StringPropertiesActions")
    await plugin.set_up({'string': 'test'})


async def test_should_set_up_plugin_regex_match_action():
    
    module = import_package("tracardi.process_engine.action.v1.strings.regex_match.plugin")
    plugin_class = load_callable(module, "RegexMatchAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.strings.regex_match.plugin", 
                       className="RegexMatchAction")
    await plugin.set_up({'group_prefix': 'Group', 'pattern': '<pattern>', 'text': '<text or path to text>'})


async def test_should_set_up_plugin_regex_validator_action():
    
    module = import_package("tracardi.process_engine.action.v1.strings.regex_validator.plugin")
    plugin_class = load_callable(module, "RegexValidatorAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.strings.regex_validator.plugin", 
                       className="RegexValidatorAction")
    await plugin.set_up({'data': 'a', 'validation_regex': '/a/'})


async def test_should_set_up_plugin_string_validator_action():
    
    module = import_package("tracardi.process_engine.action.v1.strings.string_validator.plugin")
    plugin_class = load_callable(module, "StringValidatorAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.strings.string_validator.plugin", 
                       className="StringValidatorAction")
    await plugin.set_up({'data': 'test', 'validator': 'test'})


async def test_should_set_up_plugin_splitter_action():
    
    module = import_package("tracardi.process_engine.action.v1.strings.string_splitter.plugin")
    plugin_class = load_callable(module, "SplitterAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.strings.string_splitter.plugin", 
                       className="SplitterAction")
    await plugin.set_up({'delimiter': '.', 'string': 'test.test'})


async def test_should_set_up_plugin_join_action():
    
    module = import_package("tracardi.process_engine.action.v1.strings.string_join.plugin")
    plugin_class = load_callable(module, "JoinAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.strings.string_join.plugin", 
                       className="JoinAction")
    await plugin.set_up({'delimiter': ',', 'string': 'payload@test'})


async def test_should_set_up_plugin_parse_u_r_l_parameters():
    
    module = import_package("tracardi.process_engine.action.v1.strings.url_parser.plugin")
    plugin_class = load_callable(module, "ParseURLParameters")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.strings.url_parser.plugin", 
                       className="ParseURLParameters")
    await plugin.set_up({'url': 'session@context.page.url'})


async def test_should_set_up_plugin_regex_replacer():
    
    module = import_package("tracardi.process_engine.action.v1.strings.regex_replace.plugin")
    plugin_class = load_callable(module, "RegexReplacer")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.strings.regex_replace.plugin", 
                       className="RegexReplacer")
    await plugin.set_up({'find_regex': 'abc', 'replace_with': '123', 'string': 'abc'})


async def test_should_set_up_plugin_search_string_similarity_action():
    
    module = import_package("tracardi.process_engine.action.v1.strings.string_similarity.plugin")
    plugin_class = load_callable(module, "SearchStringSimilarityAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.strings.string_similarity.plugin", 
                       className="SearchStringSimilarityAction")
    await plugin.set_up({'first_string': 'abc', 'second_string': 'abc', 'algorithm': 'levenshtein'})


async def test_should_set_up_plugin_sleep_action():
    
    module = import_package("tracardi.process_engine.action.v1.time.sleep_action")
    plugin_class = load_callable(module, "SleepAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.time.sleep_action", 
                       className="SleepAction")
    await plugin.set_up({'wait': 1})


async def test_should_set_up_plugin_today_action():
    
    module = import_package("tracardi.process_engine.action.v1.time.today_action")
    plugin_class = load_callable(module, "TodayAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.time.today_action", 
                       className="TodayAction")
    await plugin.set_up({'timezone': 'session@context.time.tz'})


async def test_should_set_up_plugin_day_night_action():
    
    module = import_package("tracardi.process_engine.action.v1.time.day_night.plugin")
    plugin_class = load_callable(module, "DayNightAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.time.day_night.plugin", 
                       className="DayNightAction")
    await plugin.set_up({'latitude': 1.2, 'longitude': 2.1})


async def test_should_set_up_plugin_local_time_span_action():
    
    module = import_package("tracardi.process_engine.action.v1.time.local_time_span.plugin")
    plugin_class = load_callable(module, "LocalTimeSpanAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.time.local_time_span.plugin", 
                       className="LocalTimeSpanAction")
    await plugin.set_up({'end': '10:10:10', 'start': '12:10:10', 'timezone': 'session@context.time.tz'})


async def test_should_set_up_plugin_profile_live_time_action():
    
    module = import_package("tracardi.process_engine.action.v1.time.profile_live_time.plugin")
    plugin_class = load_callable(module, "ProfileLiveTimeAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.time.profile_live_time.plugin", 
                       className="ProfileLiveTimeAction")
    await plugin.set_up({'end': '10:10:10', 'start': '12:10:10', 'timezone': 'session@context.time.tz'})


async def test_should_set_up_plugin_time_diff_calculator():
    
    module = import_package("tracardi.process_engine.action.v1.time.time_difference.plugin")
    plugin_class = load_callable(module, "TimeDiffCalculator")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.time.time_difference.plugin", 
                       className="TimeDiffCalculator")
    await plugin.set_up({'now': 'now', 'reference_date': '12:10:10'})


async def test_should_set_up_plugin_consent_ux():
    
    module = import_package("tracardi.process_engine.action.v1.ux.consent.plugin")
    plugin_class = load_callable(module, "ConsentUx")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.ux.consent.plugin", 
                       className="ConsentUx")
    await plugin.set_up({'agree_all_event_type': 'agree-all-event-type', 'enabled': True, 'endpoint': 'http://localhost:8686', 'event_type': 'user-consent-pref', 'expand_height': 400, 'position': 'bottom', 'uix_source': 'http://localhost:8686'})


async def test_should_set_up_plugin_html_page_fetch_action():
    
    module = import_package("tracardi.process_engine.action.v1.connectors.html.fetch.plugin")
    plugin_class = load_callable(module, "HtmlPageFetchAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.html.fetch.plugin", 
                       className="HtmlPageFetchAction")
    await plugin.set_up({'body': '', 'cookies': {}, 'headers': {}, 'method': 'get', 'ssl_check': True, 'timeout': 30, 'url': 'http://localhost'})


async def test_should_set_up_plugin_remote_call_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'url': 'http://localhost'},
                test={'url': 'http://localhost'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.api_call.plugin")
    plugin_class = load_callable(module, "RemoteCallAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.api_call.plugin", 
                       className="RemoteCallAction")
    await plugin.set_up({'body': {'content': '{}', 'type': 'application/json'}, 'cookies': {}, 'endpoint': '/test', 'headers': {}, 'method': 'post', 'source': {'id': '1', 'name': 'Some value'}, 'ssl_check': True, 'timeout': 30})


async def test_should_set_up_plugin_smtp_dispatcher_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'smtp': 'a', 'port': 1, 'username': 'u', 'password': 'p'},
                test={'smtp': 'a', 'port': 1, 'username': 'u', 'password': 'p'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.smtp_call.plugin")
    plugin_class = load_callable(module, "SmtpDispatcherAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.smtp_call.plugin", 
                       className="SmtpDispatcherAction")
    await plugin.set_up({'mail': {'message': {'content': 'ss', 'type': 'text/html'}, 'reply_to': 'mail@mail.co', 'send_from': 'mail@mail.co', 'send_to': 'mail@mail.co', 'title': 'title'}, 'resource': {'id': '', 'name': ''}})


async def test_should_set_up_plugin_segment_profile_action():
    
    module = import_package("tracardi.process_engine.action.v1.segmentation.force.plugin")
    plugin_class = load_callable(module, "SegmentProfileAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.segmentation.force.plugin", 
                       className="SegmentProfileAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_has_segment_action():
    
    module = import_package("tracardi.process_engine.action.v1.segmentation.has.plugin")
    plugin_class = load_callable(module, "HasSegmentAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.segmentation.has.plugin", 
                       className="HasSegmentAction")
    await plugin.set_up({'segment': 'abc'})


async def test_should_set_up_plugin_profile_segment_action():
    
    module = import_package("tracardi.process_engine.action.v1.segmentation.conditional.plugin")
    plugin_class = load_callable(module, "ProfileSegmentAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.segmentation.conditional.plugin", 
                       className="ProfileSegmentAction")
    await plugin.set_up({'condition': 'profile@id exists', 'false_action': 'remove', 'false_segment': 'xxx', 'true_action': 'add', 'true_segment': 'zzz'})


async def test_should_set_up_plugin_add_segment_action():
    
    module = import_package("tracardi.process_engine.action.v1.segmentation.add.plugin")
    plugin_class = load_callable(module, "AddSegmentAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.segmentation.add.plugin", 
                       className="AddSegmentAction")
    await plugin.set_up({'segment': 'abc'})


async def test_should_set_up_plugin_delete_segment_action():
    
    module = import_package("tracardi.process_engine.action.v1.segmentation.delete.plugin")
    plugin_class = load_callable(module, "DeleteSegmentAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.segmentation.delete.plugin", 
                       className="DeleteSegmentAction")
    await plugin.set_up({'segment': 'abc'})


async def test_should_set_up_plugin_move_segment_action():
    
    module = import_package("tracardi.process_engine.action.v1.segmentation.move.plugin")
    plugin_class = load_callable(module, "MoveSegmentAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.segmentation.move.plugin", 
                       className="MoveSegmentAction")
    await plugin.set_up({'from_segment': 'abc', 'to_segment': 'asd'})


async def test_should_set_up_plugin_add_interest_action():
    
    module = import_package("tracardi.process_engine.action.v1.interest.add.plugin")
    plugin_class = load_callable(module, "AddInterestAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.interest.add.plugin", 
                       className="AddInterestAction")
    await plugin.set_up({'interest': 'abc', 'value': '1.0'})


async def test_should_set_up_plugin_increase_interest_action():
    
    module = import_package("tracardi.process_engine.action.v1.interest.increase.plugin")
    plugin_class = load_callable(module, "IncreaseInterestAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.interest.increase.plugin", 
                       className="IncreaseInterestAction")
    await plugin.set_up({'interest': 'abc', 'value': '1.0'})


async def test_should_set_up_plugin_decrease_interest_action():
    
    module = import_package("tracardi.process_engine.action.v1.interest.decrease.plugin")
    plugin_class = load_callable(module, "DecreaseInterestAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.interest.decrease.plugin", 
                       className="DecreaseInterestAction")
    await plugin.set_up({'interest': 'abc', 'value': '1.0'})


async def test_should_set_up_plugin_object_to_json_action():
    
    module = import_package("tracardi.process_engine.action.v1.converters.data_to_json.plugin")
    plugin_class = load_callable(module, "ObjectToJsonAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.converters.data_to_json.plugin", 
                       className="ObjectToJsonAction")
    await plugin.set_up({'to_json': '{}'})


async def test_should_set_up_plugin_json_to_object_action():
    
    module = import_package("tracardi.process_engine.action.v1.converters.json_to_data.plugin")
    plugin_class = load_callable(module, "JsonToObjectAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.converters.json_to_data.plugin", 
                       className="JsonToObjectAction")
    await plugin.set_up({'to_data': '{}'})


async def test_should_set_up_plugin_discord_web_hook_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'url': 'http://webhook_url'},
                test={'url': 'http://webhook_url'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.discord.push.plugin")
    plugin_class = load_callable(module, "DiscordWebHookAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.discord.push.plugin", 
                       className="DiscordWebHookAction")
    await plugin.set_up({'resource': {'id': 'id', 'name': 'name'}, 'message': 'message', 'timeout': 10, 'username': 'test'})


async def test_should_set_up_plugin_geo_i_p_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'accountId': 123, 'license': 'test'},
                test={'accountId': 123, 'license': 'test'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.maxmind.geoip.plugin")
    plugin_class = load_callable(module, "GeoIPAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.maxmind.geoip.plugin", 
                       className="GeoIPAction")
    await plugin.set_up({'ip': 'event@request.ip', 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_weather_action():
    
    module = import_package("tracardi.process_engine.action.v1.connectors.weather.msn_weather.plugin")
    plugin_class = load_callable(module, "WeatherAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.weather.msn_weather.plugin", 
                       className="WeatherAction")
    await plugin.set_up({'city': 'London', 'system': 'C'})


async def test_should_set_up_plugin_token_getter(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'url': 'http://url', 'token': 'abc'},
                test={'url': 'http://url', 'token': 'abc'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.oauth2_token.plugin")
    plugin_class = load_callable(module, "TokenGetter")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.oauth2_token.plugin", 
                       className="TokenGetter")
    await plugin.set_up({'destination': 'payload@dest', 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_slack_poster(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'abc'},
                test={'token': 'abc'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.slack.send_message.plugin")
    plugin_class = load_callable(module, "SlackPoster")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.slack.send_message.plugin", 
                       className="SlackPoster")
    await plugin.set_up({'channel': 'xxx', 'message': 'xxx', 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_google_sheets_integrator_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': 'api_key'},
                test={'api_key': 'api_key'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.google.sheets.modify.plugin")
    plugin_class = load_callable(module, "GoogleSheetsIntegratorAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.google.sheets.modify.plugin", 
                       className="GoogleSheetsIntegratorAction")
    await plugin.set_up({'range': 'A1:A2', 'read': False, 'sheet_name': 'sheet', 'source': {'id': '1', 'name': 'Some value'}, 'spreadsheet_id': '1', 'values': '[["Name", "John"]]', 'write': False})


async def test_should_set_up_plugin_twitter_tweet_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': '<api_key', 'api_secret': '<api_secret>', 'access_token': '<access_token>', 'access_token_secret': '<access_token_secret>'},
                test={'api_key': '<api_key', 'api_secret': '<api_secret>', 'access_token': '<access_token>', 'access_token_secret': '<access_token_secret>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.twitter.tweet.plugin")
    plugin_class = load_callable(module, "TwitterTweetAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.twitter.tweet.plugin", 
                       className="TwitterTweetAction")
    await plugin.set_up({'source': {'id': '1', 'name': '1'}, 'tweet': 'tweet'})


async def test_should_set_up_plugin_assign_profile_id_action():
    
    module = import_package("tracardi.process_engine.action.v1.internal.assign_profile_id.plugin")
    plugin_class = load_callable(module, "AssignProfileIdAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.internal.assign_profile_id.plugin", 
                       className="AssignProfileIdAction")
    await plugin.set_up({'value': ''})


async def test_should_set_up_plugin_event_source_fetcher_action():
    
    module = import_package("tracardi.process_engine.action.v1.internal.event_source_fetcher.plugin")
    plugin_class = load_callable(module, "EventSourceFetcherAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.internal.event_source_fetcher.plugin", 
                       className="EventSourceFetcherAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_inject_event():
    
    module = import_package("tracardi.process_engine.action.v1.internal.inject_event.plugin")
    plugin_class = load_callable(module, "InjectEvent")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.internal.inject_event.plugin", 
                       className="InjectEvent")
    await plugin.set_up({'event_id': 'abc'})


async def test_should_set_up_plugin_inject_profile_by_field():
    
    module = import_package("tracardi.process_engine.action.v1.internal.inject_profile_by_field.plugin")
    plugin_class = load_callable(module, "InjectProfileByField")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.internal.inject_profile_by_field.plugin", 
                       className="InjectProfileByField")
    await plugin.set_up({'field': 'data.contact.email', 'value': 'test@test.com'})


async def test_should_set_up_plugin_add_empty_profile_action():
    
    module = import_package("tracardi.process_engine.action.v1.internal.add_empty_profile.plugin")
    plugin_class = load_callable(module, "AddEmptyProfileAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.internal.add_empty_profile.plugin", 
                       className="AddEmptyProfileAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_previous_event_getter():
    
    module = import_package("tracardi.process_engine.action.v1.internal.get_prev_event.plugin")
    plugin_class = load_callable(module, "PreviousEventGetter")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.internal.get_prev_event.plugin", 
                       className="PreviousEventGetter")
    await plugin.set_up({'event_type': {'id': '@current', 'name': '@current'}, 'offset': -1})


async def test_should_set_up_plugin_previous_session_action():
    
    module = import_package("tracardi.process_engine.action.v1.internal.get_prev_session.plugin")
    plugin_class = load_callable(module, "PreviousSessionAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.internal.get_prev_session.plugin", 
                       className="PreviousSessionAction")
    await plugin.set_up({'offset': -1})


async def test_should_set_up_plugin_count_records_action():
    
    module = import_package("tracardi.process_engine.action.v1.internal.query_string.plugin")
    plugin_class = load_callable(module, "CountRecordsAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.internal.query_string.plugin", 
                       className="CountRecordsAction")
    await plugin.set_up({'index': 'None', 'query': '', 'time_range': '+1d'})


async def test_should_set_up_plugin_add_empty_session_action():
    
    module = import_package("tracardi.process_engine.action.v1.internal.add_empty_session.plugin")
    plugin_class = load_callable(module, "AddEmptySessionAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.internal.add_empty_session.plugin", 
                       className="AddEmptySessionAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_create_response_action():
    
    module = import_package("tracardi.process_engine.action.v1.internal.add_response.plugin")
    plugin_class = load_callable(module, "CreateResponseAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.internal.add_response.plugin", 
                       className="CreateResponseAction")
    await plugin.set_up({'body': '{}', 'default': True, 'key': 'key'})


async def test_should_set_up_plugin_key_counter_action():
    
    module = import_package("tracardi.process_engine.action.v1.metrics.key_counter.plugin")
    plugin_class = load_callable(module, "KeyCounterAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.metrics.key_counter.plugin", 
                       className="KeyCounterAction")
    await plugin.set_up({'key': '1', 'save_in': '2'})


async def test_should_set_up_plugin_microservice_action():
    
    module = import_package("tracardi.process_engine.action.v1.microservice.plugin")
    plugin_class = load_callable(module, "MicroserviceAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.microservice.plugin", 
                       className="MicroserviceAction")
    await plugin.set_up({})


async def test_should_set_up_plugin_consent_adder():
    
    module = import_package("tracardi.process_engine.action.v1.consents.add_consent_action.plugin")
    plugin_class = load_callable(module, "ConsentAdder")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.consents.add_consent_action.plugin", 
                       className="ConsentAdder")
    await plugin.set_up({'consents': 'aa'})


async def test_should_set_up_plugin_require_consents_action():
    
    module = import_package("tracardi.process_engine.action.v1.consents.require_consents_action.plugin")
    plugin_class = load_callable(module, "RequireConsentsAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.consents.require_consents_action.plugin", 
                       className="RequireConsentsAction")
    await plugin.set_up({'consent_ids': [], 'require_all': False})


async def test_should_set_up_plugin_contains_string_action():
    
    module = import_package("tracardi.process_engine.action.v1.contains_string_action")
    plugin_class = load_callable(module, "ContainsStringAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.contains_string_action", 
                       className="ContainsStringAction")
    await plugin.set_up({'field': 'payload@field', 'substring': 'contains'})


async def test_should_set_up_plugin_base64_encode_action():
    
    module = import_package("tracardi.process_engine.action.v1.converters.base64.encode.plugin")
    plugin_class = load_callable(module, "Base64EncodeAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.converters.base64.encode.plugin", 
                       className="Base64EncodeAction")
    await plugin.set_up({'source': '', 'source_encoding': ''})


async def test_should_set_up_plugin_base64_decode_action():
    
    module = import_package("tracardi.process_engine.action.v1.converters.base64.decode.plugin")
    plugin_class = load_callable(module, "Base64DecodeAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.converters.base64.decode.plugin", 
                       className="Base64DecodeAction")
    await plugin.set_up({'source': '', 'target_encoding': ''})


async def test_should_set_up_plugin_sort_array_action():
    
    module = import_package("tracardi.process_engine.action.v1.sort_array_action")
    plugin_class = load_callable(module, "SortArrayAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.sort_array_action", 
                       className="SortArrayAction")
    await plugin.set_up({'data': 'event@properties.list_of_something', 'direction': 'asc'})


async def test_should_set_up_plugin_git_hub_list_issues_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_url': 'https://api.github.com', 'personal_access_token': '<your-PAT-here>'},
                test={'api_url': 'https://api.github.com', 'personal_access_token': '<your-PAT-here>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.github.issues.list.plugin")
    plugin_class = load_callable(module, "GitHubListIssuesAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.github.issues.list.plugin", 
                       className="GitHubListIssuesAction")
    await plugin.set_up({'resource': {'id': '', 'name': ''}, 'timeout': 10, 'owner': 'tracardi', 'repo': 'tracardi'})


async def test_should_set_up_plugin_git_hub_get_issue_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_url': 'https://api.github.com', 'personal_access_token': '<your-PAT-here>'},
                test={'api_url': 'https://api.github.com', 'personal_access_token': '<your-PAT-here>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.github.issues.get.plugin")
    plugin_class = load_callable(module, "GitHubGetIssueAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.github.issues.get.plugin", 
                       className="GitHubGetIssueAction")
    await plugin.set_up({'resource': {'id': '', 'name': ''}, 'timeout': 10, 'owner': 'tracardi', 'repo': 'tracardi', 'issue_id': '1'})


async def test_should_set_up_plugin_query_local_database():
    
    module = import_package("tracardi.process_engine.action.v1.connectors.elasticsearch.query_local.plugin")
    plugin_class = load_callable(module, "QueryLocalDatabase")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.elasticsearch.query_local.plugin", 
                       className="QueryLocalDatabase")
    await plugin.set_up({'index': 'index', 'query': '{"query":{"match_all":{}}}'})


async def test_should_set_up_plugin_elastic_search_fetcher(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'url': 'host', 'port': 9200, 'scheme': 'https', 'verify_certs': False},
                test={'url': 'host', 'port': 9200, 'scheme': 'https', 'verify_certs': False}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.elasticsearch.query.plugin")
    plugin_class = load_callable(module, "ElasticSearchFetcher")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.elasticsearch.query.plugin", 
                       className="ElasticSearchFetcher")
    await plugin.set_up({'index': {'id': '1', 'name': 'Some value'}, 'query': '{"query":{"match_all":{}}}', 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_sms77_send_sms_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': 'api_key'},
                test={'api_key': 'api_key'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.sms77.sendsms.plugin")
    plugin_class = load_callable(module, "Sms77SendSmsAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.sms77.sendsms.plugin", 
                       className="Sms77SendSmsAction")
    await plugin.set_up({'resource': {'id': '1', 'name': '1'}, 'message': 'text', 'recipient': 'a', 'sender': 'b'})


async def test_should_set_up_plugin_influx_sender(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'url': 'http://localhost:8086', 'token': '<token>'},
                test={'url': 'http://localhost:8086', 'token': '<token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.influxdb.send.plugin")
    plugin_class = load_callable(module, "InfluxSender")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.influxdb.send.plugin", 
                       className="InfluxSender")
    await plugin.set_up({'bucket': 'bucket', 'fields': {}, 'measurement': 'measurement', 'organization': 'measurement', 'source': {'id': '1', 'name': 'Some value'}, 'tags': {}, 'time': None})


async def test_should_set_up_plugin_influx_fetcher(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'url': 'http://localhost:8086', 'token': '<token>'},
                test={'url': 'http://localhost:8086', 'token': '<token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.influxdb.fetch.plugin")
    plugin_class = load_callable(module, "InfluxFetcher")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.influxdb.fetch.plugin", 
                       className="InfluxFetcher")
    await plugin.set_up({'aggregation': 'abc', 'bucket': 'test', 'filters': {}, 'organization': 'test', 'source': {'id': '1', 'name': 'Some value'}, 'start': '-15m', 'stop': '0m'})


async def test_should_set_up_plugin_elastic_email_contact_adder(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': '<api-key>', 'public_account_id': '<public-account-id>'},
                test={'api_key': '<api-key>', 'public_account_id': '<public-account-id>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.elastic_email.add_contact.plugin")
    plugin_class = load_callable(module, "ElasticEmailContactAdder")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.elastic_email.add_contact.plugin", 
                       className="ElasticEmailContactAdder")
    await plugin.set_up({'additional_mapping': {}, 'email': 'abc@test.com', 'source': {'id': '1', 'name': '1'}})


async def test_should_set_up_plugin_elastic_email_contact_status_change(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': '<api-key>', 'public_account_id': '<public-account-id>'},
                test={'api_key': '<api-key>', 'public_account_id': '<public-account-id>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.elastic_email.contact_status_change.plugin")
    plugin_class = load_callable(module, "ElasticEmailContactStatusChange")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.elastic_email.contact_status_change.plugin", 
                       className="ElasticEmailContactStatusChange")
    await plugin.set_up({'email': 'test@rest.co', 'status': 'status', 'source': {'id': '1', 'name': '1'}})


async def test_should_set_up_plugin_elastic_email_transactional_mail_sender(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': '<api-key>', 'public_account_id': '<public-account-id>'},
                test={'api_key': '<api-key>', 'public_account_id': '<public-account-id>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.elastic_email.transactional_email.plugin")
    plugin_class = load_callable(module, "ElasticEmailTransactionalMailSender")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.elastic_email.transactional_email.plugin", 
                       className="ElasticEmailTransactionalMailSender")
    await plugin.set_up({'message': {'content': {'content': '', 'type': 'text/plain'}, 'recipient': 'test@rest.co', 'subject': 'subject'}, 'sender_email': 'test@rest.co', 'source': {'id': '1', 'name': '1'}})


async def test_should_set_up_plugin_elastic_email_bulk_mail_sender(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': '<api-key>', 'public_account_id': '<public-account-id>'},
                test={'api_key': '<api-key>', 'public_account_id': '<public-account-id>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.elastic_email.bulk_email.plugin")
    plugin_class = load_callable(module, "ElasticEmailBulkMailSender")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.elastic_email.bulk_email.plugin", 
                       className="ElasticEmailBulkMailSender")
    await plugin.set_up({'message': {'content': {'content': '', 'type': 'text/plain'}, 'recipient': 'test@rest.co', 'subject': 'subject'}, 'sender_email': 'test@rest.co', 'source': {'id': '1', 'name': '1'}})


async def test_should_set_up_plugin_sendgrid_contact_adder(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<token>'},
                test={'token': '<token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.sendgrid.add_contact_to_list.plugin")
    plugin_class = load_callable(module, "SendgridContactAdder")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.sendgrid.add_contact_to_list.plugin", 
                       className="SendgridContactAdder")
    await plugin.set_up({'additional_mapping': {}, 'list_ids': 'a,b', 'email': 'test@rest.co', 'source': {'id': '1', 'name': '1'}})


async def test_should_set_up_plugin_sendgrid_global_suppression_adder(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<token>'},
                test={'token': '<token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.sendgrid.add_email_to_global_suppression.plugin")
    plugin_class = load_callable(module, "SendgridGlobalSuppressionAdder")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.sendgrid.add_email_to_global_suppression.plugin", 
                       className="SendgridGlobalSuppressionAdder")
    await plugin.set_up({'email': 'test@rest.co', 'source': {'id': '1', 'name': '1'}})


async def test_should_set_up_plugin_sendgrid_e_mail_sender(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<token>'},
                test={'token': '<token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.sendgrid.send_email.plugin")
    plugin_class = load_callable(module, "SendgridEMailSender")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.sendgrid.send_email.plugin", 
                       className="SendgridEMailSender")
    await plugin.set_up({'message': {'content': {'content': '', 'type': 'text/plain'}, 'recipient': 'test@rest.co', 'subject': 'subject'}, 'sender_email': 'test@rest.co', 'source': {'id': '1', 'name': '1'}})


async def test_should_set_up_plugin_postgre_s_q_l_connector_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'host': '', 'database': 'database', 'user': 'user', 'password': 'password'},
                test={'host': '', 'database': 'database', 'user': 'user', 'password': 'password'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.postgresql.query.plugin")
    plugin_class = load_callable(module, "PostgreSQLConnectorAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.postgresql.query.plugin", 
                       className="PostgreSQLConnectorAction")
    await plugin.set_up({'query': 'select 1', 'source': {'id': '1', 'name': 'Some value'}, 'timeout': 20})


async def test_should_set_up_plugin_mongo_connector_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'uri': 'mongodb://127.0.0.1:27017/', 'timeout': 5000},
                test={'uri': 'mongodb://127.0.0.1:27017/', 'timeout': 5000}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mongo.query.plugin")
    plugin_class = load_callable(module, "MongoConnectorAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mongo.query.plugin", 
                       className="MongoConnectorAction")
    await plugin.set_up({'collection': {'id': '1', 'name': '1'}, 'database': {'id': '1', 'name': '1'}, 'query': '{}', 'source': {'id': '1', 'name': '1'}})


async def test_should_set_up_plugin_mysql_connector_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'host': 'localhost', 'port': 3306, 'user': '<username>', 'password': '', 'database': '<database>'},
                test={'host': 'localhost', 'port': 3306, 'user': '<username>', 'password': '', 'database': '<database>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mysql.query.plugin")
    plugin_class = load_callable(module, "MysqlConnectorAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mysql.query.plugin", 
                       className="MysqlConnectorAction")
    await plugin.set_up({'data': [], 'query': 'SELECT 1', 'source': {'id': '', 'name': ''}, 'timeout': 10, 'type': 'select'})


async def test_should_set_up_plugin_data_extension_sender(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'client_id': '<your-client-id>', 'client_secret': '<your-client-secret>', 'subdomain': '<your-subdomain>'},
                test={'client_id': '<your-client-id>', 'client_secret': '<your-client-secret>', 'subdomain': '<your-subdomain>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.salesforce.marketing_cloud.send.plugin")
    plugin_class = load_callable(module, "DataExtensionSender")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.salesforce.marketing_cloud.send.plugin", 
                       className="DataExtensionSender")
    await plugin.set_up({'extension_id': '1', 'mapping': {}, 'source': {'id': '', 'name': ''}, 'update': False})


async def test_should_set_up_plugin_zapier_web_hook_action():
    
    module = import_package("tracardi.process_engine.action.v1.connectors.zapier.webhook.plugin")
    plugin_class = load_callable(module, "ZapierWebHookAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.zapier.webhook.plugin", 
                       className="ZapierWebHookAction")
    await plugin.set_up({'url': 'http://test.com', 'body': '{}', 'timeout': 30})


async def test_should_set_up_plugin_mqtt_publish_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'url': '<url>', 'port': 100, 'username': '<username>', 'password': '<password>'},
                test={'url': '<url>', 'port': 100, 'username': '<username>', 'password': '<password>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mqtt.publish.plugin")
    plugin_class = load_callable(module, "MqttPublishAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mqtt.publish.plugin", 
                       className="MqttPublishAction")
    await plugin.set_up({'payload': '{}', 'qos': '0', 'retain': False, 'source': {'id': '', 'name': ''}, 'topic': ''})


async def test_should_set_up_plugin_mix_panel_sender(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token', 'server_prefix': 'EU'},
                test={'token': 'token', 'server_prefix': 'EU'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mixpanel.send.plugin")
    plugin_class = load_callable(module, "MixPanelSender")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mixpanel.send.plugin", 
                       className="MixPanelSender")
    await plugin.set_up({'mapping': {}, 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_mix_panel_funnel_fetcher(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token', 'server_prefix': 'EU', 'username': 'username', 'password': 'password'},
                test={'token': 'token', 'server_prefix': 'EU', 'username': 'username', 'password': 'password'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mixpanel.fetch_funnel.plugin")
    plugin_class = load_callable(module, "MixPanelFunnelFetcher")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mixpanel.fetch_funnel.plugin", 
                       className="MixPanelFunnelFetcher")
    await plugin.set_up({'from_date': '2000-01-01', 'funnel_id': 1, 'project_id': 1, 'source': {'id': '1', 'name': 'Some value'}, 'to_date': '2000-01-01'})


async def test_should_set_up_plugin_send_to_airtable_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': '<your-api-key>'},
                test={'api_key': '<your-api-key>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.airtable.send_record.plugin")
    plugin_class = load_callable(module, "SendToAirtableAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.airtable.send_record.plugin", 
                       className="SendToAirtableAction")
    await plugin.set_up({'base_id': 1, 'mapping': {}, 'source': {'id': '1', 'name': 'Some value'}, 'table_name': 'None'})


async def test_should_set_up_plugin_fetch_from_airtable_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': '<your-api-key>'},
                test={'api_key': '<your-api-key>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.airtable.fetch_records.plugin")
    plugin_class = load_callable(module, "FetchFromAirtableAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.airtable.fetch_records.plugin", 
                       className="FetchFromAirtableAction")
    await plugin.set_up({'base_id': 1, 'formula': 'None', 'source': {'id': '1', 'name': 'Some value'}, 'table_name': 'None'})


async def test_should_set_up_plugin_send_event_to_matomo_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<your-token>', 'api_url': '<your-matomo-url>'},
                test={'token': '<your-token>', 'api_url': '<your-matomo-url>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.matomo.send_event.plugin")
    plugin_class = load_callable(module, "SendEventToMatomoAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.matomo.send_event.plugin", 
                       className="SendEventToMatomoAction")
    await plugin.set_up({'dimensions': {}, 'goal_id': 'None', 'rck': 'session@context.utm.term', 'rcn': 'session@context.utm.campaign', 'revenue': None, 'search_category': None, 'search_keyword': None, 'search_results_count': None, 'site_id': 1, 'source': {'id': '1', 'name': 'Some value'}, 'url_ref': 'event@context.page.referer.host'})


async def test_should_set_up_plugin_hub_spot_company_adder(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<your-app-access-token>'},
                test={'token': '<your-app-access-token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.hubspot.add_company.plugin")
    plugin_class = load_callable(module, "HubSpotCompanyAdder")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.hubspot.add_company.plugin", 
                       className="HubSpotCompanyAdder")
    await plugin.set_up({'source': {'id': '1', 'name': '1'}, 'properties': {}})


async def test_should_set_up_plugin_hub_spot_contact_adder(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<your-app-access-token>'},
                test={'token': '<your-app-access-token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.hubspot.add_contact.plugin")
    plugin_class = load_callable(module, "HubSpotContactAdder")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.hubspot.add_contact.plugin", 
                       className="HubSpotContactAdder")
    await plugin.set_up({'source': {'id': '', 'name': ''}, 'properties': []})


async def test_should_set_up_plugin_hub_spot_company_getter(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<your-app-access-token>'},
                test={'token': '<your-app-access-token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.hubspot.get_company.plugin")
    plugin_class = load_callable(module, "HubSpotCompanyGetter")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.hubspot.get_company.plugin", 
                       className="HubSpotCompanyGetter")
    await plugin.set_up({'source': {'id': '', 'name': ''}, 'company_id': '1'})


async def test_should_set_up_plugin_hub_spot_contact_getter(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<your-app-access-token>'},
                test={'token': '<your-app-access-token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.hubspot.get_contact.plugin")
    plugin_class = load_callable(module, "HubSpotContactGetter")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.hubspot.get_contact.plugin", 
                       className="HubSpotContactGetter")
    await plugin.set_up({'source': {'id': '', 'name': ''}, 'contact_id': '1'})


async def test_should_set_up_plugin_hub_spot_company_updater(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<your-app-access-token>'},
                test={'token': '<your-app-access-token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.hubspot.update_company.plugin")
    plugin_class = load_callable(module, "HubSpotCompanyUpdater")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.hubspot.update_company.plugin", 
                       className="HubSpotCompanyUpdater")
    await plugin.set_up({'source': {'id': '', 'name': ''}, 'company_id': '1', 'properties': {}})


async def test_should_set_up_plugin_hub_spot_contact_updater(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<your-app-access-token>'},
                test={'token': '<your-app-access-token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.hubspot.update_contact.plugin")
    plugin_class = load_callable(module, "HubSpotContactUpdater")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.hubspot.update_contact.plugin", 
                       className="HubSpotContactUpdater")
    await plugin.set_up({'source': {'id': '', 'name': ''}, 'contact_id': '1', 'properties': {}})


async def test_should_set_up_plugin_full_contact_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token'},
                test={'token': 'token'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.full_contact.person_enrich.plugin")
    plugin_class = load_callable(module, "FullContactAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.full_contact.person_enrich.plugin", 
                       className="FullContactAction")
    await plugin.set_up({'source': {'id': '1', 'name': '2'}, 'pii': {}})


async def test_should_set_up_plugin_fetch_active_campaign_profile_by_email_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': '<api-key>', 'api_url': '<api-url>'},
                test={'api_key': '<api-key>', 'api_url': '<api-url>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.active_campaign.fetch_by_email.plugin")
    plugin_class = load_callable(module, "FetchActiveCampaignProfileByEmailAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.active_campaign.fetch_by_email.plugin", 
                       className="FetchActiveCampaignProfileByEmailAction")
    await plugin.set_up({'email': 'some@email.com', 'source': {'id': '', 'name': ''}})


async def test_should_set_up_plugin_send_to_active_campaign_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': '<api-key>', 'api_url': '<api-url>'},
                test={'api_key': '<api-key>', 'api_url': '<api-url>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.active_campaign.add_contact.plugin")
    plugin_class = load_callable(module, "SendToActiveCampaignAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.active_campaign.add_contact.plugin", 
                       className="SendToActiveCampaignAction")
    await plugin.set_up({'fields': {}, 'source': {'id': '1', 'name': '1'}})


async def test_should_set_up_plugin_rabbit_publisher_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'uri': 'amqp://localhost:5672/', 'port': '5672', 'timeout': '5', 'virtual_host': ''},
                test={'uri': 'amqp://localhost:5672/', 'port': '5672', 'timeout': '5', 'virtual_host': ''}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.rabbitmq.publish.plugin")
    plugin_class = load_callable(module, "RabbitPublisherAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.rabbitmq.publish.plugin", 
                       className="RabbitPublisherAction")
    await plugin.set_up({'queue': {'auto_declare': True, 'compression': None, 'name': 'queue', 'queue_type': 'direct', 'routing_key': 'None', 'serializer': 'json'}, 'source': {'id': '', 'name': ''}})


async def test_should_set_up_plugin_add_civi_contact_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'api_key': '<api-key>', 'site_key': '<site-key>', 'api_url': 'http://localhost'},
                test={'api_key': '<api-key>', 'site_key': '<site-key>', 'api_url': 'http://localhost'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.civi_crm.add_contact.plugin")
    plugin_class = load_callable(module, "AddCiviContactAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.civi_crm.add_contact.plugin", 
                       className="AddCiviContactAction")
    await plugin.set_up({'contact_type': 'Individual', 'fields': {}, 'source': {'id': '', 'name': ''}})


async def test_should_set_up_plugin_amplitude_send_event(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token'},
                test={'token': 'token'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.amplitude.send_events.plugin")
    plugin_class = load_callable(module, "AmplitudeSendEvent")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.amplitude.send_events.plugin", 
                       className="AmplitudeSendEvent")
    await plugin.set_up({'source': {'id': '1', 'name': '1'}})


async def test_should_set_up_plugin_aws_sqs_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'aws_access_key_id': 'str', 'aws_secret_access_key': 'str'},
                test={'aws_access_key_id': 'str', 'aws_secret_access_key': 'str'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.aws.sqs.plugin")
    plugin_class = load_callable(module, "AwsSqsAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.aws.sqs.plugin", 
                       className="AwsSqsAction")
    await plugin.set_up({'source': {'id': '1', 'name': '2'}, 'message': {'content': 'sssssss', 'type': 'plain/text'}, 'region_name': '', 'queue_url': 'http://test', 'message_attributes': ''})


async def test_should_set_up_plugin_scheduler_plugin(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'callback_host': 'http://localhost:8686'},
                test={'callback_host': 'http://localhost:8686'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.pro.scheduler.plugin")
    plugin_class = load_callable(module, "SchedulerPlugin")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.pro.scheduler.plugin", 
                       className="SchedulerPlugin")
    await plugin.set_up({'resource': {'id': '1', 'name': '2'}, 'source': {'id': '1', 'name': '2'}, 'event_type': 'type', 'postpone': 10})


async def test_should_set_up_plugin_novu_trigger_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token'},
                test={'token': 'token'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.novu.trigger.plugin")
    plugin_class = load_callable(module, "NovuTriggerAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.novu.trigger.plugin", 
                       className="NovuTriggerAction")
    await plugin.set_up({'payload': '{}', 'recipient_email': 'profile@data.contact.email', 'source': {'id': '', 'name': ''}, 'subscriber_id': 'profile@id', 'template': {'id': '', 'name': ''}})


async def test_should_set_up_plugin_pushover_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<token>', 'user': '<user>'},
                test={'token': '<token>', 'user': '<user>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.pushover.push.plugin")
    plugin_class = load_callable(module, "PushoverAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.pushover.push.plugin", 
                       className="PushoverAction")
    await plugin.set_up({'source': {'id': '', 'name': ''}, 'message': 'test'})


async def test_should_set_up_plugin_sentiment_analysis_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token'},
                test={'token': 'token'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.sentiment_analysis.plugin")
    plugin_class = load_callable(module, "SentimentAnalysisAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.meaningcloud.sentiment_analysis.plugin", 
                       className="SentimentAnalysisAction")
    await plugin.set_up({'source': {'id': '', 'name': ''}, 'language': 'en', 'text': 'text'})


async def test_should_set_up_plugin_language_detect_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token'},
                test={'token': 'token'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.language_detection.plugin")
    plugin_class = load_callable(module, "LanguageDetectAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.meaningcloud.language_detection.plugin", 
                       className="LanguageDetectAction")
    await plugin.set_up({'source': {'id': '', 'name': ''}, 'message': 'Hello world', 'timeout': 15})


async def test_should_set_up_plugin_text_classification_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token'},
                test={'token': 'token'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.text_classification.plugin")
    plugin_class = load_callable(module, "TextClassificationAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.meaningcloud.text_classification.plugin", 
                       className="TextClassificationAction")
    await plugin.set_up({'source': {'id': '', 'name': ''}, 'language': 'en', 'model': 'social', 'title': 'title', 'text': 'text'})


async def test_should_set_up_plugin_corporate_reputation_plugin(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token'},
                test={'token': 'token'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.corporate_reputation.plugin")
    plugin_class = load_callable(module, "CorporateReputationPlugin")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.meaningcloud.corporate_reputation.plugin", 
                       className="CorporateReputationPlugin")
    await plugin.set_up({'source': {'name': 'Test', 'id': '1'}, 'text': 'text', 'lang': 'auto', 'focus': 'focus', 'company_type': 'type', 'relaxed_typography': False})


async def test_should_set_up_plugin_topics_extraction_plugin(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token'},
                test={'token': 'token'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.topics_extraction.plugin")
    plugin_class = load_callable(module, "TopicsExtractionPlugin")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.meaningcloud.topics_extraction.plugin", 
                       className="TopicsExtractionPlugin")
    await plugin.set_up({'source': {'name': 'test', 'id': '1'}, 'text': 'test', 'lang': 'auto'})


async def test_should_set_up_plugin_summarization_plugin(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token'},
                test={'token': 'token'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.summarization.plugin")
    plugin_class = load_callable(module, "SummarizationPlugin")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.meaningcloud.summarization.plugin", 
                       className="SummarizationPlugin")
    await plugin.set_up({'source': {'name': 'Test', 'id': '1'}, 'text': 'text', 'lang': 'auto', 'sentences': '2'})


async def test_should_set_up_plugin_deep_categorization_plugin(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': 'token'},
                test={'token': 'token'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.deep_categorization.plugin")
    plugin_class = load_callable(module, "DeepCategorizationPlugin")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.meaningcloud.deep_categorization.plugin", 
                       className="DeepCategorizationPlugin")
    await plugin.set_up({'source': {'name': 'Test', 'id': '1'}, 'text': 'Text', 'model': 'IAB_2.0-tier3'})


async def test_should_set_up_plugin_mautic_contact_adder(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'public_key': '<client-public-key>', 'private_key': '<client-private-key>', 'api_url': '<url-of-mautic-instance>'},
                test={'public_key': '<client-public-key>', 'private_key': '<client-private-key>', 'api_url': '<url-of-mautic-instance>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mautic.add_contact.plugin")
    plugin_class = load_callable(module, "MauticContactAdder")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mautic.add_contact.plugin", 
                       className="MauticContactAdder")
    await plugin.set_up({'additional_mapping': {}, 'email': 'test@test.com', 'overwrite_with_blank': False, 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_mautic_contact_by_i_d_fetcher(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'public_key': '<client-public-key>', 'private_key': '<client-private-key>', 'api_url': '<url-of-mautic-instance>'},
                test={'public_key': '<client-public-key>', 'private_key': '<client-private-key>', 'api_url': '<url-of-mautic-instance>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mautic.fetch_contact_by_id.plugin")
    plugin_class = load_callable(module, "MauticContactByIDFetcher")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mautic.fetch_contact_by_id.plugin", 
                       className="MauticContactByIDFetcher")
    await plugin.set_up({'contact_id': '1', 'source': {'id': 'None', 'name': 'None'}})


async def test_should_set_up_plugin_mautic_contact_by_email_fetcher(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'public_key': '<client-public-key>', 'private_key': '<client-private-key>', 'api_url': '<url-of-mautic-instance>'},
                test={'public_key': '<client-public-key>', 'private_key': '<client-private-key>', 'api_url': '<url-of-mautic-instance>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mautic.fetch_contact_by_email.plugin")
    plugin_class = load_callable(module, "MauticContactByEmailFetcher")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mautic.fetch_contact_by_email.plugin", 
                       className="MauticContactByEmailFetcher")
    await plugin.set_up({'contact_email': 'test@test.com', 'source': {'id': 'None', 'name': 'None'}})


async def test_should_set_up_plugin_mautic_points_editor(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'public_key': '<client-public-key>', 'private_key': '<client-private-key>', 'api_url': '<url-of-mautic-instance>'},
                test={'public_key': '<client-public-key>', 'private_key': '<client-private-key>', 'api_url': '<url-of-mautic-instance>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mautic.edit_points.plugin")
    plugin_class = load_callable(module, "MauticPointsEditor")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mautic.edit_points.plugin", 
                       className="MauticPointsEditor")
    await plugin.set_up({'action': 'add', 'contact_id': '1', 'points': 1, 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_mautic_segment_editor(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'public_key': '<client-public-key>', 'private_key': '<client-private-key>', 'api_url': '<url-of-mautic-instance>'},
                test={'public_key': '<client-public-key>', 'private_key': '<client-private-key>', 'api_url': '<url-of-mautic-instance>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mautic.add_remove_segment.plugin")
    plugin_class = load_callable(module, "MauticSegmentEditor")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mautic.add_remove_segment.plugin", 
                       className="MauticSegmentEditor")
    await plugin.set_up({'action': 'add', 'contact_id': '1', 'segment': 'None', 'source': {'id': 'None', 'name': 'None'}})


async def test_should_set_up_plugin_transactional_mail_sender(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '<token>'},
                test={'token': '<token>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mailchimp.transactional_email.plugin")
    plugin_class = load_callable(module, "TransactionalMailSender")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mailchimp.transactional_email.plugin", 
                       className="TransactionalMailSender")
    await plugin.set_up({'message': {'content': {'content': 'None', 'type': 'text/html'}, 'recipient': 'test@test.com', 'subject': 'None'}, 'sender_email': 'test@test.com', 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_mail_chimp_audience_adder(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '1-2'},
                test={'token': '1-2'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mailchimp.add_to_audience.plugin")
    plugin_class = load_callable(module, "MailChimpAudienceAdder")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mailchimp.add_to_audience.plugin", 
                       className="MailChimpAudienceAdder")
    await plugin.set_up({'email': 'email@email.com', 'list_id': '1', 'merge_fields': {}, 'source': {'id': '1', 'name': 'test'}, 'subscribed': False, 'update': False})


async def test_should_set_up_plugin_mail_chimp_audience_remover(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'token': '1-2'},
                test={'token': '1-2'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.connectors.mailchimp.remove_from_audience.plugin")
    plugin_class = load_callable(module, "MailChimpAudienceRemover")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.connectors.mailchimp.remove_from_audience.plugin", 
                       className="MailChimpAudienceRemover")
    await plugin.set_up({'delete': False, 'email': 'test@test.com', 'list_id': 'None', 'source': {'id': 'None', 'name': 'None'}})


async def test_should_set_up_plugin_write_to_memory_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'url': '<url>', 'user': '<user>', 'password': '<password>'},
                test={'url': '<url>', 'user': '<user>', 'password': '<password>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.operations.write_to_memory.plugin")
    plugin_class = load_callable(module, "WriteToMemoryAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.operations.write_to_memory.plugin", 
                       className="WriteToMemoryAction")
    await plugin.set_up({'key': 'test-key', 'ttl': 15, 'value': 'test-value'})


async def test_should_set_up_plugin_read_from_memory_action(mocker):
    
    mocker.patch(
        # api_call is from slow.py but imported to main.py
        'tracardi.service.storage.driver.elastic.resource.load',
        return_value=Resource(
            id="test-resource",
            type="test",
            credentials=ResourceCredentials(
                production={'url': '<url>', 'user': '<user>', 'password': '<password>'},
                test={'url': '<url>', 'user': '<user>', 'password': '<password>'}
            )
        )
    )

    module = import_package("tracardi.process_engine.action.v1.operations.read_from_memory.plugin")
    plugin_class = load_callable(module, "ReadFromMemoryAction")
    plugin = plugin_class()
    plugin.node = Node(id="node-id", 
                       name="test-node", 
                       module="tracardi.process_engine.action.v1.operations.read_from_memory.plugin", 
                       className="ReadFromMemoryAction")
    await plugin.set_up({'key': 'test-key'})
