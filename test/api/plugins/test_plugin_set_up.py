
from test.api.plugins.test_all_endpoints import _load_plugin_registry_metadata
from tracardi.service.module_loader import load_callable, import_package


async def test_should_set_up_plugin_payload_memory_collector():
    module = import_package("tracardi.process_engine.action.v1.memory.collect.plugin")
    plugin_class = load_callable(module, "PayloadMemoryCollector")
    plugin = plugin_class()
    await plugin.set_up({'name': 'Test name', 'type': 'list'})


async def test_should_set_up_plugin_password_generator_action():
    module = import_package("tracardi.process_engine.action.v1.password_generator_action")
    plugin_class = load_callable(module, "PasswordGeneratorAction")
    plugin = plugin_class()
    await plugin.set_up({'lowercase': 4, 'max_length': 13, 'min_length': 8, 'special_characters': 2, 'uppercase': 2})


async def test_should_set_up_plugin_week_days_checker():
    module = import_package("tracardi.process_engine.action.v1.weekdays_checker_action")
    plugin_class = load_callable(module, "WeekDaysChecker")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_start_action():
    module = import_package("tracardi.process_engine.action.v1.flow.start.start_action")
    plugin_class = load_callable(module, "StartAction")
    plugin = plugin_class()
    await plugin.set_up({'debug': False, 'event_id': None, 'event_type': {'id': '', 'name': ''}, 'event_types': [], 'profile_less': False, 'properties': '{}', 'session_less': False})


async def test_should_set_up_plugin_property_exists_action():
    module = import_package("tracardi.process_engine.action.v1.flow.property_exists.plugin")
    plugin_class = load_callable(module, "PropertyExistsAction")
    plugin = plugin_class()
    await plugin.set_up({'property': 'event@context.page.url'})


