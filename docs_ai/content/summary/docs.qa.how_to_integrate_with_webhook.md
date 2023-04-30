Once the profile is merged, we can start tracking customer journeys and use the data collected from the webhooks to
improve our understanding of customer behavior. To do this, we need to create a mapping between the events sent by the
external system and the events in Tracardi. This mapping is used to create a journey in Tracardi, which is then used to
track customer behavior.

The mapping is done by creating a `Webhook Event` in Tracardi, which is associated with the event sent by the external
system. This event is then used to create a journey in Tracardi, which is then used to track customer behavior.

In summary, integrating an external system using webhooks is a complex process. It requires creating a URL webhook in
Tracardi and adding it to the external system as the URL to send data when an event occurs. The data sent by the
external system must be consistent and grouped per user, and an identifier must be sent to keep the data within one
profile. Finally, a mapping between the events sent by the external system and the events in Tracardi must be created to
track customer behavior.