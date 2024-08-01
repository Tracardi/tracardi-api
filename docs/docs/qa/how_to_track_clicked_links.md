# How to Track Links and Viewed Images?

## Two Methods

There are two ways to track user activity in the system.

* __[Redirected Links](../getting_started/processes/integration/redirect/index.md)__: This method involves creating
  special links that, when clicked, send information to Tracardi about the user and then redirect them to a specific page. The information is stored within the link itself.

* __[Parameterized Links](../getting_started/processes/integration/param/index.md)__: The second method involves adding
  a parameter `__tr_pid` to an existing link. This parameter contains user information. When user visits the target
  page, the tracking script, that must exist on the target page, sends an event to Tracardi and use the
  parameter `__tr_pid` to identify the customer. 

Both methods are similar, but they differ in who sends the event to the system. In Redirected Links, Tracardi handles
the event since the link is within the system. In the second method, the script located at the destination address is
responsible for sending the event.

## Pros and Cons

The first method requires creating artificial links, which can be a bit cumbersome to manage when there are many of
them.

The second method avoids this problem since it uses existing links and only requires appending a parameter, like a
profile ID. However, the Tracardi system script must be present on the page.

These two techniques serve different purposes. The first one is useful for tracking if a client has viewed specific
images. Since images cannot have a tracking script directly, the first method utilizes artificial links that redirect to
the desired image. When the image is downloaded, Tracardi automatically sends an event. This is often used to track
email openings (email tracking). If an email contains images and they are downloaded, it indicates that the user has
seen the email.

The second technique is handy for checking if a user accessed our website from a specific email. By adding parameters
with the user's ID or session to the URL, we can track this information.

Keep in mind that if a session number is provided, the event will be attached to the corresponding profile. If only a
profile ID is given, a new session will be created for that profile.

Both techniques have a wide range of applications, primarily tracking page transitions, image views, file downloads, and
more.