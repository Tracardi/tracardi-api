# Resource Definition

A resource is a configurable object that represents an external service, data source, or API that Tracardi
can connect to and interact with. Resources are used to manage credentials, configurations, and connections to these
external systems, allowing Tracardi to perform actions such as data retrieval, sending data, and integrating with
third-party services.

## Components of a Resource

1. **Resource ID**: A unique identifier for the resource.
2. **Resource Name**: A descriptive name for the resource.
3. **Resource Configuration**: The configuration details needed to connect to the resource. This typically includes
   parameters such as URLs, API keys, authentication credentials, and other settings.
4. **Resource Type**: The type of resource, which determines the kind of connection and interactions that Tracardi will
   have with it (e.g., database, API, messaging service).
5. **Tags**: Keywords or tags associated with the resource to help categorize and filter resources within the system.

## Creating and Managing Resources

Resources are created and managed within Tracardi's GUI. Here are the steps typically involved:

1. **Define the Resource**: Specify the resource details, including its name, type, and configuration settings.
2. **Configure the Resource**: Input the necessary configuration parameters, such as API URLs, authentication
   credentials, and any other required settings.
3. **Save the Resource**: Save the resource configuration, making it available for use in workflows and other parts of
   the system.

## Using Resources in Workflows

Resources can be utilized in workflows to perform various actions, such as fetching data from an API, sending data to an
external service, or integrating with other systems. Here’s how resources are typically used in Tracardi workflows:

1. **Reference the Resource**: In a workflow node or plugin, reference the resource by its ID or name.
2. **Access the Resource Configuration**: Use the resource's configuration details to establish a connection and perform
   actions.
3. **Execute Actions**: Carry out the desired actions using the resource, such as sending a request to an API or
   retrieving data from a database.

## Example: API Resource

Here’s an example of how an API resource might be configured and used in Tracardi:

1. **Resource Definition** - This is an internal object that is created when using GUI:
    ```json
    {
      "id": "api-resource",
      "name": "Example API",
      "config": {
        "url": "https://api.example.com",
        "method": "GET",
        "headers": {
          "Authorization": "Bearer YOUR_API_KEY"
        }
      },
      "type": "api",
      "tags": ["example", "api"]
    }
    ```

2. **Using the Resource in a Plugin**:
    ```python
    import requests
    from tracardi.service.storage.driver.elastic import resource as resource_db

    class ExampleApiPlugin(ActionRunner):
        config: dict
        credentials: dict

        async def set_up(self, config):
            self.config = config
            resource = await resource_db.load(config['resource']['id'])
            self.credentials = resource.credentials

        async def run(self, payload: dict, in_edge=None):
            response = await self._call_api()
            return Result(port="response", value=response)

        async def _call_api(self):
            url = self.credentials['url']
            headers = self.credentials.get('headers', {})
            response = requests.get(url, headers=headers)
            return response.json()
    ```

## Resource Types

Tracardi supports various types of resources, including but not limited to:

- **API Resources**: For interacting with RESTful APIs.
- **Database Resources**: For connecting to databases like PostgreSQL, MySQL, etc.
- **Messaging Services**: For connecting to messaging platforms like Kafka, RabbitMQ, etc.
- **Storage Services**: For connecting to cloud storage services like AWS S3, Google Cloud Storage, etc.

## Benefits of Using Resources

- **Centralized Configuration**: Resources provide a centralized way to manage connection details and credentials for
  external services.
- **Reusability**: Once defined, resources can be reused across multiple workflows and plugins, reducing duplication and
  configuration overhead.
- **Security**: Resources allow for secure handling of sensitive information like API keys and authentication
  credentials.

## Credentials

Most of the resources need credentials that are used to connect to the resource. Credentials are attached to resource
and stored inside Tracardi.

### Credentials caching

Credentials are subject to caching. That means that after they are changed you will not see the change immediately but
after a certain number of seconds. Usually 60 seconds.

## Extending Resource Types

Resources are an [extension point](../definitions/extension_point.md) in tracardi meaning you can easily code your
own destination and add it to the system core.
