# Sequencer Matcher

The Sequencer Matcher plugin is used to look for a sequence of events in a given list of events. It allows you to define a sequence of events and check if that sequence occurs in the list of events. This plugin is part of the Tracardi Pro License.

## Description

The Sequencer Matcher plugin searches for a sequence of events in a delivered list of events. It compares the defined sequence of events with the events in the list and determines whether the sequence occurs. The plugin provides options to control the matching behavior, such as strict ordering and disallowing intermediate events.

# Inputs and Outputs

This plugin has one input:

- **payload** (dict): This port accepts a payload object.

This plugin has three outputs:

- **true**: Returns the defined sequence of events if the sequence is found in the list of events.
- **false**: Returns the defined sequence of events if the sequence is not found in the list of events.
- **error**: Returns an error message if an exception occurs during the execution of the plugin.

# Configuration

The configuration of the Sequencer Matcher plugin includes the following parameters:

- **Sequence**: Type the sequence of events to look for.
- **List of events**: Type the reference to the list of events. This is usually the output of the "Event sequence" action, which returns the list of events at `payload@sequence`.
- **Disallow intermediate events**: If enabled, the defined sequence must occur in the precise order without any intermediate events. For example, if the sequence is [event1, event3], it will match [event1, event3], but not [event1, event2, event3]. If intermediate events are allowed, [event1, event2, event3] will be considered a valid match for [event1, event3].

Here is an example configuration:

- Sequence: [event1, event2, event3]
- List of events: `payload@sequence`
- Disallow intermediate events: Yes

# Required resources

This plugin does not require external resources to be configured.

# Errors

The Sequencer Matcher plugin may encounter the following error:

- **Exception message**: This error occurs when an exception is raised during the execution of the plugin. The error message provides details about the specific exception that occurred.

Note: The payload will be returned along with the error message in the **error** output port.