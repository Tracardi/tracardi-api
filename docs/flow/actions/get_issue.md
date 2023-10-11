# GitHub Issue Retrieval Component

## Description
The GitHub Issue Retrieval component is designed to fetch a single issue from a GitHub repository using user-defined input parameters. It allows you to configure the resource, specify the owner of the repository, provide the repository name, and set a timeout for the issue retrieval operation.

## Inputs

### Resource Configuration
- **Type:** String
- **Description:** Specifies the resource configuration, which might include details like API endpoints, authentication credentials, and other relevant configuration options.

### Owner
- **Type:** String
- **Description:** Specifies the owner of the GitHub repository from which the issue will be retrieved.

### Repository Name
- **Type:** String
- **Description:** Specifies the name of the GitHub repository from which the issue will be retrieved.

### Issue ID
- **Type:** Integer
- **Description:** Specifies the ID of the issue to be retrieved from the repository.

### Timeout
- **Type:** Integer (in milliseconds)
- **Description:** Sets a timeout for the issue retrieval operation. If the retrieval process exceeds this timeout, an error will be generated.

## Outputs

### Issue
- **Type:** GitHub Issue object
- **Description:** Returns the retrieved GitHub issue, including details like title, description, comments, and more.

### Error
- **Type:** Error Message
- **Description:** Returns an error message if any issues occur during the retrieval process, such as connection problems or invalid input parameters.

## Example Usage

Here's an example of how you can use the GitHub Issue Retrieval component in Python:

resource_config = "https://api.github.com"
owner = "example_user"
repository_name = "example_repo"
issue_id = 123
timeout = 5 seconds

# Call the GitHub Issue Retrieval component
issue, error = retrieve_github_issue(resource_config, owner, repository_name, issue_id, timeout)

```python

if issue:
    print("GitHub Issue Title:", issue["title"])
    print("GitHub Issue Description:", issue["description"])
    # Process the retrieved issue data here
else:
    print("Error during GitHub issue retrieval:", error)
