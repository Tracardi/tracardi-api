# Tag Event

Tag Event is a Tracardi action plugin that ads tags to the current event.

# Version

The documentation was created for version 0.8.0 of the Tag Event plugin.

## Description

The Tag Event plugin, as its name suggests, is primarily used to add tags to the current event. This plugin does not modify the payload.


# Inputs and Outputs

Tag Event plugin accepts one input called "payload". While it also returns the input payload on the output port "payload".

Sample Input:
```markdown
{
  // payload to be processed by the plugin
}
```

Sample Output:
```markdown
{
  // returned input payload
}
```

# Configuration

The plugin is configured using the following parameters:

- `tags`: A string containing the tags to be added to the current event.

# JSON Configuration

The initial configuration of the plugin can look like:

```markdown
{
  "tags": "tag1, tag2, tag3"
}
```

In the above configuration, the plugin will add the tags 'tag1', 'tag2', and 'tag3' to the current event.

# Required resources

This plugin does not require external resources to be configured.

# Errors

Tag Event plugin does not return any error under normal conditions.

If you see any error, it might be related to internal problems in the system or issues with the payload schema. Please check your configuration parameters and payload.