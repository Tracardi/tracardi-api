# How to insert variables into the request body in a Remote API call?

When inserting variables into the request body of a Remote API call in Tracardi, you can utilize the dot notation, which
is represented as `data-source@field.path`. This notation allows you to access specific data fields within a data
source. For instance, using `profile@id` would retrieve the `id` field from the `profile` data source, effectively
yielding `profile.id`.

You can apply this principle within JSON objects to reference data inside the object. For example, in a JSON request
body, you can specify:

```json
{
  "id": "profile@id"
}
```

This structure tells the system to replace `"profile@id"` with the actual value of `profile.id` from the current data
context. So, if `profile.id` is `9c98443a-0637-42f2-a4e2-f7b750a0b650`, the processed JSON object would appear as:

```json
{
  "id": "9c98443a-0637-42f2-a4e2-f7b750a0b650"
}
```

Here, `"id"` in the JSON object gets the value of the current `profile.id`, demonstrating how you can dynamically insert
data from Tracardi sources into your API request bodies.
