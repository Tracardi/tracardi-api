# Redirect Bridge

A redirect bride is a valuable tool for tracking and associating clicks on links with user profiles. It is commonly used
when sending emails with community invites, promotions, etc. or monitoring email openings. By creating redirected links,
we can track user interactions and gather data. For example, we can create a link that redirects to a tiny 1px image.
When that image is displayed, Tracardi receives an event indicating the email was opened. Additionally, the redirect
link can include the customer's session ID to identify the specific customer.

The Inbound Traffic/Event Redirects feature allows you to redirect traffic from specific links to a designated URL. When
a user clicks on one of these predefined links, they will be redirected to the defined URL. Simultaneously, Tracardi
will receive an event containing information about the redirect, along with any predefined event properties you have
set. This feature helps gather valuable data about user interactions and link activities.

The process of setting up Inbound Traffic/Event Redirects involves the following steps:

* Define the links that you want to redirect: This could be any link on your website or in an email that you want to
  redirect to a specific URL.

* Set the target URL: This is the URL that the user will be redirected to when they click on one of the defined links.

* Define the event properties: These are additional pieces of information that you want to send to Tracardi along with
  the event. This could include information such as the type of event, the source of the event, or any other relevant
  data that you want to track.

* Set up the event tracking in Tracardi: This involves configuring Tracardi to receive and process the events that will
  be sent from your Inbound Traffic/Event Redirects setup.

Once you have completed these steps, your Inbound Traffic/Event Redirects setup will be ready to use. When a user clicks
on one of your defined links, they will be redirected to the target URL and an event will be sent to Tracardi, providing
information about the redirect and any event properties that you have defined.

## Redirect links

All redirect links are in the form of:

```
http://<tracardi-api-url>/redirect/<redirect-id>
```

* __tracardi-api-url__ the url to Tracardi API server
* __redirect-id__ id of the redirection. Click on any item in __Inbound Traffic/Event redirects___ to see the full url
  path.

## Redirect links with session

By default, all redirect links do not contain any user profile. However, it is possible to include a session ID in the
redirect link when sending a message from Tracardi. To do this, use the following format for the extended link:

```
http://<tracardi-api-url>/redirect/<redirect-id>/<session-id>
```

When using this extended link, Tracardi will associate the click with the profile that corresponds to the specified
session ID.

To obtain the session ID, use session@id. If you wish to send the redirect link via email, you can use the provided
template and access the session ID using {{session@id}}.

