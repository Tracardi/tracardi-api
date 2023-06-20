# My live segmentation does not change profile traits?

Live segmentation process does not update profile traits unless there is a change in the segment associated with the
profile. In other words, if the segment of a particular profile remains the same during the live segmentation run, the
profile traits associated with that segment will not be updated.

Live segmentation process is designed to periodically evaluate and categorize profiles based on certain criteria defined
in segmentation workflow. However, it only updates the profile traits if there has been a change in the segment to which
a profile belongs.