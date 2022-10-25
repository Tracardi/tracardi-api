# Production installation

Tracardi is a distributed system and as such should be installed on production servers. The installations described in
the previous sections are mainly used for testing purposes. A production installation should be built with at least five
Tracardi API instances, two instances of GUI, and three elasticsearch instances.

Setting up an elastic search cluster is beyond Tracardi configuration and can be handled by ready to use cloud instances
that expose one IP but hide 3 and more instances of the database.

## API and GUI

The production setup should have a clusters with Tracardi API and one cluster with Tracardi GUI (2 instances). GUI
cluster should be accessible only from trusted network for security reasons. Although the cluster with Tracardi API may
be set up as one cluster we recommend running 2 clusters with slightly reconfigured instances.

One cluster, the one available on the Internet, consisting of at least 3 instances should be configured with
environment variable `EXPOSE_GUI_API` set to `no`. This way the publicly available API will have only `/track` endpoint available.
This cluster will be used for event collection from the website on the Internet. All other endpoints that are needed for
the GUI will be disabled.

Another cluster, the one available in the internal network, or available on the Internet but restricted to certain set
of IPs, should have the environment variable `EXPOSE_GUI_API` set to `yes`. This cluster will be used by GUI to control Tracardi.

## Tracardi API cluster

A single instance of Tracardi API (by default run from docker container) starts 25 workers. Each worker is able to
handle asynchronous connections.

Each instance of Tracardi API should be run on a separate server (physical or virtual). The point is that in the event
of failure, the other instances could take over the tasks of the failed instance. There is no obstacle to run more than
three Tracardi instances.

!!! Tip

    We recommend installing Tracardi inside a k8s environment. Kubernetes automatically can bring back to life failed
    docker instances.

## Load balancing

A cluster of Tracardi instances (GUI or API) should be hidden behind the load balancer that will expose one IP to the
world and direct external traffic to individual instances. To avoid single point of failure create multiple instances of
load balancer.  
Tracardi do not require long-lasting sticky sessions, so you can configure your DNS servers to return multiple A
records (IP addresses) for your domain.

This kind of architecture will allow you to scale Tracardi for small and high traffic.

If Tracardi is configured to run in HTTPS mode, the load balancer should accept encrypted traffic. Requests inside the
cluster may stay not encoded. This way, you can bypass the certificate management problems for each Tracardi instance.

# Tracardi GUI cluster

Tracardi GUI cluster should be created the same way the API cluster. If you have 2 separate clusters for internal and
external traffic remember to configure GUI to connect to cluster handling internal traffic.

# Q & A

Q: __What is the minimal number of instances?__
A: This all depends on your traffic. If you do not have big traffic you
could run one cluster of APIs with 2 instances and install GUI on your local machine.

Q: __Do tracardi need any particular routing inside cluster?__ 
A: The internal routing from load balancer to Tracardi instances can be for example: round-robin. Tracardi do not 
require long-lasting sticky sessions.

Q: __What load can take Tracardi?__
A: We tested single instance of Tracardi with 25 workers connected to one instance of
elasticsearch, and it was capable of responding to 600 requests per second. 



