# What does the open source Tracardi worker do?

Just like other Tracardi workers, the open source Tracardi worker handles tasks that run in the background. It takes
care of importing data and ensuring that the system data is migrated and upgraded to newer versions. Without this
worker, you won't be able to import or upgrade the system. If the worker is not functioning properly, you will notice
that all the background processes are in a pending state.