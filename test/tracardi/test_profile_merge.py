import asyncio
from pprint import pprint

from tracardi.domain.pii import PII
from tracardi.domain.profile import Profile
from tracardi.domain.profile_traits import ProfileTraits
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import storage_manager


def test_profile_merging():
    async def async_main():
        profile = Profile(id="1",
                          pii=PII(
                              email="test@test.com"
                          ),
                          traits=ProfileTraits(
                              private={
                                  "email": "john@test.com",
                                  "Name": "John Marble"
                              },
                              public={
                                  "married": True,
                                  "list_of_values": [1, 2, 3]
                              }
                          ))

        await storage.driver.profile.save_profile(profile, refresh_after_save=True)

        profile = Profile(
            id="2",
            pii=PII(
                email="test@test.com"
            ),
            traits=ProfileTraits(
                private={
                    "email": "test@test.com",
                    "Name": "Johny Marble"
                }
            ))

        await storage.driver.profile.save_profile(profile, refresh_after_save=True)

        profile = Profile(id="3", traits=ProfileTraits(private={
            "email": "other@test.com",
            "Name": "Johny Marble"
        }))

        await storage.driver.profile.save_profile(profile, refresh_after_save=True)

        await storage.driver.profile.refresh()

        await storage_manager('profile').query({'size': 2000, 'query': {'term': {'pii.email': 'test@test.com'}}})

        # -------------------------
        # TEST no override on data

        profile = Profile(
            id="4",
            pii=PII(
                email="test@test.com"
            ),
            traits=ProfileTraits(
                private={
                    "email": "test@test.com",
                    "Name": "Ian Marble"
                },
                public={
                    "list_of_values": [3, 4]
                }
            )
        )

        # profile.operation.merge = ['profile@traits.private.email']
        profile.operation.merge = ['profile@pii.email']

        profiles = await profile.merge(storage.driver.profile.load_profiles_to_merge, override_old_data=False)

        # Merged profile mut be the first one
        assert {profiles[0].id, profiles[1].id} == {'1', '2'}
        assert profiles[0].metadata.merged_with == profile.id
        assert profiles[1].metadata.merged_with == profile.id

        # Profile id 4 must be mutated
        assert profile.id == '4'
        assert profile.metadata.merged_with is None
        assert isinstance(profile.traits.private['Name'], list) and set(profile.traits.private['Name']) == {
            'Ian Marble', 'John Marble', 'Johny Marble'}
        assert isinstance(profile.traits.private['email'], list) and set(profile.traits.private['email']) == {
            'john@test.com', 'test@test.com'}
        assert profile.traits.public['married'] is True
        assert profile.traits.public['list_of_values'] == [1, 2, 3, 4]

        # -------------------------
        # TEST data override

        profile = Profile(
            id="4",
            pii=PII(
                email="test@test.com"
            ),
            traits=ProfileTraits(
                private={
                    "email": "test@test.com",
                    "Name": "Ian Marble"
                },
                public={
                    "list_of_values": [3, 4]
                }
            )
        )

        # profile.operation.merge = ['profile@traits.private.email']
        profile.operation.merge = ['profile@pii.email']

        profiles = await profile.merge(storage.driver.profile.load_profiles_to_merge, override_old_data=True)

        # Merged profile mut be the first one
        assert {profiles[0].id, profiles[1].id} == {'1', '2'}
        assert profiles[0].metadata.merged_with == profile.id
        assert profiles[1].metadata.merged_with == profile.id

        # Profile id 4 must be mutated
        assert profile.id == '4'
        assert profile.metadata.merged_with is None
        assert profile.traits.private['Name'] == "Ian Marble"
        assert profile.traits.private['email'] == "test@test.com"
        assert profile.traits.public['married'] is True
        assert profile.traits.public['list_of_values'] == [3, 4]

    loop = asyncio.new_event_loop()
    loop.run_until_complete(async_main())
    loop.close()
