# Where can I save in profile such timestamp like last visit, last message send, last contact, etc ?

To store additional timestamps except last_visit, eg. last message sent, or last contact in a profile in Tracardi, you can use
the `profile@metadata.aux` field. This field is specifically designed to hold additional information, including various
timestamps.

You can create a `timestamp` subfield under `metadata.aux` and save any relevant timestamp data there. For instance, to
record the time of the last chat or the last sent email, you might use fields like `metadata.aux.timestamp.last_chat`
and `metadata.aux.timestamp.last_send_email`, respectively, and assign the corresponding dates to them.

Here's an example of how you might structure this:

- `metadata.aux.timestamp.last_chat` = [date/time of last chat]
- `metadata.aux.timestamp.last_send_email` = [date/time of last sent email]

This approach allows you to neatly organize and store various timestamp-related data within the profile structure.
The `metadata.aux` is indexed but can not be aggregated.