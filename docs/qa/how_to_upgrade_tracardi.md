# How to upgrade Tracardi?

To upgrade Tracardi, you need to navigate to the maintenance/migration page and locate the migration script from the old
version. Follow the instructions provided in the script to complete the data migration. This feature is only available
in Tracardi version 0.7.2 and higher. If you are using an older version, you will need to upgrade to at least 0.7.2 in
order to access this functionality.

When performing multiple upgrades of Tracardi, the system will create a large number of new indices, which may cause you
to reach the Elasticsearch limit of 1000 indices. To resolve this issue, you can either increase the limit in the
Elasticsearch configuration or delete the indices used by old Tracardi versions. Tracardi version 0.8.0 includes a
feature in the GUI to delete old indices. If you are using an older version, you can use the API to delete old indices,
such as issuing a HTTP DELETE call to /indices/version/0.7.2 to delete the 0.7.2 version indices. However, be cautious
when deleting old data, as there is no way to revert the system to a previous version.