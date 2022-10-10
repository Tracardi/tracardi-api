# Part 3. Data reference and resource in plugins

In the third part of the tutorial, we will learn how to use data references, how to use resources and how to connect to
external services. We will extend our plugin with the following functionality. 

The plugin needs to send the user defined data to be sent to user defined API. We will also have to extend our form with
the above data (data, and API endpoint).

## Let's get started

Often when coding a plugin, we want to use the data defined by the user. For example, the user references some data
from the internal state of the workflow that he wants to an external API. To do this he uses so-called dot notation. 
Dot notation is a way of specifying the location of the data. It looks like this. 

```
<source>@<path.to.data>
```

This is a working example:

```
event@properties.email
```

It means get the data from the event from its `properties.email`. A full description of all sources and how the data
reference works can be found [here](../../notations/dot_notation.md).

In this tutorial we are interested in how to use this entry and retrieve data, and how to put a field in the form that
will require a dot notation entry.

## Data reference

Let's start with the form. To add a new field to the form we will use the `dotPath` component and in the `form / FromGroup
/ FormFields` section we will add the following code:


```python
FormField (
   id = "data",
   name = "Data to send",
   description = "Please provide data to send",
   component = FormComponent (type = "dotPath", props = {"label": "Data to send"})
)
```

This way we get:
```python hl_lines="10-15"
form = Form(groups=[
    FormGroup(
        name="Event type plugin configuration",
        description="Define required event type",
        fields=[
            FormField(
                id="event_type", name="Event type",
                description="Event type to check",
                component=FormComponent(type="text", props={"label": "Event type"})),
            FormField(
                id="data",
                name="Data to send",
                description="Please provide data to send",
                component=FormComponent(type="dotPath", props={"label": "Data to send"})
            )
        ]
    ),
]),
```

With this, we will get a field of this type in the form.

![Dot path form field](../../images/dot_path.png)

Then we need to extend `init` in register function with a `data` field and extend an object that will store the data and
verify its correctness at the same time.

So I would add to init:

```python
init = {
  "event_type": "",
  "data": ""
}
```

and add to the `Configuration` object:


```python hl_lines="12-16"
class Configuration(PluginConfig):
    event_type: str
    date: str

    @validator("event_type")
    def must_not_be_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Event type can not be empty.")
        return value


    @validator("data")  # (1)
    def data_must_not_be_empty(cls, value):
        if len(value) == 0:
            raise ValueError("Data can not be empty. ")
        return value
```

1. Validates the data property.

We have configuration data, now it's time to read data entered in the form and read data
from [dot notation](../../notations/dot_notation.md).

We do it as follows:

In the run method:

```python hl_lines="2 3"
async def run(self, payload: dict, in_edge=None):
    dot = self._get_dot_accessor(payload)  # (1)
    data_to_send = dot[self.config.data]  # (2)

    if self.event.type == self.config.event_type:
        return Result(port="MyEvent", value=payload)
    else:
        return Result(port="NotMyEvent", value={})
```

1. Get the DotAccessor object that will convert the dot notation to the data. 
2. Convert anything that is defined in `config.data` to the real data form the workflow and assign it to data_to_send