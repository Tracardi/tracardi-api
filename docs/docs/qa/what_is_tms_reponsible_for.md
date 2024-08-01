# What is tenant management service responsible for?

A tenant management service (TMS) is responsible for managing various aspects related to tenants within a system or
platform.  It is a separate microservice. Its responsibilities include:

1. `Creating tenants`: The TMS handles the creation of new tenant accounts within the system, setting up the necessary
   infrastructure and resources for them to operate.

2. `Returning tenants`: The service allows for retrieving information about existing tenants, providing functionality to
   query and access tenant-specific data, settings, and attributes.

3. `Validating tenants`: The TMS ensures the validity of tenants, particularly within Tracardi. It checks if a tenant is
   registered and authorized to access the system.

4. `Storing tenant-specific data`: The TMS manages the storage of tenant-related data, such as installation tokens, tenant
   email addresses, and additional attributes or mappings associated with each tenant. This data may include information
   required for integration with partner systems.

5. `Tracardi integration`: The TMS is used by Tracardi, a system operating in a multi-tenant environment where multiple
   tenants log in. Tracardi relies on the TMS to validate tenant credentials and ensure they are registered. Other
   operations like creating or deleting a tenant are also handled by the TMS.

In summary, a tenant management service is responsible for creating, returning, and validating tenants, storing
tenant-specific data, and enabling the integration and management of tenants within platforms like Tracardi.
