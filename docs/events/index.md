# Event's Core Definitions

## Event properties

Event properties refer to the characteristics or attributes of an event that can be recorded and analyzed. These
properties can provide valuable information about the event, such as the time it occurred, the location, the
participants, and any relevant details or context. In the context of event reshaping, event properties may be separated
out from the rest of the data in order to facilitate their analysis and interpretation. Event properties can be used to
better understand the event, and can be useful in identifying trends, patterns, or relationships within the data.

## Event traits

Event traits are characteristics of an event that are indexed in the system for the purpose of analysis and aggregation.
Traits differ from event properties in that they are structured in a way that allows them to be searched, analyzed, and
aggregated more effectively.

To index event data, the data is moved from the properties of the event to traits. For example, if an event includes a
property that describes the type of device that was used to initiate the event, that property could be converted to a
trait so that all events involving the same device type could be identified and aggregated.

Event traits can provide valuable insights into the behavior and patterns of users or other entities within a system. By
analyzing events with traits, it is possible to identify trends, correlations, and other relationships that may not be
immediately apparent from the raw event data.

## Profile less event

A profile-less event is an event that cannot be assigned to any particular profile. This means that it does not contain
sufficient information to identify a specific user or entity associated with the event.

An example of a profile-less event might be an event that describes an error in the system. In this case, the event
would provide information about the error itself (such as the type of error, the location, and any relevant details),
but it would not be tied to a specific user or profile.

Profile-less events can still be useful for understanding the use journey, but they may not provide as much context or
insight as events that are tied to specific profiles.

## Event context

Event context refers to data that is not directly connected to the properties or traits of an event, but may provide
additional context or background information that is relevant to understanding the event.

For example, if an event represents a customer making a purchase at a store, the event context might include information
about the weather conditions at the time of the purchase. This information would not be directly related to the event
itself (i.e., the purchase), but it might be relevant to understanding the circumstances surrounding the event.

## Event states

Events can take the following states:

| State         | Description                |
|---------------|----------------------------|
| `collected`   | Event was collected        |
| `processed`   | Event was processed        |
| `warning`     | Workflow logged warnings   |
| `error`       | Workflow returned errors   |
| `ok`          | Event wsa processed without errors |

## Event routing

Event routing is the process of directing events to specific workflows or processes based on the type and source of the
event. This allows businesses to handle different types of events in different ways, and to route events to the most
appropriate workflow based on their characteristics.

For example, an e-commerce platform might route events related to product purchases to a workflow that handles order
processing and fulfillment, while routing events related to customer login attempts to a workflow that handles
authentication and security. By routing events to the appropriate workflow, businesses can more effectively manage and
process the data associated with the event.

## Events synchronization

In Tracardi, event synchronization is the process of managing the order in which events are processed. This includes
ensuring that events for a specific profile are processed in a specific order. Essentially, this means that events for
one profile are processed sequentially, while events for other profiles are processed sequentially but in parallel to
each other.

