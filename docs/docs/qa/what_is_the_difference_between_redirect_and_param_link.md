# What is the difference between redirect link and parametrized link in tracardi?


In Tracardi, redirect links and parameterized links serve similar purposes. They are used to customer journey:

### Redirect Links

Redirect links in Tracardi are used primarily to track user interactions by redirecting them through a specified URL
before reaching the final destination. These links help in gathering valuable data about user interactions and link
activities.

**Key Features:**

1. **Tracking Clicks:** When a user clicks on a predefined link, they are redirected to a designated URL.
   Simultaneously, Tracardi receives an event containing information about the redirect and any predefined event
   properties.
2. **Link Format:** The links follow a specific format: `http://<tracardi-api-url>/redirect/<redirect-id>`.
3. **Session Association:** It's possible to include a session ID in the redirect link to associate the click with a
   specific user session, which allows to retrieve a profile that started the session. This way system identifies the customer/user that clicked the link..
4. **Hidden Link URL**: Contrary to the next method the Redirect Link hides the target link.

**Usage Example:**

```plaintext
http://<tracardi-api-url>/redirect/<redirect-id>/<session-id>
```

This format allows Tracardi to associate the click with the profile that corresponds to the specified session ID.

### Parameterized Links

Parameterized links in Tracardi include specific parameters in the URL to track and identify user interactions. 
These parameters can include profile IDs, source IDs, and other relevant data such as session ID, that help in identifying the
user and their session across different interactions.

**Key Features:**

1. **Profile and Source ID:** By adding parameters like `__tr_pid` (profile ID) and `__tr_src` (source ID) to the URL,
   you can ensure that the interactions are tracked with the correct user profile and source. This is useful when redirecting users from emails or other sources and ensuring that the
   specific user's activity is tracked by Tracardi.
2. **Requires JavaScript tracker on the target page:** The parameterized links work only when the target page has JavaScript snippet installed.

**Usage Example:**

```plaintext
http://example.com?__tr_pid=<profile-id>&__tr_src=<source-id>
```

This format ensures that the user's activity is tracked and associated with the correct profile and source ID.

### Differences

Both methods are similar, but they differ in who sends the event to the system. In Redirected Links, Tracardi handles
the event since the link is within the system and it does not need the Javascript to be installed on web page. In the second method, the script located at the target page is
responsible for sending the event.