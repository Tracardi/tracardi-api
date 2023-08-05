# Load report data

The Load report data plugin is used to load the results of a specified report into the payload. It allows you to select
a report and provide the necessary configuration to retrieve the report data. This plugin is part of the Tracardi Pro
License.

## Description

The Load report data plugin loads the results of a selected report and adds them to the payload. It uses the Tracardi
Reports to retrieve the report data based on the provided configuration.

# Inputs and Outputs

This plugin has one input:

- **payload** (dict): This port accepts a payload object.

This plugin has two outputs:

- **result**: Returns the results of the selected report if the report data retrieval is successful.
- **error**: Returns an error message if an exception occurs during the report data retrieval.

# Configuration

The configuration of the Load report data plugin includes the following parameters:

- **Report configuration**: Select the report and provide the necessary configuration. You can use dot paths as values
  to specify the report parameters.

Here is an example configuration:

- Report configuration:
    - Report:
        - ID: "report_id"
        - Name: "report_name"
    - Params: "{}"

Note: The report configuration includes the report ID, report name, and the parameters required to retrieve the report
data.

# Required resources

This plugin does not require external resources to be configured.

# Errors

The Load report data plugin may encounter the following error:

- **Error detail**: This error occurs when an exception is raised during the report data retrieval. The error detail
  provides more information about the specific error that occurred.

Note: The error message will be returned in the **error** output port.

