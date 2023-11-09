# List Issues

This is a Tracardi plugin which allows for the listing of GitHub issues.

# Version

This documentation was created for the "List Issues" plugin version 0.7.4.

## Description

The "List Issues" plugin is designed to retrieve issues from a specified GitHub repository. It begins with pre-defined configuration parameters, including a GitHub repository, which are stored in a dictionary form.

Next, a resource is loaded and the credentials from the configuration dictionary are used to initialise a GitHub client. 

The final step is the execution of the **list_issues()** function. This retrieves the list of issues from GitHub and returns the result based on the response's 'status' parameter.

If the status is either 200, 201, 202, 203, or 204, the result is returned at the payload port. On the other hand, if the status is different than the aforementioned, the result is returned at the error port.

For example, if an error arises during the execution, you will receive a return with an error port.

Please note that the returned result is dependent on the status of the response.

# Inputs and Outputs

The plugin takes one input:

- "payload": This port takes the payload object as an argument.

It gives two outputs:

- "payload": This port returns the issues data from the GitHub repository.
- "error": This port returns an error message if the **list_issues()**function returns a status other than 200, 201, 202, 203, or 204.

Note that this plugin cannot start a workflow.

# Configuration

The following are all configuration parameters for the plugin:

- "resource": This specifies the GitHub API resource and should be provided as a string. 
- "owner": This is the username of the GitHub account owner. 
- "repo": This specifies the GitHub repository from which you want to list issues. 
- "timeout": This allows you to set a timeout limit for the GitHub client to fetch the resource.


# JSON Configuration

Here is an example configuration:

```json
{
"resource": "ExampleResource",
"owner": "John Doe",
"repo": "example-repo",
"timeout": 120
}
```

# Required resources

The plugin requires access to the GitHub API, therefore you will need to configure it with your own GitHub repository credentials.

# Errors

If the **list_issues()** function returns a status other than 200, 201, 202, 203, or 204, the response will be returned through the error port.