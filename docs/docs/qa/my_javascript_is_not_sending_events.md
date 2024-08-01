## My javascript is not sending events

If your JavaScript is not sending events, there could be several reasons for this issue:

* __Placement of the JavaScript__: Ensure that the JavaScript code is placed correctly on the page. The configuration
  part should be placed first, followed by the script for event sending. Check if the code is properly integrated within
  the HTML structure of the page.

* __Incorrect API address__: Verify that the API address in your JavaScript code is correct and points to your Tracardi
  server. If the API address is incorrect, the events will be sent to the wrong destination.

* __Incorrect source ID__: Make sure that the source ID specified in the JavaScript code is correct and matches the
  registered event sources in Tracardi. If the source ID is incorrect, Tracardi will not recognize the events coming
  from your JavaScript code.

* __Disabled event source__: Check if the event source specified in your script is enabled in Tracardi. If the event source
  is disabled, the events will not be processed or stored by Tracardi.

* __Transitional event source__: If the events are being sent but not saved, it is possible that the event source is set to
  be transitional. This means that the events are considered ephemeral and are processed without being permanently
  stored. Review the settings of the event source to determine if this is the case.
