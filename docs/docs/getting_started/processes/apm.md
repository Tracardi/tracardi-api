# Automatic Profile Merging (APM) Documentation

Automatic Profile Merging (APM) is the process of merging user profiles in Tracardi. This feature ensures that all data
related to a user is consolidated into a single profile. APM operates as a background process, merging profiles when
specific predefined fields, known as merging keys, contain matching data.

## Key Steps in Automatic Profile Merging

* **Data Collection and [Profile Identification](identification.md)**:
    - When a user interacts with a website or app, Tracardi collects data and creates a new profile if one does not
      already exist.
    - Each profile has a unique Profile ID.

* **Profile Matching**:
    - Tracardi continuously monitors changes in the profile fields designated as merging keys.
    - When a change is detected in these fields, the system identifies profiles that need merging.

* **Merging Profiles**:
    - Upon finding a match, Tracardi automatically merges the new profile data with the existing profile.
    - **Combining Attributes and Traits**: Profile data is merged according to the defined merging strategy for each
      field.
    - **Updating the Existing Profile**: The existing profile is updated with new data from the incoming profile.
    - **Retaining Historical Data**: All events and sessions are updated and accurately reflected in the merged profile.
    - **Maintaining All Profile IDs**: The Profile IDs from the individual profiles are moved to the `profile.ids` field
      in the merged profile. A new primary ID is then selected from the available `profile.ids`. This new primary ID
      will be returned in the Tracardi response.

* **Handling Conflicts**:
    - During the merge, if there are conflicting data points (e.g., different values for the same attribute), Tracardi
      follows predefined rules to resolve these conflicts.
    - Typically, the most recent data or the data deemed most reliable is retained.

* **Profile Consolidation**:
    - The merged profile now represents a comprehensive view of the user, consolidating data from all matched profiles.
    - This unified profile gets a new Profile ID and is saved in the database.

## Details

* **Merging Keys**:
    - Tracardi uses predefined fields as **merging keys** to identify profiles that should be merged. These fields typically
      include:
        - Email addresses (`data.contact.email.main`, `data.contact.email.business`, `data.contact.email.private`)
        - Phone
          numbers (`data.contact.phone.main`, `data.contact.phone.business`, `data.contact.phone.whatsapp`, `data.contact.phone.mobile`)
        - Identifiers (`data.identifier.pk`, `data.identifier.id`)

* **Merging Process**:
    - Profiles flagged for merging (it happens when a change in a **merging key** is noticed) are processed by a background
      worker.
    - This worker consolidates the profiles, moving the profile IDs from the individual profiles fields into the `profile.ids`
      field of the merged profile as hashed values.
    - A new client ID is selected from the available `profile.ids`, and this new ID is returned in the Tracardi
      response.

* **Profile IDs Management**:
    - The generated IDs that are stored in the `profile.ids` field have specific prefixes to indicate their origin:
        - `emm-` hash from main email (`data.contact.email.main`)
        - `emb-` hash from business email (`data.contact.email.business`)
        - `emp-` hash from private email (`data.contact.email.private`)
        - `phm-` hash from main phone (`data.contact.phone.main`)
        - `phw-` hash from WhatsApp phone (`data.contact.phone.whatsapp`)
        - `phb-` hash from business phone (`data.contact.phone.business`)
        - `pho-` hash from mobile phone (`data.contact.phone.mobile`)
        - `ipk-` hash from `data.identifier.pk`
        - `iid-` hash from `data.identifier.id`

## Enabling Auto Profile Merging

* **Add Environment Parameter**:
    - Add the `AUTO_PROFILE_MERGING` environment parameter with a key of at least 20 characters when starting the
      Tracardi API (include it in the Docker command).
    - This key is used as salt when hashing emails and phone numbers.

* **Enable Unique ID Generation**:
    - Enabling the `AUTO_PROFILE_MERGING` parameter also automatically enables the generation and storage of unique IDs
      for every email address processed by the system.
