# How to Install Redis on Kubernetes?

This article will guide you through the process of installing Redis, a popular in-memory data structure store, on a
Kubernetes (K8s) environment. Kubernetes, with its robust orchestration capabilities, is ideal for managing Redis
instances that require high availability and quick scalability.

Before you begin, ensure you have a working Kubernetes cluster with `kubectl` installed and properly configured. This
initial setup is crucial for successfully deploying and managing Redis within your Kubernetes infrastructure.

## Prerequisites

- A Kubernetes cluster up and running.
- `kubectl` tool installed and configured to interact with your cluster.
- Helm package manager installed on your local machine

## Setting Up the Environment

**Note:**
Kubernetes uses namespaces to organize and isolate cluster resources by team, application, or environment. In this
guide, we will deploy Redis in its own namespace to keep it separate from other applications.

### Step 1: Add the Helm Repository

Helm is a package manager for Kubernetes that simplifies the deployment and management of applications. The first step
in installing Redis is to add the Bitnami repository, which contains a pre-configured Helm chart for Redis:

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

This command registers the Bitnami repository with Helm, making the Redis chart available for installation.

### Step 2: Update the Helm Repository

After adding the new repository, update your Helm chart repository to ensure you have the latest list of charts and
updates:

```bash
helm repo update
```

This command synchronizes your local Helm chart repository with the remote one, ensuring you have access to the latest
charts provided by Bitnami.

## Configuration

### Prepare the `values.yaml` File

To customize the Redis deployment to your specific needs, you will need to create and modify a `values.yaml` file. This
file contains configuration settings like resource limits and storage options. Here is an example `values.yaml`:

```yaml
master:
  persistence:
    size: 2Gi
  resources:
    limits:
      memory: 2Gi
    requests:
      memory: 1Gi
replica:
  persistence:
    size: 5Gi
  replicaCount: 1
  resources:
    limits:
      memory: 2Gi
    requests:
      memory: 1Gi
```

This configuration defines the resource allocation and storage requirements for both the Redis master and replica
instances. It ensures that Redis has enough memory and disk space to perform effectively while managing cost and
resource usage within your cluster.

## Installation

### Create a Namespace for Redis

Before deploying Redis, create a dedicated namespace for it:

```bash
kubectl create namespace redis
```

This command creates a new namespace named `redis`, providing an isolated environment for running your Redis instances.

### Install Redis Using Helm

Now, install Redis into the newly created namespace using the Helm chart:

```bash
helm upgrade --install redis bitnami/redis --values values.yaml --namespace redis --create-namespace
```

This command tells Helm to install the Redis chart from the Bitnami repository. If Redis is not already installed, Helm
will install it (`--install`). The `upgrade` option allows you to update an existing installation or configure
additional parameters without affecting existing data. It uses the configurations specified in `values.yaml` and deploys
Redis in the `redis` namespace.

## Wrap Up

After deployment, you can monitor the status of the Redis pods to ensure they are running correctly:

```bash
kubectl get pods -n redis
```

You should expect output similar to this, confirming that the Redis instances are up and operational:

``` title="Expected output"
NAME                       READY   STATUS    RESTARTS   AGE
redis-master-0             1/1     Running   0          10m
redis-replica-0            1/1     Running   0          10m
```

By following these steps, you will have successfully deployed a scalable and robust Redis instance on your Kubernetes
cluster, ready to handle your application's caching and data structure management needs effectively.