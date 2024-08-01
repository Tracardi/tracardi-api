# Does the system store an update timestamp for each field in a profile?

Yes, if possible, Tracardi stores all field updates in `metadata.fields`. This data is utilized during
profile merging. However, note that this feature is available only in the commercial version of Tracardi. Some merging
strategies may not work in the open-source version.