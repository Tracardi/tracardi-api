# Could you please explain why there is no drop-down list or other options in the ‘destination’ field in the outbound traffic?

In Tracardi, a "destination" in the outbound traffic settings is a location or service where you can send or store
processed data. However, to use the destination field, you first need to create a "resource." A resource in Tracardi is
an external entity or service that a plugin can interact with, such as databases, APIs, or other systems. These
resources are crucial for storing the configuration data necessary for connecting and interacting with these external
entities.

As of version 0.8.2, Tracardi supports the following resources for sending data to:

1. REST API endpoint
2. RabbitMQ
3. Mautic

Without setting up one of these resources, the destination field won't offer any dropdown options or other choices.