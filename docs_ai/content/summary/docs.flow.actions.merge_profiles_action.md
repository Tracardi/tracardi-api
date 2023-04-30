The "Merge Profile Action" is a feature in the commercial Tracardi system that allows customers to combine different
profiles into one consistent profile. This is done by setting a merge key in the settings of the "merge profile" step.
The merge key is a unique identifier such as an email, phone number, or ID. The system will look for other profiles that
have the same key and merge them together. All the information from the profiles will be combined into one single
profile and any actions related to those profiles will now be related to the merged one. Any extra profiles that are no
longer needed will be deleted, but their ID will still be connected to the new merged profile. If more than one key is
used to merge profiles, like email and name, the system will look for profiles that have both those keys. The merge key
should be provided in a JSON array and can be accessed using dotted notation.

The identification point feature in Tracardi allows the system to identify customers during their journey. This is done
by setting an identification point, which is like an airport or police check. Once the customer is identified, all their
past events become part of their identified profile. If identification happens multiple times on different communication
channels, all the anonymous actions will become not anonymous anymore. For example, if a customer's profile in the
system has an email address that matches the email delivered in a new event, then the system can match anonymous
customer data with the existing profile and merge all previous interactions/events.