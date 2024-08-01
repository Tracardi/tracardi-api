# Tracardi Processes

Tracardi is build around 5 major processes.

## Key Processes

* **[Integration](integration/index.md)**: Integration is not a process within Tracardi. Instead, it occurs within a company and involves integrating systems
      with Tracardi to send data from various systems, websites, and databases to Tracardi.

* **[Collection](collection.md)**: Collection is the process responsible for gathering and ingesting data. It consists of several subprocesses:
      * **[Tracking](tracking.md)**: The process of maintaining a consistent single Profile ID across all customer interactions on a single device. It is the responsibility of the device/client to keep the Profile ID unchanged.
      * **[Identity Resolution and Merging](identity_resolution.md)**: The process of maintaining a consistent single profile across all customer devices. It is Tracardi's responsibility to merge all profiles created on different devices whenever possible.
      * **Storing Data**: This process involves storing collected data in one profile record and referencing all historical events and sessions.

* **[Automation](automation.md)**: This process automates the customer journey, enhances customer profiles, personalizes customer experiences, and triggers messaging.

* **[Audiences and Activations](audience.md)**: The process of creating audiences/segments and orchestrating them to external systems such as Marketing Automation platforms.

* **[Orchestrator/Router](orchestration.md)**: The process responsible for sending customer data to external systems.
