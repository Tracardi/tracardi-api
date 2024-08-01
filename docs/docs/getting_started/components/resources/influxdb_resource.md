InfluxDB is an open-source time series database (TSDB). It includes APIs for storing and querying data, processing it in
the background for ETL or monitoring and alerting purposes, user dashboards, and visualizing and exploring the data and
more.

# Resource configuration and set-up

In order to enable an integration between __InfluxDB__ and Tracardi you need an API. The __InfluxDB__ API provides a programmatic 
interface for all interactions with __InfluxDB__, it uses API tokens to authorize API requests. API tokens ensure secure 
interaction between __InfluxDB__ and Tracardi. An API token belongs to a specific user and identifies InfluxDB permissions 
within the user’s organization.

To manage InfluxDB API Tokens in the __InfluxDB UI__:

1. Navigate to the API Tokens management page.
2. In the navigation menu on the left, select Data (Load Data) > Tokens.
3. Click a token name in the list to view the token and a summary of access permissions.

For Creating a token in the __InfluxDB UI__:

1. From the API Tokens management page, click __Generate__ and select a token type (Read/Write Token or All Access API
   Token).
2. In the window that appears, enter a description for your token in the __Description__ field.<br>
3. If generating a read/write token:
   * Search for and select buckets to read from in the Read pane.
   * Search for and select buckets to write to in the Write pane.
4. Click __Save__.

If you need more help with getting your API Token visit: https://docs.influxdata.com/influxdb/v2.4/security/tokens/
