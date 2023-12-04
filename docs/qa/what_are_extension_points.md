# What are extension points?

Tracardi is a modular customer data platform that allows for easy extension of various parts of its system to enhance
functionality and customization. The main extension points in Tracardi include:

1. **Inbound Traffic Extension Point**: This feature enables the creation of new event sources using different types of
   data bridges. Users can develop custom data bridges to gather information from a variety of sources or to generate
   data in unique ways. This includes the implementation of API bridges, such as a RabbitMQ API bridge, and redirect
   bridges for collecting data from link clicks.

2. **Resources Extensions**: These extensions facilitate the connection to external systems, comprising both resources
   and plugins. An example is the Airtable extension, which includes one resource and two plugins. Tracardi also allows
   the integration of microservices as extensions, providing new functionalities without the need for system updates.
   These microservices are configurable within Tracardi and can interact with various external systems or platforms,
   such as Trello.

3. **Outbound Traffic Extension Point**: This point is concerned with transmitting data from user profiles to external
   systems. It involves installing various destinations within the system, like Maori and RabbitMQ, thereby broadening
   Tracardi's capabilities to interact with external platforms.

4. **Workflow Actions Extensions**: This extension point is related to the addition of process-related actions within
   the Tracardi system, specifically focusing on action plugins used in workflows. These plugins are crucial for
   integrating external systems and services into the Tracardi workflow, allowing for a seamless blend of internal
   processes with external functionalities.

Additionally, the commercial version of Tracardi uses Apache Pulsar Queues, which serve as another extension point.
These queues can be utilized to consume events and profiles, as well as to trigger actions in external systems. This
functionality further enhances Tracardi's ability to interact dynamically with a range of systems and services, making
it a versatile tool for managing customer data and automating marketing processes.