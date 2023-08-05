# How can I load profile in workflow?

My question is "I have a profile-less event. How can I load a profile using the data I have sent in event properties?"

The best way to load a profile in Tracardi system is by using the "Load profile by..." plugin. This plugin enables
Tracardi to load and replace the current profile in the workflow. To load the profile using this plugin, the user can
configure it by specifying profile id or e-mail.

It is also possible to load the profile right in the webhook bridge. Go to your webhook event source and click edit and
find "Replace Profile ID". This feature is available in webhook event source starting from version 0.8.1.

---
This document also answers the questions:

- How can I replace profile inside workflow?
- Can a profile-less event have profile ID?
- How to load profile by event property?