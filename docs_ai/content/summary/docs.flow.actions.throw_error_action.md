The Throw Error plugin is a useful tool for ending a workflow with a given error message. It takes any payload as input
and does not have any output ports. The configuration for this plugin requires a JSON object with a "message" field,
which should contain the desired error message. This message will be displayed when the workflow is ended with the Throw
Error plugin. This plugin is useful for providing more detailed information about why a workflow has failed, and can be
used to help debug any issues that may arise.