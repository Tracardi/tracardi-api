# How can you calculate something under aggregation conditions? How to count the number of events that meet given conditions? For example, how do I calculate purchases over the last 7 days? Or how do I calculate all purchases over 100 dollars in the last 7 days?

To achieve this, you can utilize elastic queries and generate reports in Tracardi. Firstly, it's important to learn how
to craft Elasticsearch queries. For detailed guidance on Elasticsearch aggregations, please
visit [Elasticsearch Aggregations Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html).

Here's how to create a report in Tracardi:

1. Navigate to the 'Reporting' section.
2. Complete the form and insert your Elasticsearch query.
3. Test the query to see the results.
4. Assign a name to your report and save it.
5. Your report will now appear in the report listings.
6. Open the report to find the endpoint (e.g., `POST /report/f48d0c9f-8d5c-41e9-a04f-28c934189327/run`), which will
   fetch the query results.
7. These reports can also be integrated into workflows.

Alternatively, you can use metrics to execute an aggregation and store the results directly in the profile.