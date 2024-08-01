# What is minor version upgrade?

A minor version upgrade refers to an update or release that introduces new features, improvements, and bug fixes to a
software system, but does not involve any changes in the underlying database structure.

In the context of Tracardi, a minor version upgrade is indicated by a change in the last number of the version. For
example, upgrading from version 0.8.1.x to version 0.8.1.y would be considered a minor upgrade.

During a minor version upgrade of Tracardi, the system can be updated simply by upgrading the Docker tag to the new
version. This means that you can change the version number in the Docker tag to the desired minor version, and the
system will continue to work as it did before the upgrade.

Since there are no changes in the database structure, data migration is not required during a minor upgrade. The upgrade
process mainly involves updating the software and taking advantage of the new features and bug fixes introduced in the
new version.

It's important to regularly perform minor version upgrades to ensure that your Tracardi system stays up-to-date with the
latest improvements and enhancements provided by the software.