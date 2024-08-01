# Tracardi Concepts

Tracardi is build around 5 major processes.

### Key Processes in Tracardi

* **[Integration](processes/integration/index.md)**: Integration is not a process within Tracardi. Instead, it occurs within a company and involves integrating systems
      with Tracardi to send data from various systems, websites, and databases to Tracardi.

* **[Collection](processes/collection.md)**: Collection is the process responsible for gathering and ingesting data. It consists of several subprocesses:
      * **[Tracking](processes/tracking.md)**: The process of maintaining a consistent single Profile ID across all customer interactions on a single device. It is the responsibility of the device/client to keep the Profile ID unchanged.
      * **[Identity Resolution and Merging](processes/identity_resolution.md)**: The process of maintaining a consistent single profile across all customer devices. It is Tracardi's responsibility to merge all profiles created on different devices whenever possible.
      * **Storing Data**: This process involves storing collected data in one profile record and referencing all historical events and sessions.

* **[Automation](processes/automation.md)**: This process automates the customer journey, enhances customer profiles, personalizes customer experiences, and triggers messaging.

* **[Audiences and Activations](processes/audience.md)**: The process of creating audiences/segments and orchestrating them to external systems such as Marketing Automation platforms.

* **[Orchestrator/Router](processes/orchestration.md)**: The process responsible for sending customer data to external systems.

## Core Definitions

In order to understand how Tracardi CPD works you will need to learn the following definitions.

### [Traffic](definitions/traffic.md)

Tracardi is capable of both receiving and sending data, thus defining two types of traffic:

1. **Inbound Traffic:** This includes systems that send data to Tracardi, such as websites, internal systems, and
   services. The incoming traffic is usually associated with [event source](components/event_source.md) and identified
   by an Source ID defined in Tracardi.

2. **Outgoing Traffic:** This involves external systems or services to which Tracardi can sends data. Outgoing Traffic
   is usually associated [destinations](components/destination.md).

!!! Tip

    In the system, we call inbound traffic - event sources.
    In the system, we call outbound traffic - destinations.

### [Bridge](components/bridge.md)

A [bridge](components/bridge.md) is a piece of software that connects two separate systems or applications, allowing
them to communicate and
exchange data. In Tracardi **a bridge is a piece of software that collects data from a particular event source using
particular protocol**, such as a API call, queue, email, and transfer to the system collector. For example, Tracardi
come with an open source API bridge that allows it to collect data from an API `/track` endpoint and transfer it to the
system. Commercial versions of Tracardi may come with other types of bridges, such as a Kafka bridge, which allows it to
collect data from a Kafka message broker.

Bridge is strictly related to Event Source, when a new event source is created, the appropriate bridge must be selected
to facilitate the collection and transfer of data.

### [Event Source](components/event_source.md) - Inbound Traffic

In order to kick-start your new project with Tracardi, you must create a new [event source](components/event_source.md).
That source will give you an
identifier which when attached to your track calls will start collecting data about your users. Event source needs a
bridge that will transfer data to the system.

!!! Note

    An event source can be configured as ephemeral, meaning that data received from this type of event source 
    is not permanently saved in the system but is only processed by the workflow. Ephemeral event sources handle 
    data temporarily, using it solely for the duration of the workflow. This enables real-time data processing 
    and analysis without the need for long-term storage.

## [Destination](components/destination.md) - Outbound Traffic

In Tracardi, a [destination](components/destination.md) is an external system where profile or event data is sent. To
function, a destination
requires a specific resource, such as an API endpoint or queue service, to receive and process the data.

A resource in this context acts similarly to a [bridge](components/bridge.md) in
the [Event Source](components/event_source.md), facilitating the connection to the external
system.

!!!Note 

    Not all resources are available as destinations in Tracardi. 

In summary, a destination is a system or service where data is forwarded for further processing or storage, enabling
data transfer and integration between different platforms.

## Data

### [Resource](components/resource.md)

A service [resource](components/resource.md) refers to a service or application accessed over a network or the Internet,
providing functions such
as data storage, communication, and computation.

In Tracardi, resources are [credentials](definitions/credentials.md) to datasets or services that can be queried for
data, often requiring authentication (e.g., passwords or tokens) for access. When creating a resource in Tracardi, you
may need to provide access details for both test and production environments.

!!! Info

    Tracardi allows you to test your internal processes by running workflows in test mode. In this mode,
    workflows connect with test resources to prevent any changes that could impact the production environment.

### [Session](components/session.md)

