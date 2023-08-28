# Guide for Setting Up in Production

## Dependencies

Tracardi depends on:

* Redis
* Elastic search

Elasticsearch and Redis setup in Tracardi goes beyond its configuration. Utilize cloud instances or on-premises
installation. Refer to manuals for guidance.

## Installation best practises

To enhance security, consider setting up encrypted connections for Tracardi API access. You can encode external traffic
to the load balancer while keeping internal cluster communication unencoded, ensuring both security and efficiency.
Alternatively, encrypt the entire cluster by creating HTTPS versions of Tracardi Docker images for comprehensive
encryption. Find detailed instructions in the [documentation](../../configuration/tracardi_ssl.md).

### Separation of track server and GUI API

#### API

A recommended approach involves having two Tracardi API instances: one for the GUI and another for event collection.

1. **Event Collection Cluster:** This cluster is accessible over the Internet and handles event collection. To achieve
   this:
    - Set the environment variable `EXPOSE_GUI_API` to `no`.
    - Only the `/track` endpoint is accessible publicly, while other GUI-specific endpoints are disabled.
    - This cluster is designed to gather data from websites and other online sources.

2. **GUI Control Cluster:** This separate cluster operates within the internal network or is accessible over the
   Internet but limited to specific IP addresses. This setup is for GUI control of Tracardi:
    - Configure the environment variable `EXPOSE_GUI_API` as `yes`.
    - This cluster is utilized by the GUI to control Tracardi.

#### GUI

GUI should be accessible only from trusted network for security reasons.

## Scaling

Scaling means adjusting the system to handle more or less traffic. In Tracardi, this could mean adding more servers (
tracardi-api) to deal with more event tracking requests.

Tracardi is stateless, it means it doesn't rely on data stored inside docker, so it's easy to scale by adding or removing
dockers without causing problems. To handle this, we recommend using Kubernetes, a tool that helps manage these servers.
Tracardi API doesn't need special treatment when being restarted or relaunched.

A single docker replica of Tracardi API starts 1 worker. Each worker is able to handle multiple asynchronous
connections. You can run multiple replicas of Tracardi API.

## Tracardi Service List

Apart from the mentioned API and GUI, Tracardi manages additional services for task execution, such as jobs and workers.
Check out [this document](services.md) for a comprehensive list.


-------------

# Q & A

Q: __What is the minimal number of instances?__
A: This all depends on your traffic. If you do not have big traffic you could run one cluster of APIs with 3 instances
and install GUI on your local machine.

Q: __Do tracardi need any particular routing inside cluster?__
A: The internal routing from load balancer to Tracardi instances can be for example: round-robin. Tracardi do not
require long-lasting sticky sessions.

Q: __What load can take Tracardi?__
A: We conducted tests with a single Tracardi instance comprising 10 API replicas linked to one Elasticsearch instance.
Each replica was configured to use a maximum of 0.5 CPU and 150MB of RAM. The setup managed to handle 3000 requests per
second effectively.



