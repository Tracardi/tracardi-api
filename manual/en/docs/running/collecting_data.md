# The process of collecting data.

Tracardi has the following process of collecting data.

Data is collected every time a client calls /track API with event payload.

*Example of event payload*

```json
{
  "source": {
    "id": "source-id"
  },
  "session": {
    "id": "session-id"
  },
  "profile": {
    "id": "profile-id"
  },
  "context": {},
  "properties": {},
  "events": [
    {
      "type": "purchase-order",
      "properties": {
        "product": "Nike shoes",
        "quantity": 1
      }
    },
    {
      "type": "page-view"
    }
  ],
  "options": {}
}
```

Tracardi will save the event and then look for rules that define which workflow is to be used to process the events.
Rule is a simple filtering process that checks if the event is from defined resource and has defined event type. For
example simple rule may require resource to be a web page and an event to be a page-view event type. Then if the event
meets this critera the rule will fire a defined workflow and pass event data.

## Workflows

Workflow is a graph of actions that will run when an event is matched with workflow. Actions may run one after another
or in parallel. Workflow is represented as a graph of nodes and connections between them. Actions are assigned to nodes
in the workflow graph. Actions may perform different tasks such as copying data from the event to profile, save profile,
query for additional data, send parts or whole data to another system or emit another event.

When the workflow ends Tracardi checks if there is a need for profile update, segmentation, and merging.

## Segmentation

Segmentation is a term that refers to aggregating prospective customers into groups or segments with common needs.
Segmentation enables companies to target different categories of consumers who perceive the full value of certain
products and services differently from one another.

Common characteristics of a market segment include interests, lifestyle, age, gender, frequency, etc. Common examples of
market segmentation include geographic, demographic, psychographic, and behavioral.

Segmentation in Tracardi is based on a segment logic that is defined in the system, e.g. apply
segment `frequent-customer` to a profile that visited the page more than 10 times.

## Merging

Profile merging is the process of finding customer profiles that belong to one person and have been saved as separate
records for various reasons. In order to combine data into one record, it is necessary to indicate the field containing
the value by which the customer data could be combined. This process will start automatically if the workflow has a merge
profile action. 