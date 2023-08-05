# Troubleshooting "Network Error" when Selecting the API URL

If you encounter the error message "Status: undefined, Message: undefined, Details Error: Network Error" while trying to
access the API URL, it indicates that there might be an issue with the connection to the Tracardi API. To troubleshoot
this problem, follow these steps:

1. **Double-check the API URL**: Ensure that the API URL you are using is accurate and correctly points to the Tracardi
   API. A mistyped or incorrect URL could lead to a 404 response or similar errors.

2. **Test the API URL in the browser**: To confirm if the URL is correct, enter the API URL directly into your web
   browser and see if you receive a response. A valid response should look like this:
   ```json
   {
     "details": "Not found"
   }
   ```
   The "Not found" message is expected since you are providing the API URL only, not the full endpoint URL.

3. **Check API logs**: Examine the logs of the API server to identify any errors related to the connection between the
   API and the Elasticsearch server. If there are issues with the connection, it could result in the "Network Error"
   mentioned in the original message.

4. **Verify Elasticsearch connectivity**: Ensure that the Elasticsearch server is operational and accessible. The API
   should be able to establish a connection to the Elasticsearch server for proper functionality. If there are any
   problems with Elasticsearch, it may prevent the API from functioning correctly. Please note that connection
   to `localhost:9200` is not possible when running docker. Use IP instead.

5. **Verify Redis connectivity**: Ensure that the Redis server is operational and accessible. The API should be able to
   establish a connection to the Redis server for proper functionality. If there are any problems with Redis, it may
   prevent the API from functioning correctly. Please note that connection to `localhost:6379` is not possible when
   running docker. Use IP instead.

By following these steps, you can effectively troubleshoot and identify the cause of the "Network Error" when selecting
the API URL. If you still experience issues please look for `Docker container installation` in documentation. 

---
This document also answers the questions:

* I see error: Status: undefined, Message: undefined, Details Error: Network Error, when selecting the API URL
* I see error: Error connection to localhost:6379

