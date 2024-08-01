# What are the differences between major and minor upgrades

The main differences between minor and major upgrades can be summarized as follows:

Minor Upgrades:

1. Changes: Minor upgrades involve updates that do not require modifications to the underlying database structure.
2. Version Number: Minor upgrades are indicated by a change in the last number of the version. For example, going from
   version 1.2.0.1 to 1.2.0.1.
3. Data Migration: Minor upgrades generally do not require data migration or schema updates.
4. Compatibility: Minor upgrades are designed to ensure backward compatibility, meaning that the system will continue to
   work as it did before the upgrade.

Major Upgrades:

1. Changes: Major upgrades involve substantial changes, including modifications to the underlying database structure.
2. Version Number: Major upgrades are indicated by a change in a number other than the last one in the version. For
   example, going from version 2.0.0 to 3.0.0 or 0.8.0 rto 0.8.1.
3. Data Migration: Major upgrades often require data migration or schema updates to align the existing data with the new
   version.
4. Upgrade Process: Major upgrades typically involve a more involved process, including running two copies of the
   system (old and new) and migrating the data from the old version to the new version.
5. Compatibility: Major upgrades may introduce backward-incompatible changes, meaning that the system may require
   additional steps and effort to ensure that existing functionalities and data work correctly with the new version.

In summary, minor upgrades involve smaller updates that do not require significant changes to the system's database
structure. Major upgrades, on the other hand, encompass substantial changes, including modifications to the database
structure, and often require data migration and careful planning to ensure a smooth transition to the new version.