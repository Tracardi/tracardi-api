from typing import Optional, Dict, List

from dotty_dict import dotty
from pydantic import BaseModel
from tabulate import tabulate

from tracardi.service.dot_notation_converter import dotter
from tracardi.service.events import cache_predefined_event_types, _predefined_event_types


class Doc(BaseModel):
    name: str
    description: str
    id: str
    properties: Optional[dict] = None
    traits: Optional[dict] = None
    profile: Optional[dict] = None


def conv(c):
    if c in ['equal', 'equals']:
        return "Data will be assigned to profile always regardless if it was set or not."
    elif c == 'delete':
        return "Data will be deleted."
    else:
        return "Data will be assigned to profile if it does not exist."


cache_predefined_event_types()
for name, data in _predefined_event_types.items():
    doc = Doc(**data)

    dots = dotter(doc.properties)
    dotted = dotty(doc.properties)

    props = tabulate(
        [[k, dotted[k], f"%%Write example of {k} for {name} event.%%" if k in dotted else "n/a"] for k in dots],
        ["Name", "Expected type", "Example"], tablefmt="github") if doc.properties else "None defined."
    event = tabulate(
        [[k, v] for k, v in doc.traits.items()],
        ["Event trait", "Event properties"], tablefmt="github") if doc.traits else "Data will no be indexed."

    profile = tabulate(
        [[k, v[0], conv(v[1])] for k, v in doc.profile.items()],
        ["Profile field", "Event field", "Action"],
        tablefmt="github") if doc.profile else "Data will no be copied to profile."

    template = f"# Event: {doc.name} \n\n %% Rewrite it to be more verbose: This event should be used when {doc.description.lower()}%%. %%Write example usage%%"
    template += f"""

## Expected properties. 

!!! Tip
    All properties are optional. If any property is missing it will not be processed and no error will be reported.
    
{props}

## Auto indexing

Auto indexing helps to make data easy to find by creating a structure that organizes the data. This structure is made by copying information from the different parts of the data and putting it into a specific format that can be used to analyze and group the data. This is particularly helpful when dealing with unstructured data that needs to be organized in order to be useful.

This table describes which event property will be copied to event traits.

{event} 


## Copy event data to profile

When an event occurs, the data associated with it will be automatically duplicated in certain profile properties. You can refer to the table below for the exact mapping of which fields will be copied.

{profile}

## JSON example

%% Write jso example using the expected properties table %%
    """
    with open(f"mds/{name}.md", 'w') as f:
        f.write(template)
