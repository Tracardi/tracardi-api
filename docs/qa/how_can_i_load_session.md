# How can I load session in workflow?

My question is "I have a profile-less event. How can I load a session using the data I have sent in event properties?"

It is possible to load the session right in the webhook bridge. Go to your webhook event source and click edit and
find "Replace Session ID". This feature is available in webhook event source starting from version 0.8.1.

---
This document also answers the questions:

- How can I replace session in profile-less event?
- Can a profile-less event have session ID?
- How to load session by event property?