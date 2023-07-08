# How to aggregate events for segmentation?

To aggregate data for segmentation in Tracardi, you can follow these steps:

1. Ensure that events (certain event type) capture the relevant information you need for segmentation, such as transaction amounts and wallet
   additions.

2. Create reports that aggregate and summarize the event data, using Elasticsearch query.

3. Design a segmentation workflow that utilizes these reports as a basis for segmenting the profiles. Use load report plugin.

4. The aggregation happens at the profile level by grouping the events associated with each profile. This allows you to
   calculate aggregated values per profile, such as the total transaction amount over a specified period.

Additionally, the segmentation workflow is executed on every profile within the tenant. The system efficiently filters
profiles that need to be segmented, reducing unnecessary processing.

If you have complex aggregation requirements or want to populate profiles with necessary data for segmentation, you can consider using
custom jobs. These jobs can aggregate data and update profile stats with the aggregated information, enabling
conditional segmentation based on the updated profile stats.
