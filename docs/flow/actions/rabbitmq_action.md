# RabbitMQ publisher

The purpose of this plugin is to publish payload to RabbitMQ.

It reads payload and sends it to defined RabbitMQ. RabbitMq must be defined as source in Tracardi.

# Configuration

This node requires configuration.

Example configuration

```json
{
  "source": {
    "id": "58df3b5c-3109-4750-bb5b-81f5386950b1"
  },
  "queue": {
    "name": "tracardi",
    "routingKey": "trk"
  }
}
```

# Input payload

This node reads input payload.

# Output

This node has no output. 
 
