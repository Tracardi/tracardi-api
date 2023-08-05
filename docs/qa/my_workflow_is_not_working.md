# My workflow is not working

If your workflow is not working, there may be several reasons for it:

1. There might be an error in the workflow itself. To address this, it is recommended to debug the workflow. You can
   start by selecting an event that is not working and trace its path through the workflow. Events that fail to process
   often have tags like "error" or "warning" associated with them.

2. Ensure that your workflow is connected to the correct event type. For instance, if you are collecting page view
   events, you should route these events to the appropriate workflow. You can configure this in the routing section,
   which can usually be found in the workflow editor under buttons like "rules" or "routing."

3. Check if you have placed the necessary JavaScript code correctly on your webpage, or if the source ID of the
   JavaScript is incorrect. If the JavaScript code is not properly implemented or the source ID is incorrect, events
   will not be visible in the system and consequently won't be processed.