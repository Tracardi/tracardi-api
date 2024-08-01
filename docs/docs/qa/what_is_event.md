# What is event?

In the context of Tracardi, an event refers to a piece of data that represents an action, occurrence, or happening
within a system. Events are fundamental units of data collected and processed by Tracardi to analyze user behavior,
system interactions, and other activities. Each event contains specific characteristics or attributes, known as event
properties, which provide valuable information about the event, such as its timestamp, source, and relevant details.

Tracardi uses events to track and understand user interactions, record system activities, and trigger specific workflows
based on event data. Events play a crucial role in data processing and analysis, enabling businesses to gain insights
into user journeys, detect patterns, and make informed decisions based on the data collected from various sources.

Event consist of:

1. Event Properties:
    - Characteristics or attributes of an event that can be recorded and analyzed.
    - Provide valuable information about the event, such as time, location, participants, and relevant context.

2. Event Traits:
    - Characteristics of an event that are indexed in the system for analysis and aggregation.
    - Structured in a way that allows effective searching, analysis, and aggregation.
    - Event data is moved from properties to traits for better analysis.
    - Provide insights into user behavior, patterns, and correlations in the data.

3. Profile-less Event:
    - An event that cannot be assigned to any specific profile or user.
    - Lacks sufficient information to identify a particular user associated with the event.
    - Still useful for understanding the user journey but may not provide as much context as profiled events.

4. Event Context:
    - Data not directly connected to event properties or traits but provides additional context.
    - Offers background information relevant to understanding the event's circumstances.

5. Event States:
    - Events can have different states based on their processing status.
    - States include: "collected" (event was collected), "processed" (event was processed), "warning" (workflow logged
      warnings), "error" (workflow returned errors), and "ok" (event was processed without errors).

##  Event processes

1. Event Routing:
    - Process of directing events to specific workflows or processes based on their type and source.
    - Allows businesses to handle different types of events differently and route them to appropriate workflows.

2. Events Synchronization:
    - Process of managing the order in which events are processed in Tracardi.
    - Ensures events for a specific profile are processed sequentially, while events for different profiles are
      processed sequentially but in parallel to each other.

In summary, events in Tracardi carry various properties and traits, and they can be routed and synchronized to undergo
different workflows for analysis and processing. The information gathered from events helps businesses gain valuable
insights into user behavior and make informed decisions based on the data collected.