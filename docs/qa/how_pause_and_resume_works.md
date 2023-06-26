# Does the pause event impact the performance? Causing the workflow cannot complete in several days.

The pause event does not directly impact the performance of the current event process. When you pause an
event, it is sent to a background scheduled task and placed in a queue for completion. This means that the current event
process continues without being affected by the pause.

Once the pause time is finished, the event either resumes as a separate event if it has been configured as such, or it
resumes as an internal system event that is not recorded but processed. In either case, the response to the current
event is returned immediately, allowing the process to continue uninterrupted.

Overall, the pause event has minimal impact on the performance of the current event process, as it is handled separately
in the background without interrupting the ongoing operations.