**Event Redirects**

**Overview:**
Event redirects are a type of event source that enables you to create a clickable link. When this link is clicked, it
triggers a specific event in Tracardi and redirects the user to a designated URL.

**How It Works:**

You can generate an event redirect link in the following format:

```
http://api.tracardi.com/redirect/{redirect-identifier}/{optional-session-id}
```

- `{redirect-identifier}`: A unique identifier for the redirect you want to trigger.
- `{optional-session-id}`: An optional session identifier that can be attached to the link.

**Example:**

Let's break down an example to illustrate how event redirects work:

- You create a link like this:
  ```
  http://api.tracardi.com/redirect/d81c184a-eb5d-4f9e-b0f0-4b62bf7066dd/{optional-session-id}
  ```

- When a customer clicks the above link, they will be redirected to (this is defined by user):
  ```
  https://join.slack.com/t/tracardi/shared_invite/abcd
  ```

- Simultaneously, a "slack-invite-link" event will be registered in Tracardi, including the specified properties.

**Session-ID Attachment:**

You have the option to attach a session identifier to the link. Here's why you might want to do that:

- If you're working with a specific user profile and have their session ID, attaching it to the link ensures that the
  event triggered by the link is automatically associated with that profile and its current session.

- Tracardi profiles can be loaded using either their profile ID or one of their session ID. So, if you're running a workflow for a
  particular profile and want to send an email with a link that, when clicked, registers an event in Tracardi, attach
  the session ID. This way, the click event will be seamlessly linked to the profile and its ongoing session.

In essence, event redirects offer a straightforward way to capture user interactions, trigger events, and maintain
associations with user profiles and sessions in Tracardi.