# How to start Tracardi in multi-tenant mode?

To start Tracardi in multi-tenant mode, follow these steps:

1. Obtain a commercial Tracardi API Docker: Multi-tenancy is a commercial feature, so you will need to acquire a
   commercial version of the Tracardi API Docker.

2. In the Docker configuration, set the MULTI_TENANT environment variable to "yes". This enables the multi-tenant mode
   in Tracardi.

3. Configure the Tenant Management Service (TMS): Tracardi's multi-tenant setup relies on a dependent system called the
   Tenant Management Service (TMS). You will need to provide the necessary configuration details for the TMS to
   integrate it with Tracardi. Specifically, you need to provide the following to the tracardi-api docker:

    - MULTI_TENANT_MANAGER_URL: This is the URL of the Tenant Management Service (TMS). Set it to the appropriate
      endpoint where the TMS is running.

    - MULTI_TENANT_MANAGER_API_KEY: Provide the API key for the TMS. This is used for authentication and authorization
      between Tracardi and the TMS.

