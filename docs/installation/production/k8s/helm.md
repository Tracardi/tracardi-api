## Tracardi Helm Chart Installation Guide

This document provides comprehensive instructions for installing the commercial Tracardi application on a Kubernetes (
K8s) cluster using the Helm chart.

### Prerequisites

Before initiating the installation process, ensure you have completed the following prerequisites:

1. **Obtain Helm Chart and License Information**: Upon agreeing to the license agreement, you will receive a Helm chart
   archive. Extract the contents of this archive into a folder named "tracardi". You will also receive a Docker Hub
   login token, which is required to access the commercial Docker images. Additionally, make sure you have the Tracardi
   license key.

2. **Elasticsearch and Redis Credentials**: Gather the username and password for Elasticsearch and the password for
   Redis. These credentials will be necessary during the installation process.

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
  elastic: <elastic-password>

---
apiVersion: v1
kind: Secret
metadata:
  name: redis-secret
type: Opaque
data:
  redis-password: <redis-password>

---
apiVersion: v1
kind: Secret
metadata:
  name: tracardi-license
type: Opaque
data:
  key: <license-key>
```

Apply this secret configuration using the following command:

```bash
kubectl apply -f tracardi-secrets.yaml -n tracardi
```

## Helm chart default configuration

## Tracardi Helm Chart Default Configuration

This section outlines the default configuration settings for the Tracardi Helm chart. The configuration details are
defined in the file `tracardi/values.yaml`. Please note that these settings may experience slight variations from one
version to another. As of version 0.8.1, the default configuration is presented below:

```yaml
secrets:
  dockerHub: "SET-DOCKERHUB-SECRET"
  installationToken: "SET-INSTALLATION-SECRET"

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

### Default Values

Below is an overview of some key default values present in the configuration:

- **Replicas**: The default number of replicas for each service is typically set to 1.
- **Images**: The default images for services are defined in `config.image.<name-of-service>`

These settings constitute the starting point for configuring the Tracardi components and services using the Helm chart.
You can customize these values according to your requirements during the installation process.

## Customizing installation

