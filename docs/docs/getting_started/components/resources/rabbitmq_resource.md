***RabbitMQ allows to process compute intensive data outside tracardi server. You may want to run some data processing in
the background and distribute the load to multiple servers.***

For Extensive Information about RabbitMQ visit : https://www.rabbitmq.com/documentation.html

- _You can create new user for accessing your RabbitMQ broker. Normally port used is 5672 but you can change it in your configuration file._

- _So suppose your IP is 1.1.1.1 and you created user test with password test and you want to access vhost "dev" (without quotes) then it will look something like this:
amqp://test:test@1.1.1.1:5672/dev_

- _A virtual host has a name. When an AMQP 0-9-1 client connects to RabbitMQ, it specifies a vhost name to connect to. If authentication succeeds and the username provided was granted permissions to the vhost, connection is established._

# Resource configuration and set-up

1. Type the RabbitMQ url
2. Type the port Number.
3. Type the Virtual Host Name(if any)
4. Type the Connection Timeout limit.

## Info

This resource can be used as destination.
