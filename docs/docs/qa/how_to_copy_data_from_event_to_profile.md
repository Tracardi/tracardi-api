# How can you copy data from events to profiles?

To copy data from events to profiles, you will need to create a workflow with a start node and a node called "
copy data". In the "copy data" node, you can select the destination and set it to the event property e.g. "phone", "
email", etc. Another way to copy data is to use the "Auto group merge event properties" node, which will automatically
merge all event properties to the profile traits.

## Auto coping

Tracardi offers an easy way to copy data from events to profiles with its auto-coping feature, available in the
commercial version. Users can define an event type and specify which properties to copy, and the system will handle the
copying automatically.

## Pre-build event types

Starting from version 0.8.1, Tracardi includes build-in event types that can be used for auto-coping. These internal
event types are designed to track the customer journey on websites or applications, and they come with default
properties that eliminate the need for manual copying.

Using these internal event types streamlines the use of Tracardi and simplifies the process of data collection and
analysis. When an internal event type is utilized, the system automatically detects it and populates the profile and
session with relevant data. To learn more about the available default event types, [please refer to the provided list](../getting_started/components/events/internal_events.md).