# What are the pros and cons of multi-tenant setup of Tracardi?

Pros of Multi-tenant Setup:

1. Simplified Maintenance: Shared application instances across all tenants simplify maintenance and upgrade rollouts,
   reducing maintenance overhead.
2. Scalability: Multi-tenant setups allow for efficient resource utilization and scalability by sharing infrastructure
   and resources among multiple tenants.
3. Cost-effectiveness: By sharing resources, a multi-tenant setup can reduce infrastructure and operational costs
   compared to maintaining separate instances for each tenant.
4. One-click Onboarding: Multi-tenant setups can enable one-click onboarding of new clients, streamlining the process of
   provisioning necessary infrastructure and mappings.
5. Data Backup and Disaster Recovery: Multi-tenant setups can utilize backup mechanisms like Elasticsearch's snapshot
   repositories to ensure data backups, disaster recovery, and data protection for all tenants.

Cons of Multi-tenant Setup:

1. Limited Customization: In a multi-tenant setup, it may be challenging to provide extensive customization options for
   individual tenants since upgrades and modifications affect all tenants simultaneously.
2. Upgrades and Patches: Upgrades and patches need to be applied uniformly across all tenants, making it challenging to
   cherry-pick upgrades for specific tenants. This can result in more maintenance work compared to single-tenant setups.
3. Dependency on Tenant Management Service (TMS): Multi-tenant setups rely on a Tenant Management Service (TMS) for
   tenant management, which introduces an additional dependency that needs to be properly configured and maintained.
4. Data Security and Isolation: Ensuring data security and isolation among tenants can be more complex in a multi-tenant
   environment compared to separate instances.
5. Increased Complexity: Multi-tenant setups introduce additional complexity in terms of architecture, infrastructure
   management, and data segregation, requiring careful planning and implementation.

It's important to note that the pros and cons may vary depending on the specific implementation and requirements of the
multi-tenant setup.