In Tracardi, a [session](components/session.md) represents a period during which a user actively interacts with a
website or application. It is
often associated with a visit to the site or app. The [session](components/session.md) remains active as long as there
is ongoing interaction.
The session ID is assigned when data is sent to Tracardi and is typically managed by the client program. Session data is
immutable for the entire duration of the [session](components/session.md) and contains information about the user's
visit, such as the operating
system, application, browser, screen resolution, and device used.

### [Event](components/event.md)

In Tracardi, [events](components/event.md) are representations of actions or occurrences at a specific moment in
time. [Events](components/event.md) can be used to
track visitor behavior on a website or application, capturing a wide range of actions and interactions. Examples include
clicks on links, logins, form submissions, page views, and purchase orders. Events can carry additional data such as
usernames, purchased items, or viewed pages, depending on the type of event and the information being tracked.

Website [events](components/event.md) in Tracardi are typically triggered when JavaScript is executed on a selected page
or when an API query
is made to the `/track` endpoint. Since the tracking code is present on every page, it can
emit [events](components/event.md) as users interact
with the site. The events and their types are configurable, allowing for customization of the data sent for each event.

[Events](components/event.md) can either be stored inside Tracardi and passed to a workflow for external processing.
This provides flexibility
in how events are tracked and utilized within the Tracardi system.

### [Profile](components/profile.md)

In Tracardi, a [profile](components/profile.md) represents an aggregated and comprehensive set of data about a customer,
built dynamically as
events are processed by the system. The profile is essentially the central data structure that captures all relevant
information and interactions pertaining to a user/customer, allowing for personalized and context-aware actions within
Tracardi workflows.

A [profile](components/profile.md) in Tracardi comprises several key components, including data, custom traits,
metadata, etc. Profile is
referenced in [sessions](components/session.md), and [events](components/event.md). Data are key-value pairs that store
personal details such as name, email, and
preferences, forming the core attributes of the profile. Custom traits represend custom data stored for profile.
Metadata provides additional context about the profile, such as creation and update timestamps, source information, and
tags that help categorize the profile.

[Profiles](components/profile.md) are built through the processing of events. When an event occurs, it is sent to
Tracardi along with relevant
data, which may include initial profile information. Tracardi then identifies whether the profile already exists using
unique identifiers such as email or user ID. If the [profile](components/profile.md) exists, it is retrieved and
updated; if not, a new profile
is created.

The profile's data and custom traits are then enriched with new data from the event, updating or adding new attributes
as necessary. Session management ensures that new sessions are created or existing ones are updated to reflect ongoing
interactions. The metadata is updated to reflect the latest changes, maintaining an accurate record of profile
modifications and their sources.

## Automation

### [Triggers](components/trigger.md)

In the Tracardi system, [triggers](components/trigger.md) determine which [workflow](components/workflow.md) should be
executed when an [event](components/event.md) arrives. A rule consists
of a condition and a workflow name. When an event is received, the system evaluates the rule's condition to determine if
it is met. If the condition is met, the associated workflow is executed.

The condition of a [trigger](components/trigger.md) includes two required elements and one optional element: the event
type and the [event](components/event.md)
source are required. The condition is considered met if the event is of a specified type and originates from a specified
source. Optionally, the triggering can be restricted based on user consents. For example, if a user has not consented to
data enhancement, the workflow responsible for enhancing profiles will not be executed.

Triggers in Tracardi create a direct link between incoming [events](components/event.md) and
the [workflows](components/workflow.md) that should be triggered in
response. By defining appropriate rules, you can automate workflow execution based on the arrival of specific events in
the system. This automation enables efficient and responsive handling of various event-driven scenarios.

### [Workflow](components/workflow.md)

A [workflow](components/workflow.md) is a series of actions that are executed in response to
an [event](components/event.md). When an event is matched with a [workflow](components/workflow.md) ,
the actions in the workflow are executed according to the defined graph of nodes and connections.

In Tracardi a [workflow](components/workflow.md) is represented as a graph of nodes, with actions being assigned to
individual nodes. The
connections between nodes represent the flow of data from one action to another. Actions may perform a variety of tasks,
such as copying data from the event to a user profile, saving the profile, querying for additional data, sending data to
another system, or emitting a new event.

Actions in a [workflow](components/workflow.md) may be executed one after another, or they may be run in parallel. This
allows for a high degree
of flexibility in defining the sequence and execution of actions within a workflow. By constructing the appropriate
graph of nodes and connections, it is possible to create complex, multi-step workflows that perform a wide range of
tasks in response to events.

### Actions

In the Tracardi system, an action is a single task that is performed as part of a [workflow](components/workflow.md). An
action consists of input
and output ports, which are used to receive and send data, respectively. The input ports of an action are used to
receive data from other actions or from external sources, while the output ports are used to send data to other actions
or external systems.

