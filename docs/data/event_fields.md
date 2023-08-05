# Event Fields

- `id`: The event ID, representing a unique identifier for each event.
- `metadata`: Contains metadata information related to the event, such as time, time zone, visits, and auxiliary
  metadata.
    - `aux`: Additional auxiliary metadata associated with the event.
    - `time`: Sub-field that stores various time-related information.
        - `insert`: Represents the timestamp when the event was inserted.
        - `create`: Indicates the timestamp of the event creation.
        - `process_time`: Stores the time taken to process the event.
    - `status`: Indicates the status of the event.
    - `channel`: Stores the channel from which the event originated.
    - `ip`: Represents the IP address associated with the event.
    - `processed_by`: Contains information about the processing of the event, such as the rules, flows, and third-party
      systems involved.
    - `profile_less`: Indicates whether the event is associated with a profile or not.
    - `valid`: Represents the validity status of the event.
    - `warning`: Indicates if there are any warnings associated with the event.
    - `error`: Indicates if there are any errors associated with the event.
    - `instance`: Contains information about the instance of Tracardi where the event was processed.
    - `debug`: Indicates if the event is in debug mode.
- `type`: This field represents the event type, usually expressed as a slug derived from the event name. It is lowercase
  with hyphens replacing spaces.
- `name`: The human-readable event name, derived from the event type. The first letter of each word is capitalized, and
  hyphens are replaced by spaces.
- `source`: A reference to the source from which the event was collected.
- `device`: Contains information about the device from which the event was collected, including the device name, brand,
  model, IP address, type, touch capability, resolution, color depth, orientation, and geographic details.
- `os`: Contains information about the operating system from which the event was collected, including the OS name and
  version.
- `app`: Contains information about the application from which the event was collected, including the app type (mobile
  app or browser), bot status, name, version, language, and resolution.
- `hit`: Contains information about the page or screen from which the event was collected, including the name, URL,
  referer, query parameters, and category.
- `utm`: Contains information about the marketing campaign that the event originated from, including source, medium,
  campaign, term, and content.
- `history`: Contains the history of hits, including the name, URL, referer, query parameters, and category.
- `session`: References a session associated with the event, allowing events to be grouped within a visit.
- `profile`: References the profile associated with the event, indicating the owner of the event.
- `entity`: References an entity if the event is related to any specific entity, such as a product for a purchase event.
- `aux`: Auxiliary data associated with the event.
- `trash`: Data that is marked for removal at some point, typically used to temporarily store obsolete data or data
  created during the data migration process.
- `config`: Configuration specific to the event.
- `context`: The context of the event, providing additional contextual information.
- `tags`: Tags associated with the event.
- `journey`: Indicates how the event is positioned within the customer journey, representing the stage and rate of
  progress.
- `data`: Contains the actual event data with a predefined structure used for reporting and describing the profile,
  event, etc.
- `request`: Contains the request headers associated with the event.
- `properties`: Represents the properties of the event, which are the basic characteristics that can be recorded and
  searched but not directly aggregated. Properties can store any data, even if there are collisions in data types.
- `traits`: Represents the traits of the event, where custom profile attributes/properties can be stored. Traits have a
  structured format with predefined data types, allowing for searching, analysis, and aggregation of events.
- `trash`: Data that is marked for removal at some point, typically used to temporarily store obsolete data or data
  created during the data migration process.

