# Identification point

An identification point in Tracardi is an event within the customer's journey that can be used to uniquely identify the
customer and merge their data across multiple interactions and profiles.

## Key Components of Identification Points

* **Event-Based Identification**:  Certain events in the customer journey serve as identification points. For example, a
  user logging in with their email address or phone number is an event that provides a unique identifier. Identification
  Point is triggered by event, contrary to APM which is a background watch dog like process.

* **Unique Identifiers**: Identification points rely also on unique identifiers such as email addresses, phone numbers,
  usernames, or other personal identifiers that can uniquely distinguish one user from another. Event that is used to
  identify and merge customer profile must have a unique identifier.

* **Profile Matching and Merging**: When Tracardi processes an event that includes an identification point, it checks if
  the identifier matches any existing profiles. If a match is found, the data from the current event is merged with the
  existing profile, and the profile is further processed.

## How Identification Points Work in Tracardi

* **Data Collection**: As users interact with a website or app, Tracardi collects data and events. Each event may
  include identification points, such as an email address provided during registration.

* **Identification Point Settings**: If the event is set in Tracardi as an `Identification Point` and it includes
  defined identifier, Tracardi will merge profiles before further processing the event.

## Example of Identification Points in Action

1. **Identification Point Settings**: System administrator marks two events `sign-in`, and `contact-form-data` event as
   an identification points. The first has an email as merging key. The second has a telephone number as merging key.

2. **Initial Interaction**: A user registers on a website with their email address user@example.com and a phone.
   Tracardi creates a profile with `profile-id-123` and stores the email and phone in profile.

3. **Subsequent Interaction**:  The user logs in from a different device using the same email address. Tracardi
   recognizes that the `sign-in` is the identification point and the email is a merging key. Then it looks up the
   database for all the profiles with the delivered e-mail and matches it to `profile-id-123`, and merges both profiles.

4. **Cross-Device Tracking**: If the user later provides their phone number within `contact-form-data` event, Tracardi
   again searches the database for the profiles, but this time uses phone as merging key (identifier). If profiles are
   found then system merges them.

5. **New profile ID**: Every time the profiles are merged
   the [new profile id is returned in the Tracardi response](../processes/merging.md#why-my-profile-id-in-the-response-from-tracardi-is-different-then-the-one-i-have-sent). 
