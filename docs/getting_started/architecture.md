# System architecture

Tracardi is a distributed system that consists of the following components.

* Database where events are stored. Tracardi uses elasticsearch as its backend database.
* Data processing library
* `RESTful API`, `GraphQL API` - Application Programming Interface
* `GUI` - Graphical User interface

Data processing library is a library that deals with starting the workflow for selected events and transferring them to
external systems. For the end user, the library does not exist alone as such, but in conjunction with the API. Programmers 
may use this library to develop [Tracardi plugins](../plugins/index.md).

The GUI is a graphical interface for the end user, it runs in the user's browser.

Each of the elements of this system (API and GUI and Database) can be run in multiple instances. It can also be
installed separately.

## Connecting parts of the system

In order for the system to work fully, three elements must be activated.

* Database
* System API
* Graphical user interface

The GUI connects to the API and the API connects to the database.

