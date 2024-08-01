# How profile is restored? Why my tracardi profile is restored even if I deleted it from the localStorage in browser.

The restoration of a profile in Tracardi, even after deleting it from localStorage, can occur due to a synchronization
between the client-side and the server. If the tracker payload sent to Tracardi does not provide a profile ID, or
if the profile ID provided does not exist in Tracardi's database, the system will create a new profile ID.

Additionally, if a valid previous session is provided but the profile ID is not, Tracardi will attempt to search for the
lost profile by matching the last valid session and return the correct profile ID (restore the profile). It's crucial to
synchronize the
profile ID returned in the response with the profile ID saved on the client side. If the profile ID in the response is
different from the one sent, the client should update its profile ID and include the new one in the next call to
Tracardi. Failing to synchronize these IDs may result in the profile ID being recreated with each call to the /track
API, potentially causing issues with tracking and profiling of customer behavior.

SO the answer to the question is:

To completely delete a profile ID reference, it is necessary to delete not only the profile ID from local storage
but also the session ID from cookies. Tracardi is capable of recreating a profile from the session ID, which explains
why profiles are sometimes restored even after the profile ID is deleted from local storage.

# Browser fingerprint

Additionally, the commercial version of Tracardi might employ browser fingerprinting to identify profiles. This means
that even removing cookies, session, and profile IDs from localStorage won't prevent Tracardi from restoring the correct
profile ID. In such cases, changing your IP or browser may be necessary to completely evade profile restoration.
