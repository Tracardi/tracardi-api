# Installation with HelmChart version 0.8.2

This document provides comprehensive instructions for installing the commercial Tracardi application on a Kubernetes (
K8s) cluster using the Helm chart.

## Prerequisites

Before initiating the installation process, ensure you have completed the following prerequisites:

1. **Install K8S and Helm**: Make sure that you have installed K8S and Helm.

2. **Obtain Helm Chart and License Information**: Upon agreeing to the license agreement, you will receive a Helm chart
   archive. Extract the contents of this archive into a folder named "tracardi". You will also receive a Docker Hub
   login token, which is required to access the commercial Docker images. Additionally, make sure you have the Tracardi
   license key.
3. **[Install Dependant Services](../../dependencies/index.md)**: Elasticsearch, redis, mysql and apache pulsar are required. 

4. **Elasticsearch, Redis, Mysql, Apache Pulsar Credentials**: Gather for all required services it will be necessary during the installation process.

### Namespace Creation

Execute the following command to create a Kubernetes namespace named "tracardi":

```bash
kubectl create ns tracardi
```

### Docker Hub Access Configuration

Configure access to Docker Hub by creating a Kubernetes secret containing your Docker Hub login token. Use the following
command:

```bash
kubectl create secret docker-registry tracardi-dockerhub \
    --docker-server=index.docker.io/v1/  \
    --docker-username=tracardi \
    --docker-password=<docker-hub-token> \
    -n tracardi
```

### System Secrets Configuration

To proceed with the installation, you need to set up essential system secrets including the license key, Elasticsearch
password, and Redis password. Create a Kubernetes secret file, as illustrated in the example below:

Save this content as "tracardi-secrets.yaml":

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: elastic-secret
type: Opaque
data:
  elastic: <base64-elastic-password>

---
apiVersion: v1
kind: Secret
metadata:
  name: redis-secret
type: Opaque
data:
  redis-password: <base64-redis-password>

---
apiVersion: v1
kind: Secret
metadata:
  name: tracardi-license
type: Opaque
data:
  key: <base64-license-key>

---
apiVersion: v1
kind: Secret
metadata:
  name: tms
type: Opaque
data:
  secret: <base64-tms-secret>
  api-key: <base64-tms-api-key>
```

Apply this secret configuration using the following command:

```bash
kubectl apply -f tracardi-secrets.yaml -n tracardi
```

## Helm chart default configuration

The configuration details are defined in the file `tracardi/values.yaml` (look inside the helm-chart.zip). Please note
that these settings may experience slight variations from one version to another. As of version 0.8.1, the default
configuration is presented below:

```yaml
secrets:
  installationToken: "SET-INSTALLATION-SECRET"
  dockerHub: "tracardi-dockerhub"
  license:
    secretName: "tracardi-license"
    secretKey: "license-key"
  tms:
    secretName: "tms"
    secret:
      secretKey: "secret"
    apiKey:
      secretKey: "api-key"

config:
  multiTenant:
    multi: "no"
    tms_service: tms-svc
  image:
    tag: 0.8.1
    api:
      repository: tracardi/com-tracardi-api
      pullPolicy: IfNotPresent
    gui:
      repository: tracardi/tracardi-gui
      pullPolicy: IfNotPresent
    tms:
      repository: tracardi/tms
      pullPolicy: IfNotPresent

gui:
  port: 8787
  replicas: 1
  ingress:
    enabled: false
    domain: gui.tracardi.example.com
    ingressClassName: ""
    tls:
      enable: true
      secretName: ""
    annotations: { }

# (More sections like 'tms', 'collector', 'staging', etc.)

# Infrastructure

elastic:
  host: "elastic-svc"
  schema: https
  username: "elastic"
  existingSecret: "elastic-secret"
  existingSecretPasswordKey: "elastic"
  verifyCerts: "no"
  port: 9200

redis:
  existingSecret: "redis-secret"
  existingSecretPasswordKey: "redis-password"
  schema: "redis://"
  host: redis-svc
  port: "6379"
  db: "0"
```

Please be aware that the above configuration is illustrative and may change across different versions of Tracardi.

### Installing helm chart with default values

Run the following command to install tracardi with default settings:

```bash
helm install tracardi tracardi -n tracardi
```

This will install tracardi in tracardi namespace.

### Custom Configuration Overrides

If you wish to tailor the default configuration to better suit your specific requirements, you have the flexibility to
override default values. To achieve this, follow these steps:

1. **Duplicate `values.yaml`**: Copy the `tracardi/values.yaml` file to a new file, such as `settings.yaml`.

2. **Modify Settings**: Within the newly created `settings.yaml`, remove any configuration entries that you wish to
   retain as per the default settings. Keep only those settings that you intend to customize.


### Running helm with custom values

Run the following command to install tracardi with default settings

```bash
helm install --values settings.yaml tracardi tracardi -n tracardi
```

### Upgrading the helm installation

```bash
helm upgrade --wait --timeout=1200s --install --values settings.yaml tracardi tracardi -n tracardi
```


### Configuration Changes

The YAML file contains distinct sections that configure various aspects of the Tracardi setup. Each section corresponds
to a specific component or functionality within Tracardi.

#### Infrastructure Configuration

The "Infrastructure" section is dedicated to establishing connections with Elasticsearch and Redis, which are components
of the Tracardi system. The configuration settings within this section enable communication with these backend services.
Here is an example of how these connections are configured:

```yaml
# Infrastructure

