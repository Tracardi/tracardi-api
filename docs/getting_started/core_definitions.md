# Tracardi Core Definitions

In order to understand how Tracardi CPD works you will need to learn the following definitions.

## Traffic

Tracardi is able to receive and send data. Therefore, the system defines two types of traffic. Incoming, i.e. systems that
are able to send data to Tracardi. These will be websites, internal systems and services. Basically, logged inbound
traffic is defined by the id that tracardi creates and which we use to identify the traffic.

The second type of traffic is outgoing traffic. These are external systems to which we send data or send data inquiries.

!!! Tip

    In the system, we call incoming traffic - event sources.
    In the system, we call outgoing traffic - destinations.

### Bridge

A bridge is a piece of software that connects two separate systems or applications, allowing them to communicate and exchange data. In Tracardi **a bridge collects data from a particular source**, such as a queue, email, or social media, and transfer it through event source. For example, Tracardi come with an open source API bridge that allows it to collect data from an API `/track` endpoint and transfer it to the system. Commercial versions of Tracardi may come with other types of bridges, such as a Kafka bridge, which allows it to collect data from a Kafka message broker. 

When a new event source is created, the appropriate bridge must be selected to facilitate the collection and transfer of data.


### Event source - inbound traffic

In order to kick-start your new project with Tracardi, you must create a new event source. That source will give you an identifier which when attached to your track calls will start collecting data about your users. Event source needs a bridge that will transfer data to the system.

!!! Note

    An event source may set to be ephemeral, meaning that the data that is received through this type of event
    source is not saved in the system, but is only processed by the workflow. Ephemeral event sources do not 
    store data permanently, and the data is typically only used for the duration of the workflow. This allows 
    for the processing and analysis of data in real-time, without the need for long-term storage.

!!! Warning

    Some sources may require user consent to collect data from this source. A web page requires consent from the user to
    collect and store their data.
   

### Resource

A service resource is a type of resource that refers to a service or application that is accessed over a network or the Internet. Service resources can provide a wide range of functions and capabilities, including data storage, communication, computation, and more.

In Tracardi, resources are data sets or services that can be queried for data. They often require authentication, such as passwords or tokens, in order to access their data. When creating a resource in Tracardi, you may be asked to provide access to both test and production resources.

Tracardi allows you to [test your internal processes](../flow/index.md) by running workflows in test mode. In test mode, a workflow must connect with test resources in order to avoid making changes that could potentially cause problems in the production environment.

!!! Info

    The part of the resource definition that contains sensitive data is encrypted. 

## Session

In the Tracardi, a session is a type of data that is often associated with a visit to a website or application. As long as the session remains unchanged, the visit is considered to be ongoing. The session id is set when data is sent to Tracardi, and it is typically under the control of the client program.

The session often contains data about the context in which an event was launched, such as the type of device, operating system, or other characteristics of the user's environment. This data can be used to understand the context in which events are occurring, and to tailor the response or actions taken in response to those events.

In general, a session is a period of time during which a user is actively interacting with a system or application. Sessions are often used to track the actions and behavior of users over a period of time, and to provide personalized experiences or services based on that data.

!!! Note
    
    One key characteristic of a session is that the data associated with it is usually temporary and volatile.
    This means that the data is typically only stored for the duration of the session, and is not persisted beyond
    that point. As a result, the data in a session is often considered to be ephemeral, and is not relied upon for 
    long-term storage or analysis.


## Event

In the Tracardi, events are representations of something that is happening at a particular time. **Events can be used to track visitor behavior** on a website or application, and they can capture a wide range of actions and interactions. Examples of events may include clicks on links, logins, form submissions, page views, or any other action that needs to be tracked, such as a purchase order. Events can pass additional data, such as a username, a purchased item, or a viewed page, depending on the type of event and the data that is being tracked.

Web site events in Tracardi are typically triggered when JavaScript is executed on a selected page, or when an API query is made to the `/track` endpoint. Since the tracking code is present on every page, it can emit events as users interact with the site. The events and their types are configurable, and it is possible to configure the data that is sent for each event.

Events can be stored inside Tracardi, or they can be passed to a workflow to be processed outside the system. This allows for a wide range of flexibility in terms of how events are tracked and used within the Tracardi system.

