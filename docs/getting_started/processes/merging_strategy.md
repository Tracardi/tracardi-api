# Profile Merging Strategies

## What is a Merging Strategy?

The merging strategy in Tracardi is the method or algorithm used for combining different profiles or events to form a
single cohesive profile. It is one of the predefined methods that the system will use in case there is conflicting data
in the set of profiles that need to be merged into a single profile. An example of a strategy is an algorithm that
prioritizes the last update made to a profile, regardless of the channel from which the data was collected.

### Example of a Merging Strategy

**Last Profile Update Wins**:

- Prioritizes the most recent information when merging profiles.
- Useful for ensuring the most current data is always reflected in the unified profile.

**Example Scenario**:

- **Profile A**: Last Updated: 2024-01-01
- **Profile B**: Last Updated: 2024-02-01
- **Profile C**: Last Updated: 2024-03-01

Using this strategy, In case of a conflicting data in field e.g. last name the value form Profile C's will be used in
the unified profile since it is the most recently updated profile.

## What is a Set of Merging Strategies?

Merging strategies are defined in sets. It is a sequence in which the system should attempt to resolve conflicts in
profile data. An example of a set may look like this.

1. `LAST_UPDATE`: Selects the most recently updated field.
2. `LAST_PROFILE_UPDATE_TIME`: Selects the value from the most recently updated profile.
3. `LAST_PROFILE_INSERT_TIME`: Selects the value from the most recently inserted profile.

If the primary merge strategy cannot be applied (e.g., missing update times), a fallback (next in sequence) strategy is used. 

## How Merging Strategies are Matched

In case of a conflict during merging the system selects which merge strategy to use. Merging strategies are matched using either exact or wildcard field matches:

- **Exact Match**: Specific to a field, e.g., `profile.ids`.
- **Wildcard Match**: Applies to multiple fields, e.g., `profile.*` or `*`.

## Available Merge Strategies

| Strategy ID                 | Name                       | Description                                              |
|-----------------------------|----------------------------|----------------------------------------------------------|
| `LAST_UPDATE`               | Last updated value         | Uses the update date to select the most recent value.    |
| `FIRST_UPDATE`              | First inserted value       | Uses the update date to select the first inserted value. |
| `MIN`                       | Minimal value              | Selects the minimal value.                               |
| `MAX`                       | Maximal value              | Selects the maximal value.                               |
| `SUM`                       | Sum of values              | Sums all values.                                         |
| `AVG`                       | Average of values          | Averages all values.                                     |
| `LAST_DATETIME`             | Last date                  | Selects the most recent date.                            |
| `FIRST_DATETIME`            | First date                 | Selects the earliest date.                               |
| `ALWAYS_TRUE`               | Always TRUE                | Always returns TRUE.                                     |
| `ALWAYS_FALSE`              | Always FALSE               | Always returns FALSE.                                    |
| `AND`                       | AND Operator               | Uses AND operator on all boolean values.                 |
| `OR`                        | OR Operator                | Uses OR operator on all boolean values.                  |
| `MERGE_LISTS`               | Merge Values From Lists    | Concatenates all values from lists.                      |
| `MERGE_LISTS_DISTINCT`      | Merge Unique Values        | Concatenates unique values from lists.                   |
| `MERGE_LISTS_AND_VALUES`    | Merge Values and Lists     | Concatenates all values and lists.                       |
| `CONCAT_VALUES_TO_LIST`     | Concatenate Values to List | Concatenates all values into a list.                     |
| `FIRST_PROFILE_INSERT_TIME` | First Profile Insert Time  | Uses the value from the first inserted profile.          |
| `FIRST_PROFILE_UPDATE_TIME` | First Profile Update Time  | Uses the value from the first updated profile.           |
| `LAST_PROFILE_CREATE_TIME`  | Last Profile Create Time   | Uses the value from the last created profile.            |
| `LAST_PROFILE_UPDATE_TIME`  | Last Profile Update Time   | Uses the value from the last updated profile.            |
| `LAST_PROFILE_INSERT_TIME`  | Last Profile Insert Time   | Uses the value from the last inserted profile.           |
| `FIRST_ITEM`                | No Merging                 | Does not merge anything.                                 |

## Examples

### Last Update Strategy

- Prioritizes the most recent field update.
- Example: Two profiles with conflicting email fields will use the email that is the most recently updated (oldest field timestamp).

### Last Profile Update Time Strategy

- Selects the value from the profile that was last updated.
- Example: Two profiles with conflicting email fields will use the email from the most recently updated profile (oldest profile timestamp).

### Last DateTime Strategy

- Selects the most recent date.
- Example: Three profiles with different last login dates will use the most recent login date, regardless of the field timestamp.