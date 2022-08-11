import asyncio

from tracardi.domain.entity import Entity
from tracardi.domain.value_object.storage_info import StorageInfo
from tracardi.service.storage.factory import StorageFor


def test_should_save_data_when_has_storage_info():
    class TestEntityInfo(Entity):
        version: str

        @staticmethod
        def storage_info() -> StorageInfo:
            return StorageInfo(
                'version',
                TestEntity,
                multi=False
            )

    class TestEntity(Entity):
        version: str

    async def async_main():
        entity = TestEntityInfo(id="abc", version="test")
        result = await StorageFor(entity).index().save()
        assert result.saved == 1

        entity = TestEntity(id="abc", version="test")
        result = await StorageFor(entity).index("version").save(entity)
        assert result.saved == 1

    loop = asyncio.new_event_loop()
    loop.run_until_complete(async_main())
    loop.close()
