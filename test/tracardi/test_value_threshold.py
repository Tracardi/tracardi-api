from tracardi.process_engine.action.v1.operations.threshold.service.value_threshold_manager import ValueThresholdManager


async def test_should_save_and_load_value_threshold():
    vtm = ValueThresholdManager(node_id=1, profile_id=2, name="test_threshold", default_value=0, ttl=3)
    result = await vtm.save_current_value(current_value=1)
    assert result.saved == 1

    record = await vtm.load_last_value()
    assert record.name == "test_threshold"
    assert record.last_value == 1
    assert record.default_value == 0
    assert record.ttl == 3

    await vtm.delete()


async def test_should_should_pass_threshold_once():
    vtm = ValueThresholdManager(node_id=1, profile_id=2, name="test_threshold", default_value=0, ttl=3)
    await vtm.delete()
    assert await vtm.load_last_value() is None
    results = [await vtm.pass_threshold(x) for x in [1, 1, 1, 1]]
    assert results == [True, False, False, False]
    await vtm.delete()


async def test_should_should_pass_threshold_with_every_change():
    vtm = ValueThresholdManager(node_id=1, profile_id=2, name="test_threshold", default_value=0, ttl=3)
    await vtm.delete()
    assert await vtm.load_last_value() is None
    results = [await vtm.pass_threshold(x) for x in [1, 1, 2, 1, 1, 1, -1, 2]]
    assert results == [True, False, True, True, False, False, True, True]
    await vtm.delete()


async def test_should_should_pass_threshold_once_on_object():
    vtm = ValueThresholdManager(node_id=1, profile_id=2, name="test_threshold", default_value=0, ttl=3)
    await vtm.delete()
    assert await vtm.load_last_value() is None
    results = [await vtm.pass_threshold(x) for x in
               [{"a": {"b": 1}}, {"a": {"b": 1}}, {"a": {"b": 2}}, {"a": {"b": 2}}]]
    assert results == [True, False, True, False]
    await vtm.delete()


async def test_should_should_pass_threshold_once_on_condition():
    vtm = ValueThresholdManager(node_id=1, profile_id=2, name="test_threshold", default_value=0, ttl=3)
    await vtm.delete()
    assert await vtm.load_last_value() is None
    results = [await vtm.pass_threshold(x) for x in
               ["a" == "a", "a" != "a", "a" == "a", "a" == "a"]]
    assert results == [True, True, True, False]
    await vtm.delete()
