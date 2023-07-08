# The overall concept of segmentation in Tracardi

The overall concept of segmentation in Tracardi involves aggregating event data to facilitate the segmentation process
or segmenting on profile data. Tracardi offers two types of segmentation: conditional and workflow. Conditional
segmentation applies specific conditions to the data and identifies profiles that meet those conditions it does not
check the events. On the other hand, workflow segmentation evaluates each profile and determines whether it should be
assigned to a particular segment based on the workflow's logic. Workflow logic can aggregate events to retrieve more
insights about profile past behaviour.

# What types of segmentation algorithms are in tracardi?

Tracardi utilizes a combination of conditional segmentation and workflow segmentation mechanisms. The segmentation
workflow applies conditions to the data and marks profiles that meet the specified criteria. The workflow segmentation
processes each profile and determines whether it should be moved to a specific segment based on the workflow's logic.

Therefore, the type of segmentation mechanism in Tracardi is a combination of conditional segmentation and workflow
segmentation.

# How can I achieve this use case: Create a segment based on the users who have transacted worth X USD in the last 30 days and have added Y USD to the wallet in the last 30 days. Looks like it is based on event properties. But I'm not sure how we can find the profiles that have X events with a value of property Y.

To achieve this use case, you can utilize a combination of segmentation and event properties. You can create a
segmentation workflow that filters profiles based on event properties such as transaction amount and wallet addition
amount. By specifying the desired values for X and Y, you can define the criteria for segmenting the users. The
segmentation workflow will evaluate the event properties for each profile and include the profiles that meet the
specified criteria in the segment.

# Where is this data stored? In events?

Yes, the relevant data such as transaction amounts and wallet additions would typically be stored within the events.
Events are structured data entries that capture specific actions or occurrences related to user behavior or system
events. By extracting and analyzing the event properties, you can derive valuable insights and create targeted segments
based on specific event criteria.

# Just want to understand if this use case is doable and how to achieve it. Let's assume I have an event for every transaction, and the amount of the transaction is a property of the event.

Yes, the use case you described is achievable by leveraging event properties. If you have an event for every
transaction, and the transaction amount is a property of the event, you can use that information to filter and segment
profiles based on their transaction history and wallet additions. By defining the desired criteria and applying them in
your segmentation workflow, you can create segments that meet the specified conditions.

# So I understand correctly. We have events like purchase with some amount.

Yes, that's correct. In this case, the events represent purchases, and the corresponding event properties capture the
transaction amounts associated with each purchase. By analyzing these event properties, you can gain insights into user
spending behavior and create segments based on specific purchase criteria.

# We need to aggregate on it in some period of time? To sum up the amounts?

Yes, you can perform aggregation on the event data over a specific period of time to derive meaningful insights. For
example, you can aggregate the transaction amounts for each user over the last 30 days to determine their total spending
during that period. By summing up the transaction amounts, you can identify users who have transacted a certain worth (X
USD) within the specified timeframe.

# Yes, correct. And then how do we know the profiles that match that criteria?

To identify the profiles that match the specified criteria (e.g., users who have transacted worth X USD and added Y USD
to the wallet), you can use the segmentation workflow. The segmentation workflow applies the defined criteria to the
event data and filters out the profiles that meet the criteria. This way, you can obtain a segment of users who fulfill
the required transaction and wallet addition conditions.

# Ok, we need to use the segmentation workflow and reports. Can you give me access to your demo so I can create the report, and you can see how I have done it?

Unfortunately, as an AI language model, I don't have the capability to provide access to specific demos or systems.
However, I can help guide you through the general process of creating a segmentation workflow and utilizing reports. If
you have any specific questions or need assistance with the steps involved, feel free to ask!

# Ok, so it's a combination of both segmentation and reports. But then I need to generate the event first so you can do the report, right? I just want to understand how this is achievable.

That's correct. To generate the necessary data for the reports and segmentation, you would need to have the events
capturing the relevant information. In this case, the events would include details of user transactions and wallet
additions. Once the events are recorded, you can create reports that aggregate and summarize the data, allowing you to
analyze the transaction and wallet information. The segmentation workflow can then utilize these reports to filter and
segment the profiles based on the desired criteria.

