# Event Sequence

The Sequencer Query plugin is used to retrieve an events sequence from the database based on a defined time range and
context. It allows you to filter events using a query and set up the context for sequence matching. This plugin is part
of the Tracardi Pro License.

## Description

The Sequencer Query plugin selectively loads events into the payload for a specified time period. It searches for events
that match the defined query and retrieves the sequence of event types. The plugin supports filtering events based on
time range, session, and other criteria. The retrieved sequence can be used for further processing in the workflow.

# Inputs and Outputs

This plugin has one input:

- **payload** (dict): This port accepts a payload object.

This plugin has two outputs:

- **result**: Returns the sequence of event types if the query is successful.
- **error**: Returns an error message if an exception occurs during the execution of the plugin.

# Configuration

The configuration of the Sequencer Query plugin includes the following parameters:

- **Filter events**: Query to filter the events and set up the context for sequence matching. You can reference data by
  using `{{ }}` placeholder. For example, `{{event@properties.product_id}}`.
- **Events must occur in current session**: If enabled, events must be in the current event session. This means that the
  customer traveled the sequence during the current visit.
- **Maximal time span to look for the sequence**: Defines the maximum time span to look for the sequence. The value is
  rounded down to UTC 00:00. For example, a time period of 1 day is not 24 hours but one day.
- **Time unit for the time span**: A unit of measurement for the time span, such as seconds, minutes, hours, or days.

Here is an example configuration:

- Query: `properties.product_id: {{event@properties.product_id}}`
- Events must occur in current session: No
- Maximal time span to look for the sequence: 7
- Time unit for the time span: Days

# Required resources

This plugin does not require external resources to be configured.

# Errors

The Sequencer Query plugin may encounter the following errors:

- **ValueError: Profile event sequencing can not be performed without profile. Is this a profile less event?**: This
  error occurs when the plugin is unable to perform profile event sequencing because there is no profile associated with
  the event. Make sure the event has a valid profile.
- **ValueError: Can not find events in the context of the session when there is no session in the event. Is this a
  profile less or events less event?**: This error occurs when the plugin is unable to find events in the context of the
  session because there is no session associated with the event. Ensure that the event has a valid session when using
  the "Events must occur in the current session" option.

Note: The payload will be returned along with the error message in the **error** output port.