async def test_should_set_up_plugin_end_action():
    module = import_package("tracardi.process_engine.action.v1.end_action")
    plugin_class = load_callable(module, "EndAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_raise_error_action():
    module = import_package("tracardi.process_engine.action.v1.raise_error_action")
    plugin_class = load_callable(module, "RaiseErrorAction")
    plugin = plugin_class()
    await plugin.set_up({'message': 'Flow stopped due to error.'})


async def test_should_set_up_plugin_inject_action():
    module = import_package("tracardi.process_engine.action.v1.inject_action")
    plugin_class = load_callable(module, "InjectAction")
    plugin = plugin_class()
    await plugin.set_up({'destination': 'payload', 'value': '{}'})


async def test_should_set_up_plugin_increase_views_action():
    module = import_package("tracardi.process_engine.action.v1.increase_views_action")
    plugin_class = load_callable(module, "IncreaseViewsAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_increase_visits_action():
    module = import_package("tracardi.process_engine.action.v1.increase_visits_action")
    plugin_class = load_callable(module, "IncreaseVisitsAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_increment_action():
    module = import_package("tracardi.process_engine.action.v1.increment_action")
    plugin_class = load_callable(module, "IncrementAction")
    plugin = plugin_class()
    await plugin.set_up({'field': 'profile@stats.counters.test', 'increment': 1})


async def test_should_set_up_plugin_decrement_action():
    module = import_package("tracardi.process_engine.action.v1.decrement_action")
    plugin_class = load_callable(module, "DecrementAction")
    plugin = plugin_class()
    await plugin.set_up({'decrement': 1, 'field': 'profile@stats.counters.test'})


async def test_should_set_up_plugin_if_action():
    module = import_package("tracardi.process_engine.action.v1.if_action")
    plugin_class = load_callable(module, "IfAction")
    plugin = plugin_class()
    await plugin.set_up({'condition': 'event@id=="1"'})


async def test_should_set_up_plugin_starts_with_action():
    module = import_package("tracardi.process_engine.action.v1.starts_with_action")
    plugin_class = load_callable(module, "StartsWithAction")
    plugin = plugin_class()
    await plugin.set_up({'field': 'event@id', 'prefix': 'test'})


async def test_should_set_up_plugin_ends_with_action():
    module = import_package("tracardi.process_engine.action.v1.ends_with_action")
    plugin_class = load_callable(module, "EndsWithAction")
    plugin = plugin_class()
    await plugin.set_up({'field': 'event@id', 'prefix': 'test'})


async def test_should_set_up_plugin_new_visit_action():
    module = import_package("tracardi.process_engine.action.v1.new_visit_action")
    plugin_class = load_callable(module, "NewVisitAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_new_profile_action():
    module = import_package("tracardi.process_engine.action.v1.new_profile_action")
    plugin_class = load_callable(module, "NewProfileAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_template_action():
    module = import_package("tracardi.process_engine.action.v1.template_action")
    plugin_class = load_callable(module, "TemplateAction")
    plugin = plugin_class()
    await plugin.set_up({'template': ''})


async def test_should_set_up_plugin_get_uuid4_action():
    module = import_package("tracardi.process_engine.action.v1.misc.uuid4.plugin")
    plugin_class = load_callable(module, "GetUuid4Action")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_copy_trait_action():
    module = import_package("tracardi.process_engine.action.v1.traits.copy_trait_action")
    plugin_class = load_callable(module, "CopyTraitAction")
    plugin = plugin_class()
    await plugin.set_up({'traits': {'set': {}}})


async def test_should_set_up_plugin_append_trait_action():
    module = import_package("tracardi.process_engine.action.v1.traits.append_trait_action")
    plugin_class = load_callable(module, "AppendTraitAction")
    plugin = plugin_class()
    await plugin.set_up({'append': {'target1': 'source1', 'target2': 'source2'}, 'remove': {'target': ['item1', 'item2']}})


async def test_should_set_up_plugin_cut_out_trait_action():
    module = import_package("tracardi.process_engine.action.v1.traits.cut_out_trait_action")
    plugin_class = load_callable(module, "CutOutTraitAction")
    plugin = plugin_class()
    await plugin.set_up({'trait': 'event@...'})


async def test_should_set_up_plugin_delete_trait_action():
    module = import_package("tracardi.process_engine.action.v1.traits.delete_trait_action")
    plugin_class = load_callable(module, "DeleteTraitAction")
    plugin = plugin_class()
    await plugin.set_up({'delete': ['event@id']})


async def test_should_set_up_plugin_auto_merge_properties_to_profile_action():
    module = import_package("tracardi.process_engine.action.v1.traits.auto_merge_properties_to_profile_action")
    plugin_class = load_callable(module, "AutoMergePropertiesToProfileAction")
    plugin = plugin_class()
    await plugin.set_up({'sub_traits': '', 'traits_type': 'public'})


async def test_should_set_up_plugin_assign_condition_result_plugin():
    module = import_package("tracardi.process_engine.action.v1.traits.assign_condition_result.plugin")
    plugin_class = load_callable(module, "AssignConditionResultPlugin")
    plugin = plugin_class()
    await plugin.set_up({'conditions': {}})


async def test_should_set_up_plugin_condition_set_plugin():
    module = import_package("tracardi.process_engine.action.v1.traits.condition_set.plugin")
    plugin_class = load_callable(module, "ConditionSetPlugin")
    plugin = plugin_class()
    await plugin.set_up({'conditions': {}})


async def test_should_set_up_plugin_hash_traits_action():
    module = import_package("tracardi.process_engine.action.v1.traits.hash_traits_action")
    plugin_class = load_callable(module, "HashTraitsAction")
    plugin = plugin_class()
    await plugin.set_up({'func': 'md5', 'traits': []})


async def test_should_set_up_plugin_mask_traits_action():
    module = import_package("tracardi.process_engine.action.v1.traits.mask_traits_action")
    plugin_class = load_callable(module, "MaskTraitsAction")
    plugin = plugin_class()
    await plugin.set_up({'traits': []})


async def test_should_set_up_plugin_join_payloads():
    module = import_package("tracardi.process_engine.action.v1.operations.join_payloads.plugin")
    plugin_class = load_callable(module, "JoinPayloads")
    plugin = plugin_class()
    await plugin.set_up({'default': True, 'reshape': '{}', 'type': 'dict'})


async def test_should_set_up_plugin_merge_profiles_action():
    module = import_package("tracardi.process_engine.action.v1.operations.merge_profiles_action")
    plugin_class = load_callable(module, "MergeProfilesAction")
    plugin = plugin_class()
    await plugin.set_up({'mergeBy': ['profile@pii.email']})


async def test_should_set_up_plugin_segment_profile_action():
    module = import_package("tracardi.process_engine.action.v1.operations.segment_profile_action")
    plugin_class = load_callable(module, "SegmentProfileAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_update_profile_action():
    module = import_package("tracardi.process_engine.action.v1.operations.update_profile_action")
    plugin_class = load_callable(module, "UpdateProfileAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_update_event_action():
    module = import_package("tracardi.process_engine.action.v1.operations.update_event_action")
    plugin_class = load_callable(module, "UpdateEventAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_update_session_action():
    module = import_package("tracardi.process_engine.action.v1.operations.update_session_action")
    plugin_class = load_callable(module, "UpdateSessionAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_array_reducer():
    module = import_package("tracardi.process_engine.action.v1.operations.reduce_array.plugin")
    plugin_class = load_callable(module, "ArrayReducer")
    plugin = plugin_class()
    await plugin.set_up({'array': ''})


async def test_should_set_up_plugin_write_to_memory_action():
    module = import_package("tracardi.process_engine.action.v1.operations.write_to_memory.plugin")
    plugin_class = load_callable(module, "WriteToMemoryAction")
    plugin = plugin_class()
    await plugin.set_up({'key': 'test-key', 'ttl': 15, 'value': 'test-value'})


async def test_should_set_up_plugin_read_from_memory_action():
    module = import_package("tracardi.process_engine.action.v1.operations.read_from_memory.plugin")
    plugin_class = load_callable(module, "ReadFromMemoryAction")
    plugin = plugin_class()
    await plugin.set_up({'key': 'test-key'})


async def test_should_set_up_plugin_calculator_action():
    module = import_package("tracardi.process_engine.action.v1.calculator_action")
    plugin_class = load_callable(module, "CalculatorAction")
    plugin = plugin_class()
    await plugin.set_up({'calc_dsl': 'a = profile@id + 1'})


async def test_should_set_up_plugin_mapping_action():
    module = import_package("tracardi.process_engine.action.v1.mapping_action")
    plugin_class = load_callable(module, "MappingAction")
    plugin = plugin_class()
    await plugin.set_up({'case_sensitive': False, 'mapping': {'a': 'profile@id'}, 'value': 'x'})


async def test_should_set_up_plugin_random_item_action():
    module = import_package("tracardi.process_engine.action.v1.return_random_element_action")
    plugin_class = load_callable(module, "RandomItemAction")
    plugin = plugin_class()
    await plugin.set_up({'list_of_items': [1, 2, 3, 4, 5]})


async def test_should_set_up_plugin_log_action():
    module = import_package("tracardi.process_engine.action.v1.log_action")
    plugin_class = load_callable(module, "LogAction")
    plugin = plugin_class()
    await plugin.set_up({'message': '<log-message>', 'type': 'warning'})


async def test_should_set_up_plugin_html_xpath_scrapper_action():
    module = import_package("tracardi.process_engine.action.v1.scrapper.xpath.plugin")
    plugin_class = load_callable(module, "HtmlXpathScrapperAction")
    plugin = plugin_class()
    await plugin.set_up({'content': None, 'xpath': None})


async def test_should_set_up_plugin_value_threshold_action():
    module = import_package("tracardi.process_engine.action.v1.operations.threshold.plugin")
    plugin_class = load_callable(module, "ValueThresholdAction")
    plugin = plugin_class()
    await plugin.set_up({'assign_to_profile': True, 'name': None, 'ttl': 1800, 'value': None})


async def test_should_set_up_plugin_circular_geo_fence_action():
    module = import_package("tracardi.process_engine.action.v1.geo.fence.circular.plugin")
    plugin_class = load_callable(module, "CircularGeoFenceAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_geo_distance_action():
    module = import_package("tracardi.process_engine.action.v1.geo.distance.plugin")
    plugin_class = load_callable(module, "GeoDistanceAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_reshape_payload_action():
    module = import_package("tracardi.process_engine.action.v1.traits.reshape_payload_action")
    plugin_class = load_callable(module, "ReshapePayloadAction")
    plugin = plugin_class()
    await plugin.set_up({'default': True, 'value': '{}'})


async def test_should_set_up_plugin_detect_client_agent_action():
    module = import_package("tracardi.process_engine.action.v1.detect_client_agent_action")
    plugin_class = load_callable(module, "DetectClientAgentAction")
    plugin = plugin_class()
    await plugin.set_up({'agent': 'session@context.browser.browser.userAgent'})


async def test_should_set_up_plugin_field_type_action():
    module = import_package("tracardi.process_engine.action.v1.traits.field_type_action")
    plugin_class = load_callable(module, "FieldTypeAction")
    plugin = plugin_class()
    await plugin.set_up({'field': None})


async def test_should_set_up_plugin_event_counter():
    module = import_package("tracardi.process_engine.action.v1.events.event_counter.plugin")
    plugin_class = load_callable(module, "EventCounter")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_event_aggregator():
    module = import_package("tracardi.process_engine.action.v1.events.event_aggregator.plugin")
    plugin_class = load_callable(module, "EventAggregator")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_event_discarder():
    module = import_package("tracardi.process_engine.action.v1.events.event_discarder.plugin")
    plugin_class = load_callable(module, "EventDiscarder")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_schema_validator():
    module = import_package("tracardi.process_engine.action.v1.json_schema_validation_action")
    plugin_class = load_callable(module, "SchemaValidator")
    plugin = plugin_class()
    await plugin.set_up({'validation_schema': {}})


async def test_should_set_up_plugin_string_properties_actions():
    module = import_package("tracardi.process_engine.action.v1.strings.string_operations.plugin")
    plugin_class = load_callable(module, "StringPropertiesActions")
    plugin = plugin_class()
    await plugin.set_up({'string': ''})


async def test_should_set_up_plugin_regex_match_action():
    module = import_package("tracardi.process_engine.action.v1.strings.regex_match.plugin")
    plugin_class = load_callable(module, "RegexMatchAction")
    plugin = plugin_class()
    await plugin.set_up({'group_prefix': 'Group', 'pattern': '<pattern>', 'text': '<text or path to text>'})


async def test_should_set_up_plugin_regex_validator_action():
    module = import_package("tracardi.process_engine.action.v1.strings.regex_validator.plugin")
    plugin_class = load_callable(module, "RegexValidatorAction")
    plugin = plugin_class()
    await plugin.set_up({'data': None, 'validation_regex': None})


async def test_should_set_up_plugin_string_validator_action():
    module = import_package("tracardi.process_engine.action.v1.strings.string_validator.plugin")
    plugin_class = load_callable(module, "StringValidatorAction")
    plugin = plugin_class()
    await plugin.set_up({'data': None, 'validator': None})


async def test_should_set_up_plugin_splitter_action():
    module = import_package("tracardi.process_engine.action.v1.strings.string_splitter.plugin")
    plugin_class = load_callable(module, "SplitterAction")
    plugin = plugin_class()
    await plugin.set_up({'delimiter': '.', 'string': None})


async def test_should_set_up_plugin_parse_u_r_l_parameters():
    module = import_package("tracardi.process_engine.action.v1.strings.url_parser.plugin")
    plugin_class = load_callable(module, "ParseURLParameters")
    plugin = plugin_class()
    await plugin.set_up({'url': 'session@context.page.url'})


async def test_should_set_up_plugin_regex_replacer():
    module = import_package("tracardi.process_engine.action.v1.strings.regex_replace.plugin")
    plugin_class = load_callable(module, "RegexReplacer")
    plugin = plugin_class()
    await plugin.set_up({'find_regex': None, 'replace_with': None, 'string': None})


async def test_should_set_up_plugin_sleep_action():
    module = import_package("tracardi.process_engine.action.v1.time.sleep_action")
    plugin_class = load_callable(module, "SleepAction")
    plugin = plugin_class()
    await plugin.set_up({'wait': 1})


async def test_should_set_up_plugin_today_action():
    module = import_package("tracardi.process_engine.action.v1.time.today_action")
    plugin_class = load_callable(module, "TodayAction")
    plugin = plugin_class()
    await plugin.set_up({'timezone': 'session@context.time.tz'})


async def test_should_set_up_plugin_day_night_action():
    module = import_package("tracardi.process_engine.action.v1.time.day_night.plugin")
    plugin_class = load_callable(module, "DayNightAction")
    plugin = plugin_class()
    await plugin.set_up({'latitude': None, 'longitude': None})


async def test_should_set_up_plugin_local_time_span_action():
    module = import_package("tracardi.process_engine.action.v1.time.local_time_span.plugin")
    plugin_class = load_callable(module, "LocalTimeSpanAction")
    plugin = plugin_class()
    await plugin.set_up({'end': None, 'start': None, 'timezone': 'session@context.time.tz'})


async def test_should_set_up_plugin_time_diff_calculator():
    module = import_package("tracardi.process_engine.action.v1.time.time_difference.plugin")
    plugin_class = load_callable(module, "TimeDiffCalculator")
    plugin = plugin_class()
    await plugin.set_up({'now': 'now', 'reference_date': None})


async def test_should_set_up_plugin_snack_bar_ux():
    module = import_package("tracardi.process_engine.action.v1.ux.snackbar.plugin")
    plugin_class = load_callable(module, "SnackBarUx")
    plugin = plugin_class()
    await plugin.set_up({'hide_after': 6000, 'message': '', 'position_x': 'center', 'position_y': 'bottom', 'type': 'success', 'uix_mf_source': 'http://localhost:8686'})


async def test_should_set_up_plugin_consent_ux():
    module = import_package("tracardi.process_engine.action.v1.ux.consent.plugin")
    plugin_class = load_callable(module, "ConsentUx")
    plugin = plugin_class()
    await plugin.set_up({'agree_all_event_type': 'agree-all-event-type', 'enabled': True, 'endpoint': 'http://localhost:8686', 'event_type': 'user-consent-pref', 'expand_height': 400, 'position': 'bottom', 'uix_source': 'http://localhost:8686'})


async def test_should_set_up_plugin_cta_message_ux():
    module = import_package("tracardi.process_engine.action.v1.ux.cta_message.plugin")
    plugin_class = load_callable(module, "CtaMessageUx")
    plugin = plugin_class()
    await plugin.set_up({'border_radius': 2, 'border_shadow': 1, 'cancel_button': '', 'cta_button': '', 'cta_link': '', 'hide_after': 6000, 'max_width': 500, 'message': '', 'min_width': 300, 'position_x': 'right', 'position_y': 'bottom', 'title': '', 'uix_mf_source': 'http://localhost:8686'})


async def test_should_set_up_plugin_rating_popup_plugin():
    module = import_package("tracardi.process_engine.action.v1.ux.rating_popup.plugin")
    plugin_class = load_callable(module, "RatingPopupPlugin")
    plugin = plugin_class()
    await plugin.set_up({'api_url': 'http://localhost:8686', 'dark_theme': False, 'event_type': None, 'horizontal_position': 'center', 'lifetime': '6', 'message': None, 'save_event': True, 'title': None, 'uix_source': 'http://localhost:8686', 'vertical_position': 'bottom'})


async def test_should_set_up_plugin_question_popup_plugin():
    module = import_package("tracardi.process_engine.action.v1.ux.question_popup.plugin")
    plugin_class = load_callable(module, "QuestionPopupPlugin")
    plugin = plugin_class()
    await plugin.set_up({'api_url': 'http://localhost:8686', 'content': None, 'dark_theme': False, 'event_type': None, 'horizontal_pos': 'center', 'left_button_text': None, 'popup_lifetime': '6', 'popup_title': None, 'right_button_text': None, 'save_event': True, 'uix_source': 'http://localhost:8686', 'vertical_pos': 'bottom'})


async def test_should_set_up_plugin_contact_popup_plugin():
    module = import_package("tracardi.process_engine.action.v1.ux.contact_popup.plugin")
    plugin_class = load_callable(module, "ContactPopupPlugin")
    plugin = plugin_class()
    await plugin.set_up({'api_url': 'http://localhost:8686', 'contact_type': 'email', 'content': None, 'dark_theme': False, 'event_type': None, 'horizontal_pos': 'center', 'save_event': True, 'uix_source': 'http://localhost:8686', 'vertical_pos': 'bottom'})


async def test_should_set_up_plugin_generic_uix_plugin():
    module = import_package("tracardi.process_engine.action.v1.ux.generic.plugin")
    plugin_class = load_callable(module, "GenericUixPlugin")
    plugin = plugin_class()
    await plugin.set_up({'props': {}, 'uix_source': None})


async def test_should_set_up_plugin_html_page_fetch_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.html.fetch.plugin")
    plugin_class = load_callable(module, "HtmlPageFetchAction")
    plugin = plugin_class()
    await plugin.set_up({'body': '', 'cookies': {}, 'headers': {}, 'method': 'get', 'ssl_check': True, 'timeout': 30, 'url': None})


async def test_should_set_up_plugin_remote_call_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.api_call.plugin")
    plugin_class = load_callable(module, "RemoteCallAction")
    plugin = plugin_class()
    await plugin.set_up({'body': {'content': '{}', 'type': 'application/json'}, 'cookies': {}, 'endpoint': None, 'headers': {}, 'method': 'post', 'source': {'id': '1', 'name': 'Some value'}, 'ssl_check': True, 'timeout': 30})


async def test_should_set_up_plugin_smtp_dispatcher_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.smtp_call.plugin")
    plugin_class = load_callable(module, "SmtpDispatcherAction")
    plugin = plugin_class()
    await plugin.set_up({'message': {'message': '', 'reply_to': '', 'send_from': '', 'send_to': '', 'title': ''}, 'source': {'id': '', 'name': ''}})


async def test_should_set_up_plugin_profile_segment_action():
    module = import_package("tracardi.process_engine.action.v1.segments.profile_segmentation.plugin")
    plugin_class = load_callable(module, "ProfileSegmentAction")
    plugin = plugin_class()
    await plugin.set_up({'condition': '', 'false_action': 'remove', 'false_segment': '', 'true_action': 'add', 'true_segment': ''})


async def test_should_set_up_plugin_object_to_json_action():
    module = import_package("tracardi.process_engine.action.v1.converters.data_to_json.plugin")
    plugin_class = load_callable(module, "ObjectToJsonAction")
    plugin = plugin_class()
    await plugin.set_up({'to_json': None})


async def test_should_set_up_plugin_json_to_object_action():
    module = import_package("tracardi.process_engine.action.v1.converters.json_to_data.plugin")
    plugin_class = load_callable(module, "JsonToObjectAction")
    plugin = plugin_class()
    await plugin.set_up({'to_data': None})


async def test_should_set_up_plugin_transactional_mail_sender():
    module = import_package("tracardi.process_engine.action.v1.connectors.mailchimp.transactional_email.plugin")
    plugin_class = load_callable(module, "TransactionalMailSender")
    plugin = plugin_class()
    await plugin.set_up({'message': {'content': None, 'recipient': None, 'subject': None}, 'sender_email': None, 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_elastic_search_fetcher():
    module = import_package("tracardi.process_engine.action.v1.connectors.elasticsearch.query.plugin")
    plugin_class = load_callable(module, "ElasticSearchFetcher")
    plugin = plugin_class()
    await plugin.set_up({'index': None, 'query': '{"query":{"match_all":{}}}', 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_mail_chimp_audience_adder():
    module = import_package("tracardi.process_engine.action.v1.connectors.mailchimp.add_to_audience.plugin")
    plugin_class = load_callable(module, "MailChimpAudienceAdder")
    plugin = plugin_class()
    await plugin.set_up({'email': None, 'list_id': None, 'merge_fields': {}, 'source': {'id': None, 'name': None}, 'subscribed': False, 'update': False})


async def test_should_set_up_plugin_mail_chimp_audience_remover():
    module = import_package("tracardi.process_engine.action.v1.connectors.mailchimp.remove_from_audience.plugin")
    plugin_class = load_callable(module, "MailChimpAudienceRemover")
    plugin = plugin_class()
    await plugin.set_up({'delete': False, 'email': None, 'list_id': None, 'source': {'id': None, 'name': None}})


async def test_should_set_up_plugin_trello_card_adder():
    module = import_package("tracardi.process_engine.action.v1.connectors.trello.add_card_action.plugin")
    plugin_class = load_callable(module, "TrelloCardAdder")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_trello_card_remover():
    module = import_package("tracardi.process_engine.action.v1.connectors.trello.delete_card_action.plugin")
    plugin_class = load_callable(module, "TrelloCardRemover")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_trello_card_mover():
    module = import_package("tracardi.process_engine.action.v1.connectors.trello.move_card_action.plugin")
    plugin_class = load_callable(module, "TrelloCardMover")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_trello_member_adder():
    module = import_package("tracardi.process_engine.action.v1.connectors.trello.add_member_action.plugin")
    plugin_class = load_callable(module, "TrelloMemberAdder")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_amplitude_send_event():
    module = import_package("tracardi.process_engine.action.v1.connectors.amplitude.send_events.plugin")
    plugin_class = load_callable(module, "AmplitudeSendEvent")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_mongo_connector_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.mongo.query.plugin")
    plugin_class = load_callable(module, "MongoConnectorAction")
    plugin = plugin_class()
    await plugin.set_up({'collection': None, 'database': None, 'query': '{}', 'source': {'id': None}})


async def test_should_set_up_plugin_full_contact_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.full_contact.person_enrich.plugin")
    plugin_class = load_callable(module, "FullContactAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_zapier_web_hook_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.zapier.webhook.plugin")
    plugin_class = load_callable(module, "ZapierWebHookAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_pushover_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.pushover.push.plugin")
    plugin_class = load_callable(module, "PushoverAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_discord_web_hook_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.discord.push.plugin")
    plugin_class = load_callable(module, "DiscordWebHookAction")
    plugin = plugin_class()
    await plugin.set_up({'message': '', 'timeout': 10, 'url': None, 'username': None})


async def test_should_set_up_plugin_mqtt_publish_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.mqtt.publish.plugin")
    plugin_class = load_callable(module, "MqttPublishAction")
    plugin = plugin_class()
    await plugin.set_up({'payload': '{}', 'qos': '0', 'retain': False, 'source': {'id': '', 'name': ''}, 'topic': ''})


async def test_should_set_up_plugin_geo_i_p_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.maxmind.geoip.plugin")
    plugin_class = load_callable(module, "GeoIPAction")
    plugin = plugin_class()
    await plugin.set_up({'ip': 'event@metadata.ip', 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_mysql_connector_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.mysql.query.plugin")
    plugin_class = load_callable(module, "MysqlConnectorAction")
    plugin = plugin_class()
    await plugin.set_up({'data': [], 'query': 'SELECT 1', 'source': {'id': '', 'name': ''}, 'timeout': 10, 'type': 'select'})


async def test_should_set_up_plugin_postgre_s_q_l_connector_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.postgresql.query.plugin")
    plugin_class = load_callable(module, "PostgreSQLConnectorAction")
    plugin = plugin_class()
    await plugin.set_up({'query': None, 'source': {'id': '1', 'name': 'Some value'}, 'timeout': 20})


async def test_should_set_up_plugin_weather_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.weather.msn_weather.plugin")
    plugin_class = load_callable(module, "WeatherAction")
    plugin = plugin_class()
    await plugin.set_up({'city': None, 'system': 'C'})


async def test_should_set_up_plugin_aws_sqs_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.aws.sqs.plugin")
    plugin_class = load_callable(module, "AwsSqsAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_sentiment_analysis_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.sentiment_analysis.plugin")
    plugin_class = load_callable(module, "SentimentAnalysisAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_language_detect_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.language_detection.plugin")
    plugin_class = load_callable(module, "LanguageDetectAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_text_classification_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.text_classification.plugin")
    plugin_class = load_callable(module, "TextClassificationAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_token_getter():
    module = import_package("tracardi.process_engine.action.v1.connectors.oauth2_token.plugin")
    plugin_class = load_callable(module, "TokenGetter")
    plugin = plugin_class()
    await plugin.set_up({'destination': None, 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_slack_poster():
    module = import_package("tracardi.process_engine.action.v1.connectors.slack.send_message.plugin")
    plugin_class = load_callable(module, "SlackPoster")
    plugin = plugin_class()
    await plugin.set_up({'channel': None, 'message': None, 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_google_sheets_integrator_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.google.sheets.modify.plugin")
    plugin_class = load_callable(module, "GoogleSheetsIntegratorAction")
    plugin = plugin_class()
    await plugin.set_up({'range': None, 'read': False, 'sheet_name': None, 'source': {'id': '1', 'name': 'Some value'}, 'spreadsheet_id': None, 'values': '[["Name", "John"]]', 'write': False})


async def test_should_set_up_plugin_deep_categorization_plugin():
    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.deep_categorization.plugin")
    plugin_class = load_callable(module, "DeepCategorizationPlugin")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_corporate_reputation_plugin():
    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.corporate_reputation.plugin")
    plugin_class = load_callable(module, "CorporateReputationPlugin")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_topics_extraction_plugin():
    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.topics_extraction.plugin")
    plugin_class = load_callable(module, "TopicsExtractionPlugin")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_summarization_plugin():
    module = import_package("tracardi.process_engine.action.v1.connectors.meaningcloud.summarization.plugin")
    plugin_class = load_callable(module, "SummarizationPlugin")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_influx_sender():
    module = import_package("tracardi.process_engine.action.v1.connectors.influxdb.send.plugin")
    plugin_class = load_callable(module, "InfluxSender")
    plugin = plugin_class()
    await plugin.set_up({'bucket': None, 'fields': {}, 'measurement': None, 'organization': None, 'source': {'id': '1', 'name': 'Some value'}, 'tags': {}, 'time': None})


async def test_should_set_up_plugin_influx_fetcher():
    module = import_package("tracardi.process_engine.action.v1.connectors.influxdb.fetch.plugin")
    plugin_class = load_callable(module, "InfluxFetcher")
    plugin = plugin_class()
    await plugin.set_up({'aggregation': None, 'bucket': None, 'filters': {}, 'organization': None, 'source': {'id': '1', 'name': 'Some value'}, 'start': '-15m', 'stop': '0m'})


async def test_should_set_up_plugin_mix_panel_sender():
    module = import_package("tracardi.process_engine.action.v1.connectors.mixpanel.send.plugin")
    plugin_class = load_callable(module, "MixPanelSender")
    plugin = plugin_class()
    await plugin.set_up({'mapping': {}, 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_mix_panel_funnel_fetcher():
    module = import_package("tracardi.process_engine.action.v1.connectors.mixpanel.fetch_funnel.plugin")
    plugin_class = load_callable(module, "MixPanelFunnelFetcher")
    plugin = plugin_class()
    await plugin.set_up({'from_date': None, 'funnel_id': None, 'project_id': None, 'source': {'id': '1', 'name': 'Some value'}, 'to_date': None})


async def test_should_set_up_plugin_elastic_email_contact_adder():
    module = import_package("tracardi.process_engine.action.v1.connectors.elastic_email.add_contact.plugin")
    plugin_class = load_callable(module, "ElasticEmailContactAdder")
    plugin = plugin_class()
    await plugin.set_up({'additional_mapping': {}, 'email': None, 'source': {'id': None, 'name': None}})


async def test_should_set_up_plugin_elastic_email_transactional_mail_sender():
    module = import_package("tracardi.process_engine.action.v1.connectors.elastic_email.transactional_email.plugin")
    plugin_class = load_callable(module, "ElasticEmailTransactionalMailSender")
    plugin = plugin_class()
    await plugin.set_up({'message': {'content': '', 'recipient': '', 'subject': ''}, 'sender_email': '', 'source': {'id': '', 'name': ''}})


async def test_should_set_up_plugin_elastic_email_bulk_mail_sender():
    module = import_package("tracardi.process_engine.action.v1.connectors.elastic_email.bulk_email.plugin")
    plugin_class = load_callable(module, "ElasticEmailBulkMailSender")
    plugin = plugin_class()
    await plugin.set_up({'message': {'content': '', 'recipient': '', 'subject': ''}, 'sender_email': '', 'source': {'id': '', 'name': ''}})


async def test_should_set_up_plugin_mautic_contact_adder():
    module = import_package("tracardi.process_engine.action.v1.connectors.mautic.add_contact.plugin")
    plugin_class = load_callable(module, "MauticContactAdder")
    plugin = plugin_class()
    await plugin.set_up({'additional_mapping': {}, 'email': None, 'overwrite_with_blank': False, 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_mautic_contact_by_i_d_fetcher():
    module = import_package("tracardi.process_engine.action.v1.connectors.mautic.fetch_contact_by_id.plugin")
    plugin_class = load_callable(module, "MauticContactByIDFetcher")
    plugin = plugin_class()
    await plugin.set_up({'contact_id': None, 'source': {'id': None, 'name': None}})


async def test_should_set_up_plugin_mautic_contact_by_email_fetcher():
    module = import_package("tracardi.process_engine.action.v1.connectors.mautic.fetch_contact_by_email.plugin")
    plugin_class = load_callable(module, "MauticContactByEmailFetcher")
    plugin = plugin_class()
    await plugin.set_up({'contact_email': None, 'source': {'id': None, 'name': None}})


async def test_should_set_up_plugin_mautic_points_editor():
    module = import_package("tracardi.process_engine.action.v1.connectors.mautic.edit_points.plugin")
    plugin_class = load_callable(module, "MauticPointsEditor")
    plugin = plugin_class()
    await plugin.set_up({'action': None, 'contact_id': None, 'points': None, 'source': {'id': '1', 'name': 'Some value'}})


async def test_should_set_up_plugin_mautic_segment_editor():
    module = import_package("tracardi.process_engine.action.v1.connectors.mautic.add_remove_segment.plugin")
    plugin_class = load_callable(module, "MauticSegmentEditor")
    plugin = plugin_class()
    await plugin.set_up({'action': None, 'contact_id': None, 'segment': None, 'source': {'id': None, 'name': None}})


async def test_should_set_up_plugin_send_to_airtable_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.airtable.send_record.plugin")
    plugin_class = load_callable(module, "SendToAirtableAction")
    plugin = plugin_class()
    await plugin.set_up({'base_id': None, 'mapping': {}, 'source': {'id': '1', 'name': 'Some value'}, 'table_name': None})


async def test_should_set_up_plugin_fetch_from_airtable_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.airtable.fetch_records.plugin")
    plugin_class = load_callable(module, "FetchFromAirtableAction")
    plugin = plugin_class()
    await plugin.set_up({'base_id': None, 'formula': None, 'source': {'id': '1', 'name': 'Some value'}, 'table_name': None})


async def test_should_set_up_plugin_send_event_to_matomo_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.matomo.send_event.plugin")
    plugin_class = load_callable(module, "SendEventToMatomoAction")
    plugin = plugin_class()
    await plugin.set_up({'dimensions': {}, 'goal_id': None, 'rck': 'session@context.utm.term', 'rcn': 'session@context.utm.campaign', 'revenue': None, 'search_category': None, 'search_keyword': None, 'search_results_count': None, 'site_id': None, 'source': {'id': '1', 'name': 'Some value'}, 'url_ref': 'event@context.page.referer.host'})


async def test_should_set_up_plugin_add_civi_contact_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.civi_crm.add_contact.plugin")
    plugin_class = load_callable(module, "AddCiviContactAction")
    plugin = plugin_class()
    await plugin.set_up({'contact_type': 'Individual', 'fields': {}, 'source': {'id': '', 'name': ''}})


async def test_should_set_up_plugin_fetch_active_campaign_profile_by_email_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.active_campaign.fetch_by_email.plugin")
    plugin_class = load_callable(module, "FetchActiveCampaignProfileByEmailAction")
    plugin = plugin_class()
    await plugin.set_up({'email': None, 'source': {'id': None, 'name': None}})


async def test_should_set_up_plugin_send_to_active_campaign_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.active_campaign.add_contact.plugin")
    plugin_class = load_callable(module, "SendToActiveCampaignAction")
    plugin = plugin_class()
    await plugin.set_up({'fields': {}, 'source': {'id': None, 'name': None}})


async def test_should_set_up_plugin_data_extension_sender():
    module = import_package("tracardi.process_engine.action.v1.connectors.salesforce.marketing_cloud.send.plugin")
    plugin_class = load_callable(module, "DataExtensionSender")
    plugin = plugin_class()
    await plugin.set_up({'extension_id': None, 'mapping': {}, 'source': {'id': '', 'name': ''}, 'update': False})


async def test_should_set_up_plugin_notification_generator_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.novu.plugin")
    plugin_class = load_callable(module, "NotificationGeneratorAction")
    plugin = plugin_class()
    await plugin.set_up({'payload': '{}', 'recipient_email': 'profile@pii.email', 'source': {'id': '', 'name': ''}, 'subscriber_id': 'profile@id', 'template_name': None})


async def test_should_set_up_plugin_assign_profile_id_action():
    module = import_package("tracardi.process_engine.action.v1.internal.assign_profile_id.plugin")
    plugin_class = load_callable(module, "AssignProfileIdAction")
    plugin = plugin_class()
    await plugin.set_up({'value': ''})


async def test_should_set_up_plugin_event_source_fetcher_action():
    module = import_package("tracardi.process_engine.action.v1.internal.event_source_fetcher.plugin")
    plugin_class = load_callable(module, "EventSourceFetcherAction")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_inject_event():
    module = import_package("tracardi.process_engine.action.v1.internal.inject_event.plugin")
    plugin_class = load_callable(module, "InjectEvent")
    plugin = plugin_class()
    await plugin.set_up({'event_id': None})


async def test_should_set_up_plugin_inject_profile():
    module = import_package("tracardi.process_engine.action.v1.internal.inject_profile.plugin")
    plugin_class = load_callable(module, "InjectProfile")
    plugin = plugin_class()
    await plugin.set_up({'query': ''})


async def test_should_set_up_plugin_add_empty_profile_action():
    module = import_package("tracardi.process_engine.action.v1.internal.add_empty_profile.plugin")
    plugin_class = load_callable(module, "AddEmptyProfileAction")
    plugin = plugin_class()
    await plugin.set_up({})


async def test_should_set_up_plugin_previous_event_getter():
    module = import_package("tracardi.process_engine.action.v1.internal.get_prev_event.plugin")
    plugin_class = load_callable(module, "PreviousEventGetter")
    plugin = plugin_class()
    await plugin.set_up({'event_type': {'id': '@current', 'name': '@current'}, 'offset': -1})


async def test_should_set_up_plugin_find_previous_session_action():
    module = import_package("tracardi.process_engine.action.v1.internal.get_prev_session.plugin")
    plugin_class = load_callable(module, "FindPreviousSessionAction")
    plugin = plugin_class()
    await plugin.set_up({'offset': -1})


async def test_should_set_up_plugin_count_records_action():
    module = import_package("tracardi.process_engine.action.v1.internal.query_string.plugin")
    plugin_class = load_callable(module, "CountRecordsAction")
    plugin = plugin_class()
    await plugin.set_up({'index': None, 'query': '', 'time_range': None})


async def test_should_set_up_plugin_add_empty_session_action():
    module = import_package("tracardi.process_engine.action.v1.internal.add_empty_session.plugin")
    plugin_class = load_callable(module, "AddEmptySessionAction")
    plugin = plugin_class()
    await plugin.set_up({})


async def test_should_set_up_plugin_entity_upsert_action():
    module = import_package("tracardi.process_engine.action.v1.internal.entity.upsert.plugin")
    plugin_class = load_callable(module, "EntityUpsertAction")
    plugin = plugin_class()
    await plugin.set_up({'id': None, 'properties': '{}', 'reference_profile': True, 'traits': '{}', 'type': ''})


async def test_should_set_up_plugin_entity_load_action():
    module = import_package("tracardi.process_engine.action.v1.internal.entity.load.plugin")
    plugin_class = load_callable(module, "EntityLoadAction")
    plugin = plugin_class()
    await plugin.set_up({'id': None, 'reference_profile': True, 'type': {'id': '', 'name': ''}})


async def test_should_set_up_plugin_entity_delete_action():
    module = import_package("tracardi.process_engine.action.v1.internal.entity.delete.plugin")
    plugin_class = load_callable(module, "EntityDeleteAction")
    plugin = plugin_class()
    await plugin.set_up({'id': '', 'reference_profile': True, 'type': {'id': '', 'name': ''}})


async def test_should_set_up_plugin_get_report_action():
    module = import_package("tracardi.process_engine.action.v1.internal.get_report.plugin")
    plugin_class = load_callable(module, "GetReportAction")
    plugin = plugin_class()
    await plugin.set_up({'report_config': {'params': '{}', 'report': {'id': '', 'name': ''}}})


async def test_should_set_up_plugin_create_response_action():
    module = import_package("tracardi.process_engine.action.v1.internal.add_response.plugin")
    plugin_class = load_callable(module, "CreateResponseAction")
    plugin = plugin_class()
    await plugin.set_up({'body': '{}', 'default': True, 'key': ''})


async def test_should_set_up_plugin_key_counter_action():
    module = import_package("tracardi.process_engine.action.v1.metrics.key_counter.plugin")
    plugin_class = load_callable(module, "KeyCounterAction")
    plugin = plugin_class()
    await plugin.set_up({'key': None, 'save_in': None})


async def test_should_set_up_plugin_microservice_action():
    module = import_package("tracardi.process_engine.action.v1.microservice.plugin")
    plugin_class = load_callable(module, "MicroserviceAction")
    plugin = plugin_class()
    await plugin.set_up({})


async def test_should_set_up_plugin_consent_adder():
    module = import_package("tracardi.process_engine.action.v1.consents.add_consent_action.plugin")
    plugin_class = load_callable(module, "ConsentAdder")
    plugin = plugin_class()
    await plugin.set_up({'consents': None})


async def test_should_set_up_plugin_require_consents_action():
    module = import_package("tracardi.process_engine.action.v1.consents.require_consents_action.plugin")
    plugin_class = load_callable(module, "RequireConsentsAction")
    plugin = plugin_class()
    await plugin.set_up({'consent_ids': [], 'require_all': False})


async def test_should_set_up_plugin_scheduler_plugin():
    module = import_package("tracardi.process_engine.action.v1.pro.scheduler.plugin")
    plugin_class = load_callable(module, "SchedulerPlugin")
    plugin = plugin_class()
    await plugin.set_up(None)


async def test_should_set_up_plugin_rabbit_publisher_action():
    module = import_package("tracardi.process_engine.action.v1.connectors.rabbitmq.publish.plugin")
    plugin_class = load_callable(module, "RabbitPublisherAction")
    plugin = plugin_class()
    await plugin.set_up({'queue': {'auto_declare': True, 'compression': None, 'name': None, 'queue_type': 'direct', 'routing_key': None, 'serializer': 'json'}, 'source': {'id': None}})


async def test_should_set_up_plugin_postpone_event_action():
    module = import_package("tracardi.process_engine.action.v1.flow.postpone_event.plugin")
    plugin_class = load_callable(module, "PostponeEventAction")
    plugin = plugin_class()
    await plugin.set_up(None)
