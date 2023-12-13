# Resolve conditions

This plugin returns results with a resolved condition set, designed to evaluate specific conditions within a workflow
and provide outcomes based on these evaluations.

# Version

0.8.2

## Description

The Resolve conditions plugin operates by taking a set of user-defined conditions and evaluating them against provided
data. Each condition is assessed to determine if it is true or false. For instance, you might want to check if a profile
has given marketing consent or if the current weather condition is rain. The plugin processes these conditions and
returns an object indicating the outcome of each condition.

The plugin achieves this by using the __Condition__ class to evaluate each condition against the provided payload. The
payload is accessed using a __DotAccessor__, allowing the plugin to extract specific data points based on dot notation,
like __profile@consents.marketing__. Each condition is defined in the plugin's configuration and is checked against the
payload. The results are then compiled into an object, with each key representing a condition and its evaluated Boolean
value.

# Inputs and Outputs

- **Input**: The plugin accepts any type of payload as input. This input is used to evaluate the specified conditions.
- **Output**: The plugin outputs an object where each key corresponds to a condition, and the value is a Boolean
  indicating whether the condition was met (__true__) or not (__false__).

Example Output:

```json
{
  "marketing-consent": true,
  "is-it-raining": false
}
```

# Configuration

- __Conditions__: Key-value pairs where the key is a custom name for a condition and the value is the condition to be
  evaluated. For example, checking if marketing consent is not empty in a profile (__profile@consents.marketing EMPTY__). For the syntax of condition see Tracardi documentation.

# JSON Configuration

Example Configuration:

```json
{
  "conditions": {
    "marketing-consent": "profile@consents.marketing EXISTS",
    "is-it-raining": "lowercase(payload@weather.condition) == 'rain'"
  }
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

- **"Could not parse the condition __{value}__. Got error: {str(e)}"**: This error occurs when the plugin encounters an
  issue in parsing or evaluating a condition. It might happen if the condition is incorrectly formatted or if the
  required data is not present in the payload.