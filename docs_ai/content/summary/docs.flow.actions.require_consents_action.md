The Require Consents plugin is a tool that allows users to check if a given profile has granted one or more consents.
The plugin takes any payload as input and outputs the given payload on port true if the required consents are granted,
or on port false if the required consents are not granted.

The plugin can be configured with a form or with advanced configuration. With the form, users can provide a list of
consents that they want to require to be granted by the profile, and they can also set a switch to require all of the
provided consent types to be granted by the profile, or only one consent.

The advanced configuration requires users to provide a JSON object with a list of consent IDs and names, as well as a
boolean value for the "require_all" field. This allows users to provide more detailed information about the consents
that they want to require to be granted by the profile.