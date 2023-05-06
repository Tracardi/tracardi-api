This documentation provides information about automated system updates in Tracardi from version 0.7.0. Previous versions were unable to update system data, only code. As of version 0.7.0, the system keeps information about the indexes used and access to data is carried out using aliases. When upgrading, Tracardi leaves the old version indexes unchanged and only marks them as the previous version. New empty indexes are created along with new aliases. If the schema of the old index has not changed, the data pointer is switched from the old index to the new one. If the scheme has changed, the data is migrated using a script that rewrites the data between indexes and copies the data from the old fields to the new ones. It is important to only install dockers with a tagged version, as the latest version may contain incorrect data. Manual data migration is necessary when upgrading from a version before 0.7.0 to version 0.7.0. To transfer data, first check what indexes you have in elasticsearch by going to Monitoring/Elasticsearch indices in Tracardi. Indexes marked Connected are currently in use and are prefixed with a version number. Old indexes from system e.g. version 0.6.0, do not have a prefix and are marked as Not Connected. To transfer data, use the reindex function available in elasticsearch. Reindexing data is nothing more than copying it from one index to another.