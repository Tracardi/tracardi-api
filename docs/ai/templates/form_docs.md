You task is to describe what user should type into the form from the form definition in code.

The form is build form Objects: Form, FormGroup, FormField.

FormGroup describes the group each field belongs to. Form field is the form field where the user will fill the data.

Example form field:
```python
FormField(
    id="resource",  # Id
    name="Resource",  # Field nama
    description="Resource description", # Description usually providing the information what should be typed.
    component=FormComponent(type="resource", props={"label": "Here is the resource type", "tag": "twilio"})  # What kind of conponent is used to input data.
)
```

There are different types of components that are used for each field.
The following field types can be used in plugin's forms:

- readOnlyTags - Allows to enter a list of tags
- eventTypes - allows to select from the list of available event types
- eventType - allows to type one event type.
- resource - allows to select resource form the list of available resources in the system
- dotPath - allows to type the reference to data from profile, session, event etc. in form of the dotted notation (dotpath)
- forceDotPath - allows to type the reference to data from profile, session, event etc. in form of the dotted notation but only for selected object eg. profile
- keyValueList - allows to set a list of key value pairs
- listOfDotPaths - allows to set a list of reference to data from profile, session, event etc. in form of the dotted notation (dot paths)
- text - allows to type a text
- json - allows to type a json schema
- sql - allows to type a json schema
- textarea - allows to type a multiline text
- select - allows to select a value from a list of values
- bool - allows switch on and off
- contentInput - - allows to type a multiline text content.

Use this template to generate response:

```
* <Short field description>
<Type what data hould be typed into the form>
```
# Example 

For the following form:

```python
Form(groups=[
        FormGroup(
            name="API Webhook Bridge Configuration",
            description="The webhook bridge usually collects data without connection to a profile or session. "
                        "But, if you need to make a profile and session for the data it collects, and you want "
                        "to make sure that it matches an existing profile, you should set up matching details below.",
            fields=[
                FormField(
                    id="generate_profile",
                    name="Create profile and session for collected data.",
                    description="By default, webhook events do not include session or profile IDs. "
                                "However, if you enable this settings, it will generate the profile and session "
                                "ID for this event.",

                    component=FormComponent(type="bool", props={"label": "Create profile and session"})
                ),
                FormField(
                    id="identify_profile_by",
                    name="Identification method",
                    description="Select the method to identify the profile. If 'e-mail' or 'phone' is "
                                "chosen, a Profile will be identified by the 'e-mail' or 'phone'. "
                                "The exact location of the data should be defined in 'Set Profile ID from Payload' field. "
                                "Selecting 'nothing' means no Profile ID will be matched. If 'custom ID' is "
                                "selected, the Profile ID will be the same as the payload value referenced in "
                                "the 'Set Profile ID from Payload' field.",
                    component=FormComponent(
                        type="select",
                        props={
                            "label": "Profile identified by",
                            "items": {
                                "none": "No Reference",
                                "e-mail": 'Main E-Mail',
                                "phone": "Main Phone",
                                "id": "Custom ID"
                            }
                        }
                    )
                ),
                FormField(
                    id="replace_profile_id",
                    name="Set Profile ID from Payload",
                    description="To set the Profile ID, type the location of Profile ID Identifier in payload below or leave "
                                "the field blank if you don't wish "
                                "to set any profile or want it to have a random ID. "
                                "If 'Custom ID' is chosen as identification method, then enter the location where the Profile ID "
                                "is stored in payload the; ID will be used as is without modification. "
                                "For 'e-mail' or 'phone' options,  enter the location where e-mail or phone is stored; "
                                "the system automatically generates a secure, hash-based Profile ID from the data in "
                                "the payload. It will automatically load profile for the e-mail of phone defined "
                                "in payload. "
                                "This setting will only work when `Create session and profile` is enabled. ",
                    component=FormComponent(type="text", props={"label": "Reference to Profile ID in webhook payload"})
                ),
                FormField(
                    id="replace_session_id",
                    name="Set Session ID from Payload",
                    description="This setting will only work when `Create session and profile` is enabled. "
                                "If you intend to substitute or set the Session ID with information from the payload, "
                                "you can either use the data provided below or leave it blank if you don't wish "
                                "to set any session or want it to have a random ID. It is crucial to ensure "
                                "that the Session ID is secure and not easily predictable since simple Session "
                                "IDs may pose security threats.",
                    component=FormComponent(type="text", props={"label": "Reference to Session ID in webhook payload"})
                )
            ])
```

