# Apache Pulsar

!!! Notice

    It's important to note that this document does not cover the installation of Apache Pulsar intended for production use. For information on setting up Apache Pulsar for production environments, please refer to the official Apache Pulsar documentation dedicated to production-ready installations.



Start standalone version of Apache Pulsar with:

```
docker run -it \
-p 6650:6650 \
-p 8080:8080 \
apachepulsar/pulsar:3.1.0 \
bin/pulsar standalone
```
!!! Warning

    This docker does not have any storage volume attached to it so when stopped all the data will be lost. 

!!! Notice

    Last tested version of apache pulsar is: version 3.1.0.


Please see the Apache Pulsar Documentation for proper installation.