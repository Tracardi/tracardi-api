# How to integrate TMS with Tracardi?

To integrate TMS (Tenant Management Service) with Tracardi, follow these steps:

1. Set up Multi-tenancy: In Tracardi, multi-tenancy allows multiple tenants (clients) to use the system independently.
   To enable multi-tenancy, set the `MULTI_TENANT` environment variable to "yes" in the Tracardi API Docker
   configuration.

2. Configure the Tenant Management Service (TMS): The TMS is responsible for managing various aspects related to tenants
   within Tracardi. Provide the following configuration details for the TMS integration to the tracardi-api docker:

    - `MULTI_TENANT_MANAGER_URL`: Set this variable to the URL of the Tenant Management Service. It should point to the
      endpoint where the TMS is running.
    - `MULTI_TENANT_MANAGER_API_KEY`: Provide the API key for the TMS. This key is used for authentication and
      authorization between Tracardi and the TMS.

3. Onboard new tenants: To automate the onboarding process for new tenants, you can use the TMS API. You can make API
   calls to the TMS to create new tenants, retrieve their information, and manage tenant-specific data.

4. Obtain API Key for Tracardi: To authenticate with the Tracardi API, follow the OAuth2 authorization process. Make a
   POST request to the `/user/token` endpoint with your admin account credentials. If the authorization is successful,
   you will receive an API key as an OAuth2 token, which will be used for subsequent authenticated requests to the
   Tracardi API.

By following these steps, you can integrate TMS with Tracardi, enable multi-tenancy, automate tenant onboarding, and
authenticate API requests using the obtained API key.