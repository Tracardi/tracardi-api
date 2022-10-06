# String Validator Action

The purpose of this plugin is to validate data. We need to specify a type of validation. 

We can choose from:

* email - for example example@mail.com
* url - for example tracardi.com
* ipv4 for example 192.168.1.1
* date for example 01.01.1900
* time for example 01:01
* int for example 3
* float for example 3.4
* number_phone for example +48123456789

# Configuration

This node require configuration.

*Configuration values*

* validator - type of validation.
* data - the string that we would like to validate

*Data* can be a dotted notation path to value inside profile, event, session, etc. or any string.

## Examples

```json
{
  "validator" : "url",
  "data" : "profile@traits.private.email"
}
```

It will return `payload` on `valid` output port. `invalid` port will stay inactive. 

```json
{
  "validator" : "email",
  "data" : "12341232"
}
```

It will return `payload` on `invalid` output port. `valid` port will stay inactive. 

# Input payload

This node does not process input payload. Input payload will not be returned on output. 

# Output

This plugin has to port valid and invalid. Depending on validation result the appropriate ports will be launched with payload copied as data.
