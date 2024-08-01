# How to enable/disable system events in docker? 

To enable system events when running Tracardi with the `docker run` command, you need to set the `SYSTEM_EVENTS`
environment variable to `yes` (`no` for disable). This can be done by using the `-e` flag to pass environment variables to the Docker
container.

Here is an example command to run the Tracardi API container with system events enabled:

```bash title="docker command" hl_lines="9"
docker run -d \
  --name tracardi-api \
  -e ELASTIC_HOST=http://<elasticsearch-host>:9200 \
  -e REDIS_HOST=redis://<redis-host>:6379 \
  -e MYSQL_HOST=<mysql-host> \
  -e PULSAR_HOST=pulsar://<pulsar-host>:6650 \
  -e PULSAR_API=http://<pulsar-host>:8080 \
  -e LOGGING_LEVEL=info \
  -e SYSTEM_EVENTS=yes \  # Enable system events
  -p 8686:80 \
  tracardi/com-tracardi-api:<version>
```

Replace `<elasticsearch-host>`, `<redis-host>`, `<mysql-host>`, `<pulsar-host>`, and `<version>` with the appropriate
values for your setup.

