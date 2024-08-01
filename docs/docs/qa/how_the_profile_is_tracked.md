# How the profile is tracked?

In Tracardi, customer tracking and identity resolution are done through a combination of profile IDs and session IDs.
Here's a detailed explanation:

1. Profile ID and Session ID Storage:

* The Profile ID and Session ID are key components in tracking a customer's journey.
* The Profile ID is stored in the local storage of a user's browser.
* The Session ID, representing a visit, is stored in the browser's cookies.

2. Session Creation and Management:

* A session is initiated when a browser is opened and is terminated when it's closed. A new session is created upon
  reopening the browser.
* The Session ID remains constant throughout a browser session.
* In mobile applications, the session ID can be controlled more flexibly, for instance, by generating a new Session ID
  each time the app is opened or when certain events (like logging out) occur.

3. Profile Creation Across Different Browsers:

* Customers might use multiple browsers (e.g., one at home and another at work), leading to the creation of different
  Profile IDs for each browser.
* Each action or click by the customer is tracked as an event and linked to the respective Profile ID and Session ID.

4. Profile Merging and Identity Resolution:

* An important aspect of Tracardi's tracking system is the ability to merge profiles.
* When a customer is identified (e.g., through an email address) across different browsers or devices, Tracardi merges
  these profiles into a single profile.
* This merging process copies data from all detected profiles (say Profile A, B, and others) into one (say Profile B).
* After merging, while the Session IDs remain unique to each visit, the Profile ID becomes uniform across all browsers
  and devices.
* However, each profile still retains multiple IDs because these IDs cannot be replaced on devices not currently in use.

5. Handling Multiple Profile IDs:

* Even after merging, the old Profile IDs are still relevant.
* When a customer accesses the service from a device using an old Profile ID, Tracardi uses this ID to find the current
  profile and then updates the device with the new Profile ID.

6. Simplified Overview:

* Sessions represent visits: Each browser session or app use is tracked with a unique Session ID.
* Profiles represent the customer: Different Profile IDs created across devices or browsers are merged upon
  identification, creating a unified view of the customer.
* Merged profiles have multiple IDs: Merged profiles retain their old IDs to ensure continuity in tracking across all
  devices until they are updated with the new unified Profile ID.

This system allows Tracardi to provide a comprehensive view of a customer's journey, accounting for their interactions
across various browsers and devices, and enabling effective identity resolution.