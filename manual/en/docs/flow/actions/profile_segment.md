# Profile segmentation

This action will add/remove segment to/from the profile.

## Configuration

```json
{
  "true_segment": "frequent-user",
  "true_action": "add",
  "false_segment": "frequent-user",
  "false_action": "remove",
  "condition": "profile@stats.visits>10"
}
```

* *true_segment* - Segment name when the condition is met. Please use dashes instead of spaces.
* *true_action* - What action would you like to perform when the condition is met. The default action if "add". Though
  we have *add*, *remove*, *none* to choose from.
* *false_segment* - Segment name when the condition is NOT met. Please use dashes instead of spaces.
* *true_action* - What action would you like to perform when the condition is NOT met. The default action if "add".
  Though we have *add*, *remove*, *none* to choose from.
* *condition* - Condition for segmentation. If the condition is met then the profile will be added or removed to/from
  defined segment.

# Input

This action does not process input.

# Output

Input payload.