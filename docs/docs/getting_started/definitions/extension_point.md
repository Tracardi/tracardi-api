# Extension points

Extension points refer to parts of the system that are designed to be easily extended or customized to
enhance functionality. These extension points allow users to add new capabilities to Tracardi by integrating custom
modules, plugins, or external services written in Python. The main extension points in Tracardi include:

1. **Inbound Traffic Extension Point**: This allows for the creation of new event sources using various types
   of data
   bridges. Users can develop custom data bridges to gather information from different sources or to generate data in
   unique ways. Examples include implementing API bridges, such as a RabbitMQ API bridge, and redirect bridges for
   collecting data from link clicks.

2. **Outbound Traffic Extension Point**: This includes destinations that allow orchestrating data to external systems.

3. **Resource/Extensions**: Tracardi supports a wide range of extensions that can be installed to integrate with various
   external services. These extensions enable Tracardi to interact with different APIs, databases, and third-party
   platforms, thereby extending its core functionalities. Examples include integrations with services like
   ActiveCampaign, Airtable, Amplitude, AWS IAM, and many more.

4. **Plugins**: That are parts of the automation process and allow processing events and profiles using the graphical
   workflows.

By leveraging these extension points, users can tailor Tracardi to meet specific needs, ensuring that it fits seamlessly
into their existing workflows and systems. This modular approach enhances the flexibility and scalability of Tracardi,
making it a powerful tool for managing customer data and interactions.