This could be a possible response:

Please fill the following fields:


* Create profile and session for collected data.
Decide whether to generate a profile and session ID for webhook events. This is a boolean switch. You can turn it on or off. If you enable it, it will generate the profile and session ID for this event.

* Identification method
Choose a method for identifying the profile. Options include 'e-mail', 'phone', 'custom ID', or 'none' (no Profile ID will be matched). Select one of the provided options from the dropdown list. Your choice dictates how the profile will be identified: by email, phone, custom ID, or not at all.

* Set Profile ID from Payload
Enter the location of the Profile ID Identifier in the payload. This is used to set the Profile ID. The field's behavior depends on the identification method chosen (e.g., custom ID, e-mail, phone). Type the reference to the Profile ID in the webhook payload. If 'Custom ID' is chosen in the identification method, enter the exact payload location of the ID.

* Set Session ID from Payload
Substitute or set the Session ID with information from the payload. This setting is only functional when 'Create profile and session for collected data' is enabled.
Type the reference to the Session ID in the webhook payload. If you do not wish to set a specific session ID, you can leave it blank.

YOUR TASK. Using this information describe what user should type into this form:**

```python
Form(groups=[
        FormGroup(
            name="API Webhook Bridge Configuration",
            description="The webhook bridge usually collects data without connection to a profile or session. "
                        "But, if you need to make a profile and session for the data it collects, and you want "
                        "to make sure that it matches an existing profile, you should set up matching details below.",
            fields=[
                FormField(
                    id="generate_profile",
                    name="Create profile and session for collected data.",
                    description="By default, webhook events do not include session or profile IDs. "
                                "However, if you enable this settings, it will generate the profile and session "
                                "ID for this event.",

                    component=FormComponent(type="bool", props={"label": "Create profile and session"})
                ),
                FormField(
                    id="identify_profile_by",
                    name="Identification method",
                    description="Select the method to identify the profile. If 'e-mail' or 'phone' is "
                                "chosen, a Profile will be identified by the 'e-mail' or 'phone'. "
                                "The exact location of the data should be defined in 'Set Profile ID from Payload' field. "
                                "Selecting 'nothing' means no Profile ID will be matched. If 'custom ID' is "
                                "selected, the Profile ID will be the same as the payload value referenced in "
                                "the 'Set Profile ID from Payload' field.",
                    component=FormComponent(
                        type="select",
                        props={
                            "label": "Profile identified by",
                            "items": {
                                "none": "No Reference",
                                "e-mail": 'Main E-Mail',
                                "phone": "Main Phone",
                                "id": "Custom ID"
                            }
                        }
                    )
                ),
                FormField(
                    id="replace_profile_id",
                    name="Set Profile ID from Payload",
                    description="To set the Profile ID, type the location of Profile ID Identifier in payload below or leave "
                                "the field blank if you don't wish "
                                "to set any profile or want it to have a random ID. "
                                "If 'Custom ID' is chosen as identification method, then enter the location where the Profile ID "
                                "is stored in payload the; ID will be used as is without modification. "
                                "For 'e-mail' or 'phone' options,  enter the location where e-mail or phone is stored; "
                                "the system automatically generates a secure, hash-based Profile ID from the data in "
                                "the payload. It will automatically load profile for the e-mail of phone defined "
                                "in payload. "
                                "This setting will only work when `Create session and profile` is enabled. ",
                    component=FormComponent(type="text", props={"label": "Reference to Profile ID in webhook payload"})
                ),
                FormField(
                    id="replace_session_id",
                    name="Set Session ID from Payload",
                    description="This setting will only work when `Create session and profile` is enabled. "
                                "If you intend to substitute or set the Session ID with information from the payload, "
                                "you can either use the data provided below or leave it blank if you don't wish "
                                "to set any session or want it to have a random ID. It is crucial to ensure "
                                "that the Session ID is secure and not easily predictable since simple Session "
                                "IDs may pose security threats.",
                    component=FormComponent(type="text", props={"label": "Reference to Session ID in webhook payload"})
                )
            ])
```