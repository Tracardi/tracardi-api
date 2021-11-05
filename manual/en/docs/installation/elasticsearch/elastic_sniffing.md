# Elastic sniffing

Elasticsearch is a distributed system, which means its indices live in multiple nodes connected to each other, forming a
cluster. One of the main advantages of being a distributed system — other than fault tolerance — is data is sharded into
multiple nodes, allowing searches to run much faster than searches run through a huge single node.

A typical client configuration is a single URL that points to one node of the Elasticsearch cluster. While this is the
simplest configuration, the main disadvantage of this setup is all of the requests you make will be sent to that
specific coordination node. Since this puts a single node under stress, overall performance may be affected.

One solution is to pass a static list of nodes to the client, so your requests will be equally distributed among the
nodes.

Or you can enable a feature called sniffing.

With a static list of nodes, there’s no guarantee that the nodes will always be up and running. For example, what
happens if you take a node down to upgrade — or you add new nodes?

If you enable sniffing, the client will start calling the `_nodes/_all/http` endpoint, and the response will be a list
of all the nodes that are present in the cluster along with their IP addresses. Then the client will update its
connection pool to use all of the new nodes and keep the state of the cluster in sync with the client’s connection pool.
Note that even if the clients download the full list of nodes, the master-only nodes will not be used for generic API
calls.

Sniffing solves this discovery issue.

When you enable sniffing, you’ll make your application more resilient and able to adapt to the changes. Before doing so,
you should know your infrastructure, so you can decide what the best solution to adopt is. The best solution might even
be to not adopt sniffing.

Tracardi has some configuration that can be adopted to turn on of off sniffing. See `tracardi configuration` to get more
information on how to configure sniffing.

## Sniffing at startup

As the name suggests, when you enable this option, the client will attempt to execute a sniff request one time only
during the client initialization or first usage. It will call all nodes to obtain a list of active nodes.

## Sniffing on connection failure

If you enable this option, the client will attempt to execute a sniff request every time a node is faulty, which means a
broken connection or a dead node. 
