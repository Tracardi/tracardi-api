# What is bridge?

A bridge is a piece of software that serves as a communication link between two
separate systems or applications. Its primary function is to facilitate the exchange of data between these systems,
allowing them to interact seamlessly.

Specifically, in Tracardi, a bridge is responsible for collecting data from a particular source, such as a queue, email,
social media, or any other external system, and then transferring that data to an event source within Tracardi. The
event source, in turn, processes and handles the incoming data as part of Tracardi's workflows and data processing
capabilities.

For example, Tracardi may come with an open-source API bridge that enables the collection of data from an API's `/track`
endpoint. This data can then be seamlessly transferred to the Tracardi system for further processing and analysis.

Different types of bridges may be available based on the version of Tracardi being used. For instance, commercial
versions of Tracardi might include bridges for integrating with various data sources, such as a Kafka bridge that allows
the collection of data from a Kafka message broker.

In summary, a bridge in Tracardi acts as a conduit, connecting external data sources to the Tracardi system, enabling
smooth data transfer and integration.