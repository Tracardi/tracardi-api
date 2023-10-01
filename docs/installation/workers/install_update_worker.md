# Migration and Import Worker Docker Installation

The Migration and Import Worker is responsible for system upgrades and data import tasks, which are carried out in the
background. It ensures a seamless transition when updating the Tracardi system and handles data imports efficiently.

To run the Migration and Import Worker, execute the following Docker command:

```bash
docker run \
-e REDIS_HOST=redis://<redis-ip>:6379 \
tracardi/update-worker:0.8.1
```

Please ensure that you replace `<redis-ip>` with the actual IP address of your Redis instance.