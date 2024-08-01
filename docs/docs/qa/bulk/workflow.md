# How can I add new action nodes to Tracardi?

Tracardi is designed to be an extendable system, allowing users to add new action nodes easily via plugin classes. By
adding the module name of the desired plugin, Tracardi can install the plugin code, making it available for use within
the workflow. More information on how to write plugins is available in the documentation.

# How are actions installed in Tracardi?

Actions in Tracardi are installed by adding the module name of the desired plugin. Tracardi will automatically read the
plugin code and install it, making the actions available for use in workflows.

# What is the configuration process for actions in Tracardi?

Most actions in Tracardi require configuration. The configuration is done by filling out a configuration file in JSON
format. For the convenience of non-technical users, Tracardi provides plain forms that automatically populate the JSON
configuration based on the data entered in the form. This eliminates the need for manual editing of JSON files.

# How can I access the JSON configuration file for an action?

While most users can configure actions using the provided forms in Tracardi's Graphical User Interface, IT personnel or
advanced users may want to inspect the JSON configuration directly. Tracardi allows access to the JSON configuration
file within the action's configuration, providing visibility and flexibility for advanced configuration requirements.

# Is there additional documentation available for configuring actions?

Yes, this documentation provides detailed workflow actions documentation, including instructions on how to use and
configure each plugin. The documentation covers configuring the plugin using the JSON configuration file. Configuration
via forms is designed to be self-explanatory, so no additional documentation is necessary for that aspect.

# What are the different stages of a workflow in Tracardi?

Workflows in Tracardi have two different stages: production stage and development stage. The production stage is a copy
of the working workflow that is actively running and processing data. It cannot be changed. The development stage is a
copy of the workflow that users can edit and make changes to.

# How does Tracardi handle workflow changes to prevent breaking the system?

Tracardi automatically saves workflow changes to ensure the integrity of the system. This means that any change or error
in a workflow could potentially break the running system. To mitigate this risk, Tracardi uses a staging mechanism where
workflows are maintained in two different stages: development and production. The development workflow is editable and
serves as a sandbox for making changes, while the production workflow is the stable and running version. Users can
deploy the development workflow to production once they are confident that the changes are ready to be implemented.

# How can I change the state of a workflow from development to production?

Changing the state of a workflow from development to production in Tracardi is a simple process. Users can click the "
deploy" button in the workflow editor to initiate the deployment. This action copies the current workflow from the
development stage to the production stage. The previously deployed production workflow is saved, allowing for the
possibility of reverting back to it if needed.

# What happens to the old production workflow when a new one is deployed?

When a new workflow is deployed in Tracardi, the previous production workflow is saved. This allows for easy reversion
in case there is a need to revert back to the previously deployed workflow. The saved old production workflow ensures
that the system remains stable and functional, providing a safety net for managing workflow changes.

# What is the internal state of a workflow in Tracardi?

Each workflow in Tracardi has an internal state that is referenced in each action node. The internal state has the
profile, event, session, flow, and internal memory. Each workflow run in a context of current profile and its event and
session.

