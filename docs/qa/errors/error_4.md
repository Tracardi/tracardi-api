# What does the error message "Cannot connect to host elasticsearch:9200 ssl:default \[Connection refused\]" indicate in Tracardi?

The error message "Cannot connect to host elasticsearch:9200 ssl:default \[Connection refused\]" suggests that the
Elasticsearch server is not running or not accessible. This message is typically displayed when Tracardi starts before
Elasticsearch is ready. Tracardi will automatically resume when Elasticsearch becomes available.