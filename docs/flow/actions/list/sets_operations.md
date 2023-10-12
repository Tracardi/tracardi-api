# Set Operation Plugin

The Set Operation Plugin is used to perform various set operations on two sets of data. These sets can be referenced
from the internal state of the workflow. This plugin takes two sets of data as input, performs the specified set
operation, and returns the result.

## Version

This documentation is created for Set Operation Plugin version 8.2.0.

## Description

The Set Operation Plugin allows you to perform set operations on two sets of data. Sets can be referenced from the
internal state of the workflow. The plugin supports the following set operations:

- **Intersection**: Finds the common elements between two sets.
- **Union**: Finds the combined set of unique elements from two sets.
- **Difference**: Finds the elements that exist in one set but not in another.
- **Symmetric Difference**: Finds the elements that exist in either of the sets but not in both.
- **Subset Check**: Checks if one set is a subset of another.
- **Superset Check**: Checks if one set is a superset of another.

The operation to be performed is specified in the plugin's configuration.

### Inputs and Outputs

- **Input**: This plugin accepts a payload object.
  
  Example Input:
  ```json
  {
    "set1": [1, 2, 3, 4],
    "set2": [3, 4, 5, 6],
    "operation": "intersection"
  }
  ```

- **Outputs**: The plugin has two output ports:
  
  1. **result**: Returns the result of the intersection operation.
  
     Example Output:
     ```json
     {
       "result": [3, 4]
     }
     ```

  2. **error**: Returns an error message if an exception occurs during the operation.
  
     Example Error Output:
     ```json
     {
       "message": "Invalid operation specified."
     }
     ```

## Configuration

The Set Operation Plugin has the following configuration parameters:

- **Set 1**: Reference to the first set data.
- **Set 2**: Reference to the second set data.
- **Set Operation**: Select the set operation to perform.

## JSON Configuration

Here is an example of the JSON configuration for the Set Operation Plugin:

```json
{
  "set1": "payload@data.set1",
  "set2": "event@data.set2",
  "operation": "intersection"
}
```

In this example, the plugin is configured to perform the "intersection" operation on two sets of data located at "
payload@data.set1" and "event@data.set2."

## Required Resources

This plugin does not require external resources to be configured.

## Errors

The Set Operation Plugin may raise the following exceptions along with the conditions under which they may occur:

- **ValueError: Invalid operation specified.** This error occurs when an invalid set operation is specified in the
  configuration.
- **TypeError: The 'issubset', 'issuperset', etc. operations can only be applied to sets.** This error occurs when the "
  is_subset" or "is_superset", etc operation is applied to non-set data.
- **KeyError: 'set1' or 'set2'.** This error occurs if the specified paths for "set1" or "set2" in the configuration do
  not exist in the internal state of the workflow.
- **Exception: An unexpected error occurred.** This is a generic error that may occur due to unexpected issues during
  the set operation.

Please make sure the configuration is correctly set and that the specified paths for the sets exist in the internal
state of the workflow.