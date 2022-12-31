# Event's Core Definitions


## Event properties

Event properties refer to the characteristics or attributes of an event that can be recorded and analyzed. These properties can provide valuable information about the event, such as the time it occurred, the location, the participants, and any relevant details or context. In the context of event reshaping, event properties may be separated out from the rest of the data in order to facilitate their analysis and interpretation. Event properties can be used to better understand the event, and can be useful in identifying trends, patterns, or relationships within the data.


## Profile less event

A profile-less event is an event that cannot be assigned to any particular profile. This means that it does not contain sufficient information to identify a specific user or entity associated with the event.

An example of a profile-less event might be an event that describes an error in the system. In this case, the event would provide information about the error itself (such as the type of error, the location, and any relevant details), but it would not be tied to a specific user or profile. 

Profile-less events can still be useful for understanding the use journey, but they may not provide as much context or insight as events that are tied to specific profiles.

## Event states

Events can take the following states:

| State         | Description                |
|---------------|----------------------------|
| `received`    | Event loaded               |
| `validated`   | Event was validated        |
| `processed`   | Event was processed        |
| `warning`     | Workflow logged warnings   |
| `error`       | Workflow returned errors   |
| `ok`          | Event wsa processed without errors |

# Events synchronization

