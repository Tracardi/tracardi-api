# How Merging Strategies are Matched

The system determines which merge strategy to use when there is a conflict in profile data. Strategies can be matched
either by exact field match or wildcard field match.

## Exact Field Match

For example, if a strategy is defined to be triggered for conflicts in the field `profile.ids`, this is considered a final match, and
nothing can override this. This exact match ensures that conflicting fields are resolved using the specific set of
strategies defined for them.

## Wildcard Match

If no strategy is defined for `profile.ids`, the system looks for wildcard strategies such as `profile.*` or `*`.
The `profile.*` strategy can be applied to any missing strategy for fields that start with `profile.`. The `*` strategy
matches all fields and serves as a general fallback.

As of Tracardi 1.0.0, strategies are predefined in the system and cannot be changed. This may change in future versions.