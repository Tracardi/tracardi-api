# What are session opened and visit opened meant for?

In Tracardi, the "session-opened" and "visit-opened" events serve as triggers to capture the beginning of user
interactions on the platform.

1. Session Opened:
   The "session-opened" event is raised when a user's session starts, indicating the beginning of their continuous
   activity on the platform. A session represents a period of time during which a user engages with the platform,
   typically starting from the moment the first event is collected from the user. The session will end when the user's
   session ID changes. This event allows you to initiate additional workflows or actions that should occur at the start
   of a user's session, providing valuable insights into user activity over a specific timeframe.

2. Visit Opened:
   The "visit-opened" event is triggered when a user starts a new visit to the platform within a specific time frame
   during one session. Usually, a session has only one visit, but there are cases where a session may have several
   visits. For instance, if a customer keeps their browser open for multiple days and visits your page several times,
   with 1h intervals of inactivity between clicks. When a user visits the platform and there is no existing visit
   associated with them, Tracardi creates a new visit and raises the "visit-opened" event. This event helps you keep
   track of and manage user visits, enabling you to analyze user behavior during specific visits and better understand
   how users interact with your platform.
