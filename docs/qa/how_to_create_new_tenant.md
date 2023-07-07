## How to Create a New Tenant

To create a new tenant, you will need a tenant management service. This service facilitates the creation of a tenant
domain, installation token, and other necessary components. Once the tenant is created, they can access the designated
domain and proceed with the system installation.

## How to Automate Tenant Creation

Tenant creation can be automated by making API calls to the tenant management service. You can create a form that, when
filled out, triggers an API call to your service. This, in turn, communicates with the tenant management service API to
create the new tenant. This can also be automated using Tracardi workflows and events. 

## Can I Use My Account ID to Create a Tenant

Yes, you can use your account ID as an identifier for the tenant. It can be incorporated into the domain name that the
tenant uses to access the system. For example, if your account ID is "xxx," the domain for your tenant would be "
xxx.domain.com."