# Why my live segmentation does not work?

There could be several reasons why your live segmentation is not working as expected. Here are some possible
explanations:

* Docker Configuration: Ensure that the required Docker containers, such as tracardi/com-tracardi-segmentation-job and
  tracardi/com-tracardi-segmentation-worker, are properly installed and running. Check their status and logs to identify
  any potential issues or errors that could be preventing the live segmentation from working.

* Schedule and Frequency: Verify the schedule and frequency at which the live segmentation is set to run. If the
  schedule is not properly configured or the frequency is too low, it may result in the live segmentation not being
  triggered as frequently as desired. Adjust the schedule or frequency if necessary.

* Workflow Enablement: Check if the live segmentation workflow is enabled in your system. Navigate to the processing
  and find `live segments` section and ensure that the segmentation workflow is properly connected and enabled. If
  it is not enabled, the live segmentation will not be executed.

* Complex Segmentation Conditions: Live segmentation can involve complex conditions and logic. Review the segmentation
  conditions defined in your workflow and ensure they accurately reflect the criteria for segmenting profiles. If the
  conditions are too strict or not properly configured, it may result in profiles not meeting the segmentation criteria
  and thus not being segmented.

By addressing these aspects, you should be able to identify the underlying cause of the live segmentation not working
and take appropriate steps to resolve the issue.

---
- How ot debug live segmentation?