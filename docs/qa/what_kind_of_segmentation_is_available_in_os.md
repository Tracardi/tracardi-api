# What segmentation types are in oen-source version.

In comparing the segmentation features of the open-source and commercial versions of Tracardi, several key differences
emerge:

**Open-Source Version**:

**Post-Event Segmentation**: This is operational in the open-source version. It initiates once a profile is updated,
triggering the segmentation process based on the newly updated profile data.

**Segmentation in Workflow Using 'Add Segment' Action**: This feature is integrated into the workflow of the open-source
version, allowing segmentation to be a part of the workflow process. This segmentation is triggered by events meaning,
segmentation can only be initiated by an event and a workflow. This process is executed in the backend
instances, which may increase the workload on the Tracardi backend.

**Commercial Version**:

**Independent Workers for Segmentation Tasks**: The commercial version employs independent workers dedicated to
segmentation tasks, differing from other models.

**Repetitive Processing Capability**: These independent workers allow for repetitive processing, meaning the system can
adapt to changes over time.

**Time-Based Segmentation**: Due to its advanced setup, the commercial version can perform segmentation based on the
passage of time, offering a more dynamic and responsive segmentation process.

Overall, the commercial version of Tracardi offers more advanced segmentation capabilities, including time-based
segmentation and reduced load on backend processes, thanks to its independent worker system. The open-source version,
while offering basic segmentation features, has limitations compared to its commercial counterpart.

