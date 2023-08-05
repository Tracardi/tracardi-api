# How live segmentation works from technical point of view?

From a technical point of view, live segmentation involves several components and processes working together. Here's an
overview of how live segmentation works:

* Workflow Definition: Live segmentation starts with defining workflows, which outline the steps and logic for
  segmenting profiles. These workflows specify the conditions, actions, and filters required to classify profiles into
  segments.

* Profile Retrieval: The live segmentation system fetches the defined workflows. It then retrieves the profiles that
  need to be segmented. Profiles typically contain user data, such as demographics, preferences, behaviors, and
  interactions.

* Iteration and Execution: The system iterates over each profile and executes the defined workflow for that profile.
  This means that the segmentation logic is applied to each individual profile to determine its segment membership.

* Task Queuing: To efficiently manage the segmentation tasks, a pool of segmentations is created. Each segmentation task
  is queued in a Redis queue, which acts as a job queue system. The queue holds the tasks until a worker is available to
  process them.

* Segmentation Job Docker: The segmentation job docker container, named "tracardi/com-tracardi-segmentation-job", is
  responsible for orchestrating the segmentation tasks. It picks up all workflows, batches profiles and schedules them
  for processing.

* Segmentation Worker Docker: The segmentation worker docker container, named "
  tracardi/com-tracardi-segmentation-worker" performs the actual segmentation computations. When a worker receives a
  task from the job docker, it applies the workflow logic to the corresponding profile, determines the segment(s) the
  profile belongs to, and stores the segmentation results in profile. This way segmentation can run in parallel.

* Result Storage: After a worker finishes segmenting a profile, it stores the segmentation results in profile in key __segments__. 

* Cron Job: Live segmentation is often scheduled as a recurring task using a cron job. The cron job triggers the
  segmentation process at specified intervals, ensuring that profiles are regularly segmented based on the defined
  workflows. Docker tracardi/com-tracardi-segmentation-job is responsible for this.

In summary, live segmentation involves defining workflows, retrieving profiles, queuing segmentation tasks, and
executing the tasks using dedicated job and worker docker containers. The segmentation process applies the workflow
logic to each profile, determines the corresponding segment(s), and stores the results for further analysis.

---
THis document answers the questions:
- Which dockers are responsible for live segmentation
- Is live segmentation scheduled?
- Does live segmentation run in parallel?