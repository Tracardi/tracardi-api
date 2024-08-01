# How can I use reports?

Reports in Tracardi serve as a means to analyze and extract valuable insights from the collected data. While Tracardi
itself is not an analytical tool, it can integrate with external platforms like Tableau, Amplitude, Matomo, Google
Analytics, and others, allowing you to send data from Tracardi to these platforms for more sophisticated analysis and
report generation. This can be done by utilizing queues or other mechanisms for data transfer.

Kibana is another analytical tool that can be used with Tracardi. It is specifically designed to work with data stored
in Elasticsearch, which is the underlying database technology used by Tracardi. Kibana provides powerful visualization
and analysis capabilities, allowing you to explore and gain insights from the data stored in Elasticsearch.

In addition to integrating with external analytical platforms, Tracardi also offers its own reporting functionality. You
can use Reports in Tracardi to run Elasticsearch queries on the collected data. These queries can aggregate the data and
provide aggregated values for events, such as sums, averages, medians, or event counts based on specific properties. For
example, you could calculate the total sum of the "amount" property for purchase events associated with a particular
profile.

Once a report is created, it can be loaded into a workflow as an action. This means that you can use the report's
results as input for making decisions within the workflow. By leveraging reports in Tracardi, you can extract relevant
information from the data and incorporate it into your decision-making processes.

In summary, reports in Tracardi serve the purpose of extracting aggregated data from the Tracardi database and utilizing
it for decision-making within workflows. Additionally, Tracardi can integrate with external analytical platforms like
Tableau, Amplitude, Matomo, and Google Analytics to enable more advanced analysis and reporting capabilities.