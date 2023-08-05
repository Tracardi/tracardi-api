# My live segmentation does not change profile traits?

Live segmentation process does not update profile segments, traits, etc. unless there is a __profile update__ in the workflow.
In other words, if the segment of a particular profile is changed during the live segmentation run, the
profile will not be updated unless you use __update profile__ action.

Live segmentation process is designed to periodically evaluate and categorize profiles based on certain criteria defined
in segmentation workflow. 