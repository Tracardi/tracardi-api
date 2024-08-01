# How to test workflows?
To test workflows in Tracardi, a staging server is used. The staging server allows developers to test and debug new settings or configuration changes before they are deployed to a production server.

# What is a staging server?
A staging server is a separate server environment used to test and refine new settings and configurations without impacting the live production environment. It provides a controlled environment for testing and debugging before deploying changes to the production server.

# What is the process of staging in Tracardi?
The process of staging in Tracardi involves installing a separate copy of the system designated for staging. The "PRODUCTION" environment variable is set to "no," creating a new set of Elasticsearch indices. The staging server should be exposed on a different port than the production server and ideally not accessible from the internet.

# Do I need a separate license for the staging server if I have a commercial version of Tracardi?
No, you do not need a separate license for the staging server if you have a commercial version of Tracardi. The commercial licenses cover both staging and production servers.

# How should changes be made in Tracardi to minimize the risk of disruptions in the production environment?
Changes in Tracardi should be made on the staging server rather than directly on the production server. This allows thorough testing of the changes before deploying them to the production system. By following this practice, the risk of errors or disruptions in the live production environment is minimized.

# How can changes be deployed from the staging server to the production server?
To deploy changes from the staging server to the production server, the data from the staging server is copied to the production server. However, certain data such as events, profiles, or error logs will not be copied over to ensure the integrity of the production server data.

# What should be the role of accounts on the production server for better security?
On the production server, it is recommended to have a single admin account and marketing accounts that can view data but not change any settings. This helps to prevent unauthorized access or changes that could potentially disrupt the production environment.

## How can I find more information about Tracardi staging server deployment?
More information about Tracardi staging server deployment can be found at [https://youtu.be/10W7OzezF_k](https://youtu.be/10W7OzezF_k).