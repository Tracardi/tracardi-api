This documentation outlines the event "Checkout Status" which should be used when a customer completes a checkout step and the status changes. It provides an example of when this event should be used, which is when a customer has completed the payment process and the status of the checkout changes from "pending" to "paid".

The documentation also provides a table of expected properties for the event, which are all optional. If any property is missing, it will not be processed and no error will be reported. The table includes the name of the property, the expected type, and an example.

The documentation also explains how auto indexing works and how it helps to make data easy to find by creating a structure that organizes the data. It provides a table that describes which event property will be copied to event traits, and states that data will not be copied to the profile.

Finally, the documentation provides a JSON example of event properties. This example includes the type of the event, which is "checkout-status", and the properties, which are "status" and "id".