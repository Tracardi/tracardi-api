# Decrease Interest

Decrease Interest is a Tracardi plugin that reduces a specific interest within a user's profile, based on a configurable
interest name and decrease value.

# Version

0.8.0

## Description

The Decrease Interest plugin works by identifying a particular interest within a user's profile and decreasing it by a
specified amount. The decrease in interest is determined through an administrator-defined configuration that outlines
the name of the interest and the degree of decrease.

If a user profile does not exist or the plugin receives a profile-less event, an error message will be generated and
returned through the 'error' port. After successfully decreasing the specified interest, the plugin passes the payload
it received to the 'payload' port.

# Inputs and Outputs

Input: The plugin receives an input via the port named 'payload' in a JSON-like object format.
Output: The plugin returns an output through two ports, 'payload' and 'error'. The 'payload' port returns the received
payload object if the plugin successfully executed while the 'error' port returns an error message if the plugin
encountered issues, such as a missing profile or a profile-less event.

E.g.,
Input (JSON):

```json
{
  "profile": {
    ..
  },
  "event": {
    ..
  }
}
```

Output (JSON):

```json
{
  "message": "Can not decrease profile interest in profile-less events."
}
```

# Configuration

* Interest name: Specify the name of the interest that should be decreased.
* Interest value: Specify the degree by which the interest should be decreased.

# JSON Configuration

Example configuration:

```json
{
  "interest": "sports",
  "value": "1.0"
}
```

# Required Resources

This plugin does not require external resources to be configured.

# Errors

* "Can not decrease profile interest in profile-less events." - This error occurs when a profile-less event is
  processed.
* "Can not decrease interests to empty profile." - This error occurs when there is no profile to decrease interests
  from.