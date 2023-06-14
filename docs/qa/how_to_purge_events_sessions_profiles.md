# How to purge events, sessions, and profiles?

To purge events, you can follow these steps:

1. Go to the maintenance/indices section.
2. Locate the profile, event, and session indices.
3. Delete these indices by clicking on the trash icon located on the right side.
4. Refresh the page, and the system will reinstall those indices automatically.

For example, if you find indices like "080.fa73a.tracardi-event-2023-1," "080.fa73a.tracardi-event-2023-2," and so on,
deleting them will remove all the events collected in that respective month (e.g., January 2023).

The same process can be applied to purge profiles and sessions. Once you have deleted the data, refresh the page. In
most cases, you will be redirected to the installation page. The system detects any inconsistencies in the indices and
recreates the missing ones if needed. However, if you haven't deleted all event indices, the system may not require a
reinstallation.

It's important to note that this operation is only available for single tenant installations, such as open-source
installations. Multi-tenant installations of Tracardi do not have the option to delete indices.

Please be aware that as of version 0.8.1, there is no function to delete events, profiles, or sessions individually.

---
This document answers also questions:
- How to delete events, profiles, sessions?
- How to delete all data?
- How to delete an index?
- How to manage elasticsearch indices in Tracardi?