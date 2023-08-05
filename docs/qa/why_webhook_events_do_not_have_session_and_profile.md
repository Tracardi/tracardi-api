# Why webhook events dot not have session and profile?

By default, webhook events do not include session and profile information. This design choice is based on the fact that
most external systems are unaware of the Tracaardi Profile ID and session ID. Although it is possible to create a
webhook URL that incorporates an encoded session ID, it is rarely used due to the difficulty of passing session
information through a URL in external systems. In practice, approximately 99% of the time, the profile ID or session ID
is transmitted within the webhook payload data.

To address this limitation, we provide an option to replace or set the profile ID or session ID of the event collected
by the webhook URL using the payload data. This allows users to customize and manage the session and profile information
associated with webhook events effectively.

When configuring webhook integrations, it is important to keep in mind that the default behavior does not include
session and profile information. However, by extracting and manipulating the relevant data from the payload, users can
integrate their desired session and profile details into webhook events seamlessly.