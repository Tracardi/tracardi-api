# How to Add a New Destination Type in Tracardi

Integrating a new destination type in Tracardi enhances its functionality and customizability. This comprehensive guide
provides a step-by-step approach to adding a new destination type, using Apache Pulsar as an example.

## Detailed Steps

### Step 1: Locate the Destination Code

- The destination code resides in `tracardi/process_engine/destination`.

### Step 2: Extend `DestinationInterface`

- Your new destination class should extend `DestinationInterface`.
- This interface offers a foundational structure for your destination class.

```python
class DestinationInterface:
    # Constructor with essential parameters
    def __init__(self, debug: bool, resource: Resource, destination: Destination):
        # Initialization of properties
        self.destination = destination
        self.debug = debug
        self.resource = resource

    # Method to dispatch data to profiles
    async def dispatch_profile(self, data, profile: Profile, session: Session):
        pass

    # Method to dispatch data on events
    async def dispatch_event(self, data, profile: Profile, session: Session, event: Event):
        pass
```

### Step 3: Implement Required Methods

- Implement `dispatch_profile` and `dispatch_event` methods to manage data dispatching to the destination.

### Step 4: Understand the Class Properties

- `Resource`: Manages user-selected resource settings. See [How to add resource](resource_dev.md) for more details on how to add new resources if they are not defined already in the system.
- `Destination`: Handles user-defined destination details.
- `debug`: Indicates the debug mode status.

### Step 5: Utilize Destination Object Properties

- `package`: Name of the destination package.
- `init`: Parameters for initializing destination configuration.
- `form`: Form data structure.
- `description`: Describes the destination.
- `enabled`: Status of activation.
- `tags`: Tags for categorization.
- `mapping`: Details of data mapping.
- `condition`: Conditions for triggering.
- `on_profile_change_only`: Triggers on profile changes.
- `resource`: Linked resource information.
- `event_type`: Type of associated event.
- `source`: Source entity details.

### Step 6: Create a Pulsar Credentials Object and Pulsar topic.

We will need some objects in our example to keep the necessary data. We will need pulsar credentials to connect to credential server, and pulsar topic.


- Define an object to store Apache Pulsar connection details.

```python
class PulsarCredentials(BaseModel):
    host: str
    token: Optional[str] = None
```

- Create an object for configuring Apache Pulsar topics.

```python
class PulsarTopicConfiguration(BaseModel):
    topic: str
```

### Step 7: Develop the Pulsar Connector

- Implement the Pulsar connector class to handle communication with Apache Pulsar.

```python
class PulsarConnector(DestinationInterface):
    def _dispatch(self, payload):
        # Exception handling and setup for Pulsar client
        try:
            # Credential selection based on debug mode
            credentials = self.resource.credentials.test if self.debug else self.resource.credentials.production
            credentials = PulsarCredentials(**credentials)

            # Retrieve and apply destination configuration
            init = self.destination.destination.init
            config = PulsarTopicConfiguration(**init)

            # Setting up the Apache Pulsar client
            if credentials.token:
                client = pulsar.Client(
                    credentials.host,
                    authentication=pulsar.AuthenticationToken(credentials.token)
                )
            else:
                client = pulsar.Client(
                    credentials.host
                )
            producer = client.create_producer(config.topic)
            payload = json.dumps(
                    payload,
                    default=str
                ).encode('utf-8')
            producer.send(payload)

        except Exception as e:
            logger.error(str(e))
            raise e

    async def dispatch_profile(self, mapped_data, profile: Profile, session: Session):
        self._dispatch(mapped_data)

    async def dispatch_event(self, mapped_data, profile: Profile, session: Session, event: Event):
        self._dispatch(mapped_data)
```

#### Detailed Description

- `_dispatch` method: Manages the data sending process to Pulsar. When you develop your destination here you may code the logic of your destination plugin. Usually it will be some connection to external system. 
- Authentication: Uses `PulsarCredentials` for Pulsar connection.
- Credential Selection: Chooses credentials based on `debug` mode.
- Configuration: Retrieves settings from `PulsarTopicConfiguration`.
- Connection: Establishes a Pulsar client and sends the payload.

#### Sending Message to Pulsar

```python
# Get Client
if credentials.token:
    client = pulsar.Client(
        credentials.host,
        authentication=pulsar.AuthenticationToken(credentials.token)
    )
else:
    client = pulsar.Client(
        credentials.host
    )

# Get producer
producer = client.create_producer(config.topic)

# Encode payload
payload = json.dumps(
    payload,
    default=str
).encode('utf-8')

# Send
producer.send(payload)
```

- This code establishes the Apache Pulsar client and dispatches the payload to the specified topic.

## Conclusion

Following this tutorial, you can effectively set up a new destination type in Tracardi, exemplified here with Apache
Pulsar. Ensure your implementation complies with the `DestinationInterface` and its requirements. For further guidance,
consult existing destination types or the Tracardi documentation for more insights.