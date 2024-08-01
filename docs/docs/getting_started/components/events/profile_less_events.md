# Profile-less events

Profile-less events in Tracardi are events that are not associated with any user profile. These events are useful for
tracking interactions and occurrences that do not need to be linked to a specific user, such as anonymous user actions
or system-generated events. Here’s a detailed overview of profile-less events in Tracardi:

### Characteristics of Profile-less Events

1. **No User Association**: These events do not contain information that links them to a specific user profile.
2. **Anonymity**: Useful for tracking actions from users who have not logged in or who are interacting with the system
   anonymously.
3. **System Events**: Can also be used for system-generated events where user context is irrelevant.

### Use Cases for Profile-less Events

- **Anonymous Interactions**: Tracking page views, clicks, or other interactions from external systems that do not have
  the information about profile id.
- **System Monitoring**: Capturing events related to system performance, errors, or other technical occurrences that do
  not need to be tied to a user.

### Implementing Profile-less Events

Profile-less events are usually created when using event source that is based on a webhook bridge. Then usually you can not control schema of sent data:

### Example Configuration

Here’s an example of a profile-less event payload:

``` title="Example of profile-less data"
POST /collect/EVENT-TYPE/SOURCE-ID`
{
    "url": "https://example.com",
    "user": "John",
    "email": "a@a.com"
}
```

In this example, we use a `/collect` endpoint and send just the data without any additional metadata.

### Considerations

- **Limited Personalization**: Since these events are not linked to user profiles, they cannot be used for personalized
  interactions or targeted actions.
- **Aggregated Insights**: While useful for aggregate data analysis, these events do not provide insights at the
  individual user level.

### Summary

Profile-less events in Tracardi are designed to handle interactions and occurrences that lack user identification. They
are often generated in use cases where the user cannot be identified. However, profile-less events can be converted to
events with profiles if the event payload contains identifiable information, such as an email address, which can be used
to reference the correct profile ID.