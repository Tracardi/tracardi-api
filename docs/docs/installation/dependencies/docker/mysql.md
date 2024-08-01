# MySql

!!! Notice

    It's important to note that this document does not cover the installation of MySql intended for production use. For information on setting up MySql for production environments, please refer to the official MySql documentation dedicated to production-ready installations.

Start standalone version of mysql with root password set to `root`:

```
docker run -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 mysql
```

!!! Warning

    This docker does not have any storage volume attached to it so when stopped all the data will be lost. 

!!! Notice

    Last tested version of mysql is: version 8.3. Tracardi also works on percona version tested on 8.0.36.

Please see the MySql Documentation for proper installation.