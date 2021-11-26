# Workflow

Flow is a central mechanism of event processing. Workflow is a series of actions connected into graph. The actions are
run one after another to fetch, process, store the data. The actions (sometimes called nodes) may do different things,
such as fetching the data from external databases, storing data in profile, sending data to external services, etc. The
list of action nodes is constantly extended.

## Actions

Tracardi is an extendable system. It is build in a way that anyone with basic knowledge of python can add new action
nodes, so you can find a lot of plug-ins for Tracardi on the Internet. New actions can be installed on the system simply
by adding its module name. Tracardi will then download the plugin code and install it.

### Action configuration

Most of the actions needs configuration. It is done by filling the configuration file in JSON format. Most of
none-technical user are not familiar with JSON so the action nodes come with plain forms that fill the JSON
configuration automatically after the user saves the data from the form. There is no need for the user to manually edit
JSON files.

There are cases when IT personnel wants to inspect the configuration so the JSON file is also visible in the action
configuration in the Graphical User Interface. Information edited in JSON is automatically visible in forms, as well.

### Action documentation

This manual provides a detailed workflow actions documentation. It documents how to use and configure the plugin. The
information provided shows how to configure the plugin using the JSON configuration file. Configuration via forms should
be self-explanatory so there is no additional documentation for this.

## Flow staging

Tracardi automatically saves flow changes. This means that any change or error in workflow could break the running
system. Therefore, workflows are in 3 different stages. One is production stage. This is the stage when the workflow is
running and the data is processed. This workflow can not be changes. Well it can, but then it is automatically copied
and a copy is marked as development stage. So at the same time we have a deployed production workflow (that is running)
and a copy of this workflow that is in development stage that we can edit it. There is a third stage, and it is called
debugging. The workflow is in debugging stage when the developer runs it once to see how the data is processed. 

Changing the state of the workflow is very simple. On the GUI user clicks deploy workflow and current workflow is copied 
to production.




