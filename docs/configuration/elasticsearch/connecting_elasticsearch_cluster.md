## Connecting to elastic cluster

To connect to elastic cluster you must provide location to all cluster nodes. To configure Tracardi connection to
elastic change ELASTIC_HOST in docker-standalone.yaml file.

```yaml
    ELASTIC_HOST: "node-1,node-2,node-3"
```

If your cluster is behind a reverse proxy you will need only one url.

### SSL and Authentication

You can configure Tracardi to use SSL for connecting to your elasticsearch cluster. Use RFC-1738 to specify the urls:

```yaml
    ELASTIC_HOST: "https://user:secret@node-1:443,https://user:secret@node-2:443,https://user:secret@node-3:443"
```

There is another way to connect to elastic cluster.

```yaml
    ELASTIC_HOST: "node-1,node-2,node-3",
    ELASTIC_PORT: 443,
    ELASTIC_SCHEME: "https",
    ELASTIC_HTTP_AUTH_USERNAME: "user",
    ELASTIC_HTTP_AUTH_PASSWORD: "pass",
```

To include certificate verification and HTTP type the following line:

```yaml
    ELASTIC_CA_FILE: "path to certificate",
```

### Connect using API_KEY

Elasticsearch Service supports API key-based authentication.

To obtain an API key:

* Log in to the Elasticsearch Service Console.
* Select your deployment on the home page in the Elasticsearch Service card or go to the deployments page.
* Under the Features tab, open the API keys page. Any keys currently associated with your account are listed.
* Select Generate API key.
* Provide a name and select Generate API key.
* Copy the generated API key and store it in a safe place. You can also download the key as a CSV file.

The API key has no expiration, so it may be used indefinitely. The API key has the same permissions as the API key
owner. You may have multiple API keys for different purposes and you can revoke them when you no longer need them.

Here is the configuration for connection with API_KEY

```yaml
    ELASTIC_HOST: "site-1.local,site-2,site-3.com",
    ELASTIC_PORT: 443,
    ELASTIC_SCHEME: "https",
    ELASTIC_API_KEY_ID: 'api-key-id',
    ELASTIC_API_KEY: 'api-key'
```

### Connect using CLOUD_ID

Here is the configuration for connection with CLOUD_ID. With COULD_ID you do not need the hosts or port number.

```yaml
    ELASTIC_CLOUD_ID: 'cluster-1:dXMa5Fx...',
    ELASTIC_HTTP_AUTH_USERNAME: "user",
    ELASTIC_HTTP_AUTH_PASSWORD: "pass"
```

### CERT Verification

If your instance of elasticsearch or opensearch has certs that can not be verified set ELASTIC_VERIFY_CERTS to `no`.

```yaml
    ELASTIC_VERIFY_CERTS: "no",
```

### Other connection types

If there is a need for more advanced connection configuration the change in /app/globals/elastic_client.py should handle
all mare advanced connection types from Tracardi to elastic. 

