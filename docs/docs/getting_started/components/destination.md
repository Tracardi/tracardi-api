# Destination

Destination refers to a target endpoint or system where processed profiles or events are sent. This can include
various types of systems or services such as APIs, databases, messaging queues, and more. The concept of destinations is
used to route the profile or events to these external systems for further processing, storage, or
analysis. To function, a destination requires a specific [resource](resource.md), such as an API endpoint or queue
service, to receive and process the data.

Destinations are defined in the system and can be configured to handle asynchronous operations. This setup ensures that
data is transmitted to the destination efficiently without blocking other operations within the workflow. The definition
and configuration of destinations can be found within the outbound traffic settings, where you can specify the type of
destination, connection details, and any required authentication parameters.

For instance, a typical destination setup might involve configuring a REST API [resource](resource.md) where you would specify the URL,
HTTP method (GET, POST, etc.), headers, and any necessary payload formatting in the destination configuration. The
system can then route processed data to this endpoint as part of its execution flow.

## Available destinations

Depending on the system version, the list of available destinations may change. The easiest way to check the available
ones is to go to the `resources/extensions` tab and filter out `type/destinations`. To use one of them you need to
install.

Typical destination would be:

* Kafka
* Apache Pulsar
* Rabbitmq
* Remote API
* Mautic

Destinations are an [extension point](../definitions/extension_point.md) in tracardi meaning you can easily code your
own destination and add it to the system core.