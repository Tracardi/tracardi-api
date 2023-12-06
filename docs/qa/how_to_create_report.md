# How to create report

To create a report, first navigate to the "Reporting" section and select "Create Report." You'll need to provide a name
for your report. Next, choose the index you wish to query from the available options: 'available', 'profile', 'event',
or 'session entity'.

For querying, you'll use an Elasticsearch query. Refer to the Elasticsearch documentation for guidance on how to
construct these queries. Remember, your query will be run on the chosen index each time you execute the report.

You can incorporate parameter placeholders in your query. For instance, use {"profile.id": "{{profile_id}}"}. Any
placeholders set within {{ }} will be substituted with the actual parameters when the report runs. For example, you
could use {"profile_id": "<some-id>"}. Keep in mind that the entire string should be a parameter; partial placeholders
like "{{profile_id}}-some-other-data" won't work.

Test the query and save the report.

Reports are also available via API endpoint. Click on report to see the endpoint URL.