# So the reports for the aggregation? And then the segmentation workflow?

Yes, that's one possible approach. First, you would create reports that aggregate and summarize the event data, allowing
you to analyze specific metrics such as transaction amounts and wallet additions. These reports provide valuable
insights into user behavior. Then, you can design a segmentation workflow that utilizes these reports as a basis for
segmenting the profiles. The segmentation workflow would apply the defined criteria to the aggregated data, resulting in
the creation of segments based on the specified conditions.

# The process is like this: you are collecting events with amounts. In the system, you create a report on those events that aggregates the data and then use this report in the segmentation workflow. Segmentation kicks off every 15 minutes and uses this report to decide whether to add a segment or not.

That's a valid process flow. By collecting events with transaction amounts and wallet additions, you have the raw data
required for analysis. Then, you can create reports that aggregate and summarize this data, providing valuable insights
into user behavior and spending patterns. The segmentation workflow can utilize these reports periodically (
e.g., every 15 minutes) to assess whether a profile meets the criteria for inclusion in a specific segment. Based on the
defined conditions, the segmentation workflow will determine whether to add the profile to the segment or not.

# But then my question is, how does the aggregation happen? Because the aggregation should be per profile, and then the profiles that match this will be in the segment. The aggregation part is what confuses me because the aggregation will be done on the events index, but how is this connected to the profile? To do the aggregation of the amount of the events per profile?

The aggregation can be done at the profile level by grouping the events associated with each profile. Each event
contains information about the transaction amount and other relevant details. By grouping the events per profile, you
can calculate the aggregated values, such as the total transaction amount for each profile over a specified period. The
aggregation process connects the events to their corresponding profiles, allowing you to aggregate the event data per
profile.

# How does the aggregation happen for segmentation?

The aggregation is performed per profile, where profiles that match the aggregation criteria are included in the
segment.

# Is the aggregation done on the events index?

No, the aggregation can be performed on any index.

# Can the aggregation be extended to perform actions like sum, average, median, etc.?

Yes, the aggregation action can be extended to perform various calculations such as sum, average, median, and more.

# Do we need to use reports for aggregation?

No, there is no need to use reports for aggregation. The aggregation can be done directly within the segmentation
workflow with aggregate events plugin. But we can also use load report plugin to load report data.

# How does the system know which profiles to aggregate for?

The system understands the context and knows for which profile to perform the aggregations or reports.

# Is the segmentation workflow executed on every profile of the Tenant?

Yes, the segmentation workflow is executed on every profile within the tenant.

# How efficient is the segmentation process?

The segmentation process is efficient as it filters only the profiles that need to be segmented, reducing unnecessary
processing.

# Can a job be used for aggregating data and then applying conditional segmentation?

Yes, a job can be used to aggregate data and populate the necessary information in profile stats. Conditional
segmentation can then be applied based on the aggregated data.

# Can aggregation be performed per event type and event property?

Aggregation per event type attached to a profile can be useful for conditional segmentation. Aggregation per event
property, are also available.

# Can everything be achieved through reports, jobs, or API calls?

Yes, most requirements can be achieved using reports, custom jobs, or API calls to services with code. These methods
provide flexibility in implementing various functionalities and customizations.

# How can I create a segment based on users who have transacted a certain amount in the last 30 days and added a certain amount to their wallet in the last 30 days?

To achieve this use case, you can use a combination of segmentation workflows and reports. First, you need to have
events that track each transaction, with the transaction amount as a property of the event. Then, you can create a
report that aggregates the transaction amounts over a specific period, such as the last 30 days. Once you have the
aggregated data, you can use it in a segmentation workflow to identify the profiles that meet the criteria based on the
aggregated amounts. The segmentation workflow can be scheduled to run periodically, such as every 15 minutes, and it
will add the matching profiles to the desired segment. The aggregation is done on the events index, and the system
connects the aggregated data to the corresponding profiles for segmentation.