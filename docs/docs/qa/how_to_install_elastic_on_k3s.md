# How to Install ElasticSearch Cluster on K3s/K8s?

This post outlines the process of installing ElasticSearch (ES) on K3s, a lightweight Kubernetes distribution designed
for edge and IoT environments. Before proceeding with the installation, it is crucial to ensure that you have a
prerequisite setup, which includes a working K3s or Kubernetes (K8s) cluster with `kubectl` connected and configured.
This setup will allow you to effectively manage your cluster's resources and deploy ES using the methodologies described
here. The following steps will guide you through the installation of the ElasticSearch cluster, leveraging the
Kubernetes operator and Helm charts for a simplified and efficient deployment.

!!! Note

    Kubernetes uses namespaces to separate different projects. We will use separate namespaces for each Tracardi dependency.

The best way to install ElasticSearch (ES) on Kubernetes is to use the ES operator. A Kubernetes operator is a method of
packaging, deploying, and managing a Kubernetes application. To install it, type:

```bash
kubectl apply -f https://download.elastic.co/downloads/eck/2.10.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.10.0/operator.yaml
```

It will automatically install the ElasticSearch Kubernetes Operator, which configures and manages ES clusters in your
K8s environment.

## Helm Chart Download

Then we will use a helm chart prepared by Tracardi to simplify the whole installation. First, download the helm chart
file:

```commandline
curl -O http://tracardi.com/helm/1.0.0/elastic-1.0.0.tgz
```

This command saves the helm chart as a file named `elastic-1.0.0.tgz`.

## Configuration

Next, you need to prepare a simple file called `values.yaml` that defines how many nodes your Elastic cluster should
have:

```yaml title="Example of a values.yaml file"
version: 8.11.3  # Version of ElasticSearch

service:
  type: LoadBalancer  # LoadBalancer for ES
  port: 9200

master:
  replicas: 1  # Number of master nodes
  storage:
    size: 5Gi  # Storage size for the master node

data:
  replicas: 3 # Number of worker nodes
  storage:
    size: 10Gi # Storage size for each worker node
```

This is a very simplified installation but will install a production-ready ElasticSearch cluster. It will create storage
volumes and the defined number of nodes.

## Installation

```commandline title="This command will create elastic namespace"
kubectl create ns elastic
```

Let's install ElasticSearch. We will use the previously defined `values.yaml` file and the downloaded helm chart:

```commandline
helm install elastic elastic-1.0.0.tgz --values values.yaml -n elastic
```

This command installs the ElasticSearch cluster using the helm chart `elastic-1.0.0.tgz` within the namespace `elastic`,
applying your configuration specified in `values.yaml`. This automates the setup of your ES cluster with specified
versions, node configurations, and storage settings.

If later you would like to upgrade your installation after editing `values.yaml`, please use the following command. Note
that you will not be able to decrease the storage; you can only increase it.

```commandline
helm upgrade --install elastic elastic-1.0.0.tgz --values values.yaml -n elastic
```

# Wrap Up

After a minute or two, you should be able to see the pods in the `elastic` namespace. A pod in Kubernetes is the
smallest deployable unit that can be created, scheduled, and managed. It's essentially a group of one or more docker
containers, with shared storage/network, and a specification for how to run the containers.

To check if everything is OK, run this command:

```commandline
kubectl get pods -n elastic
```

``` title="Expected output"
NAME                                  READY   STATUS    RESTARTS       AGE
elastic-cluster-es-master-node-0      1/1     Running   0              72d
elastic-cluster-es-data-node-1        1/1     Running   0              72d
elastic-cluster-es-data-node-2        1/1     Running   0              72d
elastic-cluster-es-data-node-0        1/1     Running   0              72d
```