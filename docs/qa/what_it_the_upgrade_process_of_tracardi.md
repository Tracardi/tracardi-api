# How the progress of Tracardi upgrade looks like.

1. **Creating a New Instance**: During the upgrade process, a new instance of Tracardi is set up with an empty database.
   This is a crucial step as it ensures that the upgrade process does not interfere with the existing data and
   operations.

2. **Data Migration**: Once the new instance is set up, the next step is to migrate data from the old version to the new
   one. This process is automated within Tracardi, which simplifies the transition.

3. **Testing the New Version**: After migrating the data to the new instance, it is recommended to test the new version
   with the migrated data. This is an important step to ensure that the upgrade has been successful and that the new
   version is functioning as expected with the existing data.

4. **Switching the Domain**: Once the testing is complete and everything is running smoothly, the final step is to
   switch the domain (or IP) on your site to point to the new version of Tracardi. This step redirects all the
   operations from the old version to the upgraded version on the new instance.

This focused process ensures a smooth transition during an upgrade, minimizing risks of data loss or system downtime.