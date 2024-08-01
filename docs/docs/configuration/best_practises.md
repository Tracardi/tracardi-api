# Configuration Best Practises

To enhance security, consider setting up encrypted connections for Tracardi API access. You can encode external traffic
to the load balancer while keeping internal cluster communication unencoded, ensuring both security and efficiency.
Alternatively, encrypt the entire cluster by creating HTTPS versions of Tracardi Docker images for comprehensive
encryption.

## Set strong admin password

Having a strong admin password is especially important for systems that handle sensitive or confidential data, such as
personal information. If an admin password is weak or easily guessed, it could be exploited by attackers or unauthorized
individuals, who could gain access to sensitive data or disrupt the system's operation.

By setting a strong admin password, you can help to prevent unauthorized access and protect the security and integrity
of the system or application. This can help to ensure that your data and systems are safe from unauthorized access and
tampering, and that you can trust the security and reliability of your system or application.

## Separation of track server and GUI API

### API

A recommended approach involves having two Tracardi API instances: one for the GUI and another for event [collection](../getting_started/processes/collection.md).

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

GUI and GUI API should be accessible only from trusted network for security reasons.

-------------

# Q & A

Q: __What is the minimal number of instances?__
A: This all depends on your traffic. If you do not have big traffic you could run one cluster of APIs with 3 instances
and install GUI on your local machine.

Q: __Do tracardi need any particular routing inside cluster?__
A: The internal routing from load balancer to Tracardi instances can be for example: round-robin. Tracardi do not
require long-lasting sticky sessions.








