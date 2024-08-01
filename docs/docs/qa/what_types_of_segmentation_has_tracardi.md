# How segmentation is triggered in Tracardi?

Segmentation in Tracardi is the process of grouping profiles together. To perform segmentation, you need a profile,
which is identified by a unique profile ID in Tracardi. There are different ways to do segmentation.

1. Real-time Segmentation: This method involves categorizing customers in real time based on specific events or actions
   they take. For example, when a customer answers an email or visits a page a certain number of times, their profile is
   automatically moved to a particular segment. Tracardi provides actions like "add segment" or "delete segment" in
   workflows to perform real-time segmentation based on defined conditions real-time when the data changes.

2. Time-triggered Segmentation: This method starts the segmentation process based on the absence of certain events or
   actions. For instance, if a customer hasn't made a purchase or visited your page for a specified period, a
   time-triggered segmentation process is initiated. Tracardi runs this process periodically, such as every hour, to
   check if the defined condition is met.

3. Ad hoc Segmentation: This method involves segmenting customers based on existing data. It includes selecting profiles
   using available data, such as demographic information (age, shoe size, location), to create segments. While this
   method is less sophisticated compared to the others, it can still be useful for filtering based on aggregated values
   like the number of specific events or the most recent event type. However, adhoc segmentation is limited when it
   comes to segmenting based on event sequences or external data.

At present, Tracardi exclusively provides first two segmentation methods. However, numerous scenarios that involve the
third method can be accomplished by employing the first two methods or post event segmentation. For instance, when
segmenting based on existing data such as gender, one can identify the event responsible for altering the gender and
segment the profile in real-time as the data changes. This can be achieved by using post event segmentation or executing
an if statement and utilizing the "add segment" action to assign the relevant segment to the profile in the workflow.
