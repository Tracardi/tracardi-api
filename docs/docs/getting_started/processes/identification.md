# Profile Identification

Identification is a process of loading the correct profile from the system database. To do so Tracardi maintains various
types of IDs in the profile record. Here are the types of IDs and their purposes:

* **Client Profile ID (`profile.id`)**: This is the main identifier for each profile. This ID is usually originated by
  the client (browser). It is the ID that should be saved on the client. It represents a single user within the system.
  Note that this ID may change after profile merging because several profiles are merged and one **Client Profile ID**
  should be selected.

* **Primary ID (`profile.primary_id`)**: This is the unique Profile ID across the entire system and event sources. It
  must be delivered by an external system that serves as an authority to identify the customer. For example, this could
  be an Authorization Service that returns a profile ID after the user signs in. The Primary ID could also be computed
  based on a global
  value that identifies the customer, such as an email, phone number, or another unique identifier.

* **Previous or Other Profile IDs (`profile.ids`)**: These are additional IDs that might have been associated with the
  same user from different sources or previous instances of the profile saved on different devices. They help in
  maintaining continuity and consistency when profiles are
  identified. This allows the profile to be identified when the device has an old ID and was never updated after the
  profile was merged. When profiles are merged, the individual profile IDs are moved to the `profile.ids` field of the
  merged profile, and a new Client Profile ID is selected from these IDs. Notice that Client Profile ID and Primary ID
  are included in the `profile.ids`.

## How Tracardi Uses the IDs

When a tracker payload is sent to Tracardi, it contains the Client Profile ID. Tracardi first looks up the profile in the database. The system searches for the profile that either has `profile.id` equal to the profile ID from the tracker payload or has this ID in `profile.ids`. Once the profile is found, it is loaded, and new data is appended. This way, when the profile is correctly identified, no merging is needed.
!!! Note

    The `profile.ids` field contains all historical IDs (including the Primary ID), allowing the profile to be identified by any historical ID.

## How the System Selects the Primary ID

The Primary ID feature is available from version 0.9.0. In a distributed system where there is no single Authorization
Service, the concept of the Primary ID differs from widely used definitions. In Tracardi, the Primary ID can be empty,
which means there was no data that could identify the profile across all sources. There is a system setting that tells
Tracardi which field from the profile schema is selected to be the Primary ID. When this field is filled the Primary ID
is also filled.

!!! Note

    The environment variable `PRIMARY_ID` defines which field to use as the Primary ID. This could be data from `data.identifier.pk` or a business email from `data.contact.email.business`. Additionally, we can specify whether the Primary ID should be a hash of the field value using the `PRIMARY_ID_AS_HASH` environment variable.

## Merging

When system detects that some of the profile fields which are set to be merging key are changed it marks profile for merging. This process is called [Automatic Profile Merging](apm.md). 