# What does staging mean in tracardi version?

In Tracardi, staging refers to a server environment used to test and debug configuration changes before they are
deployed to a production server. The purpose of staging is to ensure that new configurations can be thoroughly
tested in a controlled environment without impacting the live production website or application.

When connected to the staging API, it means that you are using the API version specifically designed for collecting test
data. This allows you to perform tests without affecting the production data. The staging environment keeps the test
data separate from the production data, ensuring that any changes or experiments you make are isolated and do not
interfere with the live system.

In terms of the graphical user interface (GUI), it is possible for it to connect to both the staging and production
APIs. However, it is advisable to connect to the staging API with the GUI when performing tests. The production API
should be reserved for actual usage by webpages or mobile phones, as it needs to be exposed to the internet to receive
real user data.

By connecting to the staging API with the GUI, you can safely experiment and validate new configurations without
affecting the production environment. Also, Production data is visible in a read only mode.