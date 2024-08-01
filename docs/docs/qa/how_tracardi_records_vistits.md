# How tracardi calculate the visits

Tracardi calculates visits based on the concept of a session. A session is identified by a session ID, which is
typically a randomly generated number such as a UUID4. The session ID is used to track a user's activity and determine
the duration of their visit.

Tracardi calculates visits based on the continuity of the session ID. As long as the session ID remains the same,
Tracardi considers it to be part of the same visit.

Let's consider an example with 10 events. The first three events have a session ID of 1, the next five events have a
session ID of 2, and the remaining events have a session ID of 3. In this case, Tracardi would interpret this as three
separate visits because there are three distinct session IDs.

However, it is also possible to append events to a previous visit by sending them with the same session ID as before.
This allows for the extension of a visit beyond the initial set of events.

In the case of web data collection, Tracardi relies on the session ID stored in a cookie. When a user opens a web page,
Tracardi's JavaScript code creates a session and saves the session ID in a cookie. As long as the user continues
browsing the website without closing their browser, the same session ID is used and associated with each event generated
by the user's actions. Tracardi considers this continuous stream of events with the same session ID as a single visit.
If the user closes their browser, the cookie is deleted, indicating the end of the session. When the user visits the
website again, a new session ID is generated, and a new visit begins.

For data collected from other sources, such as mobile apps, the definition of a visit may vary. In the mobile app
context, a visit can start when the user opens the app and ends when the user closes it. To track visits in this
scenario, the mobile app needs to generate a session ID when the app starts and include the same session ID in every
event sent to Tracardi. Tracardi monitors session changes and increments the visit counter accordingly.

In cases where data is collected from an external system or data source where we are not so sure when session starts or
ends, developers can define a session based on the data that exists in the external system. For example, they can use a
visit ID or device ID as a session identifier. If no specific identifier is available, developers can define a session
as a fixed time period, such as 15 minutes, 10 events, etc. or choose to include all events in one session. Then
generate one UUID4 session ID and keep it the same for all events.

Overall, Tracardi allows developers to define how long a visit lasts by controlling the session ID and determining when
to start and end a session based on the specific data source, whether it's a web page or a mobile app.