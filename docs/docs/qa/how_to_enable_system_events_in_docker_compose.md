# How to enable system events in docker compose?

To enable system events in Tracardi when using Docker Compose, follow these steps:

1. **Locate your Docker Compose file**: This file is typically named `docker-compose.yml` and contains the configuration
   for all the services you are running.

2. **Modify the environment variables**: Add or modify the environment variables for the Tracardi service to
   include `SYSTEM_EVENTS=yes`.

Here is an example of how you can adjust your `docker-compose.yml` file:

```yaml title="Part of docker-comose.yaml" hl_lines="14"
version: '3.7'

services:
  tracardi:
    image: tracardi/com-tracardi-api:1.0.0  # or use the specific version you are running
    container_name: tracardi-api
    environment:
      - ELASTIC_HOST=http://elasticsearch:9200
      - REDIS_HOST=redis://redis:6379
      - MYSQL_HOST=mysql
      - PULSAR_HOST=pulsar://pulsar:6650
      - PULSAR_API=http://pulsar:8080
      - LOGGING_LEVEL=info
      - SYSTEM_EVENTS=yes  # Enable system events
    ports:
      - "8686:80"

# The rest of your docker-compose file.
```

3. **Deploy the updated configuration**: After making these changes, you need to restart your Docker Compose setup to
   apply the new configuration. You can do this by running:

```bash
docker-compose down
docker-compose up -d
```

By adding `SYSTEM_EVENTS=yes` to the environment variables of the Tracardi service, you enable system events within the
Tracardi instance running in Docker Compose. This will allow Tracardi to generate and handle internal system events.