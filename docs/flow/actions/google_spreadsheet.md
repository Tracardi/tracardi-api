# Google Spreadsheet

The Google Spreadsheet plugin allows Tracardi workflows to connect to Google Sheets and perform read/write operations.

# Version

0.6.1

## Description

The Google Spreadsheet plugin function allows reading or writing of data from a designated Google Spreadsheet document.
The plugin uses a specified Google Cloud Service Account Resource for authentication purposes. However, note that
simultaneous reading and writing are not permitted.

For reading data, the values (range of data) from the plugin's configuration settings are accessed. The plugin then
fetches data from these defined range locations. If no data is found, it issues a warning but continues.

Additionally, it's possible to write data on the spreadsheet. For this, the plugin takes a list of values from the
plugin's configuration settings and writes it to the specified cells range. If no data values are provided for writing,
an error is triggered, and the operation ends.

## Inputs and Outputs

The input for this plugin is a payload and the outputs can be successful payload or an error.

Here is an example of successful payload and error output in JSON format:

Success:

```json
{
  "port": "payload",
  "value": {
    # Google Spreadsheet API response...
  }
}
```

Error:

```json
{
  "port": "error",
  "value": "Error Description"
}
```

Please note that this plugin is unable to trigger new Tracardi workflows.

## Configuration

The Google Spreadsheet plugin requires the following configuration parameters:

- __Google Cloud Service Account Resource__: The resource used to connect to Google Spreadsheets.
- __Spreadsheet Id__: The Id of the Spreadsheet to connect to. The Spreadsheet Id is found in the Spreadsheet URL.
- __Sheet Name__: The name of the sheet within the spreadsheet to connect to.
- __Data Range__: The range of cells (like "A1:F4") where operations are performed.
- __Read data__: A Boolean value determining whether data is to be read from the Spreadsheet.
- __Write data__: A boolean value determining whether data is written on the Spreadsheet.
- __Values__: When writing data, the user provides a list of values (column-value pairs) for the operations.

Such configuration parameters can be represented in JSON format as follows:

```json
   {
  "source": {
    "id": "resource-id",
    "name": "resource-name"
  },
  "spreadsheet_id": "spreadsheet id",
  "sheet_name": "sheet name",
  "range": "A1:F4",
  "read": true,
  "write": false,
  "values": "[[\"Name\", \"John\"]]"
}

```

## Required resources

This plugin requires a Google Cloud Service Account Resource to function.

## Errors

- __"You can't read and write data at the same time."__: This error will be returned if both read and write fields in
  the configuration settings are set as TRUE. Only one operation can be performed at a time.
- __"If you want to parse data, set values to parse"__: This error occurs if no data values are provided for writing on
  the spreadsheet.
- __"You do not have permissions to access this spreadsheet. Please go to Google SpreadSheets and click Share in the
  upper right corner and add the following address {}."__: This error is returned if the plugin does not have
  permissions to access the Google spreadsheet. You may need to share the spreadsheet with the email mentioned in the
  error message to rectify this. Any perturbations or interruptions in the network connectivity while trying to access
  the Google spreadsheet services can trigger a generic error, returned in the form of a string.