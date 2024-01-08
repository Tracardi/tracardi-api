# Hash data

The Hash data plugin enables you to hash specified data such as profile traits. This action can be useful in workflows that require data processing tasks such as data security or unique identifiers.

# Version

The version of the plugin this documentation was created for is 0.7.0.

## Description 

The Hash data plugin takes a payload and hashes specified traits in the payload. The plugin configuration specifies the traits to be hashed and the hashing function to be used (md5, sha1, sha256, sha512). If the designated trait is not a string value, it is serialized to JSON before hashing. 

The plugin iterates over the configured traits, validates each trait, performs the hashing operation if the trait value is valid and updates the trait value in the payload with the hash result. The plugin supports updating traits within the event, profile, and session of the workflow's state. 

Finally, the plugin returns a Result object with the updated payload and specifies the output port as 'payload'. 

# Inputs and Outputs

The Hash data plugin accepts a single input port 'payload' that takes in a payload object which should include the traits specified in the plugin's configuration. 

Upon completion, the plugin returns the updated payload on the same 'payload' port (the Hash data Plugin has only one output port 'payload').

# Configuration 

The Hash data plugin requires the following configuration parameters: 

- Traits - Array of dot notation paths referencing the traits to be hashed. If a value is not a string, it is serialized to JSON before hashing. 
- Hashing function - Determines the function used for hashing. The plugin supports md5, sha1, sha256, and sha512.


# JSON Configuration

Here's an example of how to configure the Hash data plugin in JSON format:

```json
{
    "traits": ["profile@traits.email", "session@traits.username"],
    "func": "sha256"
}
```

# Required resources

This plugin does not require external resources to be configured.

# Errors 

The plugin raises warnings in two cases: 

- If a trait path references the 'flow' source. The plugin does not support hashing 'flow' values -- 'Flow values cannot be hashed.'
- If the trait path is invalid or does not exist in the payload - 'Given trait {trait path} is invalid or does not exist.'

It's important to note that these are warning messages and do not halt the execution of the plugin. However, they do indicate potential issues with the plugin's configuration.