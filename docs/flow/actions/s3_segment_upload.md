# S3 Segments Uploader Plugin

This plugin allows the collection and transmission of user profile segments to AWS S3 storage in a JSON format. It's
designed with simplicity in mind, enabling users to easily configure AWS credentials and specify the S3 bucket for
storing data. By accepting a profile payload, it gathers profile segments and uploads them as a JSON file named with the
current date and "_segments" suffix.

# Version

0.9.0

## Description

Upon execution, the plugin checks for the presence of "smi_uid" within the payload's traits. If this key is found, it
proceeds to create or update a JSON file in the specified S3 bucket. The JSON file structure aggregates profiles by
their "smi_uid" and associated segments, facilitating efficient data storage and retrieval.

For new uploads, the plugin directly creates a JSON file with the relevant data. If a file for the current date already
exists, it downloads this file, appends the new profile segment data, and re-uploads it to ensure all relevant data for
the day is consolidated in a single file. This method ensures that the data remains organized and easily accessible.

## Inputs and Outputs

**Inputs:** The plugin requires a payload containing a user profile. The essential part of this profile is the "traits"
section, which must include a "smi_uid" key for the plugin to function correctly.

**Outputs:** There are two possible outcomes of the plugin's operation:

- **success**: This output indicates that the JSON data was successfully uploaded to the S3 bucket. The output includes
  a message confirming the successful upload.
- **error**: This output signifies that an error occurred during the upload process. The error message provides details
  about the issue encountered.

## Configuration

To use the plugin, you must configure it with the following parameters:

- **AWS Access Key ID**: This is your AWS Access Key ID, used to authenticate your identity with AWS services.
- **AWS Secret Access Key**: This is your AWS Secret Access Key, acting as a secret password to secure your AWS account
  access.
- **S3 Bucket**: Specify the name of the S3 bucket where the JSON data will be uploaded. This bucket should already
  exist in your AWS account.

## JSON Configuration

Example configuration:

```json
{
  "aws_access_key_id": "your_access_key_id",
  "aws_secret_access_key": "your_secret_access_key",
  "s3_bucket": "your_s3_bucket_name"
}
```

## Required resources

This plugin does not require external resources to be configured.

## Event prerequisites

The plugin works for all types of events and does not specifically require synchronous event processing.

## Errors

- **"Could not find payload.traits.smi_uid"**: This error occurs when the payload does not include the "traits" section
  with a "smi_uid" key. Ensure the payload structure is correct and includes the necessary information.
- **"S3 upload error: {err}"**: Indicates an issue occurred during the upload process to S3. The specific error
  details ({err}) will provide more insight into what went wrong. This could be due to incorrect AWS credentials,
  permissions, or issues with the S3 service.