# How many records can tracardi store?

Tracardi can store a significant amount of data. The largest production instance currently holds 0.3 billion events
collected in 3 months. The same amount can be stored as profiles. Tracardi uses Elasticsearch as its backend storage,
which is capable of storing records in the billions. The data is split into monthly indices for easy management, data
movement between cluster nodes, and automatic archiving if needed.
