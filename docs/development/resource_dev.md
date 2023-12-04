# How to Add a Resource to Tracardi

This tutorial will guide you through adding a new resource setting to Tracardi. As an example, we will add a setting for
an Apache Pulsar client, which connects to a queue and publishes messages. This is part of a larger tutorial on adding a
destination, another extension of the system.

## Step-by-Step Guide

### 1. Understanding Resource Configuration

All resources in Tracardi are defined in a file called `setup_resource`, which contains the schema for resource
settings. This file is located in the `tracardi/service/setup` folder.

### 2. Examining an Example

Here's an example function that shows available resources:

```python
def get_resource_types() -> List[ResourceSettings]:
    os_resource_types = [
        ResourceSettings(id="api-key", ...),
        ResourceSettings(id="web-page", ...),
        ...
    ]
```

### 3. Determining Required Data

First, figure out the data needed to connect your resource. For Apache Pulsar, the client needs a __host__ and __token__:

This is the example code that we will need to run later when using the resource setting. We can see that __host__ and __token__ are required.

```python
client = pulsar.Client(
    host,
    authentication=pulsar.AuthenticationToken(token)
)
```

### 4. Adding a Resource Setting

Now, add a resource setting for Apache Pulsar at the end of `os_resource_types`:

```python
ResourceSettings(
    id='apache-pulsar',
    config={
        'host': '<host:port>',
        'token': '<token>'
    },
    icon='pulsar',
    tags=['pulsar', 'apache', 'queue'],
    name='Apache Pulsar',
    manual='apache_pulsar_resource',
)
```

### 5. Finalizing the List

The updated list of resources will now include Apache Pulsar:

```python
def get_resource_types() -> List[ResourceSettings]:
    os_resource_types = [
        ResourceSettings(id="api-key", ...),
        ResourceSettings(id="web-page", ...),
        ...
        ResourceSettings(
            id='apache-pulsar',
            config={
                'host': '<host:port>',
                'token': '<token>'
            },
            icon='pulsar',
            tags=['pulsar', 'apache', 'queue'],
            name='Apache Pulsar',
            manual='apache_pulsar_resource'
        )
    ]
```

### 6. Configuring `ResourceSettings`

- `id`: Unique identifier, use resource name with dashes.
- `config`: The required data. This will be resented to the user to fill out.
- `icon`: Name of the resource.
- `tags`: Keywords for searching the resource.
- `manual`: Location of the resource documentation.

### 7. Creating Documentation

Create a simple documentation file named `apache_pulsar_resource.md` with the following content:

```markdown
Apache Pulsar is a free, open-source platform for distributed messaging and data streaming...
```

Place this file in the `tracardi-api` repository under `docs/resources`. It's referenced in `ResourceSettings` and
displayed when creating the resource.

## Conclusion

That's it! You've successfully added a new resource to Tracardi. Now, when you go to resources, you should see your new
resource in the dropdown list. If you need any additional resources for your plugin or destination, follow these steps
to add them to the system.
