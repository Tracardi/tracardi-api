# How to get started

TRACARDI open-source customer data platform offers you excellent control over your customer data with its broad set of
features.

Here we will describe the key terms that are used in tracardi. We will also describe the way of processing the event,
through which elements of the system the event passes and what is its result.

## System architecture

Tracardi is a distributed system that consists of the following components.

* Database where events are stored. Tracardi uses elasticsearch as its backend database.
* Data processing library
* RESTful API, GraphQL API - Application Programming Interface
* GUI - Graphical User interface

Data processing library is a library that deals with starting Workflow for selected events and transferring them to
external systems. For the end user, it does not exist alone as such, but in conjunction with the API.

The GUI is a graphical interface for the end user, it runs in the user's browser.

Each of the elements of this system (API and GUI and Database) can be run in multiple instances.




