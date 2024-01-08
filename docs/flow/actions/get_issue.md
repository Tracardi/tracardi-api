# Get Issue

This plugin is used for getting GitHub issue details.

# Version

0.7.4

## Description

The Get Issue action plugin is designed to fetch the details of a specific Github issue. It interacts with the Github
API, using the provided credentials to authenticate.

The plugin operates based on an initially provided configuration which includes references to the Github repository,
owner, desired issue ID and credentials.

The plugin works by calling the GitHub API using HTTP. It employs the GET method to retrieve issue details using
the **issue_id** that is acquired from the configuration.

Upon successful request, it returns the response, which is the details of the issue from Github. However, if the request
fails, the action will return the error from the API call.

# Inputs and Outputs

The plugin takes a payload object as its input.

For outputs, it provides 2 ports:

- **payload** - This output port is triggered when the API call is successful. It returns the details of the issue from
  Github.
- **error** - This port is triggered when the API call is unsuccessful and returns the error response from the API call.

The Get Issue action cannot commence a workflow. It depends on the input data received from another plugin to execute.

# Configuration

The Get Issue action requires the following configuration:

- **resource**: This field should contain the credentials for the GitHub account.
- **owner**: This is the GitHub username. The GitHub username is used to establish a connection to the correct GitHub
  account.
- **repo**: This is the name of the GitHub repository.
- **issue_id**: ID of the GitHub issue. This is the ID number of the specific issue to be fetched from Github.
- **timeout**: This field allows you to set a timeout value for the call to the GitHub API. The value should be a positive
  integer indicating the maximum allowed time (in seconds) to fetch data from the API.

# JSON Configuration

Example configuration in JSON format:

```json
{
  "resource": "your-resource",
  "owner": "your-github-username",
  "repo": "your-repo-name",
  "issue_id": "number-of-the-issue",
  "timeout": 30
}
```

# Required resources

The Get Issue action requires the following resources:

- A valid GitHub account with the required access to make API calls.
- GitHub credentials added to Tracardi in the Resources section.

# Errors

If an error occurred during the run of the plugin, there will be an error output with the response from Github,
including the status and an error message. This error may occur if the GitHub API call was unsuccessful. This could be
due to invalid credentials, an issue with the connection, a non-existent or inaccessible repository or issue, or other
reasons that would lead to an unsuccessful HTTP request to the GitHub API.