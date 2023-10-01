# Can I only process the event?

Yes, you have the option to only process an event without saving it permanently in the system. There are two approaches
to achieve this:

1. Set the event source to be ephemeral: By designating the event source as ephemeral, the data received through this
   type of event source is processed by the workflow without being saved in the system. Ephemeral event sources are
   typically used for real-time processing and analysis, allowing for temporary data usage during the workflow without
   the need for long-term storage.

2. Adjust the event configuration: Within the event payload, there is an `options` attribute that provides additional
   instructions for event processing. By setting the `saveEvent` option to `false`, the event will be processed but not
   permanently saved in the system. This allows you to perform the necessary operations and derive insights from the
   event without persisting it.

These options give you the flexibility to choose whether to save the event or solely focus on its processing based on
your specific requirements and use case.