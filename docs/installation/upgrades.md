# Tracardi Upgrades

This documentation provides information on how to upgrade Tracardi and perform data migration between versions. It also
covers the process of updating the system and the precautions to take during the upgrade process.

## Upgrades

Tracardi is still in active development, and upgrading to a new version may introduce compatibility issues due to
changes in workflow persistence. Workflows created in one version may not work properly with all available plugins in a
newer version, or the plugins may behave differently.

To upgrade the source to the latest development version, pull the new docker image:

```bash
docker pull tracardi/tracardi-api:<version>
docker pull tracardi/tracardi-gui:<version>
```

Then you can run it the same way as written in the [installation](docker/index.md) guide.

!!! Warning

    Upgrades of minor or development versions of Tracardi may cause data loss. Each development version is
    marked with a `-dev` suffix.

### Prerequisites for Upgrading

Before upgrading, it is crucial to ensure that you only install dockers with a tagged version. Installing the latest
version without proper tagging may lead to incorrect data, resulting in the loss of continuity during the upgrade
process. Therefore, it is essential to install the appropriate tagged version to facilitate a smooth system upgrade.

### Automated System Upgrades

Starting from version 0.7.0, Tracardi offers automated system upgrades. Unlike previous versions, which could only
upgrade the code, version 0.7.0 and above maintain information about the indexes used. Access to data is achieved
through aliases, which function like symbolic links.

#### The Upgrade Process

When performing an upgrade, Tracardi leaves the old version indexes unchanged and designates them as the previous
version. Simultaneously, new empty indexes are created, along with new aliases (each prefixed with version number). If
the schema of the old index remains unchanged, the data pointer is switched from the old index to the new one. However,
if there are schema changes, the data is migrated using a script that rewrites the data between indexes and copies the
data from the old fields to the new ones accordingly. This process ensures a seamless transition during the upgrade.

---

## Upgrades post version 0.7.2

In Tracardi version 0.7.2, a feature was introduced that allows for data migration between versions. Each new Tracardi
installation creates a new, empty database, and the data from an old version can be migrated to the new one. To perform
this migration, follow these steps:

1. Navigate to the maintenance/migration page.
2. Locate the migration script from the old version.
3. Follow the instructions provided in the script to complete the data migration.

Note that this feature is only available in Tracardi version 0.7.2 and higher. If you are using an older version, you
will need to upgrade to at least 0.7.2 to access this functionality.

!!! Warning

    If you perform multiple upgrades of Tracardi, the system will create a large number of new indices, which
    may cause you to reach the Elasticsearch limit of 1000 indices. To resolve this issue, you can either increase the limit
    in the Elasticsearch configuration or delete the indices used by old Tracardi versions. Tracardi version 0.8.0 includes
    a feature in the GUI to delete old indices. If you are using an older version, you can use the API to delete old
    indices, such as issuing an HTTP DELETE call to `/indices/version/0.7.2` to delete the 0.7.2 version indices. However,
    be cautious when deleting old data, as there is no way to revert the system to an older version once the data has been
    deleted. It is important to thoroughly test your new Tracardi installation before deleting any old data.

## Installation prior Version 0.7.0

Versions prior to 0.7.0 are not aware of previous data schemas. Therefore, the system does not know what indexes were
used previously and is not able to check the changes that have occurred in their schemas. This means that manual data
migration by re-indexing is necessary. If the collected data in previous versions is not important and it is possible to
lose it, a fresh installation is recommended.

### Manual Transfer

To transfer data, first check what indexes you have in Elasticsearch. This can be done by going to _Monitoring /
Elasticsearch indices_ in Tracardi. Indexes marked as _Connected_ are currently in use and are prefixed with a version
number. Old indexes from system e.g. version 0.6.0, do not have a prefix and are marked as _Not Connected_.

To transfer data, use the reindex function available in Elasticsearch. Documentation of this functionality can be
found [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html). Reindexing data is
nothing more than copying it from one index to another.

---

This documentation answers the following questions:

* How can I upgrade Tracardi?
* What is data migration?
* How to migrate Tracardi to a new version?
* What's the minimum version required for automated system upgrades in Tracardi?
* What was the limitation with system data upgrades in versions before 0.7.0?
* How does Tracardi handle indexes when upgrading to a new version?
* Why is it important to install dockers with a tagged version during system upgrades?
* Do you need to manually migrate data when upgrading from a version before 0.7.0 to version 0.7.0?
* How can you check your indexes in Elasticsearch when transferring data?