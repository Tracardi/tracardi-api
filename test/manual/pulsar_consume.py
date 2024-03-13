import pulsar
from _pulsar import ConsumerType, InitialPosition
from pulsar.schema import JsonSchema
from com_tracardi.decorator.deffer_decorator import FunctionRecord
from com_tracardi.service.tracking.queue.pulsar_topics import pulsar_topics

client = pulsar.Client('pulsar://localhost:6650')

consumer = client.subscribe(pulsar_topics.system_function_topic,
                            'my-subscription-2',
        consumer_name="my-consumer",
        schema=JsonSchema(FunctionRecord),
        consumer_type=ConsumerType.Shared,
        initial_position=InitialPosition.Earliest)
while True:
    try:
        msg = consumer.receive(timeout_millis=5000)
        message: FunctionRecord = msg.value()
        print('----------------------------------------------------------------')
        print("System Event:", message.type)
        print("Internal Function", message.name)
        print("Data", FunctionRecord.deserializer(message.args))
        print("Context", FunctionRecord.deserializer(message.context))
        # Acknowledge successful processing of the message
        consumer.acknowledge(msg)
    except Exception as e:
        pass
client.close()
