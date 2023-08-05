# How to integrate external systems using webhooks

Integrating a system using JavaScript is easy, but using webhooks is more challenging. A webhook sends an API call when
an event occurs in an external system, such as Slack notifying when someone joins a channel or writes a message.
Intercepting a webhook is simple - create a URL webhook in Tracardi and add it to the external system as the URL to send
data when an event occurs. However, the difficulty lies in the fact that the external system lacks information about the
user who raised the event. Each external system has its own method of user identification, which means the profile ID in
the external system is different from Tracardi's.

This discrepancy means that when data is sent, the external system may not send it in any globally defined way. As a
result, it is not possible to create a Tracardi event associated with any profile. Such events are profile-less, and
unfortunately, do not contain information useful for tracking customer journeys. We must process these events and
attempt to connect them with the existing Tracardi profile.

First, we must ensure that all events collected by the webhook are grouped into one profile, even if it is not connected
to an existing Tracardi profile. Tracardi can store multiple profiles belonging to one person, so if there is a
technical possibility to connect them, it will do so. The collected data should be consistent and grouped per user.

To keep the data within one profile, the webhook needs to transmit an identifier assigned to the user, such as a user ID
from an external system. If such data is not sent, we will not be able to use it, and it is best not to collect
it unless it is needed for other purposes and can remain anonymous.

To identify the transmitted data and keep it within one profile, the event source in Tracardi has a `Replace profile ID`
field in which we specify where the ID that identifies the profiles is located in the webhook data/payload. 
This identifier is used to group events and connect each event to one profile.

Once we have grouped events, we can consider whether there is any data that allows us to merge the profile from the
external system with the profile from Tracardi. For this purpose, we use identification points and some data that 
identifies the profile across all systems. We can use email for example, which is a common part between 
Tracardi and the external system.