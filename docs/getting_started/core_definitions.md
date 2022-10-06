# Tracardi Core Definitions

In order to understand how Tracardi CPD works you will need to learn the following definitions.

## Traffic

Tracardi is able to receive and send data. Therefore, the system defines two types of traffic. Incoming, i.e. systems that
are able to send data to Tracardi. These will be websites, internal systems and services. Basically, logged inbound
traffic is defined by the id that tracardi creates and which we use to identify the traffic.

The second type of traffic is outgoing traffic. These are external systems to which we send data or send data inquiries.

!!! Tip

    In the system, we call incoming traffic - event sources.
    In the system, we call outgoing traffic - resources.

### Event source

In order to kick-start your new project with Tracardi, you must create a new event source. That source will give you an
identifier which when attached to your track calls will start collecting data about your users.

!!! Warning

    Some sources may require user consent to collect data from this source. A web page requires consent from the user to
    collect and store their data.

### Resource

Resources are data sets or services that we query for data. They often require authentication and therefore during their
creation we will be asked for passwords or tokens. Additionally, by creating resources we will be asked to provide 
access to test and production resources.

Tracardi allows you to [test your internal processes](../flow/index.md). Therefore, a workflow in test mode must connect 
with test resources, so it does not to make changes, that could cause problems in production environment.

!!! Info

    The part of the resource definition that contains sensitive data is encrypted. 

## Session

A session is a data often associated with a visit. As long as the session remains unchanged, the visit lasts. The session id is
set when sending data to Tracardi. It is under the control of the client program. The session often contains data about the 
context in which the event was launched, it can be, among others, the type of device, operating system, etc.

!!! Note
    
    A characteristic feature of the session is that the data assigned to it are usually temporary, volatile.


## Event

Events represent something that is happening at a given time. They can be used to track
visitor behaviour. Examples of events may include a click on a link on a web page, a login, a form submission, a page
view or any other action that needs to be tracked, e.g. purchase order. Events can pass additional data such as user
name, purchased item, viewed page, etc.

Site events are triggered when JavaScript is executed on the selected page or an API query to `/track` endpoint is
made. Since the tracking code is on every page, it can emit events. The events and their types are configurable by you.
Additionally, you configure what data is to be sent for each event.

Events can be stored inside Tracardi or just passed to workflow to be processed outside Tracardi.

!!! Note 

    Tracardi has 2 types of event. Event with profile and without profile. Read about event 
    in [Event's Core Definitions](../events/index.md)

## Rule

Rules define which workflow is to be executed when an event arrives in the system. Rules consist of a condition and
workflow name. If a condition is met then the flow starts to run. The condition has two elements: event type and
source. If the event is of a certain type and comes from a given source then the defined workflow is executed. 

The rules link events to the workflow.

## Workflows

Workflow is a graph of actions that will run when an event is matched with workflow. Actions may run one after another or in
parallel. Workflow is represented as a graph of nodes and connections between them. Actions are assigned to nodes. Data
flow from action to action is represented by connections between nodes. Actions may perform different tasks such as
copying data from the event to profile, save profile, query for additional data, send to another system or emit another
event.

## Actions

Action is a single task in the workflow. Actions consist of input and output ports. Input ports are used to receive
data. On the other hand, output ports send data via connection to another action. Action is basically a code in the
system. Input ports are mapped to input parameters of a function in code when output ports are mapped to the return
values. Tracardi can be extended by programmers who write code and map it with action, which later on is visible in the
workflow editor as nodes. [More on actions](../flow/actions/index.md)

## Profile

A profile is a set of data that represents user data. Profiles are updated based on incoming events and data from
external systems. The profile has public and private data. Private data is usually sensitive data such as name, surname,
e-mail, age, total purchases. Public data is data e.g. on the segment to which the user belongs, last visit, number of
visits, etc.

The profile is updated by the workflow, and more precisely by the actions performed within the workflow. Data from
profiles can be used for marketing campaigns, etc.

## Segment

The segment is the result of the segmentation of customer profiles. A segment can be described by a simple logical rule
or by more complex AI models. The segment is part of the profile. A segment defined in the Tracardi system can be used
in the segmentation workflow. The segment is represented by a simple sentence such as "Customers with high volume of
purchases". 
  
