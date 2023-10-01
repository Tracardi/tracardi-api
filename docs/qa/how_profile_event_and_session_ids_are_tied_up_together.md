# How profile, event and session ids are tied up together?

* Events have references to both the profile ID and session ID.
* Sessions have references to the profile ID.
* This means that a profile can be associated with multiple events and sessions (session is basically a visit).

To illustrate this relationship, consider the following example:

Visit one:

    Event 1, Event 2, and Event 3 are associated with Profile 1 and Session 1.

Visit two:

    Event 4, Event 5, and Event 6 are associated with Profile 1 and Session 2.

This example demonstrates that the profile is connected to multiple events and multiple sessions. The session ID changes
when the user opens a new browser or visits a new page, representing a new session or visit. However, the session ID
remains the same between the visits or interactions within a session. In the context of web page the script that is placed
on the wab page is responsible for changing the session ID when the browser is closed. 

It's important to note that the system automatically increments the visit counts in the profile when the session ID
changes, reflecting the number of visits or sessions associated with that profile.

## Data Example

Visit one.

Event tables

|Event ID  | Profile ID | Session ID |
|----------|------------|------------|
|1| 1 | 1
|2| 1 | 1
|3| 1 | 1

Visit two

|Event ID  | Profile ID | Session ID |
|----------|------------|------------|
|4| 1 | 2
|5| 1 | 2
|6| 1 | 2

Visit counts in profile are automatically incremented when the session id changes. 

## Debugging and Session IDs

When utilizing the debug mode in the workflow editor, it's important to note that the behavior of session IDs may differ
from regular operation. In debug mode, the session ID remains the same for every simulated event, which can impact the
expected functionality.

During debugging, the workflow editor creates a fake event and session to simulate the execution of the workflow. The
IDs assigned to these debug entities are constant, meaning they don't change with each iteration or interaction. This
consistent session ID can affect the expected behavior of the system, as it deviates from the dynamic session ID changes
that occur in regular user sessions.

It's crucial to consider this discrepancy when debugging workflows that involve session-dependent logic or
functionality. If the workflow relies on different session IDs for distinct visits or interactions, the debug mode's
static session ID may not accurately reflect the intended behavior (it will not increase the visits in profile).

To overcome this limitation, it's recommended to thoroughly test the workflow in a test mode (See test in the left-hand
menu). By doing so, you can ensure that
the workflow functions as expected under normal conditions, considering the dynamic nature of session IDs in actual user
sessions.

Keep in mind that the debug mode's static session ID serves the purpose of simplifying the debugging process by
providing consistency and predictability. However, it's important to be aware of its impact on session-dependent logic
when transitioning from debug mode to live deployment.