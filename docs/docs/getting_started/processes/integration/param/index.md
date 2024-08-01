# Parametrized URL

A parameterized link in Tracardi is a URL that contains specific parameters designed to track and identify user
interactions and collect data effectively. These parameters help in associating the link click with a specific user
profile, session, or other relevant information.

## Key Concepts of Parameterized Links

1. **Profile ID (`__tr_pid`):** This parameter carries the unique identifier of a user profile. When a user clicks the
   link, the profile ID is used to associate the interaction with the correct profile in Tracardi.
2. **Source ID (`__tr_src`):** This parameter identifies the source of the event. It is used to understand where the
   traffic is coming from (e.g., a specific campaign, email, or ad).
3. **Session ID (`__tr_sid`):** This parameter can be used to maintain session continuity and link interactions within
   the same session.

## Creating a Parameterized Link

To create a parameterized link, you need to append the necessary parameters to your URL. Here’s a step-by-step guide:

### Step 1: Construct the Parameterized Link

Include the profile ID, source ID, and optionally, the session ID in your URL.

**Example URL:**

```html
http://example.com/landing-page?__tr_pid=<profile-id>&__tr_src=<source-id>&__tr_sid=<session-id>
```

- Replace `<profile-id>` with the actual profile ID.
- Replace `<source-id>` with the actual source ID.
- Replace `<session-id>` with the actual session ID (if necessary).

**Example:**

```html
http://example.com/landing-page?__tr_pid=12345&__tr_src=email_campaign&__tr_sid=67890
```

### Step 2: Use the Parameterized Link in Your Campaigns

Embed this URL in your marketing campaigns, such as email newsletters, ads, or social media posts. When users click on
these links, Tracardi will track their interactions using the provided parameters.

### Step 3: Add JavaScript Snippet on the Web Page

Ensure that Tracardi is configured to recognize and process these parameters:

1. **Include JavaScript Integration on the target web page:**
    - Embed the Tracardi tracking script on your landing page. This script will capture the parameters and associate the
      interaction with the correct profile and session.

## Example Use Case

Let’s say you’re running an email campaign and want to track user interactions:

1. **Email Content:**
    - Include a parameterized link in your email:
   ```html
   <a href="http://example.com/landing-page?__tr_pid=abc123&__tr_src=email_campaign">Click here</a>
   ```

2. **Landing Page:**
    - Ensure the Tracardi JavaScript snippet is included on the landing page to capture the parameters.

3. **Data Collection:**
    - When users click the link, their profile ID and source ID are captured, and interactions are tracked in Tracardi.

### Merging

If the system already has a profile saved in the browser's local storage, it will try to merge the previous history of events on that page with the new profile ID and its history. If the user is visiting your page for
the first time, there shouldn't be any merging.

Remember that if a session number is provided, the event will be associated with the corresponding profile. If only a
profile ID is given, a new session will be created for that profile.