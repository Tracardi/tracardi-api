## Creating a New Tenant

This guide offers a comprehensive walkthrough for creating a new tenant within the Tenant Management Service (TMS)
system. By following these steps, you can provide your customers with a link to complete the installation process. It's
important to note that this approach is not a plug-and-play solution; rather, it's a pivotal step in the installation
journey, enabling you to delegate the finalization of the installation to your customers.

If you're seeking a more streamlined installation process accomplished through a single API call, you can explore the
full installation guide available [here](../configuration/multi-tenant/index.md). This resource outlines the steps for
setting up a multi-tenant environment in a more automated manner.

### Prerequisites

Before starting the tenant creation process, ensure you have access to the Tenant Management Service (TMS) and the
required API key. To create a new tenant, you'll need a TMS API key generated during TMS installation.

### Creating a New Tenant with an API Call

Follow these instructions to create a new tenant using an API call:

1. **Authorize with API Key**:

   To initiate the process, authorize yourself with the API key. Use the following CURL command to obtain a token that
   will be used for authorization in the subsequent API call:

   ```bash
   curl -X 'GET' \
     'http://TMS-server:8383/api-key/API-KEY' \
     -H 'accept: application/json'
   ```

   The response will provide a token that must be included in the header of the next API call.

2. **API Call Configuration**:

    - Utilize the HTTP POST method.
    - Direct the API call to the endpoint `/tenant`.
    - Construct the API call payload with the following details:

      ```json
      {
        "id": "uuid4-id",
        "created": "2023-08-16T16:36:13.115Z",
        "name": "tenant-name",
        "install_token": "installation",
        "email": "tenant@email",
        "expire": "2023-08-16T16:36:13.115Z"
      }
      ```

    - Example CURL:

      ```bash
      curl -X POST \
        https://TMS-server/tenant \
        -H 'Content-Type: application/json' \
        -H 'accept: application/json' \
        -H 'Authorization: Bearer TOKEN' \
        -d '{
          "id": "uuid4-id",
          "created": "2023-08-16T16:36:13.115Z",
          "name": "tenant-name",
          "install_token": "installation",
          "email": "tenant@email",
          "expire": "2023-08-16T16:36:13.115Z"
        }'
      ```

3. **Result**:

   After successfully executing the API call, a new tenant with the specified name will be created. The provided name
   will form the initial part of the tenant's URL, such as `tenant-name.mydomain.com`.

Please note that successful execution of the API call requires proper authorization using the obtained token. Replace
placeholders like `TOKEN`, `TMS-server`, `API-KEY`, and other relevant placeholders with actual values
before making the API calls.

### Can I use Account ID as a Tenant Identifier

Yes, you have the option to use your account ID as an identifier for the newly created tenant. This can be incorporated
into the domain name that the tenant uses to access the system. For instance, if your account ID is "xxx," the tenant's
domain could be "xxx.domain.com."

By following these steps, you can seamlessly create a new tenant and establish the necessary components for their access
to the system.