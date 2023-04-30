A staging server is a type of server environment that is used to test and debug new code changes before they are
deployed to a production server. Tracardi has a clear separation of a test and production data, allowing developers to
test and refine new features or bug fixes in a safe and controlled environment, without impacting the performance or
functionality of the live production website or application. To deploy Tracardi on a staging server, a separate copy of
the system must be installed and designated as such, and the staging server should be exposed on a different port than
the production server and ideally not accessible from the internet. To deploy Tracardi on a production server, another
copy of the system must be installed and configured with the "PRODUCTION" environment variable set to "yes." The
preferred settings for networking a staging server involve separating the staging and production servers by assigning
different API IP addresses. Additionally, it is important to limit access to the production server by not having
accounts with roles that allow changes to the server configuration. No need to worry about separate licenses for staging
and production servers, all commercial licenses cover both. When working with Tracardi the production server should not
be edited directly. Instead, all changes should be made on the staging server and thoroughly tested before being
deployed to the production system. This helps to minimize the risk of errors or disruptions in the live production
environment.