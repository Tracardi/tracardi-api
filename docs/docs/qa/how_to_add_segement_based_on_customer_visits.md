# How to do simple segmentation with number of visits.

To add a segment based on the number of visits made to a profile, you can follow these steps:

* Start by setting up a workflow in your system or platform.
* Use an "if" condition to check the number of visits made to the profile.
* Within the "if" condition, port TRUE connect the "add segment" action to add the desired segment to the profile.
* After adding the segment, update the profile to save the changes.

Here's an example of how the workflow could be structured:

* `Start`
* `If` (profile@metadata.time.visit.count == 1)
* On port TRUE connect `Add Segment` (choose the segment you want to add)
* `Update Profile` (save the changes)

Regarding the syntax, the profile's visit count is stored in `metadata.time.visit.count`. It is automatically 
increased with every visit.
