# Installing Pulsar on Kubernetes (K8s)

This tutorial provides step-by-step instructions for installing Apache Pulsar on a Kubernetes (K8s) cluster using the
Apache Pulsar Helm chart. The following resources and dependencies are required:

- [Pulsar Helm Chart Repository](https://github.com/apache/pulsar-helm-chart)
- [Pulsar Helm Chart Documentation](https://pulsar.apache.org/docs/3.1.x/helm-deploy/)

## Pulsar Dependencies

Before installing Apache Pulsar, ensure that the following dependencies are set up:

### Cert Manager

Cert Manager is used for managing TLS certificates in Kubernetes. We need to install it as a prerequisite for Pulsar.

```bash
# Apply the Cert Manager CRDs (Custom Resource Definitions)
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v1.13.0/cert-manager.crds.yaml

# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install Cert Manager
helm install --version v1.13.0 cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace
```

### Certification Keys

To enable authentication in Apache Pulsar, both symmetric and asymmetric keys need to be installed as secrets.

```bash
# Clone the Pulsar Helm Chart repository
git clone https://github.com/apache/pulsar-helm-chart
cd pulsar-helm-chart

# Generate secret keys and tokens for Pulsar super users
# By default, it generates an asymmetric public/private key pair. Use --symmetric to generate a symmetric secret key.
./scripts/pulsar/prepare_helm_release.sh -n pulsar -k pulsar --symmetric
./scripts/pulsar/prepare_helm_release.sh -n pulsar -k pulsar
```

The `prepare_helm_release` script creates the following resources:

- A Kubernetes namespace named "pulsar" for installing the Pulsar release.
- JWT (JSON Web Token) secret keys and tokens for three super users: "broker-admin," "proxy-admin," and "admin." These
  roles have specific purposes in Pulsar:
    - `broker-admin` role is used for inter-broker communications.
    - `proxy-admin` role is used for proxies to communicate with brokers.
    - `admin` role is used by the admin tools.

### Local Path Provisioner

Apache Pulsar requires local storage for certain functionalities. You can install the local path provisioner to provide
this storage.

```bash
# Apply the Local Path Provisioner YAML manifest
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.24/deploy/local-path-storage.yaml
```

## Pulsar Installation

With the dependencies in place, you can proceed to install Apache Pulsar using the Helm chart.

```bash
# Install Pulsar using Helm
helm install pulsar -n pulsar -f /home/risto/pulsar/values.yaml apache/pulsar

# To delete the Pulsar release, if needed
helm delete pulsar -n pulsar
```

Replace `/home/risto/pulsar/values.yaml` with the path to your Pulsar configuration values file if you have specific
configurations to apply during the installation.

This installation process deploys Apache Pulsar on your Kubernetes cluster, allowing you to utilize its powerful
messaging and event streaming capabilities. Be sure to monitor the installation process and logs for any potential
issues or errors.