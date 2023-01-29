import asyncio

from time import sleep

from tracardi.service.value_threshold_manager import ValueThresholdManager


async def _should_save_and_load_value_threshold():
    vtm = ValueThresholdManager(node_id=1, profile_id=2, name="test_threshold", ttl=0, debug=True)
    result = await vtm.save_current_value(current_value=1)
    assert result is True

    record = await vtm.load_last_value()
    assert record is not None
    assert record.name == "test_threshold"
    assert record.last_value == 1
    assert record.ttl == 0

    await vtm.delete()


async def _should_pass_threshold_once():
    vtm = ValueThresholdManager(node_id=1, profile_id=2, name="test_threshold", ttl=0, debug=True)
    last_value = await vtm.load_last_value()
    assert last_value is None
    results = [await vtm.pass_threshold(x) for x in [1, 1, 1, 1]]
    assert results == [True, False, False, False]
    await vtm.delete()


async def _should_pass_threshold_with_every_change():
    vtm = ValueThresholdManager(node_id=1, profile_id=2, name="test_threshold", ttl=0, debug=True)
    await vtm.delete()
    assert await vtm.load_last_value() is None
    results = [await vtm.pass_threshold(x) for x in [1, 1, 2, 1, 1, 1, -1, 2]]
    assert results == [True, False, True, True, False, False, True, True]
    await vtm.delete()


async def _should_pass_threshold_once_on_object():
    vtm = ValueThresholdManager(node_id=1, profile_id=2, name="test_threshold", ttl=0, debug=True)
    await vtm.delete()
    assert await vtm.load_last_value() is None
    results = [await vtm.pass_threshold(x) for x in
               [{"a": {"b": 1}}, {"a": {"b": 1}}, {"a": {"b": 2}}, {"a": {"b": 2}}]]
    assert results == [True, False, True, False]
    await vtm.delete()


async def _should_pass_threshold_once_on_condition():
    vtm = ValueThresholdManager(node_id=1, profile_id=2, name="test_threshold", ttl=0, debug=True)
    await vtm.delete()
    assert await vtm.load_last_value() is None
    results = [await vtm.pass_threshold(x) for x in
               ["a" == "a", "a" != "a", "a" == "a", "a" == "a"]]
    assert results == [True, True, True, False]
    await vtm.delete()


async def _should_pass_threshold_after_ttl():
    vtm = ValueThresholdManager(node_id=1, profile_id=2, name="test_threshold", ttl=1, debug=True)
    await vtm.delete()
    assert await vtm.load_last_value() is None
    assert await vtm.pass_threshold("1") is True
    assert await vtm.pass_threshold("1") is False
    sleep(2)
    assert await vtm.pass_threshold("1") is True
    await vtm.delete()


def test_value_threshold():
    async def main():
        await _should_save_and_load_value_threshold()
        await _should_pass_threshold_once()
        await _should_pass_threshold_with_every_change()
        await _should_pass_threshold_once_on_object()
        await _should_pass_threshold_once_on_condition()
        await _should_pass_threshold_after_ttl()

    asyncio.new_event_loop().run_until_complete(main())
