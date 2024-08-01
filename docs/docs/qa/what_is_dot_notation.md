# What is dot notation?

In short, dot notation is a way of referencing data in Tracardi. It is used to access data from the internal state of
the workflow, such as the event, profile, payload, flow, session, and memory. It is written in the form
of `<source>@<path.to.data>`, where the source is the type of data you are referencing and the path is a string of keys
that indicate where the data is located.

For example, if you wanted to access the data from the profile with the key `key.data`, the full dot notation would
be `profile@key.data`. You can also use dot notation to access parts of data, such as everything below a certain key, or
items in an array. In some cases, you may need to use dot notation to access data with keys that contain spaces, in
which case you would use `profile@key["My key with spaces"]`.

For more information look for dot notation in the documentation.

---
This document answers the following questions:
- How to get profile, event, or session data?
- How to reference profile, event, or session data?
- How to get data from profile, event, session, memory, workflow.