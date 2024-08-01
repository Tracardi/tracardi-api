# Is it possible to use Kafka as the primary source of events for Tracardi, where events from various channels are initially published to Kafka?

In the commercial version of Tracardi, there is a Kafka bridge, and the payload format aligns with the API. If you have
alternative strategies for event collection, it's possible to extend this bridge. However, it's important to note that
when collecting events through Kafka, a synchronous connection is not available. This means that if you require a
response or intend to use a widget, it may not be suitable.

Regarding the organization of data, there isn't a prescribed method; you can simply subscribe to a topic, and Tracardi
will consume the data. It's essential to ensure that the payload structure matches that of the API body.