!!! Note 

    Tracardi has 2 types of event. Event with profile and without profile. Read about event 
    in [Event's Core Definitions](../events/index.md)
    

## Routing rule

In the Tracardi system, rules are used to determine which workflow should be executed when an event arrives. A rule consists of a condition and the name of a workflow. When an event is received, the system checks the condition of the rule to see if it is met. If the condition is met, the associated workflow is executed.

The condition of a rule has two elements: the event type and the source. If the event is of a certain type and comes from a specific source, the rule's condition is considered to be met, and the associated workflow is executed.

The rules in the Tracardi system provide a link between events and the workflows that should be executed in response to those events. By defining appropriate rules, it is possible to automate the execution of workflows based on the arrival of specific events in the system.

## Workflows

A workflow is a series of actions that are executed in response to an event. When an event is matched with a workflow, the actions in the workflow are executed according to the defined graph of nodes and connections.

In Tracardi a workflow is represented as a graph of nodes, with actions being assigned to individual nodes. The connections between nodes represent the flow of data from one action to another. Actions may perform a variety of tasks, such as copying data from the event to a user profile, saving the profile, querying for additional data, sending data to another system, or emitting a new event.

Actions in a workflow may be executed one after another, or they may be run in parallel. This allows for a high degree of flexibility in defining the sequence and execution of actions within a workflow. By constructing the appropriate graph of nodes and connections, it is possible to create complex, multi-step workflows that perform a wide range of tasks in response to events.

## Actions

In the Tracardi system, an action is a single task that is performed as part of a workflow. An action consists of input and output ports, which are used to receive and send data, respectively. The input ports of an action are used to receive data from other actions or from external sources, while the output ports are used to send data to other actions or external systems.

An action is essentially a piece of code that performs a specific task within the Tracardi system. The input ports of an action are mapped to the input parameters of a function in the code, while the output ports are mapped to the return values of the function. This allows actions to be chained together in a workflow, with the output of one action being passed as the input to the next.

Tracardi can be extended by programmers who write custom code and map it to an action, which is then visible as a node in the workflow editor. An action may also be referred to as a node or an action plugin within Tracardi.

For more information about actions, see the [More on actions](../flow/actions/index.md) documentation.

## Profile

A profile is a detailed record or representation of an individual or entity, typically including information about their characteristics, interests, and activities. A profile can be used to summarize and organize data about a customer in a way that is easy to understand and access.

A profile in the Tracardi system is a set of data that represents information about a customer. Profiles can be updated based on incoming events and data from external systems, and they can contain both public and private data.

Private data in a profile is typically sensitive information, such as a user's name, email address, age, and total purchases. Public data in a profile may include information such as the segment to which a user belongs, the last time they visited a website, or the number of visits they have made.

The profile is updated by the workflow, specifically by the actions that are performed within the workflow. The data in a profile can be used for a variety of purposes, such as marketing campaigns and other types of analysis. By updating the profile based on incoming events and data from external systems, it is possible to maintain an up-to-date, comprehensive view of a customer.

## Segment

In the Tracardi system, a segment is a group of customer profiles that have been identified and grouped together based on shared characteristics or behavior. A segment can be defined using a simple logical rule or by more complex artificial intelligence (AI) models.

Once a segment has been defined, it becomes a part of the customer's profile. A segment defined in the Tracardi system can be used in the segmentation workflow, which allows for targeted marketing and other types of personalized experiences or services.

A segment is typically represented by a simple key, such as "high-volume-customers," and is described by a brief summary or description, such as "Customers with a high volume of purchases." This allows for easy identification and understanding of the characteristics or behavior that define a particular segment.
  
## Destination - Outbound traffic

In the Tracardi, a destination is an external system where profile data will be sent if it is changed. A destination requires a specific resource, such as an API endpoint or a queue service, in order to receive and process the data.

Not all resources are available as destinations in the Tracardi system. For more information about outbound traffic and the available destinations, see the [outbound traffic](../traffic/outbound/index.md) documentation.

In general, a destination is a place or system to which data is sent or forwarded for further processing or storage. It can be used to transfer data from one system or application to another, allowing for the integration and exchange of information between different platforms or services.

# Customer consent

Customer consent refers to the process of obtaining permission from an individual to collect, use, or share their personal data. This can be done through a variety of means, such as a written or oral agreement, a click-through on a website, or through the use of a consent form. User consent is an important principle in data privacy laws, as it allows individuals to control their own personal information and to make informed decisions about how it is used. 

Tracardi can store differnet types of user consents. It is used to automatically enforece data compliance with customer consents. 

# Data compliance

Data compliance refers to the practice of adhering to laws, regulations, and guidelines related to the handling, processing, and storing of data. This includes protecting the privacy and security of individuals' personal information, as well as ensuring that data is collected, used, and shared in a transparent and ethical manner. Data compliance is important because it helps to build trust and confidence in the way that organizations use data, and it helps to prevent data breaches, misuse, and abuse.

Tracari can ensure data compliance on the event property level. Meaning you can set a rule that will erase data if user did not allow you to store certain data in Tracardi. 


# Identification point

An identification point is a feature that allows the system to identify customers during their journey. When this point is set, the system will monitor for events that can be used to match the anonymous customer's identified profile.

To give an analogy, think of an identification point like the ones at an airport or during a police check. You stay anonymous until there is a moment when you need to show your ID. This is an identification point. At this point, you are no longer anonymous. The same goes for Tracardi, once you identify yourself, all your past events become part of your identified profile. If identification happens multiple times on different communication channels, all the anonymous actions will become not anonymous anymore.

For example, if a customer's profile in the system has an email address that matches the email delivered in a new event, then the system can match anonymous customer data with the existing profile and merge all previous interactions/events.

In simpler terms, identification point is a way for the system to identify customers and keep their information consistent throughout their journey.

