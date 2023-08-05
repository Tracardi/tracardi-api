# Get Previous Session

The "Get Previous Session" plugin in Tracardi is used to load the n-th last session of the current profile and inject it into the payload. This plugin is useful for retrieving information from previous sessions for segmentation and analysis purposes.

## Inputs and Outputs

- **Input**: This plugin takes any payload as input.

- **Output Ports**:
  - **found**: This port returns the session information if the session was found.
  - **not_found**: This port returns the given payload if the session was not found.

## Configuration

The "Get Previous Session" plugin has the following configuration option:

- **Offset**: This parameter determines the session offset, which is an integer value between -10 and 0 (inclusive). The offset specifies the number of sessions to go back from the current session. For example, an offset of -1 will return the last session, and an offset of -2 will return the second-to-last session.

To configure the plugin, you can use the following JSON format:

```json
{
  "offset": "<number-of-wanted-session-counting-from-current-one>"
}
```

## Example Usage

Here's an example of how the "Get Previous Session" plugin can be used:

```yaml
- get_previous_session:
    offset: -1
```

In this example, the plugin is configured to retrieve the last session of the current profile and inject it into the payload. The session information will be available on the "found" port.

