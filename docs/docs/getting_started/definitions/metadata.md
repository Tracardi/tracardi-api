# Metadata

Metadata provides additional context and information about a profile, session, or event beyond the core data
attributes. It helps in managing,and understanding the data by storing supplementary information that is
crucial for accurate data processing and analysis, such as creation date, insert date, timezones, etc.

## Metadata in context of data storage

In the context of data storage, metadata refers to all the information that allows the system to be configured. In this
case, event source data is considered auxiliary to the profile and session data, which are the most critical data that
the system stores. From version 0.8.2, metadata is stored in MySQL.