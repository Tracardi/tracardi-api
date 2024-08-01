# What is major version upgrade?

A major version upgrade refers to a significant update or release of a software system that introduces substantial
changes, including modifications to the underlying database structure.

In the context of Tracardi, a major version upgrade is indicated by a change in a number other than the last one in the
version. For example, upgrading from version 0.8.0 to version 0.8.1 would be considered a major upgrade.

During a major version upgrade of Tracardi, there may be changes to the database schema or data structure. These changes
often require data migration or data schema updates to ensure that the system functions properly with the new version.
Tracardi handles data migration during major upgrades using Elasticsearch's reindexing process.

The upgrade process typically involves running two copies of the system: one with the old version and one with the new
version. The migration process moves the data from the old version to the new version while ensuring data integrity and
consistency. Once the migration is complete, the Docker tag can be upgraded, and the system will automatically switch to
the new version.

It's important to note that major upgrades may require additional effort and planning compared to minor upgrades.
Tracardi provides migration scripts for all major versions, which help facilitate the upgrade process and ensure proper
data migration. However, skipping versions during major upgrades is not supported, and it's recommended to follow the
upgrade path version by version for data integrity and system stability.
