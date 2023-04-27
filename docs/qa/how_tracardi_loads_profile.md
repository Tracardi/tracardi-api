# How tracardi loads profile

Tracardi utilizes ID to identify profiles, with each profile having a unique identifier. When there is only one profile
per user, loading is performed through a simple query that matches the ID to the given ID. However, since Tracardi
gathers data from multiple sources and channels, passing the product ID to each of them may not always be feasible.
Hence, during the initial data collection phase when the user is anonymous, multiple profiles belonging to the same user
are stored in Tracardi. When linking profiles, all profile IDs are copied to the `IDS` field, and loading is executed by
checking whether the given ID corresponds to any of the IDs stored in the `ids` field. Despite having an `ID` field, the
possibility of outdated IDs on certain devices necessitates the use of the `ids` field during loading. This approach
enables Tracardi to merge profiles from external systems by simply adding the external system's profile ID to the `ids`
field, which can then be used to load the profile.

```json title="Example of profile data"
{
  "id": "22082393-4b65-4add-a2e1-7a6982a79d0d",
  "ids": [
    "22082393-4b65-4add-a2e1-7a6982a79d0d",
    "79d07a66-a2e1-4a44-5b65-22082393a2e1"
  ],
  ...
}
```