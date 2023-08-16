# Creating a New Tenant using API Call

This documentation outlines the process of automating the creation of a new tenant through the Tracardi API. To achieve
this, you'll need an API Key associated with the TMS, which is generated during the installation of the TMS.

## Prerequisites

- Tenant Management Service (TMS) API Key

## API Endpoint and Method

Make an API call to the Tracardi API using the POST method and the endpoint `/tenant/install`.

## Payload

Send the following payload in JSON format along with the API call:

```json
{
  "name": "name-of-the-tenant",
  "tms_api_key": "TMS-API-KEY",
  "email": "tenant@email",
  "password": "Admin account password",
  "needs_admin": true,
  "update_mapping": false
}
```

## Example CURL

Here's an example of how to make the API call using the CURL command:

```bash
curl -X POST \
  https://tracardi-api-url/tenant/install \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "name-of-the-tenant",
    "tms_api_key": "TMS-API-KEY",
    "email": "tenant@email",
    "password": "Admin account password",
    "needs_admin": true,
    "update_mapping": false
}'
```

## Result

Upon successfully making the API call, a new tenant will be created with the provided name. This name will form the
initial part of the tenant's URL, such as `name-of-the-tenant.mydomain.com`. An admin account will also be created using
the provided email as the login and the provided password. The account will have administrative privileges. 

