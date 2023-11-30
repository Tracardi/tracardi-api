# Merge profiles

This plugin combines customer profiles in Tracardi when new information about a customer is added. It helps to make one
complete profile from many separate ones.

# Version

0.8.2

## Description

The Merge Profiles Action in Tracardi is for joining different customer profiles into one. This is useful when new
personal information is added to a customer's profile. The action marks the profile to be joined together at the end of
the process. The joining is done using specific keys like email or phone number, which are unique to a user. When it
finds profiles with the same key, it puts them together, and all their information and activities become part of one
profile. The old profiles are removed but their IDs stay connected to the new combined profile.

## Additional Information

The merge key is a special part of the system that helps to put different customer profiles together into one. This key
is something unique to each customer, like their email, phone number, or ID. The system searches for other profiles with
the same key and combines them into one.

When the profiles are put together, all their details and actions become part of one big profile. The profiles that are
not needed anymore are removed, but their ID stays linked to the new big profile. So, if you look for an old profile,
the system will show you the new, combined one.

If you want to join profiles using more than one key, like both email and name, the system will look for profiles that
match both these details. You should list these merge keys in a JSON array. To find and use these merge keys, you use a
special format called dotted notation. You can learn more about this in the documentation's Notations/Dot notation
section.

# Inputs and Outputs

The plugin takes any kind of data in a JSON format and gives back the same data.

Input: `{"payload": {}}`
Output: `{"payload": {}}`

The plugin does not start the workflow.

# Configuration

- **Merge by fields**: This is a list of fields used to identify a user, such as `profile@data.contact.email.main`.
  These fields are like keys for joining profiles. Profiles with the same key values are put together.

# JSON Configuration

```json
{
  "mergeBy": [
    "profile@data.contact.email.main"
  ]
}
```

# Required resources

This plugin does not need external resources to be configured.

# Errors

- "Field mergeBy is empty and has no effect on merging. Add merging key or remove this action from flow." This error
  happens when the merge key list is empty.
- "Field `{key}` does not start with profile@... Only profile fields are used during merging." This error occurs when
  the provided merge key does not start with 'profile@'. The plugin only uses profile fields for merging.

# A Simpler Way to Combine Profiles in Commercial Tracardi

In the commercial version of Tracardi, there's a feature called an identification point that helps recognize customers
during their use of the system. This feature works by watching for certain activities. These activities help the system
figure out who the customer is, even if they were unknown before.

Here's an easy way to understand it: It's like when you go through a check at an airport or during a police stop. You're
just another person until you have to show your ID. That moment, when you show your ID, is like an identification point.
Once you're identified in Tracardi, all your past activities are linked to your known profile. This means if you're
identified in various ways over time, like with an email or a phone number, all your previously unknown activities get
linked to your known profile.

For instance, if there's already a profile in the system with an email address, and the same email shows up in a new
activity, Tracardi will realize that this anonymous data actually belongs to the existing profile. Then, it combines all
the past activities with this profile.

In simple terms, this feature in the commercial Tracardi is a way to keep track of customers and ensure their
information stays connected and current throughout their interactions with the system.