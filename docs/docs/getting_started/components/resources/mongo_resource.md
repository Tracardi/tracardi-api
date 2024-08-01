MongoDB is a source-available cross-platform document-oriented database program. Classified as a NoSQL database program,
MongoDB uses JSON-like documents with optional schemas.

# Resource configuration and set-up

* Type the __MongoDB URI__ - The URI describes the hosts to be used and options. The format of the URI is: mongodb:
  //[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database.collection][?options]] mongodb://
  is a required prefix to identify that this is a string in the standard connection format.
* Type __connection timeout__ - Tracardi will disconnect from mongoDB after this time in micro-seconds if there is no
  connection.
