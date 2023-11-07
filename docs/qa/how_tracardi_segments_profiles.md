# How tracardi segments profiles

Tracardi retrieves profiles for segmentation depends on the type of segmentation being
executed. For time-based segmentations, such as identifying profiles that have engaged more than a month ago, Tracardi
must check every profile because the qualifying criteria (time in this case) are continually changing. There's no way to
pre-filter profiles for this kind of segmentation. Workflow segmentation is this kind of segmentation type.

For property-based segmentations, Tracardi fetches only those profiles that have had recent changes, as these changes
might cause a profile to shift from one segment to another. Additionally, Tracardi can perform on-event segmentation
within automation workflows, where segments can be added dynamically based on events such as a purchase, which might
change a profile’s segment categorization. For this use-case use "add segment" action within tracardi automation workflow. 