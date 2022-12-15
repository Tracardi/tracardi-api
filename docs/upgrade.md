# Upgrades

Tracardi is being still developed. Though it can be used as is right now, upgrading may cause some issues. This is due
to the way workflows are persisted. Workflow created in one version may not have all the plugins that exist in new
version or the plugins behave a bit differently. Till Tracardi reaches version 1.0 only code is fully upgradable. We do
not upgrade the saved workflows or freeze the plugin versions. When you upgrade to new version you have to make sure
that the saved plugins behave the same way. So connect new version to old elastic instance and see what is not working
and replace old plugins with the new ones. Plugins have versions, so you can have the same plugin in two versions registered
in elastic.

To upgrade source to the latest development version pull new docker image.

```
docker pull tracardi/tracardi-api:<version>
docker pull tracardi/tracardi-gui:<version>
```

Then you can run it the same way as written in [installation](installation/index.md).

!!! Warning

    Upgrades of minor versions of Tracardi may cause data loss.

# Upgrades post version 0.7.2

Tracardi version 0.7.2 introduced a feature that allows data migration between versions. Each new installation 
creates a new emtpy Tracardi database. The data can be migrated from old version to the new one. To do this 
please click on `maintenance/migration` find the migration script from old version, and follow the instructions.

!!! Warning

    Please notice the when you make a lot of upgrades of Tracardi the system creates a lot of new indices indices 
    this way you may reach the Elasticsearch limit of 1000 indices. To solve this you may increase the limit in 
    Elasticsearch configuration or delete the indices used by old Tracardi versions. Version 0.8.0 has this feature 
    in the GUI. Older versions have an API tha can be used to delete old indices, for example a HTTP DELETE call to 
    `/indices/version/0.7.2` should delete the 0.7.2 version indices. 
    Please test new installation thoroughly before deleting old data because after deletion there is no way to revert
    system to the old version.  
