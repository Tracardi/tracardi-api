# How workflow works. What are the steps during workflow execution?

In the context of Tracardi, the event processing within a workflow follows a structured sequence and involves several
key steps:

**Workflow Internal State**:

- **Event**: Events serve as triggers for workflow actions. An event carries crucial information, including a "
profile_id" or a "session_id," the event type, and its properties.
- **Event Loading**: Upon receiving an event, the system retrieves the current profile using the provided
identifier (profile_id or session_id), ensuring the system recognizes which profile is associated with the event.
- **Assignment to Nodes**: The retrieved profile, along with session and event data, is assigned to relevant nodes
within the workflow. This establishes an internal state for the workflow, referenced in each action node. As the
workflow progresses, this internal state can evolve.
- **Dynamic State**: During the execution of the workflow, the state of the event, profile, and session can change
as various actions are performed. This reflects the dynamic nature of workflows, where information associated with
the profile, session, and event can be modified based on the sequence of actions.
- **Persistent Storage**: Notably, when the workflow concludes, any modifications made to the profile, session, and
event are saved back into the system. This ensures that the updated information is retained for future use or
processing.