# How backups are done in Tracardi.

Tracardi uses the built-in backup mechanism of Elasticsearch that allows you to create backups of your data for disaster
recovery and data protection.

Here's an overview of how backups work in Elasticsearch:

1. **Snapshot Repositories**: Elasticsearch backups are created and stored in snapshot repositories. A snapshot
   repository is a location where Elasticsearch stores the backup data. It can be a shared file system, a cloud storage
   service, or a network-attached storage (NAS).

2. **Snapshot Lifecycle**: You define a snapshot lifecycle policy that specifies how often to take backups and how long
   to retain them. This policy automates the backup process and ensures that backups are created at regular intervals.

3. **Snapshot Creation**: When a snapshot is created, Elasticsearch takes a point-in-time copy of the data and metadata
   in the cluster. This includes index data, index settings, mappings, and other relevant information. The snapshot is
   stored in the designated repository.

4. **Incremental Backups**: Elasticsearch uses incremental backups, which means that subsequent snapshots only include
   the changes since the last snapshot. This reduces the backup time and storage requirements.

5. **Snapshot and Restore API**: Elasticsearch provides a Snapshot and Restore API that allows you to manage the backup
   process. You can create, list, restore, and delete snapshots using this API. You can also monitor the status of
   snapshot operations and track the progress.

6. **Cluster Coordination**: When taking snapshots, Elasticsearch coordinates the backup process across all nodes in the
   cluster. It ensures that each shard of the data is captured and included in the backup, even in a distributed cluster
   setup.

7. **Backup Verification**: Elasticsearch allows you to verify the integrity of a snapshot by performing a verification
   process. This ensures that the backup data is intact and can be restored successfully if needed.

8. **Disaster Recovery**: In the event of a disaster or data loss, you can restore a snapshot to recover your data.
   Elasticsearch provides options to restore the entire cluster, specific indices, or individual shards from a snapshot.

Please read more about Elasticsearch (ES) backups in documentation.  