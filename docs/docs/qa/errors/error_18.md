# When I start multi-tenant installation I get the error: "Installation forbidden. Tenant XXX not allowed"

To successfully start a multi-tenant installation, it's essential to first authorize the new tenant in the Tenant Management System (TMS). This is accomplished through the TMS API by following these steps:

1. **Create the Tenant:**
   - Use the `POST /tenant` endpoint.
   - Provide all required data in the request body to register the new tenant.

2. **Install the System:**
   - After creating the tenant, access its specific API.
   - Initiate the installation process.
   - Ensure that you include the correct installation token specifically assigned to the newly created tenant.

By following these instructions, the tenant will be correctly set up and authorized, allowing the multi-tenant installation to proceed without issues.

Related documents:

* [What is TMS](../what_is_tms.md)
* [What is TMS responsible for](../what_is_tms_reponsible_for.md)
* [Who to setup multi-tenant installation](../how_do_i_setup_multi_tenant.md)
* [How to automate new tenant creation in TMS](../how_to_automate_new_tenant_creation_in_tms.md)
* [How to create new tenant](../how_to_create_new_tenant.md)
* [What are the pros and cons of mutli-tenant setup](../what_are_the_pros_and_cons_of_multi-tenant_setup.md)
* [How to integrate TMS with tracardi](../how_to_integrate_TMS_with_Tracardi.md)
