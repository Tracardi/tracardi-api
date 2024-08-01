# How to use tenant management service API.

## Tenant Management Service API - Create Tenant

### Endpoint: /tenant

#### Description:

This API endpoint is used to create a new tenant in the tenant management service.

#### Parameters:

No parameters are required for this API.

#### Request Body:

The request body should contain the following JSON payload:

```json
{
  "id": "string",
  "created": "2023-07-07T10:45:39.793Z",
  "name": "string",
  "install_key": "string",
  "email": "string",
  "license_id": "string"
}
```

- id (string): The unique identifier for the tenant.
- created (string): The timestamp indicating the creation time of the tenant.
- name (string): The name of the tenant.
- install_key (string): The installation token for the tenant.
- email (string): The email associated with the tenant.
- license_id (string): The license ID for the tenant.

#### Responses:

##### 200 - Successful Response

The API call is successful.

##### 422 - Validation Error

Occurs when there is a validation error in the request payload.

```json
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
```
