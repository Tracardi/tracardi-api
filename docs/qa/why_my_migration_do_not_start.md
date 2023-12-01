# Why my migration do not start?

Most probably the issue with your Tracardi migration is related to the Migration and Import Worker not being
started. The Migration and Import Worker is essential for system upgrades and data import tasks in Tracardi, as it
handles these processes in the background.

To resolve the issue, you should start the Migration and Import Worker. You can do this by executing the following
Docker command:

```bash

docker run \
-e REDIS_HOST=redis://<redis-ip>:6379 \
tracardi/update-worker:0.8.1
```

Make sure to replace <redis-ip> with the actual IP address of your Redis instance. This command will initiate the
Migration and Import Worker, which should facilitate the migration process.

!!! Tip

    This migration process is valid for systems before version 0.9.0
