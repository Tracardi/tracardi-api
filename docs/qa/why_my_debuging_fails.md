# Why does debugging fail to function even though the workflow runs correctly during normal execution?

Debugging might not work while the workflow executes correctly due to the way the debugging environment is set up. In a
typical workflow execution, the system automatically handles loading the internal state of workflow, which includes the
relevant event and profile data. However, in a debugging environment, this automatic setup doesn't occur by default.

The key issue here is the setup of the workflow's internal state for debugging:

1. **Selecting the Event for Debugging**: You can manually specify which event you want to debug. This is typically done
   by finding the event in a list of events and clicking the debug button. This action
   should load the selected event into the workflow for debugging.

2. **Setting Event and Profile IDs**: By default, when you enter the workflow in debug mode, it starts with an empty
   event and profile. This means that the debugger does not have any specific data to work with, leading to ineffective
   debugging. To counter this, you need to manually set the `event_id` and `profile_id` in the start node. This action
   instructs the system to load the relevant data first, creating an environment that mirrors the actual workflow
   execution.

In summary, debugging may not work because the debugger doesn't automatically know which event to process. You need to
manually set up the event and profile information in the workflow's internal state for the debugger to function
correctly. This setup discrepancy between normal execution and debugging can lead to situations where the workflow runs
fine normally but encounters issues in the debug mode.