# How Tracardi is upgraded?

Tracardi upgrades are categorized into two types: minor upgrades and major upgrades.

**Minor Upgrades**: Minor upgrades do not involve any changes in the underlying database structure. These upgrades are
indicated by a change in the last number of the version. For example, upgrading from version 0.8.1.x to version 0.8.1.y
would be considered a minor upgrade. Minor upgrades do not require data migration and can be performed simply by
upgrading the Docker tag to the new version. The system will continue to work as it did before the upgrade.

**Major Upgrades**: Major upgrades, on the other hand, involve changes in the database structure. These upgrades are
indicated by a change in a number other than the last one in the version. For example, upgrading from version 0.8.0 to
version 0.8.1 would be considered a major upgrade. Major upgrades typically require data migration or data schema
updates. In Tracardi, data migration is performed using Elasticsearch's reindexing process. This involves running two
copies of the system with separate sets of indices: one with the old version and one with the new version. Once the
migration is complete, the Docker tag can be upgraded, and the system will automatically switch to the new version.
After a period of time, the old version's data can be safely deleted.

Tracardi provides migration scripts for all major versions, allowing for smooth upgrades. However, it's important to
note that these scripts are only available from one version to the next. Skipping versions is not supported, and custom
scripts may require additional effort and commercial services. It is recommended to follow the upgrade path version by
version to ensure proper data migration and system stability.

If you are running a multi-tenant instance of Tracardi, the upgrade process will be applied to all tenants
simultaneously. This means that when performing an upgrade, the changes will be applied uniformly across all the tenants
in the system.

In the case of a major upgrade, where data structure changes are involved, it is important to note that the migration
process will require migrating the data for all tenants. This ensures that the entire system is up-to-date and
consistent with the new version. The data migration process, must be performed for
all tenants to ensure that their data aligns with the updated database structure.

By applying the major upgrade to all tenants and performing the necessary data migration, the system can maintain data
integrity.