## Dependencies Installation with helm chart scripts

Tracardi dependencies can be installed using installation scripts. 

!!! Notice 
    
    Provided script may need changes for proper scaling.

## Prerequisites

* kubectl 1.21 or higher, compatible with your cluster (+/- 1 minor release from your cluster)
* Helm v3 (3.10.0 or higher)
* A Kubernetes cluster, version 1.21 or higher.
* Access to tracardi scripts repo. This is where the scripts are stored.

### Install Apache Pulsar

```
cd argocd
bash ./pulsar-install-helm.sh
```

To customize installation values go to: pulsar/local-values.yaml

