Tracardi is a data collection platform that utilizes unique identifiers to identify user profiles. When there is only
one profile per user, loading is performed through a simple query that matches the ID to the given ID. However, when
multiple profiles belonging to the same user are stored in Tracardi, the `ids` field is used to check whether the given
ID corresponds to any of the IDs stored in the `ids` field. This approach enables Tracardi to merge profiles from
external systems by simply adding the external system's profile ID to the `ids` field, which can then be used to load
the profile. Additionally, the `ids` field is used to account for the possibility of outdated IDs on certain devices. An
example of profile data is provided in the documentation, which includes the `id` and `ids` fields.