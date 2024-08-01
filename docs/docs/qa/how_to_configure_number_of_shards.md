# How to configure number of shards?

## Helm installation.

To configure the number of shards in Tracardi, you'll need to adjust the settings in the `values.yaml` (In helm installation) file used for
your Tracardi deployment. The number of shards is part of the Elasticsearch configuration, and you can define it within
the `elastic` section of the configuration file. Here's how you can do it:

### Step-by-Step Guide to Configure Number of Shards

1. **Locate Your `values.yaml` File**:
    - This file contains the configuration settings for your Tracardi installation. It's typically used during
      deployment with Helm or another orchestration tool.

2. **Edit the Elasticsearch Configuration Section**:
    - Open the `values.yaml` file in a text editor.
    - Find the `elastic` section within the file.

3. **Set the Number of Shards and Replicas**:
    - Add or update the `index` configuration to specify the number of primary shards and replicas.

Here is an example of what the `elastic` section might look like after setting the number of shards:

```yaml
elastic:
  name: es1  # The name identifier for the Elasticsearch service
  host: elastic-std-svc.elastic-standalone.svc.cluster.local  # The hostname for the Elasticsearch service
  schema: http  # The schema to use for connecting to Elasticsearch (http/https)
  authenticate: false  # Whether to use authentication when connecting to Elasticsearch
  port: 9200  # The port on which Elasticsearch is running
  verifyCerts: "no"  # Whether to verify SSL certificates (yes/no)
  index:
    shards: 5  # Number of primary shards for the index
    replicas: 1  # Number of replica shards for the index
```

4. **Apply the Configuration**:
    - Save the changes to your `values.yaml` file.
    - If you are using Helm, you can apply the configuration with the following command:
      ```sh
      helm upgrade --install tracardi <path_to_your_chart> -f values.yaml
      ```
    - This command will apply the updated configuration to your Tracardi deployment.

### Key Considerations

- **Primary Shards (`shards`)**: This setting determines how many primary shards will be created for each index. More
  shards can improve indexing and search performance, but it also means more resources will be required.
- **Replica Shards (`replicas`)**: This setting determines how many replica shards will be created. Replicas are copies
  of primary shards and help with fault tolerance and search performance.
- **Performance Impact**: Adjusting the number of shards can significantly impact performance. More shards can improve
  parallelism, but too many shards can lead to overhead and reduced performance.

## Docker compose installation

To configure the number of shards in Tracardi using docker-compose use `ELASTIC_INDEX_SHARDS` environment variable in a Docker setup, follow these steps:

### Step-by-Step Guide

1. **Edit Docker Compose File**:
   - You will add the `ELASTIC_INDEX_SHARDS` environment variable to your Tracardi service configuration in the `docker-compose.yml` file.

Here’s an example of how to configure your `docker-compose.yml` file to include the `ELASTIC_INDEX_SHARDS` environment variable:

```yaml
version: '3'
services:
  tracardi:
    image: tracardi/tracardi-api:1.0.0
    container_name: tracardi
    environment:
      - ELASTIC_HOST=http://elasticsearch:9200
      - ELASTIC_INDEX_SHARDS=5  # Set number of shards
      - ELASTIC_INDEX_REPLICAS=1  # Set number of replicas
      # Other env settings
    ports:
      - "8686:8686"
    depends_on:
      - elasticsearch
      - redis
      - mysql

  # The rest of the configuration

```

### Explanation

- **ELASTIC_INDEX_SHARDS**: This environment variable sets the number of primary shards for Elasticsearch indices created by Tracardi.
- **ELASTIC_INDEX_REPLICAS**: This environment variable sets the number of replica shards for Elasticsearch indices created by Tracardi.

### Apply Configuration

1. **Start Docker Compose**:
   - Navigate to the directory containing your `docker-compose.yml` file.
   - Run the following command to start your services with the updated configuration:

```sh
docker-compose up -d
```

## With docker commands

To set environment variables using the `docker run` command with the `-e` option, you can specify the environment variables directly in the command. Below is an example of how to run the Tracardi container with the `ELASTIC_INDEX_SHARDS` environment variable set.

### Example Using `docker run`

```sh
docker run -d \
  --name tracardi \
  -e ELASTIC_HOST=http://localhost:9200 \
  -e REDIS_HOST=redis://localhost:6379 \
  -e MYSQL_HOST=localhost \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=root \
  -e MYSQL_DATABASE=tracardi \
  -e ELASTIC_INDEX_SHARDS=5 \
  -e ELASTIC_INDEX_REPLICAS=1 \
  -p 8686:8686 \
  tracardi/tracardi-api:1.0.0
```

### Explanation of the Command

- `docker run -d`: Runs the container in detached mode.
- `--name tracardi`: Names the container "tracardi".
- `-e ELASTIC_HOST=http://localhost:9200`: Sets the Elasticsearch host environment variable.
- `-e REDIS_HOST=redis://localhost:6379`: Sets the Redis host environment variable.
- `-e MYSQL_HOST=localhost`: Sets the MySQL host environment variable.
- `-e MYSQL_USER=root`: Sets the MySQL user environment variable.
- `-e MYSQL_PASSWORD=root`: Sets the MySQL password environment variable.
- `-e MYSQL_DATABASE=tracardi`: Sets the MySQL database name environment variable.
- `-e ELASTIC_INDEX_SHARDS=5`: Sets the number of primary shards for Elasticsearch indices.
- `-e ELASTIC_INDEX_REPLICAS=1`: Sets the number of replica shards for Elasticsearch indices.
- `-p 8686:8686`: Maps port 8686 of the host to port 8686 of the container.
- `tracardi/tracardi-api:1.0.0`: Specifies the image to use.

