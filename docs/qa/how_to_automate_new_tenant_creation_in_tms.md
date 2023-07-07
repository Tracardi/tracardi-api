# How automate the installation process for a new tenant?

To automate the installation process for a new tenant in Tracardi, the following steps can be followed:

1. **Call the Tenant Management Service (TMS) API**: To add a new tenant, you need to make an API call to the TMS. This
   call will create a new tenant and generate a corresponding URL for the Graphical User Interface (GUI) of Tracardi.

2. **Provide the GUI URL to the partner**: If our partner wants their customer to directly access and install Tracardi,
   then the partner can then share GUI URL with their customer, who can use it to access the GUI and perform the
   installation process themselves. During installation, the customer will have the opportunity to set up the admin
   account for Tracardi.

3. **Alternative approach - Create the account via Tracardi API**: If the partner prefers not to have their customers
   directly interact with Tracardi, they can use the Tracardi API instead. The partner can call the Tracardi API,
   providing the installation token obtained from the TMS. This API call will create a new account specifically for that
   tenant, ensuring the customer doesn't have to directly access Tracardi, but the account and corresponding instance is
   created.

In summary, the automated installation process for a new tenant in Tracardi involves calling the TMS API to create the
tenant and generate the GUI URL. Depending on the partner's preference, the customer can either install Tracardi
themselves using the GUI URL or have the partner create the account on their behalf using the Tracardi API.