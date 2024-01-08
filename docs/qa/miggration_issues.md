# My data was not migrated how can I debug what happened?

If you use docker on you local machine check the log of upgrade worker..

To do that, you can follow these steps:

1. **Identify the Container ID or Name**:
   First, you need to find out the ID or the name of the Docker container running the upgrade worker. You can list all
   running containers by executing:
   ```
   docker container ls
   ```
   This command will show you a list of all active containers, including their IDs, names, and other details.

2. **View Logs**:
   Once you have identified the container ID or name of the upgrade worker, you can view its logs using the following
   command:
   ```
   docker logs [CONTAINER_ID_OR_NAME]
   ```
   Replace `[CONTAINER_ID_OR_NAME]` with the actual ID or name of your upgrade worker container.

   For example, if the container ID is `abc123def456`, the command would be:
   ```
   docker logs abc123def456
   ```

3. **Tail Logs in Real-Time**:
   If you want to continuously monitor the logs as new log entries are created, you can use the `-f` flag to "follow"
   the log output:
   ```
   docker logs -f [CONTAINER_ID_OR_NAME]
   ```

4. **Filter Logs**:
   If you're looking for specific log entries or want to filter the logs, you might need to use additional command-line
   tools like `grep`. For example:
   ```
   docker logs [CONTAINER_ID_OR_NAME] | grep "some specific log text"
   ```

5. **Checking Past Logs**:
   Docker logs show the output from the container since it was started. If the container has been restarted, you might
   not see older logs. In such cases, it's important to have a logging solution in place that archives logs for future
   analysis.

These steps should help you access and analyze the logs of your upgrade worker in Docker, providing insights into its
operation and any issues it might be encountering.

# Why my data was not migrated?

We conduct tests on various data sets during migration, but there might be instances where your profiles and events are
structured in ways we didn't anticipate. In such cases, the migration mappings might not function as expected. To
identify any discrepancies, please review the upgrade worker logs to determine which fields are not aligning correctly.
After identifying these issues, kindly report them to us for further assistance.