# How can you copy data from events to profiles?

To copy data from events to profiles, you will need to create a workflow with a start node and a node called "
copy data". In the "copy data" node, you can select the destination and set it to the event property e.g. "phone", "
email", etc. Another way to copy data is to use the "Auto group merge event properties" node, which will automatically
merge all event properties to the profile traits. 