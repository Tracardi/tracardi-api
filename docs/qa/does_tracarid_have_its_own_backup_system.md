# Does tracardi has its own backup system?

No. Tracardi uses the built-in backup mechanism of Elasticsearch for data backups. Elasticsearch
allows you to create backups of your data for disaster recovery and data protection. The backup process involves
creating snapshot repositories to store the backup data, defining a snapshot lifecycle policy, and using the Snapshot
and Restore API to manage the backup process. 