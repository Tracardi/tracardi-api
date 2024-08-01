# Workflow Core Definitions

Flow is a central mechanism of event processing. Workflow is a series of actions connected into graph. The actions are
run one after another to fetch, process, store the data. The actions (sometimes called nodes) may do different things,
such as fetching the data from external databases, storing data in profile, sending data to external services, etc. The
list of action nodes is constantly extended.

## Actions

Tracardi is an extendable system. It is build in a way that anyone with basic knowledge of python can add new action
nodes. That's why you can find a lot of plug-ins for Tracardi on the Internet. New actions can be installed on the system simply
by adding its module name. Tracardi will then download the plugin code and install it. See more about plugins installation 
in plugins section.

### Action configuration

Most of the actions need configuration. It is done by filling the configuration file in JSON format. Most of
none-technical user are not familiar with JSON so the action nodes come with plain forms that fill the JSON
configuration automatically after the user saves the data in the form. There is no need for the user to manually edit
JSON files.

There are cases when IT personnel wants to inspect the configuration so the JSON file is also visible in the action
configuration in the Graphical User Interface. Information edited in JSON is automatically visible in forms, as well.

### Action documentation

This manual provides a detailed workflow actions documentation. It documents how to use and configure the plugin. The
information provided shows how to configure the plugin using the JSON configuration file. Configuration via forms should
be self-explanatory so there is no additional documentation for this.

## Workflow staging

Tracardi automatically saves workflow changes. This means that any change or error in workflow could break the running
system. Therefore, workflows are in 2 different stages. One is production stage. This is the copy of a working workflow. 
This workflow is running and the data is processed. It can not be changed. The second stage is development stage. This is a copy
of a workflow that the user is editing. The change in this workflow is saved every 3 seconds. At some point it will become
a production workflow.

Changing the state of the workflow as simple as clicking deploy button on workflow editor. Then current workflow is copied 
to production. The old production workflow is saved in case we need to revoke the deployed workflow for some reason.

## Workflow internal state

The concept of the "Workflow Internal State" is central to understanding how each workflow operates within a given
context. Workflow runs in a context of curren event, profile, and session.

1. **Event**: Events are the triggers for workflow actions. When an event is sent, it carries essential information,
   including either a "profile_id" or a "session_id," along with the event type and its associated properties.

2. **Event Loading**: When an event is received, the system retrieves the current profile using the provided
   identifier (profile_id or session_id). This step ensures that the system knows which profile is associated with the
   event.

3. **Assignment to Nodes**: The retrieved profile, along with the session and event data, is then assigned to each
   relevant node within the workflow. This means that the workflow maintains an internal state, and this state is
   referenced in each action node. As the workflow progresses, this internal state can change.

4. **Dynamic State**: Throughout the execution of the workflow, the state of the event, profile, and session may undergo
   alterations as various actions are performed. These changes reflect the dynamic nature of workflows, where the
   information associated with the profile, session, and event can be modified based on the sequence of actions.

5. **Persistent Storage**: It's important to note that when the workflow ends, any changes made to the
   profile, session, and event are saved back to the system. This ensures that the updated information is preserved for
   future reference or processing.

In summary, the "Workflow Internal State" refers to the dynamic and evolving set of data that includes events,
profiles, and sessions within a workflow.  Please read about actions and the state they hold in [Action's Core Definitions](actions/index.md)


