# What is Tenant Management Service (TMS)?

# Tenant Management Service (TMS) in a Multi-Tenant Environment

In a multi-tenant setup, Tenant Management Service (TMS) is a dedicated microservice responsible for efficiently
managing the tenants within the system. Tenant Management involves overseeing various aspects related to individual
tenants in a platform.

The key responsibilities of the Tenant Management Service (TMS) include:

1. **Creating Tenants**: TMS is responsible for creating new tenant accounts within the system. It sets up the necessary
   infrastructure and resources for each tenant, ensuring their isolation and independence.

2. **Retrieving Tenant Information**: TMS provides functionality to query and access specific data, settings, and
   attributes associated with existing tenants. This allows the system to retrieve tenant-related information whenever
   needed.

3. **Validating Tenants**: TMS ensures that only valid and authorized tenants can access the system. It performs checks
   to verify if a tenant is registered and has the required permissions to use the platform.

4. **Tracardi Integration**: In a multi-tenant environment, where multiple tenants interact with the
   system, TMS plays a pivotal role. It validates tenant credentials, ensures they are registered, and handles
   operations such as creating or deleting a tenant.

To create a new tenant in Tracardi's multi-tenant setup, developers use the Tenant Management Service (TMS) API. The
process involves setting up the TMS, making an API call to create a new tenant, and providing essential information to
set up the tenant. The API returns a generated API key, which serves as the authentication token for accessing the
Tracardi API on behalf of the tenant. Additionally, TMS facilitates the creation of a tenant domain, installation token,
and other essential components for the tenant.
