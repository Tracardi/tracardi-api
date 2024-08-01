# Bridge

A bridge in Tracardi acts as a communication link between separate systems, facilitating data exchange. It collects data
from various sources and transfers it to an event source within Tracardi, which then processes the data.
Event Source and Bridge

Event sources use bridges to collect data, each with its own configuration. When creating an event source, the form
includes a section for bridge configuration. By default Open Source Tracardi supports several types of bridges:

* [REST API Bridge](bridges/api.md) - Standard way of collecting data form external systems or the Javascript placed on the web page. 
* [Webhook Bridge](bridges/webhook.md) - Collects unstructured data
* [Redirect URL Bridge](bridges/redirect.md) - Captures data when a link is clicked

Each serves a different purpose. A bridge is an extension point of Tracardi, making it easy to code a new bridge. We
provide a tutorial to guide you through the process.