# Installation best practises

We recommend setting encrypted connection to Tracardi API. The best way to achieve this is to encode the traffic to load
balancer but leave the internal cluster traffic decoded. If you want to have encoded traffic inside cluster you will
have to prepare https versions of Tracardi docker images. See
the [documentation on how to do it](../configuration/tracardi_ssl.md).

## Separation of track server and GUI API

Best practice is to have a setup of 2 Tracardi API clusters. One for GUI and one for event collection.

The event collecting cluster, the one available on the Internet, should be configured with environment
variable `EXPOSE_GUI_API` set to `no`. This way the publicly available API will have only `/track` endpoint available.
All other endpoints that are required by the GUI will be disabled. This cluster will be used for event collection from
the website or other sources available on the Internet.

Another cluster, the one available in the internal network, or available on the Internet but restricted to certain set
of IPs, should have the environment variable `EXPOSE_GUI_API` set to `yes`. This cluster will be used by GUI to control
Tracardi.

## Scaling

We recommend using Kubernetes for scaling and maintaining the cluster health. Tracardi do not require long-lasting
sticky sessions and it is a stateless instance, so it can be killed and raised without any consequences for the cluster. 