### What is a Set of Merging Strategies?

A set of merging strategies in Tracardi defines the sequence in which the system should attempt to resolve conflicts in
profile data. For example, a default merging strategy set might
be: `[LAST_UPDATE, LAST_PROFILE_UPDATE_TIME, LAST_PROFILE_INSERT_TIME]`.

This set tells the system to:

1. First, try to merge fields based on the `LAST_UPDATE` strategy, selecting the field that was last updated.
2. If this is not possible (e.g., if field update dates are not available), then use the `LAST_PROFILE_UPDATE_TIME`
   strategy, selecting the value from the last updated profile.
3. As a final fallback, use the `LAST_PROFILE_INSERT_TIME` strategy, selecting the value from the last inserted profile.

This mechanism is known as a merge strategy fallback in Tracardi, ensuring that there is always a method available to
resolve conflicts in data merging.