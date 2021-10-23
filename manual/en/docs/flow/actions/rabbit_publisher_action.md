# RabbitMQ publisher

The purpose of this plugin is to publish payload to RabbitMQ.

It reads payload and sends it to defined RabbitMQ. RabbitMq must be defined as source in Tracardi.

# Configuration

This node requires configuration.

*Example configuration*

```json
{
  "source": {
    "name": "RabbitMQ",
    "id": "79c315aa-2780-4742-bc70-6444bf8ea444"
  },
  "queue": {
    "name": "test-test",
    "routing_key": "test",
    "queue_type": "direct",
    "compression": null,
    "auto_declare": true,
    "serializer": "json"
  }
}
```

# Input payload

This node reads input payload and sends it to the queue.

# Output

This node has no output. 
 
