# How the profile is loaded?

To load a profile, two identifiers are used: session_id and profile_id. Both of them are optional, so we have four
different loading scenarios:

1. If the session exists and the profile exists in the Tracardi database, both the profile and the session are loaded
   from the database.
2. If the session exists but the profile does not exist in the database, a new profile is created and saved to the
   database, and the existing session is loaded.
3. If the session does not exist but the profile already exists in the database, the existing profile is loaded, and a
   new session is created and saved in the database.
4. If neither the session nor the profile exists, then both the session and the profile are created and saved in the
   database.

Error scenarios that may occur:

1. Session and profile are defined, but the profile does not exist in the database. The result of this operation is that
   the saved session in the database will reference the old profile, which will be restored.
2. Session and profile are defined, but the session does not exist in the database. The result of this operation is that
   a new session will be created.
3. Session and profile are defined. The session does not exist in the database, and although the profile is defined, it
   also does not exist in the database. Attempt to fake the profile ID. The result of this operation is that a new
   session and a new profile will be created.

Device Fingerprinting:

Device Fingerprinting is activated when using the "Javascript integration" event source. This means that when
integrating with JavaScript, actions related to Device Fingerprinting are performed to identify a unique device (e.g.,
computer, phone) used by the user. The identification is based on device characteristics and behaviors, such as the
browser, screen resolution, operating system version, and more.

Matching customers based on device fingerprint is restricted by the customer's IP address and the time they access the
system. If the device, IP address, and time range match, the customer will be associated with the same profile, even if
the new webpage does not have the customer's profile ID saved. This ensures that the system can still correctly
recognize and link the customer's data based on the matching device fingerprint, IP address, and time range, even if the
profile ID is not available.

Moreover, if the customer visits a new page that already has a profile ID from their previous browsing session, the
system will match the customer with the saved profile ID. The system will not merge the profiles unless the event source
is configured to allow merging using the device fingerprint. In other words, if there is an existing profile ID
associated with the customer, the system will prioritize using that ID instead of merging it with the device
fingerprint, unless the event source specifically permits merging based on the device fingerprint. This approach ensures
better control and accuracy in associating customer data and prevents unintended merging of profiles when it is not
desired.