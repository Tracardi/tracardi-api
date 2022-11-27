import asyncio

from tracardi.domain.entity import Entity
from tracardi.service.storage.driver import storage


def test_should_save_data_via_driver():
    class TestEntityInfo(Entity):
        version: str

    async def async_main():
        entity = TestEntityInfo(id="abc", version="test")
        result = await storage.driver.version.save(entity)
        assert result.saved == 1

    loop = asyncio.new_event_loop()
    loop.run_until_complete(async_main())
    loop.close()
