import asyncio
from uuid import uuid4
from tracardi.domain.profile import Profile
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor
from tracardi_tests.utils.utils import Endpoint

endpoint = Endpoint()


async def create_profile(profile_id):
    result = await StorageFor(Profile(id=profile_id)).index().save()
    assert result.saved == 1
    await storage.driver.profile.refresh()
    return result


async def delete_profile(profile_id):
    result = await StorageFor(Profile(id=profile_id)).index().delete()
    return result['deleted'] == 1


def test_get_profile():
    profile_id = str(uuid4())
    assert endpoint.get(f'/profile/{profile_id}').status_code == 404

    asyncio.run(create_profile(profile_id))

    assert endpoint.get(f'/profile/{profile_id}').status_code == 200

