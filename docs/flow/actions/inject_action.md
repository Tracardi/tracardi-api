# Inject values

The Inject node in a workflow serves as a tool to debug workflows. This node can be used as the starting point of a flow
that has a defined payload value. The Inject node is responsible for injecting values into the internal state of the
workflow. The data that is injected can be of various types, including strings, integers, or objects.

By default, the Inject node will trigger the workflow when the "debug" button is clicked. This means that the injected
data will be available for subsequent nodes in the workflow to process. The Inject node can be used to simulate specific
conditions or scenarios that can be used for testing purposes or for troubleshooting issues that may occur during the
workflow execution.

To use the Inject node, you will need to define the payload that you want to inject. This can be done by configuring the
node properties to specify the payload data. Once the payload is defined, you can click the "debug" button to execute
the workflow with the injected data.

Overall, the Inject node is a useful tool for debugging workflows by allowing you to simulate specific conditions and
inject data into the workflow's internal state.

## Configuration

Type into configuration what you want to inject.

Example:

```json
{
  "any_value": {
    "key": "value"
  }
}
```

Select where the data should be injected. It can take te following values:

* "Event Properties",
* "Payload",
* "Profile PII",
* "Profile Traits",
* "Profile Interests",
* "Profile Counters",
* "Profile Consents",
* "Session Context"

## Side effects

This action will not run in deployed workflow. It is debug node. 