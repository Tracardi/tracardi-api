## How can processed events from all tenants be set up to be stored and assigned to profiles in a data warehouse by default?

There are two main approaches to storing and assigning processed events from all tenant accounts to profiles in a data
warehouse.

One method is to use an API that collects all the events and then connects this data to the warehouse. Then a
destination can be used to send data to that API.

Alternatively, a more direct approach involves using an internal Tracardi stream to write data directly to the
warehouse. with this approach you would need to write your own code that connects to the internal tracardi stream.
