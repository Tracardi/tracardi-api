# Where do I store the unique identifier for each profile?

You store the unique identifier for each profile in the `id` field of profile.

# Where do I store previous profile IDs and IDs from external systems?

You store previous profile IDs and IDs from external systems in the `ids` field of profile.

# Where do I store metadata information such as time, time zone, visits, and auxiliary metadata?

You store metadata information such as time, time zone, visits, and auxiliary metadata in the `metadata` field of
profile.

# Where do I store additional auxiliary metadata associated with the profile?

You store additional auxiliary metadata associated with the profile in the `metadata.aux` field of profile.

# Where do I store various time-related information, such as profile insertion timestamp, update timestamp, and segmentation timestamp?

You store various time-related information, including profile insertion timestamp, update timestamp, and segmentation
timestamp, in the `metadata.time` sub-field.

# Where do I store the actual profile data used for reporting and describing personal information?

You store the actual profile data used for reporting and describing personal information in the `data` field of profile.

# Where do I store media-related information such as images, webpages, and social media handles?

You store media-related information such as images, webpages, and social media handles in the `data.media` sub-field.

# Where do I store personally identifiable information (PII) such as name, birthday, gender, and education level?

You store personally identifiable information (PII) such as name, birthday, gender, and education level in
the `data.pii` sub-field.

# Where do I store various identifiers associated with the profile, such as ID, badge, passport, and credit card?

You store various identifiers associated with the profile, such as ID, badge, passport, and credit card, in
the `data.identifier` sub-field.

# Where do I store contact information like email, phone number, messaging app handles, and address details?

You store contact information like email, phone number, messaging app handles, and address details in the `data.contact`
sub-field.

# Where do I store job-related information such as position, salary, and company details?

You store job-related information such as position, salary, and company details in the `data.job` sub-field.

# Where do I store profile preferences such as purchases, colors, sizes, devices, and channels?

You store profile preferences such as purchases, colors, sizes, devices, and channels in the `data.preferences`
sub-field.

# Where do I store device-related information such as device names and geographic details?

You store device-related information such as device names and geographic details in the `data.devices` sub-field.

# Where do I store loyalty-related information such as loyalty codes and loyalty card details?

You store loyalty-related information such as loyalty codes and loyalty card details in the `data.loyalty` sub-field.

# Where do I store additional statistics associated with the profile, such as the number of emails sent/received and error count?

You store additional statistics associated with the profile in the `stats` field of profile.

# Where do I store custom profile attributes/properties that do not fit into the predefined profile data schema?

You store custom profile attributes/properties that do not fit into the predefined profile data schema in the `traits`
field of profile.

# Where do I store collections related to the profile, allowing the storage of one-to-many relationships with other objects?

You store collections related to the profile, allowing one-to-many relationships with other objects, in
the `collections` field of profile.

# Where do I store segments to which the profile belongs?

You store a set of segments to which the profile belongs in the `segments` field of profile.

# Where do I store a list of consents given by the profile?

You store a list of consents given by the profile in the `consents` field of profile.

# Where do I indicate whether the profile is active or inactive from a business perspective?

You indicate whether the profile is active or inactive from a business perspective in the `active` field of profile.

# Where do I store key-value pairs representing the interests of the profile?

You store key-value pairs representing the interests of the profile in the `interests` field of profile.

# Where do I store auxiliary data related to conflicts or data discrepancies, allowing temporary preservation of obsolete or migrating data?

You store auxiliary data related to conflicts or data discrepancies, allowing temporary preservation of obsolete or
migrating data, in the `aux` field of profile.

# Where do I store data that should be removed at some point, such as obsolete or data created during the migration process?

You store data that should be removed at some point, such as obsolete or data created during the migration process, in
the `trash` field of profile.

# Where do I store data that does not need to be searched or indexed, such as operational flags or non-grouping/indexing data?

You store data that does not need to be searched or indexed, such as operational flags or non-grouping/indexing data, in
the `misc` field of profile.