elastic:
  host: "elastic-svc"
  schema: https
  username: "elastic"
  existingSecret: "elastic-secret"
  existingSecretPasswordKey: "elastic"
  verifyCerts: "no"
  port: 9200

redis:
  host: redis-svc
  schema: "redis://"
  existingSecret: "redis-secret"
  existingSecretPasswordKey: "redis-password"
  port: "6379"
  db: "0"
```

- `elastic` section configures the connection to Elasticsearch with details such as the host, schema (using HTTPS),
  username, and references an existing secret named "elastic-secret" that contains the necessary authentication
  credentials.
- `redis` section configures the connection to Redis with details including the host, schema, and an existing secret
  named "redis-secret" that contains the required password for authentication.

#### General configuration

The "General Configuration" section encapsulates settings related to Docker images and their versions, as well
as the configuration for enabling or disabling the multitenant mode of the system.

```yaml
config:
  multiTenant:
    multi: "no"
    tms_service: tms-svc  # The name of the tms service
  image:
    tag: 0.8.1  # Tag should be the same for GUI and backend
    api:
      repository: tracardi/com-tracardi-api
      pullPolicy: IfNotPresent
    gui:
      repository: tracardi/tracardi-gui
      pullPolicy: IfNotPresent
    tms:
      repository: tracardi/tms
      pullPolicy: IfNotPresent
```

- `multiTenant`: This sub-section defines whether the system should operate in multitenant mode. By setting the value
  to `"no"`, the system is configured for single-tenant operation. The `tms_service` specifies the name of the tms
  service.
- `image`: This sub-section details the Docker images and their corresponding versions for different components. The
  specified Docker image repositories and tags determine which images to use for the GUI, API, and TMS services.
  The `pullPolicy` specifies whether the system should pull the image if it's not present.

## API installation

Here's an example of how the Tracardi API collector is configured by default. This configuration example allows you to
define the collector's port, the number of replicas if enabled, and several configuration settings.

```yaml
collector:
  enabled: true       # Whether the collector should be enabled
  port: 8484          # Port the collector will be exposed on
  replicas: 1         # Number of replicas if enabled
  config:
    saveLogs: "no"    # Whether to save logs
    loggingLevel: "WARNING"  # Log verbosity level
    apiDocs: "no"     # Whether to enable API documentation
    enableWorkflow: "yes"    # Whether to enable workflow
    enableEventDestinations: "yes"   # Whether to enable event destinations
    enableProfileDestinations: "yes" # Whether to enable profile destinations
```

By modifying these settings, you can adapt Tracardi to your specific use case. The `enabled` flag determines whether the
collector is active, the `port` specifies the port number it will listen on, and `replicas` allows you to define the
desired number of replicas. The `config` section enables you to fine-tune various operational aspects such as logging
behavior, API documentation availability, and the activation of different functionalities like workflow, event
destinations, and profile destinations.

Each section has similar settings.

### Installing Helm Chart with Custom Replicas and Ports

To install the Tracardi Helm chart with custom settings, you can create a custom configuration file and modify the
desired parameters. Here's an example using a file named `settings.yaml` to adjust the number of replicas and expose
services on different ports:

#### Example `settings.yaml`

```yaml
# Definition of defined secrets.

secrets:
  installationToken: "my-installation-token"
 
# General Tracardi configuration. Version, images, multi-tenancy, etc.

config:
  image:
    tag: 0.8.1

# Settings per service

gui:
  port: 80        # Custom port for the GUI service
  replicas: 2     # Increase the number of GUI replicas to 2

tms:
  enabled: false  # Disable the TMS service

collector:
  enabled: true   # Enable the collector service
  port: 8080      # Custom port for the collector service
  replicas: 10    # Increase the number of collector replicas to 10
  
staging:
  enabled: true   # Enable the staging service
  port: 8081      # Custom port for the staging service
  replicas: 3     # Increase the number of staging replicas to 3
```

In this example, the `settings.yaml` file is tailored to modify the Tracardi installation according to your preferences.
It increases the number of replicas for the GUI, collector, and staging services while also specifying custom ports for
the GUI, collector, and staging services.

To install Tracardi using these custom settings, you can run the following Helm command:

```bash
helm install tracardi ./tracardi -f settings.yaml -n tracardi
```

This approach allows you to easily adjust the deployment configuration to match your requirements while maintaining the
core Helm chart intact.