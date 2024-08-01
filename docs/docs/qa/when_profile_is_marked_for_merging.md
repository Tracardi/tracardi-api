# When profiles are marked for merging?

In Tracardi, profiles are "marked for merging" when certain conditions are met, indicating that multiple profiles
should be consolidated into a single profile. Here’s a more detailed explanation:

## Profiles Marked for Merging

Tracardi monitors the specified fields (e.g., email addresses, phone numbers) for changes or updates. If it finds that
one of the field that is marked as merging key is changed, it "marks" the profile as candidates for merging.

## What are the merging keys (fields)

- The following profile fields are used as merging keys:
  - `data.contact.email.main`
  - `data.contact.email.business`
  - `data.contact.email.private`
  - `data.contact.phone.main`
  - `data.contact.phone.business`
  - `data.contact.phone.whatsapp`
  - `data.contact.phone.mobile`

## When Profiles are Marked for Merging

Profiles are typically marked for merging under the following conditions:

1. **Matching Fields Updates**:
    - When Tracardi detects that the values in the merging key fields (such as email addresses or phone numbers) have
      changed.

2. **Profile Creation/Update**:
    - Whenever a new profile is created or an existing profile is updated with data in the monitored fields.

3. **Periodic Checks**:
    - The APM worker periodically reviews profiles to identify if there are profile duplicates that have the same values
      for merging keys.

## Example Workflow

1. **Profile Update**:
    - A user updates their email address in their profile. The system hashes the new email value and puts it
      into `profile.ids`.

2. **Mark for Merging**:
    - System marks this profile for merging. This can be see in the GUI togather with the estimated number of profiles
      to merge.

3. **APM Worker**:
    - The APM worker runs at regular intervals, reviewing profiles marked for merging. It merges the profiles,
      consolidating all data into a single profile.
4. **Watch Dog Process**:
    - A Watch Dog process runs periodically (by default every 15 minutes) to ensure there are no missing hashes in
      the `profile.ids` field. This means it checks for the presence of emails or phone numbers without corresponding
      hashes in `profile.ids`. If any missing hashes are found, they are computed and added to `profile.ids`.
      Subsequently, the regular APM Worker merges the profiles.
