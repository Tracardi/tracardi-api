# Merge Profile Action

When new personal information is added to a customer's profile, it might need to be combined with other profiles in the
system to create one consistent profile. This is done through the "merge profile" action.

When this action is used in the workflow, it will set the profile to be merged at the end of the process. To finish the
merging process, you'll need to provide a merge key in the settings of the "merge profile" step.

## Configuration

The merge key is an important part of the system that helps to combine different customer profiles into one. This key
can be something unique like an email, phone number, or ID. The system will look for other profiles that have the same
key and merge them together.

When the profiles are merged, all their information is combined into one single profile and any actions related to those
profiles are now related to the merged one. Any extra profiles that are no longer needed will be deleted, but their ID
will still be connected to the new merged profile. This means that if you try to look for an old profile, the system
will show you the new merged one.

If you want to merge profiles using more than one key, like email and name, the system will look for profiles that have
both those keys. The merge key should be provided in a JSON array. To access the merge key data, you should use dotted
notation. For more information on this notation, check the Notations/Dot notation section in the documentation.

```json
{
  "mergeBy": ["profile@data.contact.email.main"]
}

```

# A simpler way to merge profile

An identification point is a feature (in commercial Tracardi) that allows the system to identify customers during their journey. When this point
is set, the system will monitor for events that can be used to match the anonymous customer's identified profile.

To give an analogy, think of an identification point like the ones at an airport or during a police check. You stay
anonymous until there is a moment when you need to show your ID. This is an identification point. At this point, you are
no longer anonymous. The same goes for Tracardi, once you identify yourself, all your past events become part of your
identified profile. If identification happens multiple times on different communication channels, all the anonymous
actions will become not anonymous anymore.

For example, if a customer's profile in the system has an email address that matches the email delivered in a new event,
then the system can match anonymous customer data with the existing profile and merge all previous interactions/events.

In simpler terms, identification point is a way for the system to identify customers and keep their information
consistent throughout their journey.
