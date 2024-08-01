# Why my post event segmentation does not work?

There could be several reasons why your post event segmentation is not being triggered. Here are some possible
explanations:

* Event Not Occurring: Post event segmentation relies on specific events to trigger the segmentation process. If the
  expected event is not occurring or not being sent to the system, the segmentation won't be triggered. Make sure that
  the relevant events are being generated and properly captured by your system.

* Profile Not Updated: Post event segmentation is based on changes or updates to the profile data. If there are no
  changes to the profile, the segmentation conditions won't be evaluated. Ensure that the events being received are
  properly updating the profile data, triggering the segmentation process.

* Segmentation Conditions Not Met: Each segmentation has specific conditions that profiles must meet to be assigned to a
  segment. If the conditions are not being met, the segmentation won't occur. Double-check your segmentation conditions
  to ensure they are correctly defined and aligned with the profile data being updated by the events. For example, if
  you have a condition that checks if the number of visits is greater than 10, make sure that the profile data reflects
  this change and satisfies the condition.

To troubleshoot the issue, you can:

- Review your event data and check if the expected events are being received and processed.
- Monitor the profile data to ensure that it is being updated correctly in response to the events. Check if the workflow
  uses `Update Profile` after the profile data was changed.
- Verify that the segmentation conditions are properly defined and align with the updated profile data.

By analyzing these factors, you should be able to identify the cause of the post event segmentation not working as
expected and take appropriate steps to resolve the issue.

---
This document answers the following questions:

- When post event segmentation is triggered.