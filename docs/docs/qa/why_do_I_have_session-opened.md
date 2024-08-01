# Why do I have session-opened when first event is collected?

In Tracardi, the session-opened event is triggered when the first event is collected due to the platform's built-in
event types that automatically activate for specific actions. When the first event is collected, Tracardi checks if the
user has an existing session. If there is no session associated with the user, Tracardi creates a new one, and this
action triggers the session-opened event.

Similarly, this logic is applied to profile and visit events. If there is no existing profile or visit for the user,
Tracardi generates new ones and raises the respective events. This functionality is beneficial as it allows users to
associate additional workflows or actions with the event of a session being opened or a new user profile being created.
This way, users can implement custom behaviors or processes triggered by these events within the Tracardi platform.