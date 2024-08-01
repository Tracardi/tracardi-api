# Can I add custom event timestamp?

Yes, you can add a custom event timestamp. In the Event Payload structure, there is a `time` attribute which includes
the timestamp information for the event. You can set the `time.insert` attribute to the desired date and time to
override the default insert time, which represents the time of event collection.

Similarly, you can customize the `time.create` and `time.update` attributes to provide custom timestamps for event
creation and update if needed. By leveraging these attributes, you have the flexibility to control the temporal aspects
associated with the event and ensure accurate representation within your event tracking system.