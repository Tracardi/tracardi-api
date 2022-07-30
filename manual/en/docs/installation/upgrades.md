# System update

Automated system update is available from version 0.7.0. Previous versions were unable to update system data. There was
only an update of the code. As of version 0.7.0 the system keeps information about the indexes used. In addition, access
to data is carried out using aliases, these are indicators for data, something reminiscent of symbolic links.

## The update process

When upgrading, Tracardi leaves the old version indexes unchanged and only marks them as the previous version (aliases
to these indexes have the .prev suffix).

At the same time, new empty indexes are created along with new aliases. Then, if the schema of the old index has not
changed, the data pointer is switched from the old index to the new one. If the scheme has changed, the data is migrated
using a script that rewrites the data between indexes and copies the data from the old fields to the new ones,
respectively.

## Prerequisites

However, it is important to only install dockers with a tagged version. The latest version may contain incorrect data,
which may result in the loss of continuity of updates. As a result, it may be difficult to update the system.

# Installation of version 0.7.0

As it was said above the versions prior to 0.7.0 are not aware of previous data schemas. Therefore, the system does not
know what indexes were used previously and it is not able to check the changes that have occurred in their schemas. That
means, the manual data migration by re-indexing is necessary. If the collected data in previous versions is not
important and it is possible to lose it, we recommend fresh install.

## Manual transfer

To transfer data, first check what indexes you have in elasticsearch. This can be done by going to __Monitoring /
Elasticsearch indices__ in Tracardi. Indexes marked __Connected__ are currently in use and are prefixed with a version
number. Old indexes from system e.g. version 0.6.0, do not have a prefix and are marked as __Not Connected__.

To transfer data, use the reindex function available in elasticsearch. Documentation of this functionality can be found
here.

```
https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html
```

Reindexing data is nothing more than copying it from one index to another.

