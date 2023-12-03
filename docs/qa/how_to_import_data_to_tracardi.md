# How to import data to Tracardi

Tracardi provides a powerful API that allows you to easily import data into the platform. The API allows you to send
data from any source, such as a database, a web service, or a file, and have it automatically ingested into the Tracardi
platform.

There are 2 way to import data. One via GUI. Find Import in left-hand menu and follow the instructions. Note that
currently only imports from mysql and elastic search are available via gui.

To import any data into Tracardi, you will need to create an API call that sends the data to the Tracardi platform. The
API call should include the data you want to import, as well as any additional information that is needed to properly
process the data.

Once the API call is performed, you can use the Tracardi platform to manage the data. This includes creating workflows
to process the data, creating rules to shape the data, and creating segments to target customers.

For more information look for `/track` API in the documentation.



