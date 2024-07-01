# Merging

There are two types of merging processes.

* **[Automatic Profile Merging](apm.md)**: Automatic profile merging in Tracardi is a process designed to unify multiple profiles
  that represent the same user. Merging is a background process that looks for the profiles wth the same merging key,
  e.g. email.
* **[Identification Points](../definitions/identification_point.md)**: This a realtime process that merges profiles when
  a defined event was sent e.g. `Identification` and it contains data that can be used for mering.

### Example of Profile Merging

1. **Initial Interaction**:
    - A user visits a website and signs up with the email address `user@example.com`. Tracardi creates `profile-id-123`
      for this user.

2. **Subsequent Interaction on a Different Device**:
    - The same user visits the website on a different device and signs up again with the same email
      address `user@example.com`. Tracardi creates a new `profile-id-456`.

3. **[Identification Point](../definitions/identification_point.md) Match**:
    - If the [Identification point](../definitions/identification_point.md) is created for a `sign up` event then
      Tracardi detects that both profiles have the same email address. It identifies this as a match and proceeds to
      merge `profile-id-456` into `profile-id-123`.
    - If there is no identification point for this event, two profiles with the same email will be detected with the
      [Automatic Profile Merging](apm.md) (APM) and the profile will be merged.

4. **Data Merging**:
    - The system combines the data from both profiles, updating `profile-id-123` with any new information
      from `profile-id-456` and retaining all historical data.Is updates events and sessions to link to the new merged profile.

5. **[Conflict Resolution](merging_strategy.md)**:
    - Conflicting data inf profiles is resolved using predefined set of merging strategies. For example there are 3 different lastnames in the profile. 

5. **Unified Profile**:
    - The final unified profile under `profile-id-123` now contains data from both interactions, providing a complete
      view of the user's behavior and attributes across both devices.

## Why my profile ID in the response from Tracardi is different from the one I have sent?

The profile ID you send in the tracker payload might be different in the response from Tracardi due to several reasons
related to identity resolution, merging profiles, or system updates. Here are the key reasons why this might happen:

1. **[Identity Resolution](identity_resolution.md)**:
    - Tracardi performs identity resolution to merge profiles with matching identifiers (like email or phone number). If
      the system detects that the profile you sent should be merged with an existing profile, it will return the ID of
      the merged profile.

2. **[Profile Merging](merging.md)**:
    - When Tracardi background processed identifies that two profile should be combined with an existing one, it creates
      a unified profile. As a result, the returned profile ID will reflect the consolidated profile rather than the one
      originally sent.

3. **Session-Based Profile Retrieval**:
    - If the session information provided in the payload is linked to a different profile, Tracardi might return the
      profile ID associated with that session. This ensures continuity in tracking user activities across sessions. This
      usually happens when the Profile ID is corrupted.

4. **New Profile Creation**:
    - In some cases, if the profile information sent in the payload does not match any existing profiles or the system
      is configured to automatically create new profile for not existing ones then a new profile will be created, and
      the response will include a newly generated profile ID.

5. **Data Consistency and Updates**:
    - Tracardi continuously updates and maintains profiles based on the latest interactions and data. If there have been
      changes or updates to the profile since the payload was sent, the response might reflect the most current profile
      ID.

### Example Scenarios

- **Scenario 1: Identity Resolution**
    - You send a payload with `profile-id-abc123` and an email. Tracardi identifies that this email already exists
      under `profile-id-def456`. The system merges the profiles and returns `profile-id-def456`.

- **Scenario 2: Session Linking**
    - You send a payload with a session ID `session-id-1` that was originally associated with `profile-id-xyz789`. The
      system returns `profile-id-xyz789` to maintain session continuity.

- **Scenario 3: New Profile Creation**
    - You send a payload with an unknown profile ID. Tracardi creates a new profile and returns the new profile ID
      generated for this interaction.

#### Profile ID maintenance

The above scenarios show that your client software should always save the newest returned profile ID. If the Profile ID
changes it is a sign that the client should update the local Profile ID.