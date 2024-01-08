# Whois Plugin

The Whois plugin is a connector that allows you to check a specified domain using the Whois service. It checks whether a
domain exists or not and returns the details related to the domain like registrar, creation date, expiration date, etc.

# Version

This documentation was created for the Whois plugin version 0.8.0.

## Description

The Whois plugin receives a payload containing the domain to be checked. It communicates with the Whois service to
enquire about the domain. The obtained details are then encapsulated into a result, which is then passed onto the next
port as per the workflow. In case of any issues while fetching the details, the plugin returns an error message.

# Inputs and Outputs

The Whois plugin accepts one input:

- __payload__: This port accepts payload object.

The Whois plugin provides two outputs:

- __result__: Returns the response from the Whois service containing detail information about the domain.
- __error__: Returns error message if the plugin fails to retrieve the domain information.

# Configuration

The configuration for the Whois plugin is as follows:

- __domain__: This field requires the user to provide the domain to be checked in the Whois service.

# JSON Configuration

Below is an example of the JSON configuration:

```json
{
  "domain": "example.com"
}
```

# Required resources

This plugin does not require any external resources to be configured.

# Errors

If an error occurs during the execution of the plugin, an error message is returned with the following format:

- __{'message': 'error message'}__

The possible error scenarios include:

- Failure in retrieving the domain's information from the Whois service.
- Providing an empty string for the domain input. In this case, the error message will be - "Domain must not be empty."