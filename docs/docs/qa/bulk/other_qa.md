# Other Q&A

__Q: Is it possible to segment data based on leads' attributes such as lead added date, lead source, lead ID, opens,__
clicks, sold/not sold, click/open dates, etc.?

A: Yes, segmentation can be done in regular Tracardi workflows. You can segment data based on any internal or external
data or conditions set within the workflow.

__Q: How many customer interactions can Tracardi log, including opens, clicks, and sales over the life of the lead?__

A: Tracardi has been tested to store 10 million events per profile, but the limit ultimately depends on the storage
size. Tracardi is designed to handle large volumes of data efficiently, as evidenced by instances with 0.3 billion
events loading in a fraction of a second. The scalability is mainly due to the storage capabilities of Elasticsearch.

__Q: Can Tracardi import customer interactions from external email marketing software like Mailwizz? Is it streamed live
or can it be scheduled? __

A: To import customer interactions from Mailwizz or similar software, you can set up a trigger in the software's table
to copy the interaction records to another table. Then, a script can move the copied records to Tracardi using the
Tracardi API and remove the duplicated records. This process can be scheduled using cron jobs, Kubernetes jobs, or other
scheduling mechanisms. If Mailwizz supports webhooks, real-time importing can be achieved through webhooks.
Additionally, you can include pixels in emails for further tracking if required.

__Q: Can newly added data be analyzed for duplicates or used to enrich current profiles if it's the same lead? Are leads
assigned a unique ID?__

A: Tracardi's main purpose is to maintain a single profile that includes data copied from events or external systems.
The profiles are automatically merged and deduplicated at identification points if configured to do so. Tracardi assigns
unique IDs to leads, and it also keeps a history of previous IDs. This allows Tracardi to track customers across
different devices and merge their profiles.

__Q: Does Tracardi need to be integrated with a data warehouse tool to store all the data? Are there any recommendations
for such integration?__

A: Tracardi uses Elasticsearch and Kibana for simple analytics, providing a comprehensive overview of individual
profiles. However, Tracardi is not designed as an analytical tool for aggregate analysis of all customers. For in-depth
analysis, it is recommended to use an external system of your choice. Tracardi can send event data to external systems
if necessary, allowing integration with data warehouse tools or other analytical platforms.
