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

Workflow has an internal state that is referenced in each action node. Please read about actions and the state they 
hold in [Action's Core Definitions](actions/index.md)


