# Increase Interest

The Increase Interest plugin is a tool in the Tracardi suite that is used to increment a specified interest value of a
user profile.

# Version

The current version of the Increase Interest plugin is 0.8.2.

## Description

The Increase Interest plugin operates by raising the interest value associated with a specified profile by a
predetermined amount. The plugin receives a payload (in JSON format), and uses this to find the profile to be altered.
It then increases the interest of that profile according to the plugin's configuration. Dot
notation can be used to dynamically set the interest name. Though there are some restrictions. The interest name must be
an alpha-numerical string without spaces. Hyphen and dashes are allowed.

The success or failure of each operation is tracked and logged, with error messages being produced for profile-less
events and empty profiles. Finally, the plugin returns the same payload it received, allowing it to be passed on to the
next plugin in the workflow.

# Inputs and Outputs

The input for the Increase Interest plugin is a JSON object, the "payload". This object is passed into the plugin and
used to find the profile to be processed.

There are two outputs from the Increase Interest plugin: the payload and an error. The payload output port returns the
object originally received by the plugin, while the error output port returns error messages encountered during the
execution of the plugin.

# Configuration

The configuration options for the Increase Interest plugin are:

- __Interest__: This is the name of the interest that you want to increment.
- __Value__: This is the amount by which the selected interest should be increased.

# JSON Configuration

Here's an example of how the JSON configuration for the Increase Interest plugin might look:

```json
{
  "interest": "travel",
  "value": "5.0"
}
```

In this example, the value of the **travel** interest would be increased by **5.0** for the selected profile.

# Required Resources

This plugin does not require any external resources to be configured.

# Errors

The Increase Interest plugin may return the following error messages under certain conditions:

- __"Can not increase profile interest in profile less events."__: This error occurs when an attempt is made to increase
  the interest of a profile-less event.
- __"Can not increase interests to empty profile."__: This error is encountered when the plugin tries to increase the
  interest of an empty profile.
- __"Invalid interest name."__ - This error occurs when the name of the interest (key used to save it in the database)
  is
  not an alpha-numerical string. Interest name must be an alpha-numerical string without spaces. Hyphen and dashes are
  allowed.