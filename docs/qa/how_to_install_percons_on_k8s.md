# How to Install MySQL Using Percona on Kubernetes

This article guides you through the installation of Percona XtraDB Cluster (PXC), a robust and scalable SQL database
solution, on a Kubernetes (K8s) environment. Percona enhances MySQL's capabilities by providing high availability, more
consistent backups, enhanced performance, and better scalability.

## Prerequisites

Before you begin, you'll need a functioning Kubernetes cluster with `kubectl` installed and configured. Helm package
manager installed on your local machine. This setup is
essential for managing the resources and deploying the Percona database using the steps described below.

## Setting Up the Environment

**Note:**
Kubernetes namespaces allow for the isolation of cluster resources. We will deploy Percona in its own namespace to
maintain a tidy environment and facilitate resource management.

### Step 1: Add the Percona Helm Repository

Helm charts simplify the deployment and management of applications on Kubernetes. Start by adding the Percona Helm
repository:

```bash
helm repo add percona https://percona.github.io/percona-helm-charts/
```

This command adds the Percona repository, which contains the Helm charts necessary for deploying Percona XtraDB Cluster.

### Step 2: Update the Helm Repository

To ensure you have the latest Helm charts and updates, refresh your repository:

```bash
helm repo update
```

This syncs your Helm repository with the remote Percona charts, ensuring the latest versions are ready for installation.

## Configuration

### Prepare the `values.yaml` File

To tailor the Percona deployment to your needs, configure your settings in a `values.yaml` file. This file will dictate
the cluster configuration, resource allocation, and more. Here’s an example configuration:

```yaml
allowUnsafeConfigurations: true

sharding:
  enabled: false

backup:
  enabled: true

pxc:
  size: 1
  volumeSpec:
    pvc:
      resources:
        requests:
          storage: 2Gi

haproxy:
  enabled: true
  size: 1
  resources:
    requests:
      memory: 100Mi

proxysql:
  size: 1
```

This configuration sets up a single-node Percona cluster with HAProxy and ProxySQL for load balancing and routing.
Backups are enabled, ensuring data durability and recovery capabilities.

## Installation

### Create a Namespace for Percona

Organize your deployment by creating a namespace specifically for Percona:

```bash
kubectl create namespace percona
```

### Install Percona Operator and Database

Deploy the Percona Operator, which manages the lifecycle of the Percona cluster:

```bash
helm install percona-op percona/pxc-operator --namespace percona
```

Next, deploy the Percona database cluster using the previously prepared `values.yaml` file:

```bash
helm install percona-db percona/pxc-db --values values.yaml --namespace percona
```

These commands deploy the Percona Operator and the Percona database itself, configuring them according to the
specifications in your `values.yaml` file.

## Uninstalling Percona

Should you need to remove the Percona cluster, you can do so cleanly using the following commands:

```bash
NS="percona"

kubectl delete pxc percona-db-pxc-db -n $NS

helm delete percona-db --namespace $NS
helm delete percona-op --namespace $NS

kubectl delete namespace $NS
```

These commands will delete the Percona database and operator, as well as the namespace, effectively cleaning up all
resources associated with the installation.

## Wrap Up

After installation, verify the status of the Percona pods:

```bash
kubectl get pods -n percona
```

Expect output showing that your Percona cluster pods are running correctly:

``` title="Expected output"
NAME                                     READY   STATUS    RESTARTS   AGE
percona-db-pxc-db-0                      1/1     Running   0          10m
percona-db-pxc-haproxy-0                 1/1     Running   0          10m
percona-db-pxc-proxysql-0                1/1     Running   0          10m
```

By following these steps, you have successfully deployed a Percona XtraDB Cluster on your Kubernetes environment,
equipped with high availability and automatic backups, ready to handle your application’s data needs.