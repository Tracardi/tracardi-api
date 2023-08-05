# What is the difference between event traits and properties, and what is event indexing?

Event traits and properties are both characteristics of an event in Tracardi. Properties are basic characteristics that
can be recorded and searched but cannot be directly aggregated. Traits, on the other hand, are structured and have data
types, allowing for analysis and aggregation. Event indexing is the process of storing and organizing event data,
allowing for different types of reports and aggregations based on the properties and traits of events.

# How can I map event properties to profile traits or PII in Tracardi?

You can map event properties to profile traits or Personally Identifiable Information (PII) by using event-to-profile
coping in Tracardi. This allows you to define mappings between specific event properties and corresponding profile
traits or PII fields. By defining these mappings, you can transfer relevant data from events to the corresponding
profile attributes during processing.

# Can I create a segment based on profile traits without the need for events?

Yes, you can create a segment based on profile traits without the need for events. Tracardi supports conditional
segments, which are triggered periodically. You can define segment rules (condition) based on profile data and apply
them to both existing profiles and new profiles that meet the specified criteria.

# How can I create reports in Tracardi?

To create reports in Tracardi, you can utilize the reporting capabilities provided by the platform. It uses
Elasticsearch queries. Tracardi allows you to aggregate and analyze data from events and profiles to generate insightful
reports. You can define the aggregation criteria, select the relevant data sources (events, traits, properties), and
specify the desired output format.

# How can I achieve a use case where I create a segment based on specific transaction criteria in Tracardi?

To achieve a use case where you create a segment based on specific transaction criteria in Tracardi, you can follow
these steps:

- Collect events for each transaction, including the transaction amount as a property.
- Create a report that aggregates the transaction amounts per profile within a specified time period.
- Use this report as a data source in a segmentation workflow.
- Define the segment criteria based on the aggregated transaction amounts, specifying the desired thresholds or
  conditions.
- Set up the segmentation workflow to run at regular intervals, evaluating the report data and adding profiles to the
  segment if they meet the defined criteria.
