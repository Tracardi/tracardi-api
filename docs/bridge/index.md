# Bridge Documentation

## Overview

A bridge is a piece of software that serves as a communication link between two separate systems or applications. Its
primary function is to facilitate the exchange of data between these systems, allowing them to interact seamlessly.

Specifically, in Tracardi, a bridge is responsible for collecting data from a particular source, such as a queue, email,
social media, or any other external system, and then transferring that data to an event source within Tracardi. The
event source, in turn, processes and handles the incoming data as part of Tracardi's workflows and data processing
capabilities.

## Event Source and Bridge

Event source use the bridge to collect data. Event bridge may have its own configuration that defines how it handles
data. When the user creates the event source the standard event source form is extended with bridge configuration form.
There are 3 types of bridges implemented into system API:

* [REST API Bridge](rest_api.md)
* [WebHook Bridge](webhook.md)
* Redirect URL Bridge

There can be other bridges that use external dockers. 