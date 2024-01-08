# Installing Pulsar using Datastax Helm Chart

## Source

This tutorial is based on information form:

* https://datastax.github.io/pulsar-helm-chart/
* https://github.com/datastax/pulsar-helm-chart/blob/master/helm-chart-sources/pulsar/values.yaml


## Helm Repository Installation

```commandline
helm repo add datastax-pulsar https://datastax.github.io/pulsar-helm-chart
helm repo update
```

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

## Pulsar’s Token Based Authentication

This token based authentication relies on a plugin provided by Apache Pulsar using the AuthenticationProviderToken class that ships with Pulsar.

For authentication to work, the token-generation keys need to be stored in Kubernetes secrets along with some default tokens (for superuser access).

The chart includes tooling to automatically create the necessary secrets, or you can do this manually.
Automatic generation of secrets for token authentication

Use these settings in `datastax-values.yaml` to enable automatic generation of the secrets and enable token-based authentication:

```yaml
enableTokenAuth: true
autoRecovery:
  enableProvisionContainer: true
```

When the provision container is enabled, it will check if the required secrets exist. If they don’t exist, it will generate new token keys and use those keys to generate the default set of tokens

The name of the key secrets are:

    token-private-key
    token-public-key

Using these keys, it will generate tokens for each role listed in superUserRoles. Based on the default settings, the following secrets will be created to store the tokens:

    token-superuser
    token-admin
    token-proxy
    token-websocket


More information on token generation can be found [here](https://datastax.github.io/pulsar-helm-chart/)

!!! Tip

    Token stored in token-admin can be used to access Pulsar form client code. 


```commandline
helm upgrade --wait --install pulsar -f datastax-values.yaml datastax-pulsar/pulsar -n pulsar
```


## Example of datastax-values.yaml

```yaml
#
#  Copyright 2022 DataStax, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

enableAntiAffinity: false
enableTls: false
enableTokenAuth: true
restartOnConfigMapChange:
  enabled: true
extra:
  function: true
  burnell: true
  burnellLogCollector: true
  pulsarHeartbeat: true
  pulsarAdminConsole: false

zookeeper:
  replicaCount: 1
  resources:
    requests:
      memory: 300Mi
      cpu: 0.3
  configData:
    PULSAR_MEM: "-Xms300m -Xmx300m -Djute.maxbuffer=10485760 -XX:+ExitOnOutOfMemoryError"

bookkeeper:
  replicaCount: 1
  resources:
    requests:
      memory: 512Mi
      cpu: 0.3
  configData:
    BOOKIE_MEM: "-Xms312m -Xmx312m -XX:MaxDirectMemorySize=200m -XX:+ExitOnOutOfMemoryError"

broker:
  component: broker
  replicaCount: 1
  ledger:
    defaultEnsembleSize: 1
    defaultAckQuorum: 1
    defaultWriteQuorum: 1
  resources:
    requests:
      memory: 600Mi
      cpu: 0.3
  configData:
    PULSAR_MEM: "-Xms400m -Xmx400m -XX:MaxDirectMemorySize=200m -XX:+ExitOnOutOfMemoryError"

autoRecovery:
  replicaCount: 1
  enableProvisionContainer: true
  resources:
    requests:
      memory: 300Mi
      cpu: 0.3

function:
  replicaCount: 1
  functionReplicaCount: 1
  resources:
    requests:
      memory: 512Mi
      cpu: 0.3
  configData:
    PULSAR_MEM: "-Xms312m -Xmx312m -XX:MaxDirectMemorySize=200m -XX:+ExitOnOutOfMemoryError"

proxy:
  replicaCount: 1
  resources:
    requests:
      memory: 512Mi
      cpu: 0.3
  wsResources:
    requests:
      memory: 512Mi
      cpu: 0.3
  configData:
    PULSAR_MEM: "-Xms400m -Xmx400m -XX:MaxDirectMemorySize=112m"
  autoPortAssign:
    enablePlainTextWithTLS: true
  service:
    autoPortAssign:
      enabled: false
    ports:
    - name: http
      port: 8082
      protocol: TCP
    - name: pulsar
      port: 6650
      protocol: TCP
    - name: ws
      port: 8000
      protocol: TCP

grafanaDashboards:
  enabled: false

pulsarAdminConsole:
  replicaCount: 1
  service:
    type: ClusterIP

kube-prometheus-stack:
  enabled: false
  prometheusOperator:
    enabled: false
  grafana:
    enabled: false
    adminPassword: e9JYtk83*4#PM8
```