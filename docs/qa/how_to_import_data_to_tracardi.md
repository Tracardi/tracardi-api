# How to import data to Tracardi

This answer is the summary of the following video tutorial: https://www.youtube.com/watch?v=w_4gPOL0tvw

To import data into Tracardi through event collection, follow these steps:

1. **Open an Event Source**: It's recommended to open an event for the import. This is the initial step where you set up
   an event source in Tracardi.

2. **Allow Static Profile ID**: Ensure that the option "allow static profile ID" is selected. This is crucial because
   you'll be sending profile IDs from an external system, and this setting allows Tracardi to recognize and use these
   IDs.

3. **Send a Regular Event to the Tracardi Endpoint**: Simulate a regular event with some random session data. You can
   keep the session the same during the import process.

   During sending:

    1. **Include a Profile ID in Track Paylaod**: This step involves sending a profile ID. This profile ID will be
       persistent and won't be
       replaced by Tracardi's internal ID.

    2. **Include Import Source in Track Payload**: Choose the appropriate import source for your data.

    3. **Set event type to profile-update**: Indicate that you're sending profile data that you want to update. If the
       profile does not exist, it will be created with the specified ID, thanks to the option in the Event Source that
       retains this ID.

    4. **Set Profile Data**: Send the data you want to be associated with the profile. This can include various types of
       user or
       event data.

This process essentially involves setting up an event source, ensuring the correct handling of profile IDs, sending data
to Tracardi, and then verifying that the data has been correctly imported and the profiles have been updated or created
as needed.