An action is essentially a piece of code that performs a specific task within the Tracardi system. The input ports of an
action are mapped to the input parameters of a function in the code, while the output ports are mapped to the return
values of the function. This allows actions to be chained together in a workflow, with the output of one action being
passed as the input to the next.

Tracardi can be extended by programmers who write custom code and map it to an action, which is then visible as a node
in the workflow editor. An action may also be referred to as a node or an [action plugin] within Tracardi.

## Other definitions

### [Customer consent](definitions/consent.md)

Customer [consent](definitions/consent.md) refers to the process of obtaining permission from an individual to collect,
use, or share their
personal data. This can be done through a variety of means, such as a written or oral agreement, a click-through on a
website, or through the use of a consent form. User/Customer [consent](definitions/consent.md) is an important principle
in data privacy laws, as it allows
individuals to control their own personal information and to make informed decisions about how it is used.

Tracardi can store different types of user consents. It is used to automatically enforce data compliance with customer
consents.

### Data compliance

Data compliance refers to the practice of adhering to laws, regulations, and guidelines related to the handling,
processing, and storing of data. This includes protecting the privacy and security of individuals' personal information,
as well as ensuring that data is collected, used, and shared in a transparent and ethical manner. Data compliance is
important because it helps to build trust and confidence in the way that organizations use data, and it helps to prevent
data breaches, misuse, and abuse.

Tracardi can ensure data compliance on the event property level. Meaning you can set a rule that will erase data if user
did not allow you to store certain data in Tracardi.

### Identification point

An identification point is a feature that allows the system to identify customers during their journey. When this point
is set, the system will monitor for events that can be used to match the anonymous customer's identified profile.

To give an analogy, think of an identification point like the ones at an airport or during a police check. You stay
anonymous until there is a moment when you need to show your ID. This is an identification point. At this point, you are
no longer anonymous. The same goes for Tracardi, once you identify yourself, all your past events become part of your
identified profile. If identification happens multiple times on different communication channels, all the anonymous
actions will become not anonymous anymore.

For example, if a customer's profile in the system has an email address that matches the email delivered in a new event,
then the system can match anonymous customer data with the existing profile and merge all previous interactions/events.

In simpler terms, an identification point is a method the system uses to recognize customers and maintain consistent
information about them throughout their journey. It's also called a custom identification point to differentiate it from
automatic identification. Automatic identification is used by the Automatic Profile Merging mechanism, which employs
predefined keys like email addresses to detect and merge duplicate profiles.

### Automatic Profile Merging (APM)

Automatic Profile Merging (APM) in Tracardi is a background service that identifies and consolidates duplicate user
profiles automatically. This mechanism ensures that the information related to a user remains consistent and
comprehensive,
improving the quality of the data and providing a unified view of each user. APM uses predefined keys such as email
addresses, phone numbers, or other unique identifiers to detect duplicate profiles. These keys are critical pieces of
information that are likely to be unique to each user.Example: An email address is used as a merging key to identify
if two profiles belong to the same user.

### Event Validation

Event validation is the process of ensuring that incoming event data meets predefined criteria and conforms to expected
formats before it is processed, stored, or used within workflows. This is a crucial step to maintain data integrity,
consistency, and reliability across the system.

### Event Reshaping

Event reshaping refers to the process of transforming or modifying event data to fit specific
requirements or formats before further processing or storage. This functionality is critical for ensuring that events
captured from various sources are standardized, enriched, and made consistent for analytics, personalization, or any
other downstream processing.

### Event Mapping

Event mapping involves transforming the event properties into event traits. Traits are index within the system and
properties are not. Mapping events cause the data to be searchable when put in to the event traits. Mapping may include
renaming fields, converting data schema, etc.

### Event to Profile Mapping

Event to Profile Mapping in the context of Tracardi (or similar customer data platforms) refers to the process of
associating incoming events with user profiles. This mapping ensures that the actions and behaviors recorded in the
events are accurately reflected in the corresponding user profiles. Events are referenced in profile history
automatically.

Once an event is mapped connected with a profile, it can be used to enrich the profile with additional information. This
could
include updating the profile with new attributes, preferences, interests, or any other relevant data points derived from
the event properties or traits.

Profiles are continuously updated as new events are collected. This dynamic updating ensures that the profiles remain
current and reflect the latest customer data and interests.

### Audience

An audience is a group of users or profiles that have been segmented based on specific criteria or
behaviors. Audiences are created to target users more effectively for marketing campaigns, personalized content, and
other customer engagement strategies. Audiences are defined by setting criteria that profiles must meet to be included.
These criteria can be based on various attributes such as demographic information, behaviors, interactions, or any other
data points collected in the customer profiles. Example: An audience could be defined as users who have made a purchase
in the last 30 days and have an email address.

