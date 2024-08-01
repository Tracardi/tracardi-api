# Staging server

A staging server is a type of server environment that is used to test and debug new settings/configuration changes
before they are deployed to a production server. Tracardi has a clear separation of a test and production data. This
allows developers to test and refine new settings in a safe and controlled environment, without impacting
the performance or functionality of the live production website or application. It also allows QA Team to test the
application before it goes to the production. This helps ensure that the configuration is stable and functioning
properly before it is made available to end users. Overall, using a staging server helps to minimize the risk of errors
or disruptions in a live production environment, and helps to ensure the quality and stability of the final product.

## Tracardi staging server deployment

To deploy Tracardi on a staging server, a separate copy of the system must be installed and designated as such. This
involves setting the "PRODUCTION" environment variable to "no," which creates a new set of Elasticsearch indices.
Additionally, the staging server should be exposed on a different port than the production server and ideally not
accessible from the internet.

## Tracardi production server deployment

To deploy Tracardi on a production server, another copy of the system must be installed and configured with the "
PRODUCTION" environment variable set to "yes." This creates a new set of Elasticsearch indices prefixed with "prod-".

## Staging server security and networking

The preferred settings for networking a staging server involve separating the staging and production servers by
assigning different API IP addresses. This is done for security reasons, as the staging server should not be exposed to
the internet and should only be accessible within the internal network, preferably through a VPN. This ensures that only
the production collector endpoints are publicly available.

Additionally, it is important to limit access to the production server by not having accounts with roles that allow
changes to the server configuration. The best practice is to have a single admin account and only marketing accounts
that can view data but not change any settings. This helps to prevent unauthorized access or changes that could
potentially disrupt the production environment.

## Licensing commercial version of Tracardi

No need to worry about separate licenses for staging and production servers, all commercial licenses cover both servers.

!!! Tip

    When working with Tracardi the production server should not be edited directly. Instead, all changes should be made on the staging server and
    thoroughly tested before being deployed to the production system. This helps to minimize the risk of errors or
    disruptions in the live production environment.

    Once changes have been tested on the staging server, they can then be deployed to the production system. This is done by
    copying the data from the staging server to the production server. However, certain data such as events, profiles, or
    error logs will not be copied over during this process to ensure that the production server data remains intact.

## More information

More information can be found at https://youtu.be/10W7OzezF_k

