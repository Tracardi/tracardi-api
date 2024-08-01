# What is Merge Strategy Fallback?

A merge strategy fallback is a method used when the primary merge strategy cannot be applied due to missing or
incomplete data. For instance, if the update time of a field is missing, the Last Update Strategy cannot be used, and an
alternative strategy must be selected. Priorities for fallback strategies can be set within the system for each field in
the profile, ensuring that there is always a method available to resolve conflicts in data merging.