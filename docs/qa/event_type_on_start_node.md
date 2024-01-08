# In the Start plugin, you can only select a predefined event from the list. What if you need a custom one? For example, event “my-event”? If I write it in the required field, it does not be save. How do I add new events?

The most likely issue is that you didn't hit enter after entering the event type. Please note that simply adding an
event type to the start node does not automatically redirect traffic to this node. Instead, you must use a trigger to
direct the traffic. The event type defined at the start node level simply indicates where the workflow should initiate
for specific event types. This is helpful when multiple events are directed to a single workflow, but only a specific
start node should activate it. If there is only one start node or a single event routed to the workflow, defining an
event type at the node level is unnecessary.