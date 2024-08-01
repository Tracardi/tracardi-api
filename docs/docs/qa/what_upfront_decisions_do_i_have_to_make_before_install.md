# What upfront decisions do I have to make before I install production ready Tracardi.

Before installing Tracardi, there are several upfront decisions you need to make to ensure a smooth setup and operation.

Here are the key considerations:

### 1. **Decide on Deployment Type**

- **Open Source vs. Commercial**: Choose between the open-source version of Tracardi or the commercial version,
  depending on your requirements and budget.
  See [what are the differences between Open-source and Commercial version](what_is_the_difference_between_os_and_commercial.md)?
- **Deployment Environment**: Decide whether you will deploy on Docker, Kubernetes (K8s), or another environment.

### 2. **Infrastructure and Dependencies**

- **Essential Services**: Tracardi relies on several dependencies, including Redis, Elasticsearch, MySQL, and optionally
  Apache Pulsar for event streaming. It is crucial to ensure these services are set up correctly or to plan their
  installation. Scaling these services is particularly important, especially for Elasticsearch, which is quite demanding
  in terms of the number of shards that cannot be changed later. For detailed instructions,
  see [how to configure number of shards](how_to_configure_number_of_shards.md).
- **Storage and Persistence**: Plan for data persistence by ensuring storage solutions for Elasticsearch and Redis, and
  understand their configurations for production use.

### 3. **Configuration**

- **User Authentication**: Configure authentication mechanisms for accessing Tracardi services, such as secure
  credentials for databases and API endpoints.
- **Environment Variables**: Set up the necessary environment variables for configuring Tracardi components,
  especially `INSTALLATION_TOKEN` and `AUTO_PROFILE_MERGING`. For detailed guidance,
  see [Which environment variables should I set before production installation](which_env_variabes_to_tweak_before_install.md).
- **Multi-Tenancy**: Decide if you will enable multi-tenancy features to manage different clients or divisions within
  your organization. See [How to start Tracardi in multi-tenant mode](how_do_i_setup_multi_tenant.md)?
- **Data Partitioning**: Configure data partitioning strategies for events, profiles, and sessions to optimize
  performance and storage.
- **Custom Settings**: Customize settings like logging levels, API documentation, and workflow enablement according to
  your operational needs.

### 4. **Licensing and Access**

- **Commercial Licensing**: If using the commercial version, ensure you have the necessary license keys and DockerHub
  access tokens.

### 5. **Monitoring and Telemetry**

- **Monitoring Tools**: Integrate monitoring tools to keep track of system performance and health.
- **Telemetry Configuration**: Set up telemetry to gather metrics and logs, helping in proactive issue resolution and
  performance tuning.

### 6. **Backup and Disaster Recovery**

- **Backup Plans**: Establish regular backup schedules for critical data stored in Elasticsearch and MySQL.
- **Disaster Recovery**: Develop a disaster recovery plan to restore services in case of system failures.

