# Find Max Value

The Find Max Value plugin is a simple plugin designed to find the key with the maximum numeric value within a
dictionary. It operates on data from the internal state of a workflow, which is provided through the configuration. This
plugin checks the data's structure, ensuring that it is a dictionary with string keys and numeric values (int or float).
It then identifies the key associated with the maximum value and returns this information.

## Version

This documentation is based on plugin version 0.8.2.

## Description

The Find Max Value plugin serves as a utility for extracting the key with the maximum numeric value from a dictionary in
the internal state of a workflow. It performs the following steps:

1. Access the specified data from the internal state using the dot-notation path provided in the configuration.
2. Verify that the data is in the form of a dictionary with string keys and numeric values.
3. Determine the key with the highest numeric value within the dictionary.
4. Return the identified key and its corresponding maximum value as the plugin's result.

The plugin is useful for scenarios where you need to find and work with the most significant value within a dictionary,
such as identifying the most visited page on a website or the most common item in a list.

**Example Output:**

```json
{
  "key": "most_visited_page",
  "max_value": 500
}
```

In the above example, the plugin has found that the key "most_visited_page" is associated with the maximum numeric value
of 500 in the provided dictionary.

# Inputs and Outputs

- **Input**: This plugin accepts a payload object, which typically contains data from the internal state of the
  workflow.

- **Output Ports**:
    - __result__: Returns the key with the maximum numeric value in the form of a dictionary containing the key and its
      value.
    - __error__: Returns an error message in case any issues occur during the plugin's execution.

# Configuration

The Find Max Value plugin has a single configuration parameter:

- **Source Path** (Configuration Key: __source__):
    - Description: This is the dot-notation path to access the internal data in the workflow. The plugin will operate on
      this data to find the key with the maximum numeric value.
    - Example Configuration: __"source": "profile@visted.pages"__

# JSON Configuration

Here is an example JSON configuration for the Find Max Value plugin:

```json
{
  "source": "profile@visted.pages"
}
```

In this example, the plugin is configured to use the "visted.pages" data within the "profile".

# Required Resources

This plugin does not require external resources to be configured.

# Errors

The Find Max Value plugin can encounter the following errors, along with their associated error messages:

1. **ValueError: Source data is not a dictionary.**
    - Description: This error occurs when the data retrieved from the specified source path is not a dictionary.
    - Possible Condition: The data at the provided source path is not in the expected format, and it is not possible to
      find the maximum value.

2. **ValueError: Not all values in the dictionary are numeric.**
    - Description: This error occurs when the values within the dictionary retrieved from the specified source path are
      not all numeric (int or float).
    - Possible Condition: The dictionary contains values that are not numeric, preventing the plugin from identifying
      the maximum value.

3. **Exception (General Error Message)**
    - Description: This error occurs if any unexpected exception is raised during the plugin's execution.
    - Possible Condition: This error may occur due to issues such as invalid dot-notation path, internal workflow state
      not containing the expected data, or other unforeseen problems during execution.