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
docker pull tracardi/tracardi-api
docker pull tracardi/tracardi-gui
```

Then you can run it the same way as written in [installation](installation/index.md).

!!! Warning

    Upgrades of minor versions of Tracardi may cause data loss.

# Upgrades post version 1.0

After the version 1.0 is released Tracardi will maintain on only code but also will freeze saved plugins in database 
that will allow to have a smooth upgrade process between major version. 
