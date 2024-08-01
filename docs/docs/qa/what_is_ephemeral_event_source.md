# What is ephemeral transactional event source?

An ephemeral transactional event source refers to a type of event source where the data received is not stored
permanently in the system. Instead, it is processed and used only during the workflow. This approach allows for
real-time processing and analysis of data without the requirement of long-term storage. The data is utilized within the
workflow or system for immediate operations and insights, but it is not retained for the long term in the database.

# How to set-up ephemeral transactional event source?

To set up an ephemeral transactional event source, follow these steps:

1. Navigate to the `inbound traffic` / `event source` configuration settings.
2. Locate the specific event source that you want to configure as ephemeral and access its settings.
3. Look for the `advanced options` or advanced settings section within the event source configuration.
4. Within the advanced options, you should find an option related to the transactional event type.
5. Adjust the settings to enable the ephemeral mode for the event source. 
6. Save the changes to apply the ephemeral transactional settings to the event source.

By following these steps, you can configure the event source as ephemeral, ensuring that the data received through this
source is not stored permanently but is processed and used only for the duration of the workflow or a limited period of
time.