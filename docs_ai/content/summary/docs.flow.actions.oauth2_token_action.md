This plugin is used to get an OAuth2 token from an API endpoint resource. It takes any payload object as an input and outputs the given payload object modified according to the configuration. The configuration can be done either with a form or with an advanced config. 

When using the form, the user must select the API endpoint resource from which they want to get the token and type in the path to the field (starting with 'payload@') where they want to store the object returned by the endpoint. 

When using the advanced config, the user must provide a JSON object with the source (id and name of the API endpoint resource) and the destination (dot path to the destination field, which must start with 'payload@'). 

This plugin is useful for getting an OAuth2 token from an API endpoint resource and storing it in the desired field.