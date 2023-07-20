# Profile Fields

- `id`: The profile ID, representing a unique identifier for each profile.
- `ids`: A list of previous profile IDs and IDs from external systems, used to reference the same profile stored in
  external systems.
- `metadata`: Contains metadata information such as time, time zone, visits, and auxiliary metadata.
    - `aux`: Additional auxiliary metadata associated with the profile.
    - `time`: Sub-field that stores various time-related information.
        - `insert`: Represents the timestamp of the profile insertion.
        - `update`: Indicates the timestamp of the profile update.
        - `segmentation`: Stores the segmentation timestamp.
        - `visit`: Contains visit-related details such as the last visit timestamp, current visit timestamp, visit
          count, and time zone (`tz`).
- `data`: Holds the actual profile data with a predefined structure used for reporting and describing personal
  information.
    - `media`: Contains media-related information such as images, webpages, and social media handles.
    - `pii`: Stores personally identifiable information, including attributes like first name, last name, birthday,
      language preferences, gender, education level, civil status, and physical attributes.
    - `identifier`: Includes various identifiers associated with the profile, such as ID, badge, passport, credit card,
      token, and coupons.
    - `contact`: Stores contact information like email, phone number, messaging app handles, and address details.
    - `job`: Contains job-related information like position, salary, job type, company details (name, size, segment,
      country), and department.
    - `preferences`: Represents profile preferences, including purchases, colors, sizes, devices, channels, payments,
      brands, fragrances, and other preferences.
    - `devices`: Stores device-related information, including device names and geographic details like country, county,
      city, latitude, longitude, and postal code.
    - `metrics`: Includes various metrics associated with the profile, such as lifetime value (LTV), etc.
    - `loyalty`: Contains loyalty-related information, such as loyalty codes and loyalty card details (ID, name, issuer,
      points, expiration date).
- `stats`: Additional statistics associated with the profile, such as the number of emails sent/received, SMS count, and
  error count.
- `traits`: A field where custom profile attributes/properties can be stored. It allows storing any custom data that
  does not fit into the predefined profile data schema.
- `collections`: Holds collections related to the profile, allowing the storage of one-to-many relationships with other
  objects (e.g., purchases, devices).
- `segments`: Represents a set of segments to which the profile belongs. The field truncates the name if it exceeds 64
  characters.
- `consents`: Stores a list of consents given by the profile.
- `active`: Indicates whether the profile is active or inactive from a business perspective. Profiles that have not had
  any events for a year can be marked as inactive.
- `interests`: Contains key-value pairs representing the interests of the profile. For example, `{ "sports": 0.86 }`
  indicates that the person is 86% interested in sports.
- `aux`: Stores auxiliary data related to conflicts or data discrepancies, allowing temporary preservation of obsolete
  or migrating data.
- `trash`: Holds data that should be removed at some point. It can be used to temporarily store obsolete or data created
  during the migration process.
- `misc`: A field used to store data that does not need to be searched or indexed. It can include operational flags or
  data that does not require grouping or indexing.


---
This documentation answers the following questions

* What are the fields and their descriptions associated with the profile data stored in Tracardi?
* What is the purpose of the id field in the profile data?
* What does the ids field represent in the profile data, and how is it used?
* What metadata information is available in the metadata field of the profile data?
* What time-related information is stored within the metadata.time sub-field?
* What is the structure and purpose of the data field in the profile data?
* What types of information are stored within the data.media sub-field of the profile data?
* What personally identifiable information (PII) is captured and stored in the data.pii sub-field of the profile data?
* What types of identifiers can be found in the data.identifier sub-field of the profile data?
* How is contact information organized within the data.contact sub-field of the profile data?
* What job-related information is stored within the data.job sub-field of the profile data?
* What preferences and preferences-related information are captured in the data.preferences sub-field of the profile data?
* What device-related information is stored within the data.devices sub-field of the profile data?
* What metrics and loyalty-related data can be found within the data.metrics and data.loyalty sub-fields of the profile data, respectively?
* How are statistics related to the profile stored within the stats field?
* How can custom profile attributes/properties be stored and accessed within the traits field?
* What is the purpose of the collections field in the profile data?
* How are segments represented in the segments field, and what is the character limit for segment names?
* How are consents given by the profile stored within the consents field?
* How is the activity status of a profile determined and indicated in the active field?
* How are the interests of a profile represented within the interests field?
* What is the purpose of the aux field in the profile data, and what type of data can it store?
* How can the trash field be utilized in the profile data, and what kind of data can it hold?
* What is the purpose and usage of the misc field in the profile data?