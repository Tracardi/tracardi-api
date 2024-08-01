### Why Is My Script on the Page Not Sending Events?

I placed the Tracardi script but do not see any events.

There can be several reasons why your JavaScript script on the page is not sending events to Tracardi. Here are some
common issues and troubleshooting steps:

1. **Incorrect Script Placement**:
   Ensure that the Tracardi integration script is correctly placed on your webpage. The script should be placed in
   the `<head>` section of your HTML file to ensure it is loaded correctly. It should be before
   the `window.tracker.track("page-view", {});` commands.

2. **Script Errors**:
   Check the browser console for any JavaScript errors. Any errors in your script can prevent it from executing
   correctly. Make sure that you got the right Javascript snippet for your event source. To get the correct snippet go
   to `Event sources`. Select the event source then click `Javascript and use` tab and there is the script.

3. **Network Issues**:
   Verify that your network is allowing requests to Tracardi's endpoint. Sometimes, network policies or ad blockers can
   prevent the script from sending data. If your page is protected by SSL (https), then your Tracardi API should also be
   SSL. Other potential network issues include firewall restrictions and DNS problems.

4. **Configuration Issues**:
   Ensure that the configuration for your Tracardi instance is correct, including the endpoint URL and any necessary
   authentication tokens such as the source ID. If the source ID is incorrect, you should see an error message.

5. **Event Source Settings**:
   Check the event source settings in Tracardi to ensure that it is configured to accept events from your script. This
   includes checking if the configuration of the event source does not forbid events from outside the configured list of
   domains.

6. **Tracker Payload Schema**:
   Check if the tracker payload schema is correct. This issue typically arises when collecting through the API and
   setting the schema manually. If you use JavaScript, this should not be an issue.

7. **Browser Compatibility**:
   Ensure that the script is compatible with the browsers being used. Some features may not work in older or unsupported
   browsers.

### Steps to Troubleshoot

1. **Check Script Placement**:
   Ensure the script tag is correctly placed and the Tracardi endpoint is reachable.

2. **Console Logs**:
   Open the browser console (F12 or right-click -> Inspect -> Console) to check for any errors or messages.

3. **Network Tab**:
   Use the Network tab in the browser developer tools to check if the requests to the Tracardi endpoint are being sent
   and if they receive a response.

4. **Review Documentation**:
   Consult the Tracardi documentation for any recent changes or updates that might affect how events should be sent.

5. **Check Event Source Configuration**:
   Verify that the event source configuration in Tracardi is correct and matches the script settings.

By following these steps, you should be able to identify and resolve the issue preventing your JavaScript script from
sending events to Tracardi.