# How Tenants are differentiated in Tracardi multi-tenant environment?

In Tracardi's multi-tenant environment, tenants are distinguished based on their unique domains and associated API URLs.
Each tenant receives a specific GUI and API URL, along with an installation key. It's important to understand that
although the domains may differ, they all point to the same Tracardi instance.

The tenant name is derived from the API domain by removing non-alphanumeric characters. For instance, if the API domain
is "company-x.tracardi.com," the corresponding tenant name would be "companyx." This tenant name serves as a unique
identifier and helps create separate storage namespaces, ensuring data isolation between tenants.

To set up a new tenant, they access Tracardi using their dedicated GUI URL. During the initial access, they are guided
through the installation process and asked to define an admin account. To ensure security, an installation token is
provided, which must be copied into the installation form to authorize the setup.


!!! Tip

    **Important:** The installation token is a unique and hard-to-guess string provided to the tenant during the setup
    process. It acts as a verification mechanism, ensuring that only authorized individuals can install the Tracardi system
    for the respective tenant.

Once the system is installed, the tenant gains access to their admin account and can use their GUI URL to access
Tracardi. This approach allows multiple tenants to coexist within the same Tracardi instance while maintaining data
separation and tenant-specific configurations.

If multiple multi-tenant instances are needed, different domains can be used, such as "tenant-name.instance1.domain.com"
and "tenant-name.instance2.domain.com," connected to separate Elasticsearch instances. The number of tenants per
instance depends on Elasticsearch capacity.

It's essential to ensure that subdomains are directed to different IP addresses where Tracardi is installed, ensuring
instance separation.

This organization of domains and instances in Tracardi enables efficient management of multi-tenant environments,
accommodating scalability and flexibility based on the needs of each instance.