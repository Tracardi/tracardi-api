# Profile segmentation

This action will add/remove segment to/from the profile.

## Configuration

```json
{
  "segment": "frequent-user",
  "action": "add",
  "condition": "profile@stats.visits>10"
}
```

* *segment* - Segment name. Please use dashes instead of spaces.
* *action* - What action would you like to perform. The default action if "add". Though we have *add* and *remove* to
  choose from.
* *condition* - Condition for segmentation. If the condition is met then the profile will be added or removed to/from
  defined segment.

# Input

This action does not process input.

# Output

Input payload.