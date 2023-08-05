This documentation provides information about the Page View event, which should be used to track when a user views a
page on a website or application. It can provide insights into user behavior and preferences. An example of how this
event can be used is provided, as well as a table of expected properties and their types. Additionally, the
documentation explains how auto indexing works and which event property will be copied to event traits. Finally, a JSON
example is provided.

The expected properties for the Page View event are all optional, and if any property is missing it will not be
processed and no error will be reported. The expected properties are name and expected type, with an example of "
category" and "string" respectively. Auto indexing helps to make data easy to find by creating a structure that
organizes the data. This structure is made by copying information from the different parts of the data and putting it
into a specific format that can be used to analyze and group the data. The event trait "hit.page.category" will be
copied from the event property "category". Data will not be copied to profile. Finally, a JSON example is provided to
demonstrate how the event should be structured.