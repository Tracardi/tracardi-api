# How to get started with data collection from the website.

To begin with event collection in Tracardi, follow these steps:

**1. Ensure Tracardi Installation:**

- You must have Tracardi installed on your system.

**2. Understand Test and Production Modes:**

- Tracardi GUI operates in two modes: test and production.
- The test mode collects data via API which can be configured to run as Test or Production. The default mode is tests.
- A separate instance of Tracardi can be opened with environment variable PRODUCTION set to 'yes' for production data
  collection, typically on a different port.

**3. Switch Modes as Admin:**

- As an admin, you can switch between test and production modes by clicking the 'test' label next to the Tracardi logo.

**4. Note Separation of Environments:**

- Test and production modes are separate environments, meaning data collected in the test mode is not visible in
  production, and all settings are specific to one environment.

**5. Workflow:**

- The typical workflow is to set up the system in test mode, then deploy it to production by going to '
  Maintenance/Deployment' and clicking 'Deploy to Production.' This action copies all the settings to the production
  instance.

**Example for Test Environment:**

- To confirm that your API is in test mode, click on the Tracardi logo and check for results like:
    - Frontend Version: 0.8.1
    - Backend Version: 0.8.1.01506
    - DB Version: 08x
    - API context: staging
    - GUI context: staging
    - 'API context: staging' indicates the API is in test mode.
    - 'GUI context: staging' indicates the GUI is fetching data from the test environment.

**Event Collection in Test Mode:**

- Click on 'test' near the Tracardi logo to change the mode (the GUI should turn red), indicating the GUI is fetching
  data from production.

**Return to Test Mode:**

- Click again to return to test mode.

**Create an Event Source:**

- Go to 'Inbound Traffic/Event Source' and create a new event source. This source will be available only in the test
  environment.

**JavaScript Integration:**

- Select 'Use and JavaScript' and paste the script into your page.
- Don't forget to add this part to collect events:

```html

<script>
    window.tracker.track("event-type", {"property": "value"});
</script>
```

**Check Collected Events:**

- After refreshing the page, you should see the events in 'Data/Events' in the test environment. Switching to production
  mode should display no events since you did not collect them via the production API.

# Debugging Event Collection

- To debug event collection, visit the page where you placed the script.
- Right-click on it and select 'Inspect.'
- Choose the 'Network' tab and refresh the page.
- You should see all the connections made by the page, including a connection to the Tracardi API. Check for any errors.