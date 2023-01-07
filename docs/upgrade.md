# Upgrades

Tracardi is still in active development, and as such, upgrading to a new version may introduce some compatibility issues. This is due to the way that workflows are persisted, which may change between versions. Workflows created in one version may not work properly with all the available plugins in a newer version, or the plugins may behave differently.

To ensure a smooth upgrade process, it is recommended to wait until Tracardi reaches version 1.0, at which point the code will be fully upgradeable. Until then, you should carefully check for any issues when upgrading to a new version. You can do this by connecting the new version to the old Elastic instance and reviewing any saved workflows or plugin versions for compatibility. If necessary, you can replace old plugins with newer versions to ensure that everything works as expected. Note that it is possible to have multiple versions of the same plugin registered in Elastic.

To upgrade source to the latest development version pull new docker image.

```
docker pull tracardi/tracardi-api:<version>
docker pull tracardi/tracardi-gui:<version>
```

Then you can run it the same way as written in [installation](installation/index.md).

!!! Warning

    Upgrades of minor or development versions of Tracardi may cause data loss. Each development version is marked with `-dev` suffix.

# Upgrades post version 0.7.2

In Tracardi version 0.7.2, a feature was introduced that allows for data migration between versions. Each new Tracardi installation creates a new, empty database, and the data from an old version can be migrated to the new one. To perform this migration, follow these steps:

* Navigate to the maintenance/migration page.
* Locate the migration script from the old version.
* Follow the instructions provided in the script to complete the data migration.

Note that this feature is only available in Tracardi version 0.7.2 and higher. If you are using an older version, you will need to upgrade to at least 0.7.2 in order to access this functionality.

!!! Warning

     If you perform multiple upgrades of Tracardi, the system will create a large number of new indices, which may cause you to reach the Elasticsearch
     limit of 1000 indices. To resolve this issue, you can either increase the limit in the Elasticsearch configuration or delete the indices used by old
     Tracardi versions. Tracardi version 0.8.0 includes a feature in the GUI to delete old indices. If you are using an older version, you can use the API
     to delete old indices, such as issuing a HTTP DELETE call to /indices/version/0.7.2 to delete the 0.7.2 version indices. However, be cautious when 
     deleting old data, as there is no way to revert the system to an older version once the data has been deleted. It is important to thoroughly test your 
     new Tracardi installation before deleting any old data. 
