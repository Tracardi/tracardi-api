# Limiter

This node throttles the workflow execution.

## Description

The Limiter plugin is used to control the rate at which the workflow executes. It allows you to set limits on the number of allowed executions within a defined time range. If the execution exceeds the specified limit, the plugin can either allow the execution to pass through or block it based on the configured parameters.

This documentation is based on version 0.7.3 of the Limiter plugin.

# Inputs and Outputs

## Inputs

The Limiter plugin accepts the following input:

- **payload**: This port takes a payload object as input.

## Outputs

The Limiter plugin provides the following outputs:

- **pass**: Returns the input payload if the execution is not throttled.
- **block**: Returns the input payload if the execution is throttled.

# Configuration

The Limiter plugin supports the following configuration parameters:

- **Number of allowed executions**: Specify the number of allowed passes through this plugin within the defined time.
- **Time range (Time to live)**: Specify the time period (in seconds) that must pass for the limit to be reset to 0.
- **Throttle key identifier**: Select the throttle identifiers. This defines the resource that is protected by this limiter.

# JSON Configuration

Here is an example JSON configuration for the Limiter plugin:

```json
{
    "keys": ["profile"],
    "limit": 1,
    "ttl": 60
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

The Limiter plugin does not throw any specific errors.