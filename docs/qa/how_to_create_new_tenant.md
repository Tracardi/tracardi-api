# How to Create a New Tenant

To create a new tenant, you will need a tenant management service. This service facilitates the creation of a tenant
domain, installation token, and other necessary components. Once the tenant is created, they can access the designated
domain and proceed with the system installation.

# How to Automate Tenant Creation

Tenant creation can be automated by making API calls to the tenant management service. You can create a form that, when
filled out, triggers an API call to your service. This, in turn, communicates with the tenant management service API to
create the new tenant. This can also be automated using Tracardi workflows and events.

# Can I Use My Account ID to Create a Tenant

Yes, you can use your account ID as an identifier for the tenant. It can be incorporated into the domain name that the
tenant uses to access the system. For example, if your account ID is "xxx," the domain for your tenant would be "
xxx.domain.com."

# What is the process of creating a new tenant in multi-tenant setup?

To create a tenant in Tracardi, you will need to utilize the Tenant Management Service (TMS) API. The process can be
automated by following these steps:

1. Set up the Tenant Management Service (TMS): Ensure that the TMS is properly configured and integrated with Tracardi.

2. Make an API call to create a new tenant: Use the TMS API to create a new tenant account. This API call will include
   the necessary information to set up the tenant, such as tenant-specific attributes, installation tokens, and any
   mappings required for integration with partner systems.

3. Retrieve the generated API key: Once the tenant is created, the TMS API will return an API key. This API key serves
   as the authentication token for accessing the Tracardi API on behalf of the tenant.

By automating these steps through API calls to the TMS, you can programmatically create new tenants in Tracardi.