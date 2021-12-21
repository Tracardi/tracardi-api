# Upgrading Tracardi

Tracardi is being still developed. Though it can be used as is right now, upgrading may cause some issues. This is due
to the way workflows are persisted. The workflow created in one version may not have all the plugins that exist in the new
version or the plugins behave a bit differently. Till Tracardi reaches version 1.0 only code is fully upgradable. We do
not upgrade the saved workflows or freeze the plugin versions. When you upgrade to the new version you have to make sure
that the saved plugins behave the same way. To connect the new version to the old elastic instance and see what is not working
and replace old plugins with new ones. Plugins have versions, so you can have the same plugin in two versions registered
in elastic.

To upgrade the source from version 0.5.0 to 0.6.0 what you have to do is to pull a new docker image.

```
docker pull tracardi/tracardi-api
docker pull tracardi/tracardi-gui
```

Then you can run it the same way as written in installation. Upgrades between minor versions may cause loss of data.
Do not upgrade major version (e.g. 1.0.0) to minor (1.2.0) version on production.

# Upgrading Tracardi post version 1.0

After the version major 1.0 is released Tracardi will maintain code and will freeze plugins code. This will allow 
a smooth upgrade process between major version. 
