# How many events can handle Tracardi?

Tracardi can handle a high volume of events, with the exact number depending on your specific hardware configuration and
network bandwidth. However, Tracardi is designed to be scalable, so you can easily add more resources to handle
increasing event volumes.

In general, Tracardi can handle millions of events per day without any issues. For example, one Tracardi user reported
handling over 50 million events per day with a cluster of 10 Tracardi nodes.

Tracardi is a very thin layer on top of elasticsearch, redis and Apache Pulsar.

Here are some factors that can affect the number of events that Tracardi can handle:

- Hardware configuration: The more CPU cores, RAM, and disk space you have, the more events Tracardi can handle.
- Network bandwidth: The more bandwidth you have, the faster Tracardi can process and store events.
- Event size: The larger your events are, the fewer events Tracardi can handle per second.
- Event processing: The more complex your event processing rules are, the fewer events Tracardi can handle per second.

If you are concerned about the number of events that Tracardi can handle, you can contact Tracardi support for a more
specific assessment. They can help you determine the optimal hardware configuration and network bandwidth for your
needs.