# Data collection

Data collection in Tracardi is a comprehensive process responsible for gathering and ingesting data into the system.
This process begins with collecting data from various event sources through a defined bridge and involves multiple
stages to ensure data is accurately processed and stored.


## Stages

| Stage                 | Description                                                                                                                                                                                          |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Source validation`   | Tracardi must have event source defined and enabled in the system.                                                                                                                                   |
| `Event mapping`       | Tracardi can validate the event data schema, map event and reshape its schema if needed.                                                                                                             |
| `Identity resolution` | At this point the profile is identified if it exists in the system or a new anonymous profile is created. Tracardi checks if the profile can be merged with other profiles that seems to be the same |
| `Event reshaping`     | Tracardi can change the event schema if needed.                                                                                                                                                      |
| `Event collection`    | Tracardi saves the event.                                                                                                                                                                            |
| `Event routing`       | Tracardi reads a rule that defines which workflow, or destination should be triggered.                                                                                                               |

## Details

1. **Source Validation**

   Description: Tracardi must have the event source defined and enabled in the system.
   Detail: Ensures that the incoming event is from a recognized and active event source. The event source identifier is
   checked against the registered event sources in Tracardi.

2. **Event Mapping**

   Description: Tracardi can validate the event data schema, map the event, and reshape its schema if needed.
   Detail: The event's data is validated to ensure it meets the expected schema. If necessary, the event data is mapped
   to build events traits, potentially renaming fields or converting data formats for consistency and
   usability.

3. **Identity Resolution**

   Description: Identifies the profile if it exists in the system or creates a new anonymous profile. Tracardi checks if
   the profile can be merged with other profiles that seem to be the same.
   Detail: Tracardi attempts to resolve the identity of the event's originator. If a matching profile exists, it is
   retrieved; otherwise, a new anonymous profile is created. The system also looks for potential merges with existing
   profiles based on predefined keys such as email addresses.

4. **Event Reshaping**

   Description: Tracardi can change the event schema if needed.
   Detail: The event data may be further transformed to match specific workflow requirements or to enhance the data
   before processing. This could involve adding, removing, or modifying event attributes.

5. **Event Collection**

   Description: Tracardi saves the event.
   Detail: The validated and possibly reshaped event data is stored in Tracardi's database. This ensures that the event
   is available for historical analysis and future reference.

6. **Event Routing**

   Description: Tracardi reads a rule that defines which workflow must be triggered by the event.
   Detail: Based on predefined routing rules, Tracardi determines which workflow should handle the event. These rules
   consider the event type, source, and possibly other conditions.



