# Join

Joins payload from incoming data, merging different input connections into a single, unified payload.

# Version

0.7.1

## Description

The Join plugin focuses on combining data from various input connections into a single payload. This is particularly
useful when data from multiple sources needs to be gathered and analyzed as a unified set. If input connections have
specific names, the plugin organizes the merged data under these connection names. For unnamed connections, it uses the
connection IDs as keys in the resulting object.

Additionally, the plugin offers a feature for reshaping the joint data. This allows for transforming the data structure
according to a predefined JSON template. The template can include static values, dynamically fetched data using dot
notation (such as "profile@id"), or combinations thereof. This capability enables tailored data structuring to fit
specific analytical or operational needs.

# Inputs and Outputs

## Inputs:

- **Payload**: Accepts a payload object containing the data to be joined.

## Outputs:

- **Payload**: Returns the joined payload, Optionally it may be reshaped according to the configured template.

# Configuration

- **Reshape output payload**: A JSON template to reshape the output payload, allowing transformations of the joint data.
- **Type of join**: Choose between a list or a dictionary for the collection type. Dictionary type uses connection names
  as keys.
- **Missing values equal null**: If enabled, any missing values in the data will be replaced with null.

# JSON Configuration

Example configuration:

```json
{
  "reshape": "{\"some-data\": {\"key\": \"value\", \"value\": \"profile@id\", \"list\": [1, \"payload@data\"], \"event\": \"event@...\"}}",
  "default": true,
  "type": "dict"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors

- **"Invalid Configuration":** Occurs when the provided plugin configuration is not valid. This can happen if the JSON
  reshaping template is incorrectly formatted or if essential configuration parameters are missing or invalid.

# Operation

Upon execution, the plugin processes incoming data from different sources, joining them based on the defined
configuration. The reshaping feature applies the specified template to the joint data, allowing for customized data
structuring. The output is a single payload that consolidates all input data, optionally reshaped and organized
according to the plugin's configuration.